/*
 * Original shader by arlez80
 * https://godotshaders.com/shader/glitch-effect-shader/
 * Edited to use MC uniforms/inputs and texture-wrap.
*/
#version 150

#moj_import <fog.glsl>

uniform sampler2D Sampler0;

uniform float Hexbound_WorldTime;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in float vertexDistance;
in vec4 vertexColor;
in vec4 lightMapColor;
in vec4 overlayColor;
in vec2 texCoord0;
in vec4 normal;

out vec4 fragColor;

uniform float shake_power_U = 0.12;
uniform float shake_block_size = 21f;
uniform float shake_color_rate = 0.02;

uniform float max_U = 0.75f;

float random(float seed) {
    return fract(543.2543 * sin(dot(vec2(seed, seed), vec2(3525.46, -54.3415))));
}

void main() {
    vec2 direction = vec2(1f, 0f);

    vec2 fixed_uv = texCoord0;
    vec4 color = texture(Sampler0, fixed_uv);

    if (mod(Hexbound_WorldTime, 100f) < 5f) {
        fixed_uv.x += (random((trunc(texCoord0.y * shake_block_size) / shake_block_size) + mod(Hexbound_WorldTime, 200f)) - 0.5) * shake_power_U;
        fixed_uv.x = mod(fixed_uv.x + max_U, max_U);
        color = texture(Sampler0, fixed_uv);

        color.r = texture(Sampler0, fixed_uv + vec2(shake_color_rate, 0.0)).r;
        color.b = texture(Sampler0, fixed_uv + vec2(-shake_color_rate, 0.0)).b;
    }

    if (color.a < 0.1) {
        discard;
    }

    color *= vertexColor * ColorModulator;
    color.rgb = mix(overlayColor.rgb, color.rgb, overlayColor.a);

    fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
}