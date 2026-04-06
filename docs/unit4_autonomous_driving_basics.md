# Unit 4: Autonomous Driving Basics

Autonomous driving can sound huge, but the basic idea is easier to start with.

## Four Simple Steps

1. Sense the world.
2. Understand what is around the car.
3. Make a driving decision.
4. Send an action.

Example:

```text
Sense: the lane looks a little left
Understand: the car is not centered
Decide: adjust right
Action: TURN RIGHT
```

In Unit 3, your fake distance number was the sensor input. The output was an action like `MOVE`, `SLOW`, or `STOP`.

Autonomous-driving teams often use more specific names:

- `Perception`: detect lanes, signs, people, cones, and cars.
- `Localization`: estimate where the ego vehicle is on a map.
- `Planning`: choose a safe next place to drive.
- `Control`: turn the plan into steering, throttle, and brake commands.

The ego vehicle means the vehicle we are controlling.

## Tiny Lane Checker With A List

Run:

```bash
python scripts/fake_lane_checker.py
```

Expected output:

```text
Fake lane checker online.
Sample 1: lane is center -> KEEP GOING
Sample 2: lane is left -> TURN RIGHT
Sample 3: lane is right -> TURN LEFT
Sample 4: lane is unknown -> SLOW
```

Open `scripts/fake_lane_checker.py`.

Look for:

```python
lane_samples = ["center", "left", "right", "unknown"]
```

Python reads this list from left to right. The loop checks each lane status and prints a steering action.

## Visualize A Fake Camera Image

Real autonomous-driving datasets often include camera images. The KITTI dataset is one famous research benchmark with camera and laser scanner data.

This repo does not include real KITTI files. Instead, it uses a tiny fake KITTI-style text grid:

Run:

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

In the fake camera grid:

- `L` and `R` are lane markers.
- `S` is a fake stop sign.
- `.` is background.
- `-` is a road stripe.

## Read The Camera Code Logic

Open `scripts/fake_camera_grid.py`.

Look for:

```python
def count_pixels(frame, symbol):
```

This function counts symbols in the fake image.

Look for:

```python
def estimate_lane_offset(frame):
```

This function finds `L` and `R` lane markers and estimates if the lane is centered.

Look for:

```python
def choose_camera_action(stop_pixels, lane_offset):
```

This function chooses a simple action from the fake camera clues.

## Tiny Modification

Open `scripts/fake_data/kitti_style_camera_grid.txt`.

Change the four `S` characters to dots:

```text
......SS.......
......SS.......
```

becomes:

```text
...............
...............
```

Run:

```bash
python scripts/fake_camera_grid.py
```

Expected output now includes:

```text
Decision: KEEP GOING
```

If you want the original stop sign back, change the dots back to `S`.

## Extra Tiny Modification

Open `scripts/fake_lane_checker.py`.

Find:

```python
lane_samples = ["center", "left", "right", "unknown"]
```

Try adding another sample:

```python
lane_samples = ["center", "left", "right", "unknown", "center"]
```

Run:

```bash
python scripts/fake_lane_checker.py
```

Expected output includes:

```text
Sample 5: lane is center -> KEEP GOING
```

## Reflection

Which sensor view was easier for you to understand: the lane text list, the fake camera grid, or the fake point-cloud map?

In Unit 6, you will connect these ideas into one mini autonomy stack and try a website viewer for camera and point-cloud data.
