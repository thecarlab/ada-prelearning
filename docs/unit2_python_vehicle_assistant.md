# Unit 2: Python Vehicle Assistant

In this unit, you will run a tiny smart-car assistant.

It understands simple commands like `start`, `drive`, `park`, `charge`, `horn`, and `status`.

This unit owns beginner Python state. You will practice variables, dictionaries, lists, functions, and `if` statements before moving into real sensor data.

## Goal

Practice Python by running a script and changing a small message.

## Run The Assistant

From the project root, run:

```bash
python scripts/vehicle_assistant.py
```

Expected start:

```text
ADA Vehicle Assistant online.
Type one command: start, drive, park, charge, horn, status, or quit.
```

Try this:

```text
status
```

Expected output includes:

```text
Readiness: parked
Battery: 80%
Speed mode: safe
Last action: PARK
Commands tried: 1
```

Try:

```text
start
drive
horn
park
charge
quit
```

You should see simple vehicle updates like:

```text
Action: MOVE
Action: PARK
Action: CHARGE
```

## What The Code Is Doing

The script stores simple vehicle state:

- Battery level.
- Whether the car is parked or ready.
- Speed mode.
- Last action.
- A history of commands.

## Python Ideas In This Script

Open `scripts/vehicle_assistant.py`.

Look for this dictionary:

```python
vehicle_state = {
    "battery_percent": 80,
    "readiness": "parked",
    "speed_mode": "safe",
    "last_action": "PARK",
}
```

A dictionary stores related values with names. That is helpful for autonomous driving because a vehicle may track battery, speed, sensors, and decisions at the same time.

Look for this list:

```python
command_history = []
```

A list can remember many things in order. This script stores each command you type.

Look for this function:

```python
def print_status(state, history):
```

A function is a reusable mini-program. This one prints the vehicle state.

When you type a command, Python checks it with `if`, `elif`, and `else`.

## Tiny Modification

Open `scripts/vehicle_assistant.py`.

Find:

```python
assistant_name = "ADA Vehicle Assistant"
```

Change the name to something fun, like:

```python
assistant_name = "Blue Hen Drive Buddy"
```

Run it again:

```bash
python scripts/vehicle_assistant.py
```

## Reflection

If your vehicle assistant had one new command, what would it be?

Next, Unit 3 uses those same Python ideas to read camera and point-cloud sensor data.
