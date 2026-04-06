# Unit 5: Tiny ROS 2 Teaser

This is only a preview. You do not need to install ROS 2 here. You will learn the real ROS 2 material during ADA camp.

In Units 1-4, you saw a path from terminal navigation to Python state, camera/point-cloud perception, and localization-frame transforms. Unit 5 shows how those pieces would be organized in a ROS-style autonomous-driving system.

This unit owns system organization. You will not install ROS 2 or build real ROS 2 nodes here; you will learn how AV software pieces can be named and connected.

## Goal

Learn four words:

- `node`
- `topic`
- `message`
- `launch`

## Simple Idea

Autonomous driving systems often use software pieces that talk to each other.

A `node` is like one small software helper.

A `topic` is like a named message channel.

A `message` is the data sent on a topic.

A `launch` file starts many nodes together.

Tiny warm-up example:

```text
distance_sensor node -> /distance topic -> drive_decision_node
```

In plain words:

```text
One helper sends a distance message.
Another helper reads it and decides MOVE, SLOW, or STOP.
```

## More Realistic AV Topic Graph

A real AV stack usually does not pass one fake distance number. It passes sensor packets, detections, poses, planned trajectories, and control commands.

Here is a ROS-style version of the workflow from Units 3 and 4:

```text
kitti_camera_reader node -> /sensing/camera/front/image
kitti_lidar_reader node  -> /sensing/lidar/points
lidar_perception node   -> /perception/object_clusters
localization node       -> /localization/ego_pose
planner node            -> /planning/trajectory
controller node         -> /control/command
visualizer node         -> /debug/visualization
```

In plain words:

```text
Sensors publish raw data.
Perception publishes object clusters.
Localization publishes where the ego vehicle is.
Planning publishes where to go next.
Control publishes steering, throttle, and brake commands.
```

## Connect It To Our Python Scripts

In this repo:

- `kitti_lidar_perception.py` acts like a perception node reading `/sensing/lidar/points` and producing rough `/perception/object_clusters`.
- `kitti_camera_perception.py` acts like a small camera-perception helper reading `/sensing/camera/front/image`.
- `kitti_perception_localization_demo.py` acts like a localization bridge that combines object clusters with an ego pose.
- `mini_autonomy_stack.py` acts like a tiny connected autonomy system with perception, localization, planning, control, and visualization helpers.

They are not real ROS 2 nodes. They are just beginner Python scripts that help you understand the idea.

## Run The Node-Like Scripts

Run the camera-perception-like script:

```bash
python scripts/kitti_camera_perception.py
```

Before running the LiDAR and localization demos, make sure the matching tracking-task point-cloud file exists:

```text
web_sim/user_data/pointcloud/000000.bin
```

Run the LiDAR-perception-like script:

```bash
python scripts/kitti_lidar_perception.py
```

Expected output starts like:

```text
KITTI tracking LiDAR perception demo
Input file: web_sim/user_data/pointcloud/000000.bin
Raw points: 121,238
```

If the `.bin` file is missing, the script tells you to copy it into `web_sim/user_data/pointcloud/000000.bin`.

Run the localization-like bridge:

```bash
python scripts/kitti_perception_localization_demo.py
```

Expected output starts like:

```text
KITTI tracking perception + localization-frame demo
Input file: web_sim/user_data/pointcloud/000000.bin
Localization state:
```

## Read It Like ROS 2

Open `scripts/kitti_camera_perception.py`.

Match the code to ROS-style ideas:

- Input data: `IMAGE_FILE`
- Camera processing: `load_png_rows`, `summarize_region`
- Output-like data: printed image-region summaries

Open `scripts/kitti_lidar_perception.py`.

Match the code to ROS-style ideas:

- Input data: `POINT_CLOUD_FILE`
- Perception processing: `crop_driving_roi`, `split_ground`, `voxelize`, `cluster_occupied_voxels`
- Output-like data: printed obstacle clusters

Open `scripts/kitti_perception_localization_demo.py`.

Match the code to ROS-style ideas:

- Localization state: `Pose2D`
- Odometry update: `integrate_odometry`
- Frame transform: `ego_to_map`
- Output-like data: object cluster centers in map coordinates

## Tiny Modification: Rename A Topic

Open `docs/unit5_ros2_teaser.md`.

In the topic graph above, find:

```text
/perception/object_clusters
```

Change it to:

```text
/perception/lidar_clusters
```

Then read the graph again and ask: did the topic name become clearer or less clear?

## Optional Graph Modification

Open `docs/unit5_ros2_teaser.md`.

In the topic graph above, add one new node between localization and planning:

```text
prediction node         -> /prediction/tracked_objects
```

Then read the graph again:

- Perception says what objects exist now.
- Prediction estimates where moving objects may go next.
- Planning uses that future guess to choose a safer trajectory.

## Reflection

Why might it be useful to split a big driving system into nodes instead of putting sensing, perception, localization, planning, and control in one file?

Next, Unit 6 combines the previous units into one mini challenge.
