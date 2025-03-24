export const scene = new THREE.Scene();
export const objectsDistance = 4;

const sizes = { width: window.innerWidth, height: window.innerHeight };
export const cameraGroup = new THREE.Group();
scene.add(cameraGroup);

export const camera = new THREE.PerspectiveCamera(35, sizes.width / sizes.height, 0.1, 100);
camera.position.z = 6;
cameraGroup.add(camera);

export const renderer = new THREE.WebGLRenderer({ 
  canvas: document.querySelector("canvas.webgl"), 
  alpha: true 
});
renderer.setSize(sizes.width, sizes.height);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
