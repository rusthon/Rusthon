/**
 * @fileOverview JavaScript/GLSL parallel reduction for Three.js
 * @author Skeel Lee <skeel@skeelogy.com>
 * @version 1.0.3
 *
 * @example
 * //create a parallel reducer
 * var textureRes = 1024;
 * var reductionStopRes = 1;
 * var pr = new SKPR.ParallelReducer(threejsWebGLRenderer, textureRes, reductionStopRes);
 *
 * //reduce a given texture / render target
 * var reductionOp = 'sum';
 * var textureChannel = 'r';
 * pr.reduce(threejsRenderTargetToReduce, reductionOp, textureChannel);
 *
 * //if you want to read the resulting float data from the GPU to the CPU (expensive operation):
 * var resultFloat32Array = pr.getPixelFloatData(textureChannel);
 * var sum = 0;
 * var i, len;
 * for (i = 0, len = resultFloat32Array.length; i < len; i++) {
 *     sum += resultFloat32Array[i];
 * }
 */

//FIXME: pixel access still has some problems, causing interpolated values to appear. Does not matter to 'sum' mode for some reason, but other modes like 'max' will not work.
//TODO: do a vertical flip of UVs before going into shaders, so that there's no need to constantly flip the v coordinates

/**
 * @namespace
 */
var SKPR = SKPR || { version: '1.0.3' };
console.log('Using SKPR ' + SKPR.version);

/**
 * Parallel reduction class
 * @constructor
 * @param  {THREE.WebGLRenderer} renderer Renderer
 * @param  {number} res Power-of-2 resolution of textures to reduce
 * @param  {number} stopRes Power-of-2 resolution to stop the reduction process (min of 1)
 */
