import { scene, removeRenderer, initRenderer } from './shader-config.js';

let model1 = null;
let model2 = null;
export let sectionMeshes = [];
let modelsLoaded = false; // Флаг для отслеживания загрузки моделей

const loadingManager = new THREE.LoadingManager();
const gltfLoader = new THREE.GLTFLoader(loadingManager);

const createMeshes = () => {
  if (modelsLoaded) return;
  
  gltfLoader.load(
    window.MODEL_PATHS.model1,
    (gltf) => {
      if (!model1) {
        model1 = gltf.scene;
        model1.position.set(3, 0, 0);
        model1.scale.set(0.5, 0.5, 0.5);
        scene.add(model1);
        sectionMeshes.push(model1);
      }
    },
    undefined,
    (error) => {
      console.error('Error loading model1:', error);
    }
  );

  gltfLoader.load(
    window.MODEL_PATHS.model2,
    (gltf) => {
      if (!model2) { // Проверяем, не существует ли уже модель
        model2 = gltf.scene;
        model2.position.set(-3, -1, 0);
        model2.scale.set(7, 7, 7);
        scene.add(model2);
        sectionMeshes.push(model2);
      }
    },
    undefined,
    (error) => {
      console.error('Error loading model2:', error);
    }
  );
  
  modelsLoaded = true; // Устанавливаем флаг после загрузки
};

// Освещение (оставляем без изменений)
const envLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(envLight);

const dirLight = new THREE.DirectionalLight(0xfff4e6, 2.5);
dirLight.position.set(5, 10, 7);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 4096;
dirLight.shadow.mapSize.height = 4096;
dirLight.shadow.camera.near = 0.1;
dirLight.shadow.camera.far = 100;
dirLight.shadow.normalBias = 0.05;
scene.add(dirLight);

const fillLight = new THREE.HemisphereLight(0xffffbb, 0x080820, 0.7);
fillLight.position.set(-5, 3, -5);
scene.add(fillLight);

const rimLight = new THREE.DirectionalLight(0xffffff, 1.2);
rimLight.position.set(0, 5, -10);
rimLight.shadow.camera.far = 50;
scene.add(rimLight);

// Упрощенная функция checkScreenSize без проверки разрешения
export const checkScreenSize = () => {
  initRenderer();
  createMeshes();
};

// Инициализация при загрузке
checkScreenSize();
