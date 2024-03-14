import sqlite3
import os
from PIL import Image, ImageDraw
import matplotlib
from datetime import datetime
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from flaskr.db import get_db

spannung_min = 2.5
spannung_max = 4.5

display_hoehe = 480
display_breite = 800

zeit_min = 0
zeit_max = 1

def plot_voltage(path, macid, mac):
  global zeit_min, zeit_max

  cursor = get_db()

  inhalt = cursor.execute("SELECT volt, statusTime FROM volt WHERE macid = ?", (macid, )).fetchall()

  zeit_werte = [t for u, t in inhalt]
  spannung_werte = [u for u, t in inhalt]

  zeit_min = datetime.now()
  zeit_max = datetime.now()
  if (len(zeit_werte) != 0):
    zeit_min = min(zeit_werte)
    zeit_max = max(zeit_werte)

  #plot_naive(zeit_werte, spannung_werte, path)
  plot_matplotlib(zeit_werte, spannung_werte, path, mac)

def display_x(t):
  return display_breite * (t - zeit_min).seconds / max(1, (zeit_max - zeit_min).seconds)

def display_y(v):
  return display_hoehe - display_hoehe * (v - spannung_min) / max(1, (spannung_max - spannung_min))

def plot_naive(zeit_werte, spannung_werte, path):
  bild = Image.new('L', (display_breite, display_hoehe), 255)
  draw = ImageDraw.Draw(bild)
  for i in range(len(zeit_werte) - 1):
      px, py = display_x(zeit_werte[i]), display_y(spannung_werte[i])
      qx, qy = display_x(zeit_werte[i + 1]), display_y(spannung_werte[i + 1])
      draw.line((px, py, qx, qy), fill=0, width=2)
  bild.save(path+'/diagram.png')

def plot_matplotlib(zeit_werte, spannung_werte, path, mac):
  # save plt as png with given size
  plt.figure(figsize=(display_breite/100, display_hoehe/100), dpi=100)
  plt.plot(zeit_werte, spannung_werte, 'black')
  plt.title('MAC-Address: ' + mac)
  plt.savefig(path+'/diagram.png')
  plt.close()