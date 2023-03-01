#version 330
layout(location = 0) in vec2 kiskutya;

void main() { 
   gl_Position = vec4(kiskutya, 0, 1.0);
}