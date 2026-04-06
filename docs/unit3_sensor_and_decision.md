# Unit 3: Camera And Point-Cloud Perception

Autonomous vehicles use multiple sensors because no single sensor tells the whole story.

Today you will try three beginner-friendly ideas:

- `Camera image perception`: read an image and extract simple visual clues.
- `Point-cloud ego-frame localization`: understand where points are relative to the ego vehicle.
- `LiDAR point-cloud perception`: group real KITTI tracking-task LiDAR points into rough obstacle clusters.

This unit owns sensor perception. It does not estimate the ego vehicle's map pose, build ROS nodes, or tune a full controller.

Important distinction:

- In Unit 3, `localization` means locating points or obstacles relative to the ego vehicle, such as "4 meters forward and 0 meters left."
- In Unit 4, `localization` means estimating the ego vehicle pose in a shared map frame.

## Goal

Practice these Python ideas:

- A variable stores one value.
- A list stores many values.
- A function is a named block of code.
- A loop repeats code.
- An `if` statement makes a decision.
- A real image file stores pixel data.
- A point-cloud file stores many 3D measurements.

Practice these autonomous-driving ideas:

- Cameras are good at visual appearance: lane markings, signs, vehicles, pedestrians, sky, road texture, and traffic lights.
- LiDAR is good at geometry: distance, height, and 3D object shape.
- A point near `(x=0, y=4)` in an ego-frame top-down view is about 4 meters in front of the ego vehicle.
- Perception turns raw sensor data into useful clues for planning and control.

## Warm-Up: Run The Fake Distance Sensor

Run:

```bash
python scripts/fake_distance_sensor.py
```

Expected output:

```text
Fake distance sensor online.
Stop distance: 2 meters
Slow distance: 5 meters
Reading 1: 8 meters -> MOVE
Reading 2: 4 meters -> SLOW
Reading 3: 1 meters -> STOP
```

This is the easiest sensor idea: one number becomes a simple safety hint.

## Experiment 1: Camera Image Perception

Start with a tiny fake camera image so the perception logic is easy to read:

```bash
python scripts/fake_camera_grid.py
```

Expected output starts like:

```text
KITTI-style fake camera frame
Legend: L/R lane markers, S stop sign, - road stripe, . background
```

Expected output also includes:

```text
Camera summary:
- lane marker pixels: 12
- stop sign pixels: 4
- estimated lane offset: 0.0
Decision: STOP
Reason: stop sign pixels were found
```

In this tiny image:

- `L` and `R` are lane markers.
- `S` is a stop-sign-like region.
- `-` is a road stripe.
- `.` is background.

Open `scripts/fake_camera_grid.py`.

Look for:

```text
count_pixels
estimate_lane_offset
choose_camera_action
```

This is fake, but the structure is real: read image data, extract features, then make a perception summary. The printed `Decision` is only a tiny rule-based hint, not the full planning/control system.

## Experiment 2: Real KITTI Camera Image Features

Now run a tiny real-image demo using the KITTI tracking-task camera frame:

```bash
python scripts/kitti_camera_perception.py
```

Expected output starts like:

```text
KITTI camera image perception demo
Input file: web_sim/user_data/image/000000.png
Image size: 1242 x 375 pixels
Simple region summaries:
```

This script samples a few broad image regions:

- `top band`: often sky, buildings, trees, or high background.
- `center horizon band`: often far road scene and objects.
- `bottom ego-lane band`: often nearby road surface.

The script prints average RGB values and brightness. This is not object detection, but it shows the first step of camera perception: raw pixels become numbers the program can reason about.

Real camera perception can detect:

- Lanes.
- Vehicles.
- Pedestrians.
- Signs and traffic lights.
- Drivable space.

## Experiment 3: Point-Cloud Ego-Frame Localization

A point cloud is a set of 3D points. For this beginner experiment, we use a tiny fake CSV file:

```bash
python scripts/fake_pointcloud_viewer.py
```

Expected output starts like:

```text
KITTI-style fake point-cloud viewer
Legend: E ego vehicle, C car, O cone, P pedestrian, T tree
Top-down fake point cloud (front is up)
```

Expected output also includes:

```text
Closest front obstacle: cone at x=0, y=4 meters
Decision: SLOW
Reason: cone is ahead
```

In this top-down view:

- `E` is the ego vehicle.
- `y` means forward distance in meters.
- `x` means left/right distance in meters.
- `x=0, y=4` means the cone is about 4 meters straight ahead of the ego vehicle.

This is point-cloud localization in the ego frame. We are not finding the vehicle on a map yet. We are only locating points relative to the vehicle.

