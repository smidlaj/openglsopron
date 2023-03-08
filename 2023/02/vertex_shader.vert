#version 330
layout(location = 0) in vec2 kiskutya;

uniform float x;
uniform float y;

void main() { 
   gl_Position = vec4(kiskutya.x + x, kiskutya.y + y, 0, 1.0);
}
