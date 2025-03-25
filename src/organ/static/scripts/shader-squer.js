import { scene, removeRenderer, initRenderer } from './shader-config.js';

let mesh1 = null;
let mesh2 = null;
export let sectionMeshes = [];

const createMeshes = () => {
  const material1 = new THREE.MeshToonMaterial({ color: "#F5F5DC", transparent: false });
  mesh1 = new THREE.Mesh(new THREE.TorusGeometry(1, 0.4, 16, 60), material1);

  const material2 = new THREE.MeshToonMaterial({ color: "#F5F5DC", transparent: false });
  mesh2 = new THREE.Mesh(new THREE.ConeGeometry(1, 2, 32), material2);

  mesh1.position.set(3, 2, 0);
  mesh2.position.set(-3, -2, 0);

  sectionMeshes = [mesh1, mesh2];
  scene.add(mesh1, mesh2);
};

const directionalLight = new THREE.DirectionalLight("#ffffff", 0.85);
directionalLight.position.set(1, 1, 0);
scene.add(directionalLight);

export const checkScreenSize = () => {
  const shouldRender = window.innerWidth > 768;

  if (shouldRender) {
    initRenderer();
    createMeshes();
  } else {
    scene.remove(mesh1, mesh2);
    mesh1 = null;
    mesh2 = null;
    sectionMeshes = [];
    removeRenderer();
  }
};

checkScreenSize();
