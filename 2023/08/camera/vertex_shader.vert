#version 330
layout(location = 0) in vec3 v_coord;
layout(location = 1) in vec3 v_normal;
layout(location = 2) in vec2 v_texCoord;

uniform mat4 modelView;
uniform mat4 camera;
uniform mat4 perspectiveMatrix;

out vec3 normal;
out vec4 world_position;
out vec2 texCoord;

void main() {
   world_position = modelView * vec4(v_coord, 1.0);
   gl_Position = perspectiveMatrix * camera * world_position;

   normal = normalize( mat3(transpose(inverse(modelView))) * v_normal);
   texCoord = v_texCoord;
}
