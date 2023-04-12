#version 330
layout(location = 0) in vec3 v_coord;
layout(location = 1) in vec3 v_normal;

uniform mat4 modelView;
uniform mat4 perspectiveMatrix;

uniform vec3 lightPos;

out vec3 color;

void main() {
   vec4 world_position = modelView * vec4(v_coord, 1.0);
   gl_Position = perspectiveMatrix * world_position;

   vec3 normal = normalize( mat3(transpose(inverse(modelView))) * v_normal);
   vec3 lightDir = normalize( vec4(lightPos, 1.0) - world_position  ).xyz;

   float diffColor = max(dot(normal, lightDir), 0.0) * 0.9;
   color = vec3(0.4, 0, 0) + diffColor;
}
