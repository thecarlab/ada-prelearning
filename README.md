# ada-prelearning

A tiny, friendly prelearning repo for high school students joining the University of Delaware Autonomous Driving Academy (ADA) summer camp.

This is a confidence builder before camp. You will try a browser coding environment, a few terminal commands, beginner Python, and simple autonomous-driving style logic.

This is not a replacement for the first-day ADA camp ROS 2 class. ROS 2 appears here only as a tiny teaser.

## Start In Your Browser

You do not need to install Python, VS Code, ROS 2, a simulator, or any hardware.

If this repo is on GitHub:

1. Sign in to GitHub.
2. Open the `ada-prelearning` repository page.
3. Click `Code`.
4. Click the `Codespaces` tab.
5. Click `Create codespace on main`.
6. Wait for the browser coding space to open.

After the repo is published, a quick link may look like this:

```text
https://codespaces.new/OWNER/ada-prelearning
```

Replace `OWNER` with the GitHub account or organization that owns the repo.

This repo is intended to be public on GitHub, so anyone can view the learning materials. You may still need to sign in to GitHub to create a Codespace.

## What You Will Learn

- Open a coding environment in the browser.
- Use a few simple terminal commands.
- Run and edit basic Python scripts.
- Try simple autonomous-driving logic: sensing, deciding, and acting.
- Preview a few autonomous-driving ideas before camp.
- Get a tiny ROS 2 teaser without learning full ROS 2 yet.

## Units

1. [Getting Started](docs/getting_started.md)
2. [Unit 1: Linux Scavenger Hunt](docs/unit1_linux.md)
3. [Unit 2: Python Vehicle Assistant](docs/unit2_python_vehicle_assistant.md)
4. [Unit 3: Sensor And Decision Logic](docs/unit3_sensor_and_decision.md)
5. [Unit 4: Autonomous Driving Basics](docs/unit4_autonomous_driving_basics.md)
6. [Unit 5: Tiny ROS 2 Teaser](docs/unit5_ros2_teaser.md)
7. [Unit 6: Final Challenge](docs/unit6_final_challenge.md)

## Quick Test

Open a terminal in Codespaces and run:

```bash
python scripts/hello_ada.py
```

Expected output:

```text
Welcome to ADA Prelearning!
Your browser coding space is ready.
Today we will practice Python, Linux, and simple driving logic.
Action: MOVE
```

## Troubleshooting

- If Codespaces takes a minute to open, that is normal. Let it finish loading.
- If you do not see a terminal, click `Terminal`, then `New Terminal`.
- If `python` does not work, try `python3` instead.
- If you get lost in the terminal, run `pwd` to see where you are.
- If you opened the wrong folder, run `cd /workspaces/ada-prelearning` in Codespaces.

## Instructor Note

This repository supports ADA autonomous driving camp by helping students feel comfortable before camp starts. It should stay short, lightweight, and beginner friendly. It should not replace the first-day ROS 2 class or any official camp instruction.
