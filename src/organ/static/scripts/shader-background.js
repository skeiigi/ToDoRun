let camera, scene, renderer, clock;
let uniforms;

async function loadShader(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Failed to load shader: ${url}`);
    }
    return await response.text();
}

async function init() {
    const container = document.getElementById("shader");

    clock = new THREE.Clock();
    camera = new THREE.Camera();
    camera.position.z = 1;

    scene = new THREE.Scene();

    const geometry = new THREE.PlaneBufferGeometry(2, 2);

    uniforms = {
        u_time: { type: "f", value: 1.0 },
        u_resolution: { type: "v2", value: new THREE.Vector2() },
    };

    try {
        const vertexShader = await loadShader(shaderPaths.vertex);
        const fragmentShader = await loadShader(shaderPaths.fragment);

        const material = new THREE.ShaderMaterial({
            uniforms,
            vertexShader,
            fragmentShader
        });

        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        renderer = new THREE.WebGLRenderer();
        renderer.setPixelRatio(window.devicePixelRatio);

        container.appendChild(renderer.domElement);

        onWindowResize();
        window.addEventListener("resize", onWindowResize);

        animate();
    } catch (error) {
        console.error("Error loading shaders:", error);
    }
}

function onWindowResize() {
    if (renderer) {
        renderer.setSize(window.innerWidth, window.innerHeight);
        uniforms.u_resolution.value.x = renderer.domElement.width;
        uniforms.u_resolution.value.y = renderer.domElement.height;
    }
}

function render() {
    if (renderer) {
        uniforms.u_time.value = clock.getElapsedTime();
        renderer.render(scene, camera);
    }
}

function animate() {
    render();
    requestAnimationFrame(animate);
}

init();
