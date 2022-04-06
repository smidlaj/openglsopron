#version 330

in vec3 v_position;
in vec3 v_normal;
in vec2 v_texture;

out vec4 out_color;

uniform vec3 materialAmbientColor;
uniform vec3 materialDiffuseColor;
uniform vec3 materialSpecularColor;
uniform vec3 materialEmissionColor;
uniform float materialShine;

uniform vec3 lightAmbientColor;
uniform vec3 lightDiffuseColor;
uniform vec3 lightSpecularColor;

uniform vec3 lightPos;
uniform vec3 viewPos;

uniform sampler2D texture1;
uniform sampler2D texture2;

void main()
{
	vec3 ambient = materialAmbientColor * lightAmbientColor; 

    vec3 normal = normalize(v_normal);
    vec3 lightDir = normalize( vec4((lightPos - v_position), 0.0) ).xyz;
    float diffuseStr = max(dot(normal, lightDir), 0.0);
    if (dot(normal, lightDir) >= 0.0) {
    	//diffuseStr = 1.0;
    } else {
    	diffuseStr = 0.0;
    }
    vec3 diffuse = materialDiffuseColor * diffuseStr * lightDiffuseColor;
    
    vec3 viewDir = normalize(viewPos - v_position);
    vec3 reflectDir = reflect(-lightDir, normal); 
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), materialShine);
    vec3 specular = materialSpecularColor * spec * lightSpecularColor;
    
    //out_color = vec4(materialEmissionColor + ambient + diffuse + specular, 1.0);
    out_color = texture(texture1, v_texture) * diffuseStr + texture(texture2, v_texture) * (1.0 - diffuseStr) + vec4(materialEmissionColor + ambient  + specular, 1.0);
}
