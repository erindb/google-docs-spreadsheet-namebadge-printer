#!/usr/bin/python2.4
# -*- coding: latin-1 -*-

import argparse
import pandas as pd
from sys import exit

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib import utils

def parse_args():
  parser = argparse.ArgumentParser(
    description = ("Prints PDF name badges to fit Avery name badges"))
  parser.add_argument("--f", type = str,
                      help = "filename of CSV file (downloaded from gdocs)")
  parser.add_argument("--o", type = str, default = "Badges_rendered.pdf",
                      help = "output pdf filename")
  parser.add_argument("--event_name", type = str, default = "",
                      help = "output pdf filename")
  return parser.parse_args()

class BadgePrinter:
  def __init__(self, df, output_filename, event_name):
    self.df = df
    self.pdf = Canvas(output_filename, pagesize = letter)
    self.event_name = event_name
    self.logo_path = "SU_New_BlockStree_2color.png"
    
  def drawBadges(self):
    for six_registrants in self._chunkRegistrantsIntoSixes():
      self._drawOnePage(six_registrants)
    self.pdf.save()
        
  def _drawOnePage(self, registrants):
    left_column_x = 2.25
    right_column_x = 6.25
    top_y = 9
    middle_y = 6
    bottom_y = 3
    xs = []
    ys = []
    i = 0
    for x in [left_column_x, right_column_x]:
      for y in [top_y, middle_y, bottom_y]:
        if i < len(registrants):
          xs.append(x)
          ys.append(y)
        i += 1
    registrants = registrants.assign(x = xs, y = ys)
    registrants.apply(self._drawOneNameBadge, axis=1)
    self.pdf.showPage()

  def _drawLogo(self, x, y, offset):
    # no smaller than 0.375
    logo_width = 0.42 * inch

    img = utils.ImageReader(self.logo_path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    logo_height=logo_width * aspect

    # # find top corner of image
    logo_left_x = x * inch - logo_width/2
    logo_top_y = (y - 3.8 - 0.7 + 0.3 - 0.1 + offset/2) * inch + logo_width

    # allow 1/8 height of block S surrounding logo
    self.pdf.drawImage(self.logo_path,
                       x = logo_left_x,
                       y = logo_top_y,
                       width = logo_width, # 3/8 smallest
                       preserveAspectRatio = True,
                       mask = "auto")

  def _drawName(self, x, y, name):
    self.pdf.setFillColor(colors.black)
    self.pdf.setFont("Helvetica", 24)
    name_x = x * inch
    name_y = (y - 0.73 + 0.3 - 0.1) * inch
    if (len(name) > 22):
      print(name)
      name_x = x * inch
      name_y1 = name_y
      name_y2 = name_y + 0.2 * inch
      name_elements = name.split(" ")
      name1 = " ".join(name_elements[0:2])
      name2 = " ".join(name_elements[2:])
      offset = 0.375
      self.pdf.drawCentredString(name_x, name_y1 + offset/2*inch, str(name1))
      self.pdf.drawCentredString(name_x, name_y1 - offset/2*inch, str(name2))
      return offset
    else:
      self.pdf.drawCentredString(name_x, name_y, str(name))
      return 0

  def _drawOneNameBadge(self, registrant):
    x = registrant.x
    y = registrant.y
    name_offset = self._drawName(x, y, registrant.full_name)
    self._drawLogo(x, y, name_offset)
    self.pdf.setFillColor(colors.black)
    self.pdf.setFont("Helvetica", 18)
    self.pdf.drawCentredString(x * inch, (y - .25 - 0.85 + 0.3 - 0.1 - name_offset/2) * inch, str(registrant.title))
    if type(registrant.area)==str:
      self.pdf.setFont("Helvetica", 12)
      self.pdf.drawCentredString(x * inch, (y - .5 - 0.9 + 0.3 - 0.1 - name_offset/2) * inch, str(registrant.area))
    # # self.pdf.setFont("Helvetica", 6)
    # # self.pdf.setFillColor(colors.green)
    # # self.pdf.drawCentredString(x * inch, (y - .7) * inch, str(self.event_name))

  def _chunkRegistrantsIntoSixes(self):
    chunked = []
    for i in range(0, len(self.df), 6):
      chunked.append(self.df[i:i + 6])
    return chunked

def main():
  args = parse_args()
  df = pd.read_csv(args.f)
  badge_printer = BadgePrinter(df, args.o, args.event_name)
  badge_printer.drawBadges()

if __name__ == '__main__':
  main()