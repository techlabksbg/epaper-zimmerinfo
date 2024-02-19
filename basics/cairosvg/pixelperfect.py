from cairosvg import svg2png
# <!-- text-rendering="geometricPrecision" -->
svg_code = """
    <svg xmlns="http://www.w3.org/2000/svg" width="800" height="480" viewBox="-0.5 -0.5 800 480">
        <style>
            .fntsmall {
                font: 60px sans-serif;
                fill: #000;
            }
            line {
                stroke-width : 1;
                stroke-linecap : square;
                stroke-linejoin : miter;
                stroke: #000;
            }
        </style>
        <rect x="0" y="0" width="800" height="480" fill="white" stroke="#fff" />
        <line x1="10.5" y1="10.5" x2="790.5" y2="10.5"/>
        <line x1="20" y1="5" x2="20" y2="475"/>
        <text x="100" y="100" class="fntsmall">Hallo</text>
    </svg>
"""

with open("output.svg", "w") as f:
    f.write(svg_code)

svg2png(bytestring=svg_code,write_to='output.png')
