#version 330

in vec3 normal;
in vec4 world_position;

uniform vec3 lightPos;
uniform vec3 viewPos;

void main()
{  
   // diffuse
   vec3 lightDir = normalize( vec4(lightPos, 1.0) - world_position  ).xyz;
   float diffColor = max(dot(normalize(normal), lightDir), 0.0) * 0.9;
   vec3 color = vec3(0.4, 0, 0) + diffColor;

   // specular
   vec3 viewDir = normalize(viewPos - world_position.xyz);
   vec3 reflectDir = reflect(-lightDir, normal); 
   float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0) * 0.5;
   vec4 specColor = vec4(1, 1, 1, 1) * spec;

   gl_FragColor = vec4(color, 1) + specColor;
}