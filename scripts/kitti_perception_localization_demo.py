"""Connect LiDAR perception detections to a localization/map frame.

Real AV stacks keep track of coordinate frames. A perception detector may report
an obstacle as "18 meters forward and 3 meters left of the ego vehicle." The
localization system estimates the ego pose in a map frame, then the stack
transforms that obstacle into map coordinates for prediction and planning.

This demo uses the real KITTI tracking-task point cloud from web_sim/user_data and a
small odometry update to show the math without requiring ROS 2 or a full map.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from kitti_lidar_perception import (
    PROJECT_ROOT,
    cluster_occupied_voxels,
    crop_driving_roi,
    describe_cluster,
    find_point_cloud_file,
    load_kitti_pointcloud_bin,
    split_ground,
    voxelize,
)


@dataclass(frozen=True)
class Pose2D:
    x_m: float
    y_m: float
    yaw_rad: float


def integrate_odometry(pose: Pose2D, speed_mps: float, yaw_rate_radps: float, dt_s: float) -> Pose2D:
    """Predict the next ego pose from a simple bicycle-like odometry update."""
    next_yaw = pose.yaw_rad + yaw_rate_radps * dt_s
    distance = speed_mps * dt_s
    return Pose2D(
        x_m=pose.x_m + distance * math.cos(next_yaw),
        y_m=pose.y_m + distance * math.sin(next_yaw),
        yaw_rad=next_yaw,
    )


def ego_to_map(forward_m: float, left_m: float, pose: Pose2D) -> tuple[float, float]:
    """Transform a point from ego-vehicle coordinates into map coordinates."""
    cos_yaw = math.cos(pose.yaw_rad)
    sin_yaw = math.sin(pose.yaw_rad)
    map_x = pose.x_m + forward_m * cos_yaw - left_m * sin_yaw
    map_y = pose.y_m + forward_m * sin_yaw + left_m * cos_yaw
    return map_x, map_y


def main() -> None:
    point_cloud_file = find_point_cloud_file()
    points = load_kitti_pointcloud_bin(point_cloud_file)
    roi_points = crop_driving_roi(points)
    _ground_points, obstacle_points = split_ground(roi_points)
    clusters = cluster_occupied_voxels(voxelize(obstacle_points))

    start_pose = Pose2D(x_m=100.0, y_m=20.0, yaw_rad=math.radians(5.0))
    predicted_pose = integrate_odometry(
        pose=start_pose,
        speed_mps=7.0,
        yaw_rate_radps=math.radians(2.0),
        dt_s=0.2,
    )

    print("KITTI tracking perception + localization-frame demo")
    print(f"Input file: {point_cloud_file.relative_to(PROJECT_ROOT)}")
    print("Localization state:")
    print(f"- start pose: x={start_pose.x_m:.2f}m, y={start_pose.y_m:.2f}m, yaw={math.degrees(start_pose.yaw_rad):.1f}deg")
    print("- odometry input: speed=7.0m/s, yaw_rate=2.0deg/s, dt=0.2s")
    print(
        f"- predicted pose: x={predicted_pose.x_m:.2f}m, "
        f"y={predicted_pose.y_m:.2f}m, yaw={math.degrees(predicted_pose.yaw_rad):.1f}deg"
    )
    print("\nPerception clusters transformed into the map frame:")

    for index, cluster in enumerate(clusters[:6], start=1):
        map_x, map_y = ego_to_map(cluster.forward_center, cluster.left_center, predicted_pose)
        print(
            f"{index}. {describe_cluster(cluster)} | "
            f"ego=({cluster.forward_center:.1f}m forward, {cluster.left_center:.1f}m left) -> "
            f"map=({map_x:.1f}m, {map_y:.1f}m)"
        )

    print("\nReal-stack note:")
    print("A production localization module would estimate pose from GNSS, IMU, wheel odometry, LiDAR/camera map matching, or SLAM.")
    print("This lesson focuses on the coordinate-frame transform that connects localization to perception and planning.")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as error:
        print(error)
