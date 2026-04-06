const canvas = document.querySelector("#lidarCanvas");
const ctx = canvas.getContext("2d");

const cameraImage = document.querySelector("#cameraImage");
const cameraPath = document.querySelector("#cameraPath");
const pointPath = document.querySelector("#pointPath");
const loadPathsButton = document.querySelector("#loadPathsButton");
const resetButton = document.querySelector("#resetButton");
const stepButton = document.querySelector("#stepButton");
const playButton = document.querySelector("#playButton");
const cameraFile = document.querySelector("#cameraFile");
const pointFile = document.querySelector("#pointFile");
const zFilter = document.querySelector("#zFilter");
const zFilterValue = document.querySelector("#zFilterValue");
const sensorRange = document.querySelector("#sensorRange");
const sensorRangeValue = document.querySelector("#sensorRangeValue");
const perceptionText = document.querySelector("#perceptionText");
const localizationText = document.querySelector("#localizationText");
const planningText = document.querySelector("#planningText");
const controlText = document.querySelector("#controlText");

const state = {
  points: [],
  ego: { left: 0, forward: 0, heading: 0 },
  running: false,
  lastTick: 0,
  control: { steering: "straight", throttle: 0, brake: 1 },
  plan: "waiting for data",
};

const view = {
  leftMin: -18,
  leftMax: 18,
  forwardMin: 0,
  forwardMax: 55,
};

function normalizePath(path) {
  const trimmed = path.trim();
  if (trimmed.startsWith("web_sim/")) {
    return `/${trimmed}`;
  }
  return trimmed;
}

function loadCameraFromPath(path) {
  cameraImage.src = normalizePath(path);
}

async function loadPointCloudFromPath(path) {
  const normalizedPath = normalizePath(path);
  const response = await fetch(normalizedPath);
  if (!response.ok) {
    throw new Error(`Could not load ${path}. Check the path and run the web server from the repo root.`);
  }

  if (normalizedPath.toLowerCase().endsWith(".bin")) {
    const buffer = await response.arrayBuffer();
    state.points = parseKittiBin(buffer);
  } else {
    const text = await response.text();
    state.points = parseCsvPointCloud(text);
  }

  resetEgo();
  updateStack();
  draw();
}

function parseKittiBin(buffer) {
  const floats = new Float32Array(buffer);
  const points = [];

  for (let index = 0; index + 3 < floats.length; index += 4) {
    points.push({
      forward: floats[index],
      left: floats[index + 1],
      up: floats[index + 2],
      reflectance: floats[index + 3],
      label: "lidar",
    });
  }

  return points;
}

function parseCsvPointCloud(text) {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  const header = lines.shift().split(",").map((value) => value.trim().toLowerCase());

  return lines.map((line) => {
    const values = line.split(",").map((value) => value.trim());
    const row = Object.fromEntries(header.map((name, index) => [name, values[index]]));
    const forward = Number(row.forward ?? row.x ?? 0);
    const left = Number(row.left ?? row.y ?? 0);
    const up = Number(row.up ?? row.z ?? 0);
    const reflectance = Number(row.reflectance ?? row.intensity ?? 0.5);

    return {
      forward,
      left,
      up,
      reflectance,
      label: row.label ?? "sample",
    };
  });
}

function resetEgo() {
  state.ego = { left: 0, forward: 0, heading: 0 };
  state.running = false;
  playButton.textContent = "Play";
  updateStack();
  draw();
}

function pointsInEgoFrame() {
  return state.points.map((point) => ({
    ...point,
    relativeForward: point.forward - state.ego.forward,
    relativeLeft: point.left - state.ego.left,
  }));
}

function perceive() {
  const obstacleZ = Number(zFilter.value);
  const range = Number(sensorRange.value);
  const laneHalfWidth = 1.5;

  const candidates = pointsInEgoFrame()
    .filter((point) => point.relativeForward > 0)
    .filter((point) => point.relativeForward <= range)
    .filter((point) => Math.abs(point.relativeLeft) <= laneHalfWidth)
    .filter((point) => point.up >= obstacleZ);

  const nearest = candidates.reduce((best, point) => {
    if (!best || point.relativeForward < best.relativeForward) {
      return point;
    }
    return best;
  }, null);

  return {
    nearest,
    obstacleCount: candidates.length,
    laneOffset: state.ego.left,
  };
}

