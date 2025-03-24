export const scene = new THREE.Scene();
export const objectsDistance = 4;

const material1 = new THREE.MeshToonMaterial({ color: "#F5F5DC", transparent: false });
export const mesh1 = new THREE.Mesh(new THREE.TorusGeometry(1, 0.4, 16, 60), material1);

const material2 = new THREE.MeshToonMaterial({ color: "#F5F5DC", transparent: false });
export const mesh2 = new THREE.Mesh(new THREE.ConeGeometry(1, 2, 32), material2);

mesh1.position.set(3, 2, 0);
mesh2.position.set(-3, -2, 0);
scene.add(mesh1, mesh2);
export const sectionMeshes = [mesh1, mesh2];

const directionalLight = new THREE.DirectionalLight("#ffffff", 0.85);
directionalLight.position.set(1, 1, 0);
scene.add(directionalLight);

const sizes = { width: window.innerWidth, height: window.innerHeight };
export const cameraGroup = new THREE.Group();
scene.add(cameraGroup);

export const camera = new THREE.PerspectiveCamera(35, sizes.width / sizes.height, 0.1, 100);
camera.position.z = 6;
cameraGroup.add(camera);

export const renderer = new THREE.WebGLRenderer({ canvas: document.querySelector("canvas.webgl"), alpha: true });
renderer.setSize(sizes.width, sizes.height);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

window.addEventListener("resize", () => {
  sizes.width = window.innerWidth;
  sizes.height = window.innerHeight;
  camera.aspect = sizes.width / sizes.height;
  camera.updateProjectionMatrix();
  renderer.setSize(sizes.width, sizes.height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
});
