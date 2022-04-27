#version 330
out vec4 out_color;

in vec3 v_position;
in vec3 v_normal;
in vec2 v_texture;

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

uniform sampler2D textureSampler;

void main()
{    
vec3 ambient = materialAmbientColor * lightAmbientColor; 

    vec3 normal = normalize(v_normal);
    vec3 lightDir = normalize( vec4((lightPos - v_position), 0.0) ).xyz;
    vec3 diffuse = materialDiffuseColor * max(dot(normal, lightDir), 0.0) * lightDiffuseColor;
    
    vec3 viewDir = normalize(viewPos - v_position);
    vec3 reflectDir = reflect(-lightDir, normal); 
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), materialShine);
    vec3 specular = materialSpecularColor * spec * lightSpecularColor;
    
    out_color = texture(textureSampler, v_texture) * 0.5 + vec4(materialEmissionColor + ambient + diffuse + specular, 1.0);
}