#version 330 core
out vec4 FragColor;
  
in vec2 v_texCoord;

uniform sampler2D screenTexture;

const float offset = 1.0 / 300.0;  

void main()
{ 
    FragColor = texture(screenTexture, v_texCoord);


}
