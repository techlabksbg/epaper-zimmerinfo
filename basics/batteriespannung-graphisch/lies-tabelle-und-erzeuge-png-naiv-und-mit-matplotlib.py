import sqlite3
from PIL import Image, ImageDraw


spannung_min = 2.5
spannung_max = 4.5

display_hoehe = 480
display_breite = 800


verbindung = sqlite3.connect("test.db")

cursor = verbindung.cursor()

cursor.execute("SELECT volt, time FROM volt")
inhalt = cursor.fetchall()

zeit_werte = [t for u, t in inhalt]
spannung_werte = [u for u, t in inhalt]

# for zeile in inhalt:
#     print(zeile)
# print(zeit_werte)
# print(spannung_werte)

verbindung.close()

zeit_min = min(zeit_werte)
zeit_max = max(zeit_werte)
# print(f'{xwerte=}, {zeit_min=}, {zeit_max=}')

def display_x(t):
  return display_breite * (t - zeit_min) / max(1, (zeit_max - zeit_min))

def display_y(v):
  return display_hoehe - display_hoehe * (v - spannung_min) / max(1, (spannung_max - spannung_min))

bild = Image.new('L', (display_breite, display_hoehe), 255)
draw = ImageDraw.Draw(bild)
for i in range(len(zeit_werte) - 1):
    px, py = display_x(zeit_werte[i]), display_y(spannung_werte[i])
    qx, qy = display_x(zeit_werte[i + 1]), display_y(spannung_werte[i + 1])
    draw.line((px, py, qx, qy), fill=0, width=2)
bild.save('diagram.png')

from matplotlib import pyplot as plt

plt.plot(zeit_werte, spannung_werte, 'black')
plt.savefig('matplotdiagram.png', bbox_inches='tight')

graph = Image.open('matplotdiagram.png')
neu = graph.resize((display_breite, display_hoehe))
neu.save(f'matplotdiagram-{display_breite}x{display_hoehe}.png')