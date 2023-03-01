#version 330 core
out vec4 FragColor;
  
in vec2 v_texCoord;

uniform sampler2D screenTexture;

const float offset = 1.0 / 300.0;  

void main()
{ 
    //FragColor = 1.0 - texture(screenTexture, v_texCoord);
    /*vec4 color = texture(screenTexture, v_texCoord);
    float c = (color.r + color.g + color.b) / 3.0;
    FragColor = vec4(c, c, c, 1.0);*/

	    vec2 offsets[9] = vec2[](
        vec2(-offset,  offset), // top-left
        vec2( 0.0f,    offset), // top-center
        vec2( offset,  offset), // top-right
        vec2(-offset,  0.0f),   // center-left
        vec2( 0.0f,    0.0f),   // center-center
        vec2( offset,  0.0f),   // center-right
        vec2(-offset, -offset), // bottom-left
        vec2( 0.0f,   -offset), // bottom-center
        vec2( offset, -offset)  // bottom-right    
    );

    float kernel[9] = float[](
        1, 1, 1,
        1, -8, 1,
        1, 1, 1
    );
    
    vec3 sampleTex[9];
    for(int i = 0; i < 9; i++)
    {
        sampleTex[i] = vec3(texture(screenTexture, v_texCoord.st + offsets[i]));
    }
    vec3 col = vec3(0.0);
    for(int i = 0; i < 9; i++)
        col += sampleTex[i] * kernel[i] / 1;
    if (col.r > 0.1 || col.g > 0.1 || col.b > 0.1) {
        col = vec3(1, 1, 1);
    }
    FragColor = vec4(col, 1.0);
}