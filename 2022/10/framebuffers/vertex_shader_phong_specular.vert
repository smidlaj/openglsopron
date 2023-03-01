#version 330
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;

uniform mat4 projection;
uniform mat4 modelView;

out vec3 v_position;
out vec3 v_normal;


void main() { 
   gl_Position = projection * modelView * vec4((in_position), 1.0);
   
   v_position = (modelView * vec4(in_position, 1.0)).xyz;
   v_normal = mat3(transpose(inverse(modelView))) * in_normal;  
}
