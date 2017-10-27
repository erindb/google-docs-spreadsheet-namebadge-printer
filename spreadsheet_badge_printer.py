#!/usr/bin/python2.4
# -*- coding: latin-1 -*-

import getpass

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('SourceSansPro-Black', 'SourceSansPro-Black.ttf'))
# pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))

import os
import pandas as pd      # for working with csv

import gdata.spreadsheet.service

data_file="names.csv"

# from https://identity.stanford.edu/name-emblems.html#stanford-seal
logo_file="SU_Seal_Red.png"
  
class BadgePrinter:
  def __init__(self, registration_list, filename='Badges_rendered.pdf'):
    self.registration_list = registration_list
    self.pdf = Canvas(filename, pagesize = letter)
    
  def drawBadges(self):  
    for six_registrants in self._chunkRegistrantsIntoSixes():
      self._drawOnePage(six_registrants)
    self.pdf.save()
        
  def _drawOnePage(self, registrants):  
    left_column_x = 2.25
    right_column_x = 6.25
    top_y = 8.5
    middle_y = 5.5
    bottom_y = 2.5
    i = 0
    for x in [left_column_x, right_column_x]:
      for y in [top_y, middle_y, bottom_y]:
        if i < len(registrants):
          self._drawOneNameBadge(x, y, registrants[i])
        i += 1      
    self.pdf.showPage()

  def _drawOneNameBadge(self, badge_center_x, badge_center_y, registrant):
    badge_height = 3.0
    badge_width = 4.0

    def x(old):
      return (badge_center_x + old) * inch

    def y(old):
      return (badge_center_y + old) * inch

    img_size = 1.0
    self.pdf.setFillColor(colors.black)
    self.pdf.drawImage(
      "SU_Seal_Red.png",
      x(-(img_size/2)),
      y(0),
      width = img_size * inch,
      height = img_size * inch,
      mask='auto'
    )

    name = "{} {}".format(registrant["first_name"], registrant["last_name"])
    title = "{}, {}".format(registrant["title"], registrant["area"])

    if len(name)>30:
      name_start = " ".join(name.split()[:-1])
      name_continuation = name.split()[-1]

      self.pdf.setFont("SourceSansPro-Black", 19)
      self.pdf.drawCentredString(
        x(0),
        y(-0.25),
        name_start
      )

      self.pdf.setFont("SourceSansPro-Black", 19)
      self.pdf.drawCentredString(
        x(0),
        y(-0.5),
        name_continuation
      )

      self.pdf.setFont("Helvetica", 12)
      self.pdf.drawCentredString(
        x(0),
        y(-0.75),
        title
      )
    else:

      self.pdf.setFont("SourceSansPro-Black", 19)
      self.pdf.drawCentredString(
        x(0),
        y(-0.25),
        name
      )

      self.pdf.setFont("Helvetica", 12)
      self.pdf.drawCentredString(
        x(0),
        y(-0.5),
        title
      )

    # self.pdf.setFont("Helvetica", 8)
    # self.pdf.drawCentredString(x * inch, (y - .5) * inch, str(registrant.job_role))
    # self.pdf.setFont("Helvetica", 6)
    # self.pdf.setFillColor(colors.green)
    # self.pdf.drawCentredString(x * inch, (y - .7) * inch, 'Test Engineering NYC Summit 2008')

  def _chunkRegistrantsIntoSixes(self):
    chunked = []
    for i in range(0, len(self.registration_list), 6):
      chunked.append(self.registration_list[i:i + 6])
    return chunked
  
def main():

  csvfile = "names.csv"

  # get data file
  df = pd.read_csv(os.path.expanduser(csvfile))
  registrats_list = df.T.to_dict().values()

  badge_printer = BadgePrinter(registrats_list)
  badge_printer.drawBadges()

if __name__ == '__main__':
  main()