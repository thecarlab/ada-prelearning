# Unit 5: Tiny ROS 2 Teaser

This is only a preview.

You do not need to install ROS 2 here. You will learn the real ROS 2 material during ADA camp.

## Goal

Learn two words:

- `node`
- `topic`

## Simple Idea

Autonomous driving systems often use software pieces that talk to each other.

A `node` is like one small software helper.

A `topic` is like a named message channel.

Example:

```text
distance_sensor node -> /distance topic -> drive_decision node
```

In plain words:

```text
One helper sends a distance message.
Another helper reads it and decides MOVE, SLOW, or STOP.
```

## Connect It To Our Python

In this repo:

- `fake_distance_sensor.py` acts like a tiny sensor helper.
- `drive_decision.py` acts like a tiny decision helper.

They are not real ROS 2 nodes. They are just beginner Python scripts that help you understand the idea.

## Tiny Modification

Open `scripts/drive_decision.py`.

Find the message:

```python
print("ADA drive decision check")
```

Change it to:

```python
print("Pretend drive decision node online")
```

Run:

```bash
python scripts/drive_decision.py
```

Expected output now starts with:

```text
Pretend drive decision node online
```

To keep Unit 6 matching the starter code, change the line back after you test it:

```python
print("ADA drive decision check")
```

## Reflection

Why might it be useful to split a big driving system into smaller helpers?
