#version 330

in vec3 v_color;

void main()
{  
   gl_FragColor = vec4(v_color.r, v_color.g, v_color.b, 1);
   //gl_FragColor = vec4( sin(gl_FragCoord.x / 10.0) / 2 + 0.5, 0, 0, 1   );
}