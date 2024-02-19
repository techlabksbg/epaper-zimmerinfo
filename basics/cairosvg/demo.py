# from https://stackoverflow.com/questions/6589358/convert-svg-to-png-in-python

from cairosvg import svg2png

svg_code = """
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12" y2="16"/>
    </svg>
"""

svg2png(bytestring=svg_code,write_to='output.png')
