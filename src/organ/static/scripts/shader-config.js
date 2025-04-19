export const scene = new THREE.Scene();
export const objectsDistance = 4;

const sizes = { width: window.innerWidth, height: window.innerHeight };
export const cameraGroup = new THREE.Group();
scene.add(cameraGroup);

export let camera = new THREE.PerspectiveCamera(35, sizes.width / sizes.height, 0.1, 100);
camera.position.z = 6;
cameraGroup.add(camera);

export let renderer = null;
export let composer = null;
const canvasElement = document.querySelector("canvas.webgl");

export const initRenderer = () => {
  if (canvasElement && !canvasElement.parentNode) {
    document.body.appendChild(canvasElement);
  }

  renderer = new THREE.WebGLRenderer({
    canvas: canvasElement,
    alpha: true,
    antialias: true
  });
  
  renderer.setSize(sizes.width, sizes.height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  renderer.physicallyCorrectLights = true;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.shadowMap.autoUpdate = true;

  composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  
  const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    1.5,
    0.4,
    0.6 
  );
  
  const filmPass = new FilmPass(
    0.35,
    0.025,
    648,
    false
  );
  
  const colorCorrection = new ShaderPass(ColorCorrectionShader);
  colorCorrection.uniforms.contrast.value = 1.1;
  colorCorrection.uniforms.saturation.value = 1.15;
  
  composer.addPass(bloomPass);
  composer.addPass(filmPass);
  composer.addPass(colorCorrection);
};

export const removeRenderer = () => {
  if (canvasElement && canvasElement.parentNode) {
    canvasElement.remove();
  }
  if (renderer) {
    renderer.dispose();
    renderer = null;
  }
  if (composer) {
    composer.dispose();
    composer = null;
  }
  camera = null;
};

initRenderer();
