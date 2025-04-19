import { scene, removeRenderer, initRenderer } from './shader-config.js';

let model1 = null;
let model2 = null;
export let sectionMeshes = [];

const loadingManager = new THREE.LoadingManager();
const gltfLoader = new THREE.GLTFLoader(loadingManager);

const createMeshes = () => {
  gltfLoader.load(
    window.MODEL_PATHS.model1,
    (gltf) => {
      model1 = gltf.scene;
      model1.position.set(3, 0, 0);
      model1.scale.set(0.5, 0.5, 0.5);
      scene.add(model1);
      sectionMeshes.push(model1);
    },
    undefined,
    (error) => {
      console.error('Error loading model1:', error);
    }
  );

  gltfLoader.load(
    window.MODEL_PATHS.model2,
    (gltf) => {
      model2 = gltf.scene;
      model2.position.set(-3, -1, 0);
      model2.scale.set(7, 7, 7);
      scene.add(model2);
      sectionMeshes.push(model2);
    },
    undefined,
    (error) => {
      console.error('Error loading model2:', error);
    }
  );
};

const directionalLight = new THREE.DirectionalLight("#ffffff", 1);
directionalLight.position.set(1, 1, 0);
scene.add(directionalLight);

const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
scene.add(ambientLight);

export const checkScreenSize = () => {
  const shouldRender = window.innerWidth > 768;

  if (shouldRender) {
    initRenderer();
    createMeshes();
  } else {
    if (model1) scene.remove(model1);
    if (model2) scene.remove(model2);
    model1 = null;
    model2 = null;
    sectionMeshes = [];
    removeRenderer();
  }
};

checkScreenSize();
