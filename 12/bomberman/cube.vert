#version 330
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec2 in_texture;

uniform mat4 projection;
uniform mat4 world;
uniform mat4 view;

// szamitasokat sporolunk:
uniform mat4 projViewWorld;
uniform mat4 viewWorld;
uniform mat4 normalMat;

out vec3 v_position;
out vec3 v_normal;
out vec2 v_texture;

void main() { 
   // kepernyo koordinatarendszer:
   gl_Position = projection * view * world * vec4((in_position), 1.0);
   // vilag koordinatarendszer:
   v_position = (world * vec4(in_position, 1.0)).xyz;


   v_normal = mat3(transpose(inverse( world ))) * in_normal; 
   v_texture = in_texture; 
}
