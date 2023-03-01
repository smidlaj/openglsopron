#version 330
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;

uniform mat4 projection;
uniform mat4 modelView;

uniform vec3 lightPos;

out vec4 v_color;

void main() { 
   vec4 w_position = modelView * vec4((in_position), 1.0);
   gl_Position = projection * w_position;

   vec3 normal = normalize( mat3(transpose(inverse(modelView))) * in_normal);
   vec3 lightDir = normalize( vec4(lightPos, 1.0) - w_position  ).xyz;
    
   float diffColor = max(dot(normal, lightDir), 0.0) * 0.5;
      
   v_color = vec4(0.3, 0, 0, 1) + diffColor;  
}
