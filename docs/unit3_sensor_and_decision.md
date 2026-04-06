# Unit 3: Sensor Data And Decision Logic

Autonomous vehicles use sensors to learn about the world.

Today we will fake distance sensor readings and a tiny point cloud.

## Goal

Practice these Python ideas:

- A variable stores one value.
- A list stores many values.
- A function is a named block of code.
- A loop repeats code.
- An `if` statement makes a decision.

Use simple sensor rules:

- Far away means `MOVE`.
- Getting close means `SLOW`.
- Too close means `STOP`.

## Run The Fake Sensor

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

## Read The Code Logic

Open `scripts/fake_distance_sensor.py`.

Look for this list:

```python
distance_readings = [8, 4, 1]
```

That list means:

```text
First reading: 8 meters
Second reading: 4 meters
Third reading: 1 meter
```

Look for this function:

```python
def choose_distance_action(distance_meters):
```

That function receives one distance number and returns one action.

The rule is:

```text
2 meters or less -> STOP
5 meters or less -> SLOW
more than 5 meters -> MOVE
```

The loop runs the same rule for every fake sensor reading.

## Visualize A Fake Point Cloud

A point cloud is a group of points in 3D space. Real autonomous-driving datasets can have many thousands of points from LiDAR.

Here we use a tiny fake KITTI-style CSV file so it runs in the browser:

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
```

In the map:

- `E` is your vehicle.
- `O` is a cone.
- `C` is a car.
- `P` is a pedestrian.
- `T` is a tree.

This is not real KITTI data. It is a tiny fake file that helps you understand what point-cloud rows can feel like.

## Run The Combined Decision Script

Run:

```bash
python scripts/drive_decision.py
```

Expected output:

```text
ADA drive decision check
Sensor packet:
- distance_meters: 8
- lane_status: center
- traffic_light: green
- battery_percent: 72
- detected_signs: none
Decision: MOVE
Reason: path looks clear and lane is centered
Nice focus, ADA driver!
```

## Read The Combined Code Logic

Open `scripts/drive_decision.py`.

Look for this dictionary:

```python
sensor_packet = {
    "distance_meters": 8,
    "lane_status": "center",
    "traffic_light": "green",
    "battery_percent": 72,
    "detected_signs": [],
}
```

A dictionary stores values with labels. This is helpful because autonomous-driving programs often pass around many sensor values.

The function `choose_action(packet)` checks safety first:

```text
red light or stop sign -> STOP
very close object -> STOP
nearby object -> SLOW
low battery -> CHARGE
lane left -> TURN RIGHT
lane right -> TURN LEFT
lane centered -> MOVE
```

This is not a real self-driving car. It is a friendly practice version of sensing, deciding, and acting.

## Tiny Modification

Open `scripts/fake_distance_sensor.py`.

Find:

```python
distance_readings = [8, 4, 1]
```

Add one more reading:

```python
distance_readings = [8, 4, 1, 10]
```

Run:

```bash
python scripts/fake_distance_sensor.py
```

Expected output now includes:

```text
Reading 4: 10 meters -> MOVE
```

## Reflection

Why is it useful to test the same driving rule with more than one sensor reading?
