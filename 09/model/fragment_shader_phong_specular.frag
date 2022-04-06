#version 330

in vec3 v_position;
in vec3 v_normal;

out vec4 out_color;

uniform vec3 lightPos;
uniform vec3 viewPos;

void main()
{
    vec3 normal = normalize(v_normal);
    vec3 lightDir = normalize( vec4((lightPos - v_position), 0.0) ).xyz;
    
    float diffColor = max(dot(normal, lightDir), 0.0);
    
    vec3 viewDir = normalize(viewPos - v_position);
    vec3 reflectDir = reflect(-lightDir, normal); 
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 250.0);
    vec4 specColor = vec4(1, 1, 1, 1);
    
    out_color = vec4(0.3, 0, 0, 1) + diffColor + spec * vec4(1, 1, 1, 1);
}
