#version 330 core
layout (location = 0) in vec3 in_position;

uniform mat4 lightSpaceMatrix;
uniform mat4 modelView;

void main()
{
    gl_Position = lightSpaceMatrix * modelView * vec4(in_position, 1.0);
}  
