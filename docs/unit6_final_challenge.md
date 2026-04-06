# Unit 6: Mini Autonomy Stack Challenge

You made it to the final mini challenge.

Today you will connect the whole prelearning path:

- Unit 1: terminal navigation and AV architecture printouts.
- Unit 2: Python state, lists, dictionaries, functions, and commands.
- Unit 3: camera and point-cloud perception.
- Unit 4: localization and ego-to-map coordinate transforms.
- Unit 5: ROS-style nodes, topics, messages, and connected helpers.

This unit has two connected tracks:

- A small grid-world autonomy stack that shows perception, localization, planning, control, and visualization in one Python file.
- A real-data check that uses the KITTI tracking-task camera image and LiDAR point cloud.

The grid-world stack is still simplified beginner Python. The KITTI tracking scripts use real sensor files, but they are still teaching demos, not production AV software.

This unit owns integration. It reuses earlier scripts as building blocks instead of re-teaching each topic from the beginning.

## Goal

Use these scripts together:

- `scripts/mini_autonomy_stack.py`: run a small end-to-end autonomy loop.
- `scripts/kitti_camera_perception.py`: summarize a real KITTI tracking-task camera image.
- `scripts/kitti_lidar_perception.py`: process a real KITTI tracking-task LiDAR point cloud.
- `scripts/kitti_perception_localization_demo.py`: transform LiDAR perception clusters from ego coordinates into map coordinates.
- `web_sim/`: visualize the KITTI tracking-task camera image and point cloud in the browser.

The ego vehicle is the vehicle our code controls.

## Part 1: Run The Mini Stack

Run:

```bash
python scripts/mini_autonomy_stack.py
```

Expected output starts like:

```text
ADA mini autonomy stack
Legend: 'E' means ego vehicle, 'G' means goal
```

You should also see repeated autonomy cycles:

```text
--- Autonomy cycle 1 ---
Perception: ...
Localization: ...
Planning: ...
Control: ...
```

At the end, the script creates:

```text
outputs/mini_autonomy_report.html
```

In Codespaces, open that file and use the built-in preview to see the ego vehicle route.

## Part 2: Run Real KITTI Tracking Perception

Run the camera-image perception check:

```bash
python scripts/kitti_camera_perception.py
```

Expected output starts like:

```text
KITTI camera image perception demo
Input file: web_sim/user_data/image/000000.png
Image size: 1242 x 375 pixels
```

Before running the LiDAR point-cloud demos, make sure the matching point-cloud file exists:

```text
web_sim/user_data/pointcloud/000000.bin
```

Run the LiDAR point-cloud perception check:

```bash
python scripts/kitti_lidar_perception.py
```

Expected output starts like:

```text
KITTI tracking LiDAR perception demo
Input file: web_sim/user_data/pointcloud/000000.bin
Raw points: 121,238
Driving ROI points: 52,981
```

This is the Unit 3 perception experiment reused in the final challenge. If you need the full pipeline explanation, go back to Unit 3. Here, focus on how the perception result becomes one input to the larger stack.

## Part 3: Connect Perception To Localization

Run:

```bash
python scripts/kitti_perception_localization_demo.py
```

Expected output starts like:

```text
KITTI tracking perception + localization-frame demo
Input file: web_sim/user_data/pointcloud/000000.bin
Localization state:
```

Expected output also includes transformed clusters:

```text
Perception clusters transformed into the map frame:
1. large structure or mixed obstacle | ego=(18.7m forward, -4.4m left) -> map=(120.4m, 17.5m)
2. vehicle-sized obstacle | ego=(6.6m forward, -2.6m left) -> map=(108.3m, 18.2m)
```

This is the Unit 4 localization experiment reused in the final challenge. Here, focus on how map-frame objects would become useful to planning.

## Part 4: Run The Website Viewer

This repo also includes a small website. It is not CARLA or ROS RViz, but it gives students a browser-based place to see:

- A KITTI tracking-task camera frame.
- A top-down KITTI tracking-task LiDAR point cloud.

From the repo root, run:

```bash
python -m http.server 8000
```

Then open this page:

```text
http://127.0.0.1:8000/web_sim/
```

In Codespaces, open the forwarded port in your browser and make sure the URL ends with `/web_sim/`.

The website is set up for synchronized frame sequences:

```text
web_sim/user_data/image/000000.png
web_sim/user_data/pointcloud/000000.bin
web_sim/user_data/image/000001.png
web_sim/user_data/pointcloud/000001.bin
```

The image and point-cloud filenames must match. The website uses these folders by default:

```text
user_data/image
user_data/pointcloud
```

Use `Next`, `Previous`, or `Play` to move through the sequence.

The website reads KITTI LiDAR `.bin` point clouds as repeated float32 values:

