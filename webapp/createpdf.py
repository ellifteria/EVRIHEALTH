from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen.canvas import Canvas
import io
import os

def create_pdf(destination, template, data_to_add):
    template_pdf = PdfFileReader(open(template, "rb"))
    output = PdfFileWriter()

    packet = io.BytesIO()

    pdf_canvas = Canvas(packet, pagesize=LETTER)
    for page, text_to_add in data_to_add.items():
        if text_to_add is not None:
            for text, loc in text_to_add.items():
                pdf_canvas.drawString(loc[0], loc[1], text)
        pdf_canvas.showPage()
    pdf_canvas.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    for page_number, text_to_add in data_to_add.items():
        page = template_pdf.getPage(page_number)
        page.mergePage(new_pdf.getPage(page_number))
        page.compressContentStreams()
        output.addPage(page)

    outputStream = open(destination, "wb")
    output.write(outputStream)
    outputStream.close()

def delete_file(target):
    if os.path.exists(target):
        os.remove(target)