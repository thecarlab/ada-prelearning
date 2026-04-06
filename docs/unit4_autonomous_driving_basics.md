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

## Tiny Lane Checker

Run:

```bash
python scripts/fake_lane_checker.py
```

Expected output:

```text
Fake lane checker online.
Lane status: center
Decision: KEEP GOING
```

## Try Another Lane Status

Open `scripts/fake_lane_checker.py`.

Find:

```python
lane_status = "center"
```

Try:

```python
lane_status = "left"
```

Run:

```bash
python scripts/fake_lane_checker.py
```

Expected output:

```text
Decision: TURN RIGHT
```

## Tiny Modification

Change `lane_status` to:

```python
lane_status = "right"
```

Run:

```bash
python scripts/fake_lane_checker.py
```

Expected output:

```text
Decision: TURN LEFT
```

## Reflection

What is one thing a real autonomous car might need to sense besides lane position?

