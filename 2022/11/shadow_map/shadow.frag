#version 330

in vec3 v_position;
in vec3 v_normal;
in vec4 v_fragPosLightSpace;

out vec4 out_color;

uniform vec3 lightPos;
uniform vec3 viewPos;

uniform vec3 ambientColor;
uniform vec3 colorLight;

uniform sampler2D shadowMap;

bool shadowCalculation(vec4 fragPosLightSpace)
{
	vec3 projCoords = fragPosLightSpace.xyz;
	projCoords = projCoords * 0.5 + 0.5; 
	float closestDepth = texture(shadowMap, projCoords.xy).r;   
	float currentDepth = projCoords.z;
    return currentDepth > closestDepth;    
}

float shadowCalculation2(vec4 fragPosLightSpace)
{
	vec3 projCoords = fragPosLightSpace.xyz;
	projCoords = projCoords * 0.5 + 0.5; 
    float shadow = 0.0;
    int width = 7;
    int fromTo = width / 2;
    vec2 texelSize = 1.0 / textureSize(shadowMap, 0);
    for(int x = -fromTo; x <= fromTo; ++x)
    {
        for(int y = -fromTo; y <= fromTo; ++y)
        {
	        float closestDepth = texture(shadowMap, projCoords.xy + vec2(x, y) * texelSize).r;   
	        float currentDepth = projCoords.z;
            shadow += currentDepth > closestDepth ? 1.0 : 0.0;
        }
    }
    return shadow / (width * width);
}

void main()
{
    vec3 normal = normalize(v_normal);
    vec3 lightDir = normalize( vec4((lightPos - v_position), 0.0) ).xyz;
    
    float diffColor = max(dot(normal, lightDir), 0.0);
    
    vec3 viewDir = normalize(viewPos - v_position);
    vec3 reflectDir = reflect(-lightDir, normal); 
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 250.0);
    vec4 specColor = vec4(colorLight, 1);
    
    /*bool shadow = shadowCalculation(v_fragPosLightSpace);

    if (shadow) {
    	out_color = vec4(ambientColor, 1);
    } else {
    	out_color = vec4(ambientColor, 1) + diffColor * vec4(1, 1, 1, 1) + spec * vec4(1, 1, 1, 1);
    }*/

    float shadow = shadowCalculation2(v_fragPosLightSpace);

//    if (shadow > 0.0) {
//    	out_color = vec4(ambientColor, 1) * (1.0 - shadow);
//    } else {
    	out_color = (vec4(ambientColor, 1) + diffColor * vec4(1, 1, 1, 1) + spec * vec4(1, 1, 1, 1)) * (1.0 - shadow);
  //  }
}