function plan(perception) {
  if (!state.points.length) {
    return { action: "WAIT", reason: "no point cloud loaded", targetLeft: state.ego.left };
  }

  if (perception.nearest && perception.nearest.relativeForward < 5) {
    return { action: "STOP", reason: "obstacle is very close", targetLeft: state.ego.left };
  }

  if (perception.nearest && perception.nearest.relativeForward < 12) {
    const targetLeft = perception.nearest.relativeLeft >= 0 ? -2.2 : 2.2;
    return { action: "AVOID", reason: "obstacle is in the ego lane", targetLeft };
  }

  if (Math.abs(state.ego.left) > 0.2) {
    return { action: "CENTER", reason: "return to lane center", targetLeft: 0 };
  }

  return { action: "CRUISE", reason: "front lane is clear", targetLeft: 0 };
}

function controlFor(planResult) {
  if (planResult.action === "WAIT" || planResult.action === "STOP") {
    return { steering: "straight", throttle: 0, brake: 1 };
  }

  const error = planResult.targetLeft - state.ego.left;
  let steering = "straight";
  if (error < -0.15) {
    steering = "left";
  } else if (error > 0.15) {
    steering = "right";
  }

  return { steering, throttle: planResult.action === "AVOID" ? 0.25 : 0.45, brake: 0 };
}

function simulationStep(seconds = 0.5) {
  const perception = perceive();
  const planResult = plan(perception);
  const control = controlFor(planResult);

  if (control.brake === 0) {
    const targetError = planResult.targetLeft - state.ego.left;
    state.ego.left += Math.max(-0.35, Math.min(0.35, targetError));
    state.ego.forward += control.throttle * seconds * 8;
  }

  state.plan = `${planResult.action}: ${planResult.reason}`;
  state.control = control;
  updateStack();
  draw();
}

function updateStack() {
  const perception = perceive();
  const planResult = plan(perception);
  const control = controlFor(planResult);
  state.plan = `${planResult.action}: ${planResult.reason}`;
  state.control = control;

  if (perception.nearest) {
    perceptionText.textContent =
      `${perception.obstacleCount} obstacle points in lane. Nearest point is ` +
      `${perception.nearest.relativeForward.toFixed(1)} m ahead and ` +
      `${perception.nearest.relativeLeft.toFixed(1)} m left.`;
  } else if (state.points.length) {
    perceptionText.textContent = "No obstacle points in the ego lane after the current z filter.";
  } else {
    perceptionText.textContent = "Load a point cloud to begin.";
  }

  localizationText.textContent =
    `Ego pose: left ${state.ego.left.toFixed(1)} m, ` +
    `forward ${state.ego.forward.toFixed(1)} m, heading ${state.ego.heading.toFixed(0)} deg.`;
  planningText.textContent = state.plan;
  controlText.textContent =
    `steering=${control.steering}, throttle=${control.throttle.toFixed(2)}, brake=${control.brake.toFixed(2)}`;
}

function toPixel(point) {
  const x = ((point.left - view.leftMin) / (view.leftMax - view.leftMin)) * canvas.width;
  const y = canvas.height - ((point.forward - view.forwardMin) / (view.forwardMax - view.forwardMin)) * canvas.height;
  return { x, y };
}

function drawGrid() {
  ctx.fillStyle = "#020617";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#1e293b";
  ctx.lineWidth = 1;
  for (let left = -15; left <= 15; left += 5) {
    const start = toPixel({ left, forward: view.forwardMin });
    const end = toPixel({ left, forward: view.forwardMax });
    ctx.beginPath();
    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.stroke();
  }

  for (let forward = 0; forward <= 55; forward += 5) {
    const start = toPixel({ left: view.leftMin, forward });
    const end = toPixel({ left: view.leftMax, forward });
    ctx.beginPath();
    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.stroke();
  }

  ctx.strokeStyle = "#f8fafc";
  ctx.setLineDash([10, 12]);
  [-1.75, 1.75].forEach((left) => {
    const start = toPixel({ left, forward: 0 });
    const end = toPixel({ left, forward: 55 });
    ctx.beginPath();
    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.stroke();
  });
  ctx.setLineDash([]);
}

