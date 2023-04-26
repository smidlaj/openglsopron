#version 330

in vec3 normal;
in vec4 world_position;
in vec2 texCoord;

uniform vec3 lightPos;
uniform vec3 viewPos;

uniform sampler2D s_texture;

void main()
{  
   // diffuse
   vec3 lightDir = normalize( vec4(lightPos, 1.0) - world_position  ).xyz;
   float diffColor = max(dot(normalize(normal), lightDir), 0.0) * 0.2;
   vec3 color = texture(s_texture, texCoord).rgb + diffColor;

   // specular
   vec3 viewDir = normalize(viewPos - world_position.xyz);
   vec3 reflectDir = reflect(-lightDir, normal); 
   float spec = pow(max(dot(viewDir, reflectDir), 0.0), 100.0) * 0.1;
   vec4 specColor = vec4(1, 1, 1, 1) * spec;

   gl_FragColor = vec4(color, 1) + specColor;
}