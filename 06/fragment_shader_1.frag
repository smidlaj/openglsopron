#version 330
void main()
{
   //gl_FragColor = vec4(gl_FragCoord.x / 1200.0, gl_FragCoord.y / 720.0, 0.0f, 1.0f);
   //gl_FragColor = vec4(1, cos(gl_FragCoord.y / 12), sin(gl_FragCoord.x / 10), 1);
   
   //gl_FragColor.rgb = vec3(0, 1, 0);
   
   /*if ( gl_FragCoord.x > 700 ) {
   		gl_FragColor.r = 0;
   		
   	} else {
   		gl_FragColor.g = 0;
   	}
   	
   	int a;
   	for (a = 0; a < 10; a++) {
   		gl_FragColor.b *= 0.9;
   	}*/
   
   gl_FragColor = vec4(1, 0, 0, 1);
}