function drawPoints() {
  const relativePoints = pointsInEgoFrame();
  const pointLimit = 25000;
  const stride = Math.max(1, Math.ceil(relativePoints.length / pointLimit));

  for (let index = 0; index < relativePoints.length; index += stride) {
    const point = relativePoints[index];
    if (point.relativeForward < view.forwardMin || point.relativeForward > view.forwardMax) {
      continue;
    }
    if (point.relativeLeft < view.leftMin || point.relativeLeft > view.leftMax) {
      continue;
    }

    const pixel = toPixel({ left: point.relativeLeft, forward: point.relativeForward });
    const brightness = Math.max(80, Math.min(255, Math.round(point.reflectance * 255)));
    ctx.fillStyle = point.up > Number(zFilter.value) ? `rgb(255 ${brightness} 120)` : `rgb(90 ${brightness} 255)`;
    ctx.fillRect(pixel.x, pixel.y, 2, 2);
  }
}

function drawEgo() {
  const ego = toPixel({ left: 0, forward: 0 });

  ctx.fillStyle = "#22c55e";
  ctx.beginPath();
  ctx.moveTo(ego.x, ego.y - 20);
  ctx.lineTo(ego.x - 13, ego.y + 15);
  ctx.lineTo(ego.x + 13, ego.y + 15);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#052e16";
  ctx.font = "bold 13px monospace";
  ctx.textAlign = "center";
  ctx.fillText("E", ego.x, ego.y + 4);
}

function drawSensorBox() {
  const range = Number(sensorRange.value);
  const topLeft = toPixel({ left: -1.5, forward: range });
  const bottomRight = toPixel({ left: 1.5, forward: 0 });

  ctx.strokeStyle = "#facc15";
  ctx.lineWidth = 2;
  ctx.strokeRect(topLeft.x, topLeft.y, bottomRight.x - topLeft.x, bottomRight.y - topLeft.y);
}

function drawLabels() {
  ctx.fillStyle = "#e2e8f0";
  ctx.font = "14px system-ui, sans-serif";
  ctx.textAlign = "left";
  ctx.fillText("Top-down LiDAR: front is up, left/right are ego-relative", 18, 24);
  ctx.fillText(`points: ${state.points.length.toLocaleString()}`, 18, 46);
}

function draw() {
  drawGrid();
  drawPoints();
  drawSensorBox();
  drawEgo();
  drawLabels();
}

function tick(time) {
  if (!state.running) {
    state.lastTick = 0;
    return;
  }

  if (!state.lastTick) {
    state.lastTick = time;
  }

  const elapsed = (time - state.lastTick) / 1000;
  if (elapsed > 0.35) {
    simulationStep(elapsed);
    state.lastTick = time;
  }

  requestAnimationFrame(tick);
}

loadPathsButton.addEventListener("click", async () => {
  try {
    loadCameraFromPath(cameraPath.value);
    await loadPointCloudFromPath(pointPath.value);
  } catch (error) {
    perceptionText.textContent = error.message;
  }
});

resetButton.addEventListener("click", resetEgo);
stepButton.addEventListener("click", () => simulationStep());
playButton.addEventListener("click", () => {
  state.running = !state.running;
  playButton.textContent = state.running ? "Pause" : "Play";
  requestAnimationFrame(tick);
});

cameraFile.addEventListener("change", () => {
  const file = cameraFile.files[0];
  if (file) {
    cameraImage.src = URL.createObjectURL(file);
  }
});

pointFile.addEventListener("change", async () => {
  const file = pointFile.files[0];
  if (!file) {
    return;
  }

  if (file.name.toLowerCase().endsWith(".bin")) {
    state.points = parseKittiBin(await file.arrayBuffer());
  } else {
    state.points = parseCsvPointCloud(await file.text());
  }

  resetEgo();
});

zFilter.addEventListener("input", () => {
  zFilterValue.textContent = zFilter.value;
  updateStack();
  draw();
});

sensorRange.addEventListener("input", () => {
  sensorRangeValue.textContent = `${sensorRange.value} m`;
  updateStack();
  draw();
});

loadCameraFromPath(cameraPath.value);
loadPointCloudFromPath(pointPath.value).catch((error) => {
  perceptionText.textContent = error.message;
  draw();
});
