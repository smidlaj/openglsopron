#version 330
layout(location = 0) in vec3 v_coord;
layout(location = 1) in vec3 v_color;

uniform mat4 matrix;
uniform mat4 perspectiveMatrix;

out vec3 color;

void main() { 
   color = v_color;
   gl_Position = perspectiveMatrix * matrix * vec4(v_coord, 1.0);
}
