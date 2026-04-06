"""A tiny camera-image perception demo for one KITTI tracking frame.

This script intentionally avoids external image libraries so it can run in a
fresh Codespaces terminal. It reads an 8-bit RGB/RGBA PNG, samples a few simple
image regions, and prints human-readable camera clues.

This is not a production detector. Real AV camera perception usually uses
calibrated cameras, neural networks, tracking, and careful validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import struct
import zlib


PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMAGE_FILE = PROJECT_ROOT / "web_sim" / "user_data" / "image" / "000000.png"


@dataclass(frozen=True)
class ImageRegion:
    name: str
    x_min: int
    x_max: int
    y_min: int
    y_max: int


@dataclass(frozen=True)
class RegionSummary:
    name: str
    red: float
    green: float
    blue: float

    @property
    def brightness(self) -> float:
        return (self.red + self.green + self.blue) / 3


def find_image_file() -> Path:
    if IMAGE_FILE.exists():
        return IMAGE_FILE

    raise FileNotFoundError(
        "Missing KITTI tracking camera image for frame 000000.\n"
        "Copy the matching .png file into this location:\n"
        f"- {IMAGE_FILE.relative_to(PROJECT_ROOT)}"
    )


def paeth_predictor(left: int, up: int, upper_left: int) -> int:
    estimate = left + up - upper_left
    left_error = abs(estimate - left)
    up_error = abs(estimate - up)
    upper_left_error = abs(estimate - upper_left)

    if left_error <= up_error and left_error <= upper_left_error:
        return left
    if up_error <= upper_left_error:
        return up
    return upper_left


def unfilter_scanline(filter_type: int, raw: bytearray, previous: bytes, bytes_per_pixel: int) -> bytes:
    for index, value in enumerate(raw):
        left = raw[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
        up = previous[index] if previous else 0
        upper_left = previous[index - bytes_per_pixel] if previous and index >= bytes_per_pixel else 0

        if filter_type == 0:
            raw[index] = value
        elif filter_type == 1:
            raw[index] = (value + left) & 0xFF
        elif filter_type == 2:
            raw[index] = (value + up) & 0xFF
        elif filter_type == 3:
            raw[index] = (value + ((left + up) // 2)) & 0xFF
        elif filter_type == 4:
            raw[index] = (value + paeth_predictor(left, up, upper_left)) & 0xFF
        else:
            raise ValueError(f"Unsupported PNG filter type: {filter_type}")

    return bytes(raw)


def load_png_rows(path: Path) -> tuple[int, int, int, list[bytes]]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"{path} is not a PNG file")

    offset = 8
    width = height = bit_depth = color_type = interlace = None
    idat_chunks = []

    while offset < len(data):
        chunk_length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_data = data[offset + 8 : offset + 8 + chunk_length]
        offset = offset + 12 + chunk_length

        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, _compression, _filter, interlace = struct.unpack(">IIBBBBB", chunk_data)
        elif chunk_type == b"IDAT":
            idat_chunks.append(chunk_data)
        elif chunk_type == b"IEND":
            break

    if width is None or height is None:
        raise ValueError(f"{path} is missing a PNG header")
    if bit_depth != 8 or color_type not in (2, 6) or interlace != 0:
        raise ValueError("This demo supports only non-interlaced 8-bit RGB/RGBA PNG images")

    channels = 3 if color_type == 2 else 4
    row_length = width * channels
    decompressed = zlib.decompress(b"".join(idat_chunks))
    rows = []
    previous = b""
    cursor = 0

    for _row_index in range(height):
        filter_type = decompressed[cursor]
        cursor += 1
        raw = bytearray(decompressed[cursor : cursor + row_length])
        cursor += row_length
        row = unfilter_scanline(filter_type, raw, previous, channels)
        rows.append(row)
        previous = row

    return width, height, channels, rows


def summarize_region(rows: list[bytes], channels: int, region: ImageRegion) -> RegionSummary:
    red_total = green_total = blue_total = pixel_count = 0

    for y in range(region.y_min, region.y_max):
        row = rows[y]
        for x in range(region.x_min, region.x_max):
            pixel_index = x * channels
            red_total += row[pixel_index]
            green_total += row[pixel_index + 1]
            blue_total += row[pixel_index + 2]
            pixel_count += 1

    return RegionSummary(
        name=region.name,
        red=red_total / pixel_count,
        green=green_total / pixel_count,
        blue=blue_total / pixel_count,
    )


def describe_region(summary: RegionSummary) -> str:
    if summary.brightness < 80:
        return "dark region"
    if summary.blue > summary.red + 15 and summary.brightness > 90:
        return "blue-heavy region"
    if abs(summary.red - summary.green) < 12 and abs(summary.green - summary.blue) < 12:
        return "gray-balanced region"
    return "mixed camera region"


def main() -> None:
    image_file = find_image_file()
    width, height, channels, rows = load_png_rows(image_file)

    regions = [
        ImageRegion("top band", 0, width, 0, max(1, height // 4)),
        ImageRegion("center horizon band", width // 4, (width * 3) // 4, height // 3, height // 2),
        ImageRegion("bottom ego-lane band", width // 3, (width * 2) // 3, (height * 2) // 3, height),
    ]
    summaries = [summarize_region(rows, channels, region) for region in regions]

    print("KITTI camera image perception demo")
    print(f"Input file: {image_file.relative_to(PROJECT_ROOT)}")
    print(f"Image size: {width} x {height} pixels")
    print("Simple region summaries:")

    for summary in summaries:
        print(
            f"- {summary.name}: avg RGB=({summary.red:.0f}, {summary.green:.0f}, {summary.blue:.0f}), "
            f"brightness={summary.brightness:.0f} -> {describe_region(summary)}"
        )

    bottom = summaries[-1]
    print("\nCamera perception hint:")
    print(
        "The bottom-center region is the near-field driving area in a front camera. "
        f"Its brightness is {bottom.brightness:.0f}, but RGB summaries alone are not enough to prove it is drivable road."
    )

    print("\nReal-stack note:")
    print("A production camera perception module would detect lanes, vehicles, signs, pedestrians, and free space.")
    print("This demo only shows how an image can become a few simple numeric features.")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as error:
        print(error)
