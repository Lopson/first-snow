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
# Source: https://github.com/WretchedTeam/WintermuteV3/blob/main/game/mod_code/definitions/shaders/blur.rpy


from renpy.gl2.gl2shadercache import register_shader


register_shader("shaders.kawase_blur", variables="""
        uniform sampler2D tex0;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform vec2 res0;
        uniform float u_lod_bias;
        uniform float u_iteration;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_functions="""
        vec4 kawase_pass(sampler2D tex, vec2 uv, vec2 pixel_size, float iteration, float u_lod_bias)
        {
            vec2 off = (pixel_size.xy * vec2(iteration + 0.5));

            vec4 color = texture2D(tex, uv + vec2(-off.x, off.y), u_lod_bias); // Sample top left pixel
            color += texture2D(tex, uv + off, u_lod_bias); // Sample top right pixel
            color += texture2D(tex, uv + vec2(off.x, -off.y), u_lod_bias); // Sample bottom right pixel
            color += texture2D(tex, uv - off, u_lod_bias); // Sample bottom left pixel

            color *= 0.25; // Average 
            
            return color;
        } 
    """, fragment_200="""
        gl_FragColor = kawase_pass(tex0, v_tex_coord, 1.0 / res0.xy, u_iteration, u_lod_bias);
    """)
