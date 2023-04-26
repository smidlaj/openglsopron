#version 330
layout(location = 0) in vec3 v_coord;
layout(location = 1) in vec3 v_normal;

uniform mat4 modelView;
uniform mat4 perspectiveMatrix;

out vec3 normal;
out vec4 world_position;

void main() {
   world_position = modelView * vec4(v_coord, 1.0);
   gl_Position = perspectiveMatrix * world_position;

   normal = normalize( mat3(transpose(inverse(modelView))) * v_normal);
}