SKPR.ParallelReducer = function (renderer, res, stopRes) {

    //store renderer
    if (typeof renderer === 'undefined') {
        throw new Error('renderer not specified');
    }
    this.__renderer = renderer;
    this.__checkExtensions();

    //store res
    if (typeof res === 'undefined') {
        throw new Error('res not specified');
    }
    if (res & (res - 1)) {
        throw new Error('res is not a power of 2');
    }
    this.__res = res;

    //store stop res
    stopRes = stopRes || 1;
    if (res & (res - 1)) {
        throw new Error('res is not a power of 2');
    }
    this.__stopRes = stopRes;

    //check that stop res is smaller than res
    if (this.__res <= this.__stopRes) {
        throw new Error('stopRes must be smaller than res');
    }

    //init
    this.__init();
};
SKPR.ParallelReducer.prototype.__checkExtensions = function () {
    var context = this.__renderer.context;

    //determine floating point texture support
    //https://www.khronos.org/webgl/public-mailing-list/archives/1306/msg00002.html

    //get floating point texture support
    if (!context.getExtension('OES_texture_float')) {
        var msg = 'No support for floating point textures. Extension not available: OES_texture_float';
        alert(msg);
        throw new Error(msg);
    }

    //NOTE: we do not need linear filtering in this file
    // //get floating point linear filtering support
    // this.supportsTextureFloatLinear = context.getExtension('OES_texture_float_linear') !== null;
    // console.log('Texture float linear filtering support: ' + this.supportsTextureFloatLinear);
};
SKPR.ParallelReducer.prototype.__init = function () {
    this.__setupRttScene();
    this.__setupRttRenderTargets();
    this.__setupRttShaders();
    this.__pixelByteData = new Uint8Array(this.__stopRes * this.__stopRes * 4);
};
SKPR.ParallelReducer.prototype.__setupRttScene = function () {

    var size = 1.0;  //arbitrary
    var halfSize = size / 2.0;

    this.__rttScene = new THREE.Scene();

    var far = 10000;
    var near = -far;
    this.__rttCamera = new THREE.OrthographicCamera(-halfSize, halfSize, halfSize, -halfSize, near, far);

    //create quads of different sizes to invoke the shaders
    var w;
    var newMaxUv = 1.0;
    var scale = 1.0;
    var dummyTexture = new THREE.Texture();
    this.__rttQuadMeshes = [];
    for (w = this.__res; w >= 1; w /= 2) {

        //generate the plane geom
        var rttQuadGeom = new THREE.PlaneGeometry(size, size);
        rttQuadGeom.faceVertexUvs[0][0][0].set(0.0, 1.0);
        rttQuadGeom.faceVertexUvs[0][0][1].set(0.0, 1.0 - newMaxUv);
        rttQuadGeom.faceVertexUvs[0][0][2].set(newMaxUv, 1.0 - newMaxUv);
        rttQuadGeom.faceVertexUvs[0][0][3].set(newMaxUv, 1.0);
        rttQuadGeom.applyMatrix(new THREE.Matrix4().makeTranslation(0.5 * size, -0.5 * size, 0.0));
        rttQuadGeom.applyMatrix(new THREE.Matrix4().makeScale(scale, scale, scale));
        rttQuadGeom.applyMatrix(new THREE.Matrix4().makeTranslation(-0.5 * size, 0.5 * size, 0.0));

        //add mesh
        //have to load with a dummy map, or else we will get this WebGL error when we swap to another material with a texture:
        //"glDrawElements: attempt to access out of range vertices in attribute"
        //http://stackoverflow.com/questions/16531759/three-js-map-material-causes-webgl-warning
        var rttQuadMesh = new THREE.Mesh(rttQuadGeom, new THREE.MeshBasicMaterial({map: dummyTexture}));
        rttQuadMesh.visible = false;
        this.__rttScene.add(rttQuadMesh);
        this.__rttQuadMeshes.push(rttQuadMesh);

        newMaxUv /= 2.0;
        scale /= 2.0;
    }
};
SKPR.ParallelReducer.prototype.__setupRttRenderTargets = function () {
    this.__nearestFloatRgbaParams = {
        minFilter: THREE.NearestFilter,
        magFilter: THREE.NearestFilter,
        wrapS: THREE.ClampToEdgeWrapping,
        wrapT: THREE.ClampToEdgeWrapping,
        format: THREE.RGBAFormat,
        stencilBuffer: false,
        depthBuffer: false,
        type: THREE.FloatType
    };
    this.__rttRenderTarget1 = new THREE.WebGLRenderTarget(this.__res, this.__res, this.__nearestFloatRgbaParams);
    this.__rttRenderTarget1.generateMipmaps = false;
    this.__rttRenderTarget2 = this.__rttRenderTarget1.clone();
};
SKPR.ParallelReducer.prototype.__setupRttShaders = function () {

    this.__rttMaterials = {};

    this.__rttMaterials['sum'] = new THREE.ShaderMaterial({
        uniforms: {
            uTexture: { type: 't', value: null },
            uTexelSize: { type: 'f', value: 0 },
            uHalfTexelSize: { type: 'f', value: 0 },
            uChannelMask: { type: 'v4', value: new THREE.Vector4() }
        },
        vertexShader: this.__shaders.vert['passUv'],
        fragmentShader: this.__shaders.frag['parallelSum']
    });

    this.__rttEncodeFloatMaterial = new THREE.ShaderMaterial({
        uniforms: {
            uTexture: { type: 't', value: null },
            uChannelMask: { type: 'v4', value: new THREE.Vector4() }
        },
        vertexShader: this.__shaders.vert['passUv'],
        fragmentShader: this.__shaders.frag['encodeFloat']
    });

    this.__channelVectors = {
        'r': new THREE.Vector4(1, 0, 0, 0),
        'g': new THREE.Vector4(0, 1, 0, 0),
        'b': new THREE.Vector4(0, 0, 1, 0),
        'a': new THREE.Vector4(0, 0, 0, 1)
    };
};
SKPR.ParallelReducer.prototype.__shaders = {

    vert: {

        passUv: [

            //Pass-through vertex shader for passing interpolated UVs to fragment shader

            "varying vec2 vUv;",

            "void main() {",
                "vUv = vec2(uv.x, uv.y);",
                "gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);",
            "}"

        ].join('\n')

    },

    frag: {

        encodeFloat: [

            //Fragment shader that encodes float value in input R channel to 4 unsigned bytes in output RGBA channels
            //Most of this code is from original GLSL codes from Piotr Janik, only slight modifications are done to fit the needs of this script
            //http://concord-consortium.github.io/lab/experiments/webgl-gpgpu/script.js
            //Using method 1 of the code.

            "uniform sampler2D uTexture;",
            "uniform vec4 uChannelMask;",

            "varying vec2 vUv;",

            "float shift_right(float v, float amt) {",
                "v = floor(v) + 0.5;",
                "return floor(v / exp2(amt));",
            "}",

            "float shift_left(float v, float amt) {",
                "return floor(v * exp2(amt) + 0.5);",
            "}",

            "float mask_last(float v, float bits) {",
                "return mod(v, shift_left(1.0, bits));",
            "}",

            "float extract_bits(float num, float from, float to) {",
                "from = floor(from + 0.5);",
                "to = floor(to + 0.5);",
                "return mask_last(shift_right(num, from), to - from);",
            "}",

            "vec4 encode_float(float val) {",

                "if (val == 0.0) {",
                    "return vec4(0, 0, 0, 0);",
                "}",

                "float sign = val > 0.0 ? 0.0 : 1.0;",
                "val = abs(val);",
                "float exponent = floor(log2(val));",
                "float biased_exponent = exponent + 127.0;",
                "float fraction = ((val / exp2(exponent)) - 1.0) * 8388608.0;",

                "float t = biased_exponent / 2.0;",
                "float last_bit_of_biased_exponent = fract(t) * 2.0;",
                "float remaining_bits_of_biased_exponent = floor(t);",

                "float byte4 = extract_bits(fraction, 0.0, 8.0) / 255.0;",
                "float byte3 = extract_bits(fraction, 8.0, 16.0) / 255.0;",
                "float byte2 = (last_bit_of_biased_exponent * 128.0 + extract_bits(fraction, 16.0, 23.0)) / 255.0;",
                "float byte1 = (sign * 128.0 + remaining_bits_of_biased_exponent) / 255.0;",

                "return vec4(byte4, byte3, byte2, byte1);",
            "}",

            "void main() {",
                "vec4 t = texture2D(uTexture, vUv);",
                "gl_FragColor = encode_float(dot(t, uChannelMask));",
            "}"

        ].join('\n'),

        parallelSum: [

            //Fragment shader for performing parallel sum reduction

            "uniform sampler2D uTexture;",
            "uniform float uTexelSize;",
            "uniform float uHalfTexelSize;",
            "uniform vec4 uChannelMask;",

            "varying vec2 vUv;",

            "void main() {",

                "//read original texture",
                "vec4 t = texture2D(uTexture, vUv);",

                "//expand the UVs and then read data from neighbours",
                "//do dot product with uChannelMask vector to mask out only the channel value needed",
                "float oneMinusHalfTexelSize = 1.0 - uHalfTexelSize;",
                "vec2 expandedUv = vec2(",
                    "(vUv.x - uHalfTexelSize) * 2.0 + uHalfTexelSize,",
                    "(vUv.y - oneMinusHalfTexelSize) * 2.0 + oneMinusHalfTexelSize",
                ");",
                "float v1 = dot(texture2D(uTexture, expandedUv), uChannelMask);",
                "float v2 = dot(texture2D(uTexture, expandedUv + vec2(uTexelSize, 0.0)), uChannelMask);",
                "float v3 = dot(texture2D(uTexture, expandedUv + vec2(uTexelSize, -uTexelSize)), uChannelMask);",
                "float v4 = dot(texture2D(uTexture, expandedUv + vec2(0.0, -uTexelSize)), uChannelMask);",

                "//sum of values",
                "float final = v1 + v2 + v3 + v4;",

                "gl_FragColor = (vec4(1.0) - uChannelMask) * t + uChannelMask * final;",
            "}"

        ].join('\n')

    }
};
SKPR.ParallelReducer.prototype.__swapRenderTargets = function () {
    var temp = this.__rttRenderTarget1;
    this.__rttRenderTarget1 = this.__rttRenderTarget2;
    this.__rttRenderTarget2 = temp;
};
/**
 * Initiate the reduction process
 * @param  {THREE.Texture | THREE.WebGLRenderTarget} texture Texture which contains data for reduction
 * @param  {string} type Reduction type: 'sum' (only choice available now)
 * @param  {string} channelId Channel to reduce: 'r', 'g', 'b' or 'a'
 */
