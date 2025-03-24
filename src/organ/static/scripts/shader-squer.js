import { scene } from './shader-config.js';

const material1 = new THREE.MeshToonMaterial({ color: "#F5F5DC", transparent: false });
export const mesh1 = new THREE.Mesh(new THREE.TorusGeometry(1, 0.4, 16, 60), material1);

const material2 = new THREE.MeshToonMaterial({ color: "#F5F5DC", transparent: false });
export const mesh2 = new THREE.Mesh(new THREE.ConeGeometry(1, 2, 32), material2);

mesh1.position.set(3, 2, 0);
mesh2.position.set(-3, -2, 0);

const shouldRenderMeshes = window.innerWidth > 768;
mesh1.visible = shouldRenderMeshes;
mesh2.visible = shouldRenderMeshes;

scene.add(mesh1, mesh2);

export const sectionMeshes = [mesh1, mesh2];

const directionalLight = new THREE.DirectionalLight("#ffffff", 0.85);
directionalLight.position.set(1, 1, 0);
scene.add(directionalLight);

export const checkScreenSize = () => {
  const shouldRender = window.innerWidth > 768;
  mesh1.visible = shouldRender;
  mesh2.visible = shouldRender;
};
