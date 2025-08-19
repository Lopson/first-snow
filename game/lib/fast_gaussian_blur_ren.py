"""renpy
init -1 python:
"""

# BSD 3-Clause License
# 
# Copyright (c) 2019, David Lettier
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Source: https://github.com/lettier/3d-game-shaders-for-beginners/blob/master/demonstration/shaders/fragment/box-blur.frag


from renpy.gl2.gl2shadercache import register_shader


register_shader("shaders.box_blur", variables="""
    attribute vec2 a_tex_coord;
    varying vec2 v_tex_coord;
    uniform sampler2D tex0;
    uniform vec2 res0;
    uniform int u_size;
    uniform float u_separation;
""", vertex_200="""
    v_tex_coord = a_tex_coord;
""", fragment_200="""
    if (u_size <= 0) {
        gl_FragColor = texture2D(tex0, v_tex_coord);
        return;
    }

    float separation = max(u_separation, 1.0);
    vec2 texel_size = 1.0 / res0;
    
    vec3 sum = vec3(0.0);
    float count = 0.0;

    for (int i = -u_size; i <= u_size; ++i) {
        for (int j = -u_size; j <= u_size; ++j) {
            vec2 offset = vec2(float(i), float(j)) * separation * texel_size;
            sum += texture2D(tex0, v_tex_coord + offset).rgb;
            count += 1.0;
        }
    }

    vec4 original = texture2D(tex0, v_tex_coord);
    gl_FragColor = vec4(sum / count, original.a);
""")
