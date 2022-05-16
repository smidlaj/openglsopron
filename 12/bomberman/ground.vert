#version 330
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec2 kiskutya;

uniform mat4 projection;
uniform mat4 view;

out vec2 kiscica;

void main() { 
   gl_Position = projection * view * vec4((in_position), 1.0);

   kiscica = kiskutya;
}
