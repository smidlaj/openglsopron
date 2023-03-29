#version 330
layout(location = 0) in vec3 coord;

uniform mat4 matrix;
uniform mat4 perspectiveMatrix;

void main() { 
   gl_Position = perspectiveMatrix * matrix * vec4(coord, 1.0);
}
