# Unit 2: Python Vehicle Assistant

In this unit, you will run a tiny smart-car assistant.

It understands simple commands like `start`, `drive`, `park`, `charge`, `horn`, and `status`.

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

