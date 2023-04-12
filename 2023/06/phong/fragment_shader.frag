#version 330

in vec3 normal;
in vec4 world_position;

uniform vec3 lightPos;

void main()
{  
   vec3 lightDir = normalize( vec4(lightPos, 1.0) - world_position  ).xyz;
   float diffColor = max(dot(normalize(normal), lightDir), 0.0) * 0.9;
   vec3 color = vec3(0.4, 0, 0) + diffColor;

   gl_FragColor = vec4(color, 1);
}