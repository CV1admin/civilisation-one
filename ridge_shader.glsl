uniform float entropy;
uniform float coherence;

void main() {
    vec2 pos = gl_FragCoord.xy / resolution.xy;
    float ridge = sin(pos.x * 10.0 + time) * coherence;
    vec3 color = mix(vec3(0.2,0.2,0.8), vec3(0.8,0.2,0.2), entropy);
    gl_FragColor = vec4(color * ridge, 1.0);
}
