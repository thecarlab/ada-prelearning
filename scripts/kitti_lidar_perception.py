"""A small real-data LiDAR perception pass for one KITTI tracking frame.

This script reads a KITTI LiDAR .bin point cloud: float32 x, y, z, reflectance.
It then runs a lightweight version of common perception steps:

1. Crop to a driving region of interest.
2. Split low ground-like points from non-ground obstacle points.
3. Voxelize the non-ground points into a bird's-eye-view grid.
4. Cluster connected occupied grid cells into rough obstacle proposals.

It is not a trained detector like OpenPCDet or an Autoware perception node, but
it works on real point-cloud bytes instead of fake hand-written objects.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
import math
import struct


PROJECT_ROOT = Path(__file__).resolve().parents[1]
POINT_CLOUD_FILE = PROJECT_ROOT / "web_sim" / "user_data" / "pointcloud" / "000000.bin"

FORWARD_RANGE_M = (0.0, 50.0)
LEFT_RANGE_M = (-12.0, 12.0)
UP_RANGE_M = (-2.5, 2.5)
GROUND_UP_MAX_M = -1.35
VOXEL_SIZE_M = 0.75
MIN_CLUSTER_POINTS = 35
MIN_CLUSTER_CELLS = 2


@dataclass(frozen=True)
class Point:
    forward: float
    left: float
    up: float
    reflectance: float


@dataclass(frozen=True)
class Cluster:
    point_count: int
    cell_count: int
    forward_min: float
    forward_max: float
    left_min: float
    left_max: float
    up_min: float
    up_max: float

    @property
    def forward_center(self) -> float:
        return (self.forward_min + self.forward_max) / 2

    @property
    def left_center(self) -> float:
        return (self.left_min + self.left_max) / 2

    @property
    def length(self) -> float:
        return self.forward_max - self.forward_min

    @property
    def width(self) -> float:
        return self.left_max - self.left_min

    @property
    def height(self) -> float:
        return self.up_max - self.up_min


def load_kitti_pointcloud_bin(path: Path) -> list[Point]:
    """Load KITTI LiDAR points from a binary float matrix."""
    data = path.read_bytes()
    if len(data) % 16 != 0:
        raise ValueError(f"{path} is not a KITTI x/y/z/reflectance .bin file")

    return [
        Point(forward=x, left=y, up=z, reflectance=reflectance)
        for x, y, z, reflectance in struct.iter_unpack("<ffff", data)
    ]


def find_point_cloud_file() -> Path:
    """Find the required KITTI tracking point-cloud file."""
    if POINT_CLOUD_FILE.exists():
        return POINT_CLOUD_FILE

    raise FileNotFoundError(
        "Missing KITTI tracking LiDAR point cloud for frame 000000.\n"
        "Copy the matching .bin file into this location:\n"
        f"- {POINT_CLOUD_FILE.relative_to(PROJECT_ROOT)}"
    )


def in_range(value: float, bounds: tuple[float, float]) -> bool:
    return bounds[0] <= value <= bounds[1]


def crop_driving_roi(points: list[Point]) -> list[Point]:
    """Keep points in front of the vehicle and near the ego lane area."""
    return [
        point
        for point in points
        if in_range(point.forward, FORWARD_RANGE_M)
        and in_range(point.left, LEFT_RANGE_M)
        and in_range(point.up, UP_RANGE_M)
    ]


def split_ground(points: list[Point]) -> tuple[list[Point], list[Point]]:
    """Use a simple height threshold as a stand-in for ground segmentation."""
    ground_points = []
    obstacle_points = []

    for point in points:
        if point.up <= GROUND_UP_MAX_M:
            ground_points.append(point)
        else:
            obstacle_points.append(point)

    return ground_points, obstacle_points


def voxel_key(point: Point) -> tuple[int, int]:
    return (
        math.floor(point.forward / VOXEL_SIZE_M),
        math.floor(point.left / VOXEL_SIZE_M),
    )


def voxelize(points: list[Point]) -> dict[tuple[int, int], list[Point]]:
    voxels: dict[tuple[int, int], list[Point]] = defaultdict(list)
    for point in points:
        voxels[voxel_key(point)].append(point)
    return dict(voxels)


def neighbor_keys(key: tuple[int, int]) -> list[tuple[int, int]]:
    forward_cell, left_cell = key
    return [
        (forward_cell + df, left_cell + dl)
        for df in (-1, 0, 1)
        for dl in (-1, 0, 1)
        if not (df == 0 and dl == 0)
    ]


def make_cluster(component_cells: list[tuple[int, int]], voxels: dict[tuple[int, int], list[Point]]) -> Cluster:
    points = [point for cell in component_cells for point in voxels[cell]]
    return Cluster(
        point_count=len(points),
        cell_count=len(component_cells),
        forward_min=min(point.forward for point in points),
        forward_max=max(point.forward for point in points),
        left_min=min(point.left for point in points),
        left_max=max(point.left for point in points),
        up_min=min(point.up for point in points),
        up_max=max(point.up for point in points),
    )


def cluster_occupied_voxels(voxels: dict[tuple[int, int], list[Point]]) -> list[Cluster]:
    """Group connected bird's-eye-view voxels into obstacle proposals."""
    unvisited = set(voxels)
    clusters = []

    while unvisited:
        start = unvisited.pop()
        queue = deque([start])
        component_cells = [start]

        while queue:
            current = queue.popleft()
            for neighbor in neighbor_keys(current):
                if neighbor in unvisited:
                    unvisited.remove(neighbor)
                    queue.append(neighbor)
                    component_cells.append(neighbor)

        cluster = make_cluster(component_cells, voxels)
        if cluster.point_count >= MIN_CLUSTER_POINTS and cluster.cell_count >= MIN_CLUSTER_CELLS:
            clusters.append(cluster)

    return sorted(clusters, key=lambda cluster: cluster.forward_min)


