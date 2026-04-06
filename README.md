<div align="center">
  <p>
    <img src="logo/UDLogo.jpg" alt="University of Delaware logo" width="320">
    &nbsp;&nbsp;&nbsp;
    <img src="logo/CARLabLogo.png" alt="CAR Lab logo" width="150">
  </p>

  <h1>ADA Prelearning</h1>

  <p>
    A friendly browser-based prep course for students joining the
    <strong>University of Delaware Autonomous Driving Academy</strong>.
  </p>

  <p>
    <a href="https://www.pcs.udel.edu/autonomous-driving/"><strong>Official UD Autonomous Driving Academy Website</strong></a>
  </p>
</div>

---

## Welcome

This repo is a confidence builder before camp. You will try a browser coding environment, terminal commands, beginner Python, and a small autonomous-driving learning path.

The units build from basic terminal and Python skills into perception, localization, planning, control, a ROS-style system preview, and a final mini autonomy challenge.

You do not need to install Python, VS Code, ROS 2, a simulator, or any hardware.

## Start Here

Please do not create a Codespace directly from the main ADA course repository. Your experiments should happen in your own copy so the course materials stay clean for everyone.

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

## Learning Path

Follow the units in order. Each unit owns one part of the preparation path:

| Unit | Topic | What you will practice |
| --- | --- | --- |
| 0 | [Getting Started](docs/getting_started.md) | Open your own browser workspace. |
| 1 | [Linux Scavenger Hunt](docs/unit1_linux.md) | Use terminal commands and meet the AV architecture words. |
| 2 | [Python Vehicle Assistant](docs/unit2_python_vehicle_assistant.md) | Practice beginner Python state and control flow. |
| 3 | [Camera And Point-Cloud Perception](docs/unit3_sensor_and_decision.md) | Read camera and point-cloud sensor clues. |
| 4 | [Localization And Coordinate Frames](docs/unit4_autonomous_driving_basics.md) | Move perception results from ego frame into map frame. |
| 5 | [Tiny ROS 2 Teaser](docs/unit5_ros2_teaser.md) | Organize pieces as ROS-style nodes, topics, messages, and launch. |
| 6 | [Mini Autonomy Stack Challenge](docs/unit6_final_challenge.md) | Connect the earlier pieces in one final mini challenge. |

## What You Will Learn

- Open a coding environment in the browser.
- Use a few simple terminal commands.
- Run and edit basic Python scripts.
- Practice variables, lists, dictionaries, functions, loops, and `if` statements.
- Learn the core AV modules: sensing, perception, localization, planning, control, and end-to-end AV-agent research.
- Try simple KITTI tracking-task camera-image perception.
- Process a KITTI tracking-task LiDAR point cloud with a small perception pipeline.
- Transform perception clusters from ego coordinates into map coordinates.
- Preview ROS-style nodes, topics, messages, and launch concepts.
- Generate an HTML ego-vehicle route visualization that works in Codespaces.
- Open a small website that visualizes KITTI tracking-task camera images and LiDAR point clouds.

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

Try the beginner camera and point-cloud warm-ups:

```bash
python scripts/fake_camera_grid.py
python scripts/fake_pointcloud_viewer.py
```

Then run the mini autonomy stack:

```bash
python scripts/mini_autonomy_stack.py
```

The mini autonomy stack also creates:

```text
outputs/mini_autonomy_report.html
```

In Codespaces, open that file and use the built-in preview to see the ego vehicle route.

## KITTI Data Demos

This repo uses two kinds of data:

- Warm-up scripts use tiny fake data so beginners can read the whole example.
- Later units can use KITTI tracking-task camera images and LiDAR `.bin` point clouds from `web_sim/user_data/`.

Example file locations:

```text
web_sim/user_data/image/000000.png
web_sim/user_data/pointcloud/000000.bin
```

Try the real-data KITTI tracking camera demo. Then try the LiDAR demos if the matching `.bin` point-cloud file is present:

```bash
python scripts/kitti_camera_perception.py
python scripts/kitti_lidar_perception.py
python scripts/kitti_perception_localization_demo.py
```

If the point-cloud file is missing, the KITTI perception scripts tell you to copy it into:

```text
web_sim/user_data/pointcloud/000000.bin
```

The real KITTI Vision Benchmark Suite is much larger and is meant for research. Before publishing real KITTI files, check the dataset terms and citation requirements on the official KITTI page: <https://www.cvlibs.net/datasets/kitti/>

## Web Visualizer

View the KITTI tracking-task frame sequence in the browser:

```bash
python -m http.server 8000
```

Then open this page:

```text
http://127.0.0.1:8000/web_sim/
```

If you are using GitHub Codespaces, VS Code may show a port-forwarding popup for port `8000`. Open the forwarded page, then make sure the address ends with:

```text
/web_sim/
```

This website is only for visualization. It shows synchronized KITTI tracking-task camera images and LiDAR point clouds when matching files exist. Use `Next`, `Previous`, or `Play` to move through matching frame numbers.

The image and point-cloud filenames must match by frame number:

```text
web_sim/user_data/image/000000.png
web_sim/user_data/pointcloud/000000.bin
web_sim/user_data/image/000001.png
web_sim/user_data/pointcloud/000001.bin
```

The website uses these website-relative folders by default:

```text
user_data/image
user_data/pointcloud
```

The `web_sim/user_data` image and point-cloud folders are ignored by git so large dataset files do not get committed accidentally.

Longer KITTI sequences should be added only if your instructor tells you to include them.

## More Scripts To Try

```bash
python scripts/vehicle_assistant.py
python scripts/fake_distance_sensor.py
```

## Troubleshooting

- If Codespaces takes a minute to open, that is normal. Let it finish loading.
- If you do not see a terminal, click `Terminal`, then `New Terminal`.
- If `python` does not work, try `python3` instead.
- If you get lost in the terminal, run `pwd` to see where you are.
- If you opened the wrong folder, run `pwd` first. Your own fork will usually be under `/workspaces/ada-prelearning` in Codespaces.