Open `scripts/fake_pointcloud_viewer.py`.

Look for:

```text
closest_front_obstacle
choose_pointcloud_action
draw_top_down_map
```

These functions show how geometry becomes an easy-to-read perception summary. The printed `Decision` is only a simple hint from ego-frame geometry.

## Experiment 4: Real KITTI LiDAR Point-Cloud Perception

Now run a more realistic LiDAR perception script.

First make sure the matching KITTI tracking-task point-cloud file exists:

```text
web_sim/user_data/pointcloud/000000.bin
```

Run:

```bash
python scripts/kitti_lidar_perception.py
```

Expected output starts like:

```text
KITTI tracking LiDAR perception demo
Input file: web_sim/user_data/pointcloud/000000.bin
Raw points: 121,238
Driving ROI points: 52,981
Ground-like points: 35,267
Non-ground obstacle points: 17,714
Occupied BEV voxels: 150
Obstacle clusters kept: 3
```

Expected output also includes obstacle proposals like:

```text
Cluster 2: vehicle-sized obstacle | center=(6.6m forward, -2.6m left) | size=(2.9m L, 1.3m W, 1.6m H) | points=707
Decision hint: MOVE
Reason: nearest ego-corridor cluster is far away
```

If the `.bin` file is missing, the script tells you to copy it into `web_sim/user_data/pointcloud/000000.bin`.

This script reads actual KITTI tracking-task LiDAR bytes and performs common perception steps:

- Crop to a driving region of interest.
- Separate ground-like points from non-ground obstacle points.
- Voxelize the non-ground points into a bird's-eye-view grid.
- Cluster nearby occupied cells into rough obstacle proposals.

This is still not a production detector. Real systems often use trained models, calibration, tracking, and validation.

## Read The Real LiDAR Code Logic

Open `scripts/kitti_lidar_perception.py`.

Look for:

```text
load_kitti_pointcloud_bin
```

KITTI tracking-task LiDAR `.bin` files store repeated float values:

```text
x/forward, y/left, z/up, reflectance
```

Look for:

```text
crop_driving_roi
split_ground
cluster_occupied_voxels
```

These functions turn many raw 3D points into a smaller list of rough obstacles.

## Visualize The KITTI Frame In The Browser

The repo also includes a small browser viewer for the KITTI tracking-task camera image and LiDAR point cloud.

From the project root, run:

```bash
python -m http.server 8000
```

Then open:

```text
http://127.0.0.1:8000/web_sim/
```

If you are using GitHub Codespaces, VS Code may show a port-forwarding popup for port `8000`. Open the forwarded page, then make sure the address ends with:

```text
/web_sim/
```

The viewer loads matching frame numbers from:

```text
web_sim/user_data/image/000000.png
web_sim/user_data/pointcloud/000000.bin
```

The camera image looks like a front-facing road photo. You may see the road, lane area, nearby vehicles, buildings, trees, sky, or other street-scene details.

The point cloud looks different from a photo. It is a top-down LiDAR view made of many colored dots. Each dot is a 3D distance measurement:

- Up on the canvas means farther in front of the ego vehicle.
- Left and right are relative to the ego vehicle.
- Denser dot areas can show roads, cars, walls, trees, or other surfaces.
- Dot color changes with height, so taller objects can look different from low road points.

Use `Load Frame` to reload frame `000000`. If your instructor adds more matching files, use `Next`, `Previous`, or `Play` to move through the sequence.

To stop the HTTP server, click the terminal running it and press `Ctrl+C`.

## Tiny Modification

Open `scripts/fake_data/kitti_style_camera_grid.txt`.

Change the stop-sign-like pixels:

```text
......SS.......
......SS.......
```

to background pixels:

```text
...............
...............
```

Run:

```bash
python scripts/fake_camera_grid.py
```

Watch how the camera decision changes when the stop-sign-like pixels disappear.

Then change the dots back to `S` so the starter lesson stays the same.

## Optional LiDAR Modification

Open `scripts/kitti_lidar_perception.py`.

Find:

```python
GROUND_UP_MAX_M = -1.35
```

Try:

```python
GROUND_UP_MAX_M = -1.0
```

Run:

```bash
python scripts/kitti_lidar_perception.py
```

Watch how these counts change:

```text
Ground-like points
Non-ground obstacle points
Obstacle clusters kept
```

If the clustering becomes worse, change the value back to `-1.35`.

## Reflection

Which sensor view was easiest to understand: camera image, top-down point cloud, or real LiDAR cluster output? Why?

Next, Unit 4 takes perception results like "6.6 meters forward and 2.6 meters right" and transforms them into a shared map frame.
