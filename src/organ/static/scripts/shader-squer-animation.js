import {
  scene,
  camera,
  renderer,
  cameraGroup,
  objectsDistance,
} from './shader-config.js';
import { sectionMeshes, checkScreenSize } from './shader-squer.js';

let scrollY = window.scrollY;
let currentSection = 0;
let animationId = null;

const handleScroll = () => {
  if (!renderer) return;

  scrollY = window.scrollY;
  const newSection = Math.round(scrollY / window.innerHeight);

  if (newSection != currentSection && sectionMeshes[newSection]) {
    currentSection = newSection;
    gsap.to(sectionMeshes[currentSection].rotation, {
      duration: 1.5,
      ease: "power2.inOut",
      x: "+=6",
      y: "+=3",
      z: "+=1.5",
    });
  }
};

const handleMouseMove = (e) => {
  if (!renderer) return;

  cursor.x = e.clientX / window.innerWidth - 0.5;
  cursor.y = e.clientY / window.innerHeight - 0.5;
};

const cursor = { x: 0, y: 0 };
window.addEventListener("scroll", handleScroll);
window.addEventListener("mousemove", handleMouseMove);

const clock = new THREE.Clock();
let previousTime = 0;

const tick = () => {
  if (!renderer) {
    animationId = null;
    return;
  }

  const elapsedTime = clock.getElapsedTime();
  const deltaTime = elapsedTime - previousTime;
  previousTime = elapsedTime;

  camera.position.y = (-scrollY / window.innerHeight) * objectsDistance;
  const parallaxX = cursor.x * 0.5;
  const parallaxY = -cursor.y * 0.5;
  cameraGroup.position.x += (parallaxX - cameraGroup.position.x) * 5 * deltaTime;
  cameraGroup.position.y += (parallaxY - cameraGroup.position.y) * 5 * deltaTime;

  for (const mesh of sectionMeshes) {
    mesh.rotation.x += deltaTime * 0.1;
    mesh.rotation.y += deltaTime * 0.12;
  }

  renderer.render(scene, camera);
  animationId = window.requestAnimationFrame(tick);
};

if (renderer) {
  tick();
}

window.addEventListener("resize", () => {
  const sizes = { width: window.innerWidth, height: window.innerHeight };

  if (renderer) {
    camera.aspect = sizes.width / sizes.height;
    camera.updateProjectionMatrix();
    renderer.setSize(sizes.width, sizes.height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  }

  checkScreenSize();

  if (renderer && !animationId) {
    tick();
  }
});
