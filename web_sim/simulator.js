const imageFolderInput = document.querySelector("#imageFolder");
const pointFolderInput = document.querySelector("#pointFolder");
const frameNumberInput = document.querySelector("#frameNumber");
const loadButton = document.querySelector("#loadButton");
const previousButton = document.querySelector("#previousButton");
const nextButton = document.querySelector("#nextButton");
const playButton = document.querySelector("#playButton");
const statusText = document.querySelector("#statusText");
const cameraImage = document.querySelector("#cameraImage");
const canvas = document.querySelector("#pointCanvas");
const ctx = canvas.getContext("2d");

const view = {
  forwardMin: -10,
  forwardMax: 80,
  leftMin: -45,
  leftMax: 45,
};

const fallbackLayouts = [
  { imageFolder: "user_data/image", pointFolder: "user_data/pointcloud" },
];

const imageExtensions = ["png", "jpg", "jpeg"];
let points = [];
let playTimer = null;
let isLoading = false;

function normalizePath(path) {
  const trimmed = path.trim();
  if (trimmed.startsWith("web_sim/")) {
    return `/${trimmed}`;
  }
  return trimmed;
}

function cleanFolder(folder) {
  return folder.trim().replace(/\/+$/, "");
}

function frameName(frameNumber) {
  return String(frameNumber).padStart(6, "0");
}

function setStatus(message) {
  statusText.textContent = message;
}

async function fetchOk(path) {
  const response = await fetch(normalizePath(path), { method: "HEAD" });
  return response.ok;
}

function candidateLayouts() {
  const primary = {
    imageFolder: cleanFolder(imageFolderInput.value),
    pointFolder: cleanFolder(pointFolderInput.value),
  };
  const layouts = [primary];

  for (const layout of fallbackLayouts) {
    const alreadyAdded = layouts.some(
      (item) => item.imageFolder === layout.imageFolder && item.pointFolder === layout.pointFolder
    );
    if (!alreadyAdded) {
      layouts.push(layout);
    }
  }

  return layouts;
}

async function findFramePaths(frameNumber) {
  const name = frameName(frameNumber);

  for (const layout of candidateLayouts()) {
    const pointPath = `${layout.pointFolder}/${name}.bin`;
    if (!(await fetchOk(pointPath))) {
      continue;
    }

    for (const extension of imageExtensions) {
      const imagePath = `${layout.imageFolder}/${name}.${extension}`;
      if (await fetchOk(imagePath)) {
        return { imagePath, pointPath, layout };
      }
    }
  }

  throw new Error(`Could not find matching image and point cloud for frame ${name}.`);
}

function loadCamera(path) {
  return new Promise((resolve, reject) => {
    cameraImage.onload = () => resolve();
    cameraImage.onerror = () => reject(new Error(`Could not load image: ${path}`));
    cameraImage.src = normalizePath(path);
  });
}

async function loadPointCloud(path) {
  const response = await fetch(normalizePath(path));

  if (!response.ok) {
    throw new Error(`Could not load point cloud: ${path}`);
  }

  return parseKittiBin(await response.arrayBuffer());
}

function parseKittiBin(buffer) {
  const floats = new Float32Array(buffer);
  const parsedPoints = [];

  for (let index = 0; index + 3 < floats.length; index += 4) {
    parsedPoints.push({
      forward: floats[index],
      left: floats[index + 1],
      up: floats[index + 2],
      reflectance: floats[index + 3],
    });
  }

  return parsedPoints;
}

function toPixel(point) {
  return {
    x: ((point.left - view.leftMin) / (view.leftMax - view.leftMin)) * canvas.width,
    y: canvas.height - ((point.forward - view.forwardMin) / (view.forwardMax - view.forwardMin)) * canvas.height,
  };
}

function fitViewToPoints() {
  if (!points.length) {
    return;
  }

  const bounds = points.reduce(
    (current, point) => ({
      leftMin: Math.min(current.leftMin, point.left),
      leftMax: Math.max(current.leftMax, point.left),
      forwardMin: Math.min(current.forwardMin, point.forward),
      forwardMax: Math.max(current.forwardMax, point.forward),
    }),
    {
      leftMin: Infinity,
      leftMax: -Infinity,
      forwardMin: Infinity,
      forwardMax: -Infinity,
    }
  );

  const leftCenter = (bounds.leftMin + bounds.leftMax) / 2;
  const forwardCenter = (bounds.forwardMin + bounds.forwardMax) / 2;
  const leftSpan = Math.max(1, bounds.leftMax - bounds.leftMin);
  const forwardSpan = Math.max(1, bounds.forwardMax - bounds.forwardMin);
  const canvasRatio = canvas.width / canvas.height;
  const dataRatio = leftSpan / forwardSpan;
  const padding = 1.12;

  let fittedLeftSpan = leftSpan * padding;
  let fittedForwardSpan = forwardSpan * padding;

  if (dataRatio > canvasRatio) {
    fittedForwardSpan = fittedLeftSpan / canvasRatio;
  } else {
    fittedLeftSpan = fittedForwardSpan * canvasRatio;
  }

  view.leftMin = leftCenter - fittedLeftSpan / 2;
  view.leftMax = leftCenter + fittedLeftSpan / 2;
  view.forwardMin = forwardCenter - fittedForwardSpan / 2;
  view.forwardMax = forwardCenter + fittedForwardSpan / 2;
}

