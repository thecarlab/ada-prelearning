# Unit 4: Localization And Coordinate Frames

Autonomous driving can sound huge, but one core idea is simple: every module must agree on where things are.

Unit 3 focused on sensor perception: camera-image clues, ego-frame point positions, and KITTI tracking-task LiDAR obstacle clusters.

Unit 4 focuses on localization and coordinate frames: taking a perception result like "6.6 meters forward and 2.6 meters right of the ego vehicle" and placing it into a shared map frame.

This unit owns map-frame localization. It reuses perception clusters, but it does not teach camera perception, LiDAR clustering, ROS topics, or controller tuning.

## Goal

Practice these autonomous-driving ideas:

- `Ego frame`: positions measured relative to the vehicle.
- `Map frame`: positions measured in a shared world or map.
- `Pose`: the ego vehicle's `x`, `y`, and heading.
- `Odometry`: motion information such as speed and yaw rate.
- `Transform`: math that moves a point from one frame to another.

Practice these Python ideas:

- A dataclass can group related values.
- A function can calculate a new pose.
- A function can transform coordinates.
- A loop can print several transformed perception clusters.

The ego vehicle means the vehicle our code is describing.

## Coordinate Frame Idea

Perception often starts in the ego frame:

```text
object: 6.6 meters forward, 2.6 meters right of the ego vehicle
```

Localization gives the ego pose in the map frame:

```text
ego pose: x=101.39m, y=20.13m, yaw=5.4deg
```

After a transform, planning can reason in one shared frame:

```text
object map position: x=108.3m, y=18.2m
```

That is the main experiment for this unit.

## Run The Localization Transform Demo

This script computes the rough perception clusters internally, then focuses on the localization transform. You do not need to rerun Unit 3 first.

First make sure the matching point-cloud file exists:

```text
web_sim/user_data/pointcloud/000000.bin
```

```bash
python scripts/kitti_perception_localization_demo.py
```

Expected output starts like:

```text
KITTI tracking perception + localization-frame demo
Input file: web_sim/user_data/pointcloud/000000.bin
Localization state:
- start pose: x=100.00m, y=20.00m, yaw=5.0deg
- odometry input: speed=7.0m/s, yaw_rate=2.0deg/s, dt=0.2s
- predicted pose: x=101.39m, y=20.13m, yaw=5.4deg
```

Expected output also includes:

```text
Perception clusters transformed into the map frame:
1. large structure or mixed obstacle | ego=(18.7m forward, -4.4m left) -> map=(120.4m, 17.5m)
2. vehicle-sized obstacle | ego=(6.6m forward, -2.6m left) -> map=(108.3m, 18.2m)
```

If the `.bin` file is missing, the script tells you to copy it into `web_sim/user_data/pointcloud/000000.bin`.

Why this matters:

- Perception often reports objects in the ego vehicle frame.
- Localization estimates the ego vehicle pose in a map frame.
- Planning needs objects and the ego vehicle in a shared frame before it can reason about safe paths.

This script uses a small odometry update and a 2D transform. Production AV localization can fuse GNSS, IMU, wheel odometry, LiDAR or camera map matching, and SLAM.

## Read The Localization Code Logic

Open `scripts/kitti_perception_localization_demo.py`.

Look for:

```text
integrate_odometry
```

This predicts the next ego pose from motion measurements.

Look for:

```text
ego_to_map
```

This transforms a perception result from ego coordinates into map coordinates.

## Tiny Modification: Change The Pose

Open `scripts/kitti_perception_localization_demo.py`.

Find:

```python
start_pose = Pose2D(x_m=100.0, y_m=20.0, yaw_rad=math.radians(5.0))
```

Try changing the yaw to `15.0` degrees:

```python
start_pose = Pose2D(x_m=100.0, y_m=20.0, yaw_rad=math.radians(15.0))
```

Run:

```bash
python scripts/kitti_perception_localization_demo.py
```

Watch how the map coordinates change even though the ego-frame perception clusters are the same.

## Tiny Modification: Change The Speed

Find:

```python
speed_mps=7.0,
```

Try:

```python
speed_mps=12.0,
```

Run the script again. Watch how the predicted pose changes. Then change the speed back to `7.0`.

## Reflection

Why does planning need perception objects and the ego vehicle to be in a shared coordinate frame?

In Unit 5, you will preview how these pieces become ROS-style nodes and topics.
