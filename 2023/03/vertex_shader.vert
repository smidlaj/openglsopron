#version 330
layout(location = 0) in vec2 kiskutya;

uniform mat4 matrix;

void main() { 
   gl_Position = matrix * vec4(kiskutya, 0, 1.0);
}
