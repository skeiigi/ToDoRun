export const scene = new THREE.Scene();
export const objectsDistance = 4;

const sizes = { width: window.innerWidth, height: window.innerHeight };
export const cameraGroup = new THREE.Group();
scene.add(cameraGroup);

export let camera = new THREE.PerspectiveCamera(35, sizes.width / sizes.height, 0.1, 100);
camera.position.z = 6;
cameraGroup.add(camera);

export let renderer = null;
const canvasElement = document.querySelector("canvas.webgl");

export const initRenderer = () => {
  if (canvasElement && !canvasElement.parentNode) {
    document.body.appendChild(canvasElement);
  }

  renderer = new THREE.WebGLRenderer({
    canvas: canvasElement,
    alpha: true
  });
  renderer.setSize(sizes.width, sizes.height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
};

export const removeRenderer = () => {
  if (canvasElement && canvasElement.parentNode) {
    canvasElement.remove();
  }
  if (renderer) {
    renderer.dispose();
    renderer = null;
  }
  camera = null;
};

initRenderer();