function gridStart(value) {
  return Math.ceil(value / 10) * 10;
}

function drawGrid() {
  ctx.fillStyle = "#020617";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#1e293b";
  ctx.lineWidth = 1;

  for (let left = gridStart(view.leftMin); left <= view.leftMax; left += 10) {
    const start = toPixel({ left, forward: view.forwardMin });
    const end = toPixel({ left, forward: view.forwardMax });
    ctx.beginPath();
    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.stroke();
  }

  for (let forward = gridStart(view.forwardMin); forward <= view.forwardMax; forward += 10) {
    const start = toPixel({ left: view.leftMin, forward });
    const end = toPixel({ left: view.leftMax, forward });
    ctx.beginPath();
    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.stroke();
  }

  const centerStart = toPixel({ left: 0, forward: view.forwardMin });
  const centerEnd = toPixel({ left: 0, forward: view.forwardMax });
  ctx.strokeStyle = "#94a3b8";
  ctx.setLineDash([8, 10]);
  ctx.beginPath();
  ctx.moveTo(centerStart.x, centerStart.y);
  ctx.lineTo(centerEnd.x, centerEnd.y);
  ctx.stroke();
  ctx.setLineDash([]);
}

function colorForHeight(up, reflectance) {
  const height = Math.max(0, Math.min(1, (up + 2.5) / 5));
  const brightness = Math.max(90, Math.min(255, Math.round(reflectance * 255)));
  const red = Math.round(80 + height * 175);
  const green = Math.round(brightness * (1 - height * 0.35));
  const blue = Math.round(255 - height * 180);
  return `rgb(${red} ${green} ${blue})`;
}

function drawPoints() {
  const maxDrawnPoints = 60000;
  const stride = Math.max(1, Math.ceil(points.length / maxDrawnPoints));
  let visibleCount = 0;

  for (let index = 0; index < points.length; index += stride) {
    const point = points[index];
    if (point.forward < view.forwardMin || point.forward > view.forwardMax) {
      continue;
    }
    if (point.left < view.leftMin || point.left > view.leftMax) {
      continue;
    }

    const pixel = toPixel(point);
    ctx.fillStyle = colorForHeight(point.up, point.reflectance);
    ctx.fillRect(pixel.x, pixel.y, 2, 2);
    visibleCount += 1;
  }

  return visibleCount;
}

function drawLabels(visibleCount) {
  ctx.fillStyle = "#e2e8f0";
  ctx.font = "14px system-ui, sans-serif";
  ctx.textAlign = "left";
  ctx.fillText("KITTI LiDAR top view (auto-fit full scan)", 18, 26);
  ctx.fillText(`loaded points: ${points.length.toLocaleString()}`, 18, 48);
  ctx.fillText(`drawn sample points: ${visibleCount.toLocaleString()}`, 18, 70);
}

function drawPointCloud() {
  drawGrid();
  const visibleCount = drawPoints();
  drawLabels(visibleCount);
}

async function loadFrame(frameNumber) {
  const frame = Math.max(0, Number(frameNumber) || 0);
  const name = frameName(frame);
  setStatus(`Loading frame ${name}...`);

  const paths = await findFramePaths(frame);
  await loadCamera(paths.imagePath);
  points = await loadPointCloud(paths.pointPath);
  fitViewToPoints();
  drawPointCloud();

  frameNumberInput.value = frame;
  imageFolderInput.value = paths.layout.imageFolder;
  pointFolderInput.value = paths.layout.pointFolder;
  setStatus(`Frame ${name}: loaded ${points.length.toLocaleString()} points.`);
}

async function goToFrame(frameNumber) {
  if (isLoading) {
    return true;
  }

  isLoading = true;

  try {
    await loadFrame(frameNumber);
    return true;
  } catch (error) {
    setStatus(error.message);
    stopPlayback();
    return false;
  } finally {
    isLoading = false;
  }
}

function currentFrame() {
  return Math.max(0, Number(frameNumberInput.value) || 0);
}

function stopPlayback() {
  if (playTimer) {
    clearInterval(playTimer);
    playTimer = null;
  }
  playButton.textContent = "Play";
}

async function nextFrame() {
  const loaded = await goToFrame(currentFrame() + 1);
  if (!loaded && playTimer) {
    stopPlayback();
  }
}

loadButton.addEventListener("click", () => goToFrame(currentFrame()));
previousButton.addEventListener("click", () => goToFrame(Math.max(0, currentFrame() - 1)));
nextButton.addEventListener("click", nextFrame);
playButton.addEventListener("click", () => {
  if (playTimer) {
    stopPlayback();
    return;
  }

  playButton.textContent = "Pause";
  playTimer = setInterval(nextFrame, 900);
});

drawGrid();
goToFrame(0);
