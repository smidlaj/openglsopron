#version 330 core
layout (location = 0) in vec3 in_position;

out vec3 v_texture;

uniform mat4 projection;
uniform mat4 view;

void main()
{
    v_texture = in_position;
    gl_Position = projection * view * vec4(in_position, 1.0);
}  