SKPR.ParallelReducer.prototype.reduce = function (texture, type, channelId) {
    var currMaterial = this.__rttMaterials[type];
    var firstIteration = true;
    var texelSize = 1.0 / this.__res;
    var level = 1;
    this.__currRes = this.__res;
    while (this.__currRes > this.__stopRes) {

        //reduce width by half
        this.__currRes /= 2;
        // console.log('currRes: ' + this.__currRes);

        //render to do parallel reduction
        this.__swapRenderTargets();
        this.__rttQuadMeshes[level].visible = true;
        this.__rttQuadMeshes[level].material = currMaterial;
        currMaterial.uniforms['uTexture'].value = firstIteration ? texture : this.__rttRenderTarget2;
        currMaterial.uniforms['uTexelSize'].value = texelSize;
        currMaterial.uniforms['uHalfTexelSize'].value = texelSize / 2.0;
        currMaterial.uniforms['uChannelMask'].value.copy(this.__channelVectors[channelId]);
        this.__renderer.render(this.__rttScene, this.__rttCamera, this.__rttRenderTarget1, false);
        this.__rttQuadMeshes[level].visible = false;

        level += 1;

        firstIteration = false;
    }
};
/**
 * Gets the reduced float data from the previous reduction.<br/><strong>NOTE: This is an expensive operation.</strong>
 * @param  {string} channelId Channel to get float data from
 * @return {number} Floating point result of the reduction
 */
SKPR.ParallelReducer.prototype.getPixelFloatData = function (channelId) {

    //I need to read in pixel data from WebGLRenderTarget but there seems to be no direct way.
    //Seems like I have to do some native WebGL stuff with readPixels().

    //need to first render the float data into an unsigned byte RGBA texture
    this.__swapRenderTargets();
    this.__rttQuadMeshes[0].visible = true;
    this.__rttQuadMeshes[0].material = this.__rttEncodeFloatMaterial;
    this.__rttEncodeFloatMaterial.uniforms['uTexture'].value = this.__rttRenderTarget2;
    this.__rttEncodeFloatMaterial.uniforms['uChannelMask'].value.copy(this.__channelVectors[channelId]);
    this.__renderer.render(this.__rttScene, this.__rttCamera, this.__rttRenderTarget1, false);
    this.__rttQuadMeshes[0].visible = false;

    var gl = this.__renderer.getContext();

    //bind texture to gl context
    gl.bindFramebuffer(gl.FRAMEBUFFER, this.__rttRenderTarget1.__webglFramebuffer);

    //read pixels
    gl.readPixels(0, this.__res - this.__stopRes, this.__stopRes, this.__stopRes, gl.RGBA, gl.UNSIGNED_BYTE, this.__pixelByteData);

    //unbind
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);

    //cast to float
    var floatData = new Float32Array(this.__pixelByteData.buffer);

    return floatData;
};