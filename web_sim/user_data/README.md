# KITTI User Data Folder

Put local KITTI tracking-task files here when you want the browser viewer and KITTI demo scripts to load real data.

The viewer-friendly layout is:

```text
web_sim/user_data/image/
web_sim/user_data/pointcloud/
```

Use matching frame numbers:

```text
web_sim/user_data/image/000000.png
web_sim/user_data/pointcloud/000000.bin
web_sim/user_data/image/000001.png
web_sim/user_data/pointcloud/000001.bin
```

The repo may include KITTI tracking-task camera frames in `image/`. The LiDAR perception scripts also need the matching `.bin` point-cloud file in `pointcloud/`.

Most data files in these folders are ignored by git so the repository does not accidentally commit large dataset files.