def describe_cluster(cluster: Cluster) -> str:
    """Give a rough human-readable label based on bounding-box shape."""
    if cluster.length <= 6.0 and cluster.width <= 3.5 and cluster.height >= 1.0:
        return "vehicle-sized obstacle"
    if cluster.width <= 1.5 and cluster.height >= 1.0:
        return "pole/tree/pedestrian-sized obstacle"
    if cluster.height < 0.7:
        return "low obstacle or curb-like return"
    return "large structure or mixed obstacle"


def front_corridor_cluster(clusters: list[Cluster]) -> Cluster | None:
    for cluster in clusters:
        center_is_in_front_corridor = abs(cluster.left_center) <= 2.0
        if center_is_in_front_corridor and cluster.forward_max > 0:
            return cluster
    return None


def choose_action(cluster: Cluster | None) -> tuple[str, str]:
    if cluster is None:
        return "MOVE", "no non-ground cluster overlaps the ego corridor"
    if cluster.forward_min < 8.0:
        return "STOP", "a non-ground cluster is very close in the ego corridor"
    if cluster.forward_min < 20.0:
        return "SLOW", "a non-ground cluster is ahead in the ego corridor"
    return "MOVE", "nearest ego-corridor cluster is far away"


def draw_bev(clusters: list[Cluster]) -> None:
    """Draw a coarse bird's-eye-view occupancy summary."""
    print("\nCoarse bird's-eye view of clustered non-ground points")
    print("Forward is up. E is the ego vehicle. Letters are cluster centers.")
    print("left: -10m ... 0m ... +10m")

    labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cells: dict[tuple[int, int], str] = {}
    for index, cluster in enumerate(clusters[: len(labels)]):
        forward_bin = int(cluster.forward_center // 2)
        left_bin = int((cluster.left_center + 10) // 2)
        if 0 <= forward_bin <= 20 and 0 <= left_bin <= 10:
            cells[(forward_bin, left_bin)] = labels[index]

    for forward_bin in range(20, -1, -1):
        row = ""
        for left_bin in range(0, 11):
            if forward_bin == 0 and left_bin == 5:
                row += "E"
            else:
                row += cells.get((forward_bin, left_bin), ".")
        print(f"{forward_bin * 2:02d}m {row}")


def main() -> None:
    point_cloud_file = find_point_cloud_file()
    points = load_kitti_pointcloud_bin(point_cloud_file)
    roi_points = crop_driving_roi(points)
    ground_points, obstacle_points = split_ground(roi_points)
    voxels = voxelize(obstacle_points)
    clusters = cluster_occupied_voxels(voxels)
    nearest_front = front_corridor_cluster(clusters)
    action, reason = choose_action(nearest_front)

    print("KITTI tracking LiDAR perception demo")
    print(f"Input file: {point_cloud_file.relative_to(PROJECT_ROOT)}")
    print(f"Raw points: {len(points):,}")
    print(f"Driving ROI points: {len(roi_points):,}")
    print(f"Ground-like points: {len(ground_points):,}")
    print(f"Non-ground obstacle points: {len(obstacle_points):,}")
    print(f"Occupied BEV voxels: {len(voxels):,}")
    print(f"Obstacle clusters kept: {len(clusters)}")

    for index, cluster in enumerate(clusters[:8], start=1):
        print(
            f"Cluster {index}: {describe_cluster(cluster)} | "
            f"center=({cluster.forward_center:.1f}m forward, {cluster.left_center:.1f}m left) | "
            f"size=({cluster.length:.1f}m L, {cluster.width:.1f}m W, {cluster.height:.1f}m H) | "
            f"points={cluster.point_count}"
        )

    if nearest_front:
        print(
            "Nearest ego-corridor cluster: "
            f"{nearest_front.forward_min:.1f}m to {nearest_front.forward_max:.1f}m forward, "
            f"{nearest_front.left_min:.1f}m to {nearest_front.left_max:.1f}m left"
        )
    else:
        print("Nearest ego-corridor cluster: none")

    print(f"Decision hint: {action}")
    print(f"Reason: {reason}")
    draw_bev(clusters)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as error:
        print(error)
