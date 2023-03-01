#version 330
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec2 in_texture;

uniform mat4 projection;
uniform mat4 model;
uniform mat4 view;

out vec3 v_position;
out vec3 v_normal;
out vec2 v_texture;

void main() { 
   gl_Position = projection * view * model * vec4((in_position), 1.0);
   
   v_position = (view * model * vec4(in_position, 1.0)).xyz;
   v_normal = mat3(transpose(inverse( view * model ))) * in_normal; 
   v_texture = in_texture; 
}