```text
x forward, y left, z up, reflectance
```

To stop the HTTP server, click the terminal running it and press `Ctrl+C`.

## Read The Mini Stack By System

Open `scripts/mini_autonomy_stack.py`.

Look for the perception functions:

```text
detect_objects_ahead
estimate_lane_offset
```

Perception changes world data into facts the planner can use.

Look for the localization function:

```text
localize
```

Localization reports where the ego vehicle is on the small map.

Look for the planning function:

```text
plan_next_target
```

Planning chooses a target cell and explains why.

Look for the control function:

```text
make_control_command
```

Control turns the target into steering, throttle, and brake.

## Quick Real-Data Script Check

Use the Unit 3 and Unit 4 notes for the full code walkthroughs. In this final challenge, just confirm you can locate the main handoff points.

Open `scripts/kitti_camera_perception.py`.

Look for:

```text
load_png_rows
summarize_region
```

These are the Unit 3 camera-perception entry points.

Open `scripts/kitti_lidar_perception.py`.

Look for:

```text
load_kitti_pointcloud_bin
crop_driving_roi
split_ground
cluster_occupied_voxels
```

These are the Unit 3 LiDAR-perception entry points.

Open `scripts/kitti_perception_localization_demo.py`.

Look for:

```text
integrate_odometry
ego_to_map
```

These are the Unit 4 localization and coordinate-frame entry points.

## Challenge 1: Change The Mini Stack Sensor Range

In `scripts/mini_autonomy_stack.py`, find:

```python
SENSOR_RANGE = 5
```

Try:

```python
SENSOR_RANGE = 3
```

Run the script again. Watch when the ego vehicle first reports the cone in perception.

## Challenge 2: Move The Cone

In `scripts/mini_autonomy_stack.py`, find the `OBJECTS` list:

```python
{"kind": "cone", "x": 7, "y": 6, "symbol": "O"},
```

Try moving the cone out of the lane:

```python
{"kind": "cone", "x": 8, "y": 6, "symbol": "O"},
```

Run:

```bash
python scripts/mini_autonomy_stack.py
```

Question to check: does the planner still need `AVOID`, or can it `CRUISE`?

## Challenge 3: Tune The Controller

In `scripts/mini_autonomy_stack.py`, find:

```python
return {"steering": steering, "throttle": 0.4, "brake": 0.0}
```

Try a slower vehicle:

```python
return {"steering": steering, "throttle": 0.2, "brake": 0.0}
```

This script still moves one map cell at a time, but the printed control command now shows your new throttle value.

## Challenge 4: Trace The Real-Data Handoff

Run the camera and LiDAR perception checks:

```bash
python scripts/kitti_camera_perception.py
python scripts/kitti_lidar_perception.py
```

Then answer:

- What camera-image clues did the camera script summarize?
- What obstacle-cluster clues did the LiDAR script summarize?
- Which clues are appearance clues?
- Which clues are geometry clues?

This keeps Unit 6 focused on connecting outputs instead of changing the Unit 3 perception algorithm.

## Challenge 5: Trace The Localization Handoff

Run the localization-frame demo:

```bash
python scripts/kitti_perception_localization_demo.py
```

Then answer:

- What ego-frame cluster center did the script print?
- What map-frame position did it transform that cluster into?
- Why would planning prefer map-frame object positions over raw ego-frame positions?

This keeps Unit 6 focused on how Unit 4 connects to the larger stack, not on changing the Unit 4 localization math.

## Challenge 6: Explain One Autonomy Cycle

Pick one cycle from `scripts/mini_autonomy_stack.py` output and answer:

- What did perception detect?
- Where did localization say the ego vehicle was?
- What did planning choose?
- What control command was sent?

## Challenge 7: Explain One KITTI Cluster

Pick one cluster from `scripts/kitti_lidar_perception.py` output and answer:

- How far forward is the cluster center?
- Is it left or right of the ego vehicle?
- Is it vehicle-sized, pole/tree/pedestrian-sized, or a large mixed structure?
- Would you trust this simple heuristic as a production detector? Why or why not?

## Challenge 8: Explain One ROS-Style Connection

Look back at Unit 5's topic graph and answer:

- Which node would publish camera images?
- Which node would publish LiDAR object clusters?
- Which node would publish ego pose?
- Which node would consume those outputs to choose a trajectory?

## Reflection

Which part felt most like autonomous driving to you: perception, localization, planning, control, visualization, or ROS-style system organization?

## Website Reflection

After using the website viewer, compare the terminal and website versions:

- Which view made the point cloud easiest to understand?
- What details were easier to see in the real KITTI tracking-task camera image?
- Why might a real AV team use both a web/RViz-style visualization and text logs?
