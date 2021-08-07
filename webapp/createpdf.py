from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen.canvas import Canvas
import io
import os

def create_pdf(destination, template, text_to_add):
    packet = io.BytesIO()

    my_canvas = Canvas(packet, pagesize=LETTER)
    for text, loc in text_to_add.items():
        my_canvas.drawString(loc[0], loc[1], text)
    my_canvas.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    template_pdf = PdfFileReader(open(template, "rb"))
    output = PdfFileWriter()
    page = template_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    page.compressContentStreams()
    output.addPage(page)
    outputStream = open(destination, "wb")
    output.write(outputStream)
    outputStream.close()

def delete_file(target):
    if os.path.exists(target):
        os.remove(target)