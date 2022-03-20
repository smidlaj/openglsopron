#version 330

in vec3 v_position;
in vec3 v_normal;

out vec4 out_color;

uniform vec3 lightPos;

void main()
{
    vec3 normal = normalize(v_normal);
    vec3 lightDir = normalize( vec4((lightPos - v_position), 0.0) ).xyz;
    
    float diffColor = max(dot(normal, lightDir), 0.0) * 0.5;
    
    out_color = vec4(0.3, 0, 0, 1) + diffColor;
}
