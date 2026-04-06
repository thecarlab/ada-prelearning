# ada-prelearning

A tiny, friendly prelearning repo for high school students joining the University of Delaware Autonomous Driving Academy (ADA) summer camp.

This is a confidence builder before camp. You will try a browser coding environment, a few terminal commands, beginner Python, and simple autonomous-driving style logic.

The later units now include a tiny autonomy stack with perception, localization, planning, and control. They also include a browser viewer where students can visualize an ego vehicle, a camera frame, and KITTI-style point-cloud data.

This is not a replacement for the first-day ADA camp ROS 2 class. ROS 2 appears here only as a tiny teaser.

## Data Note

This repo uses tiny fake data only. Some examples are "KITTI-style" because they copy the idea of camera images and LiDAR point clouds used in autonomous-driving research, but they do not include real KITTI files.

The real KITTI Vision Benchmark Suite is much larger and is meant for research. You can learn more from the official KITTI page: <https://www.cvlibs.net/datasets/kitti/>

## Start In Your Own Browser Workspace

You do not need to install Python, VS Code, ROS 2, a simulator, or any hardware.

Please do not create a Codespace directly from the main ADA course repository. Your experiments should happen in your own copy so the course materials stay clean for everyone.

Recommended student workflow:

1. Sign in to GitHub.
2. Open the main `ada-prelearning` repository page.
3. Click `Fork`.
4. Create the fork under your own GitHub account.
5. Open your fork, not the main course repo.
6. Click `Code`.
7. Click the `Codespaces` tab.
8. Click `Create codespace on main`.
9. Wait for your browser coding space to open.

Your fork URL will look something like this:

```text
https://github.com/YOUR-GITHUB-USERNAME/ada-prelearning
```

A Codespaces quick link for your own fork may look like this:

```text
https://codespaces.new/YOUR-GITHUB-USERNAME/ada-prelearning
```

Replace `YOUR-GITHUB-USERNAME` with your GitHub username. This repo is intended to be public on GitHub, so anyone can view the learning materials. You may still need to sign in to GitHub to create a fork and Codespace.

## What You Will Learn

- Open a coding environment in the browser.
- Use a few simple terminal commands.
- Run and edit basic Python scripts.
- Try simple autonomous-driving logic: sensing, deciding, and acting.
- See how perception, localization, planning, and control can connect.
- Practice variables, lists, dictionaries, functions, loops, and `if` statements.
- Visualize tiny fake camera-image and point-cloud data in the terminal.
- Generate an HTML ego-vehicle route visualization that works in Codespaces.
- Open a small website that can load instructor-provided KITTI camera images and Velodyne point clouds.
- Preview a few autonomous-driving ideas before camp.
- Get a tiny ROS 2 teaser without learning full ROS 2 yet.

## Units

1. [Getting Started](docs/getting_started.md)
2. [Unit 1: Linux Scavenger Hunt](docs/unit1_linux.md)
3. [Unit 2: Python Vehicle Assistant](docs/unit2_python_vehicle_assistant.md)
4. [Unit 3: Sensor And Decision Logic](docs/unit3_sensor_and_decision.md)
5. [Unit 4: Autonomous Driving Basics](docs/unit4_autonomous_driving_basics.md)
6. [Unit 5: Tiny ROS 2 Teaser](docs/unit5_ros2_teaser.md)
7. [Unit 6: Mini Autonomy Stack Challenge](docs/unit6_final_challenge.md)

## Quick Test

Open a terminal in your own Codespace and run:

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

Try one of the visual demos:

```bash
python scripts/fake_camera_grid.py
python scripts/fake_pointcloud_viewer.py
python scripts/mini_autonomy_stack.py
```

The mini autonomy stack also creates:

```text
outputs/mini_autonomy_report.html
```

In Codespaces, open that file and use the built-in preview to see the ego vehicle route.

Try the website viewer:

```bash
python -m http.server 8000
```

In Codespaces, open the forwarded port and add `/web_sim/` to the URL.

The website starts with tiny sample data. If your instructor provides KITTI files, place them under:

```text
web_sim/user_data/image_2/000000.png
web_sim/user_data/velodyne/000000.bin
```

Then load these website-relative paths:

```text
user_data/image_2/000000.png
user_data/velodyne/000000.bin
```

The `web_sim/user_data` image and point-cloud folders are ignored by git so large dataset files do not get committed accidentally.

Other Python scripts to try:

```bash
python scripts/vehicle_assistant.py
python scripts/fake_distance_sensor.py
python scripts/fake_lane_checker.py
python scripts/drive_decision.py
```

## Troubleshooting

- If Codespaces takes a minute to open, that is normal. Let it finish loading.
- If you do not see a terminal, click `Terminal`, then `New Terminal`.
- If `python` does not work, try `python3` instead.
- If you get lost in the terminal, run `pwd` to see where you are.
- If you opened the wrong folder, run `pwd` first. Your own fork will usually be under `/workspaces/ada-prelearning` in Codespaces.
