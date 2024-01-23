import io

from PyPDF2 import PdfReader, PdfWriter, Transformation
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

font_path = "/Users/jooyoung/Downloads/Noto_Sans_KR/static/NotoSansKR-Light.ttf"

pdfmetrics.registerFont(TTFont("NotoSansKR", font_path))


def drawText(c, text, x, y, font_size):
    contents = text.split("\n")

    for content in contents:
        alpha = 0.5

        modified_color = c._color(80, 82, 101, alpha)

        c.setFillColor(modified_color)
        c.drawString(x, y, content)
        y = y - font_size


class GenerateFromTemplate:
    def __init__(self, template):
        self.template_pdf = PdfReader(open(template, "rb"))
        self.template_page = self.template_pdf.pages[0]

        self.packet = io.BytesIO()
        self.c = Canvas(
            self.packet,
            pagesize=(
                self.template_page.mediabox.width,
                self.template_page.mediabox.height,
            ),
        )

    def addText(self, text, point, font_family="NotoSansKR", font_size=25):
        self.c.setFillColor((82 / 255, 82 / 255, 99 / 255))
        self.c.setFont(font_family, font_size)
        self.c.drawString(point[0], point[1], text)

    def addColoredText(
        self, text, point, font_family="NotoSansKR", font_size=25, color=(80, 82, 101)
    ):
        self.c.setFillColor((color[0] / 255, color[1] / 255, color[2] / 255))
        self.c.setFont(font_family, font_size)
        self.c.drawString(point[0], point[1], text)

    def drawText(self, text, point, font_family="NotoSansKR", font_size=25):
        self.c.setFont(font_family, font_size)

        contents = text.split("\n")
        x, y = point
        for content in contents:
            self.c.drawString(x, y, content)
            y = y - (font_size + 10)

    def merge(self):
        self.c.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        result = result_pdf.pages[0]

        self.output = PdfWriter()

        op = Transformation().rotate(0).translate(tx=0, ty=0)
        result.add_transformation(op)
        self.template_page.merge_page(result)
        self.output.add_page(self.template_page)

    def generate(self, dest):
        outputStream = open(dest, "wb")
        self.output.write(outputStream)
        outputStream.close()

    def addGraphics(self, point, img, scale=1):
        img = ImageReader(img)
        img_width, img_height = img.getSize()

        self.c.drawImage(
            image=img,
            x=point[0],
            y=point[1],
            width=img_width * scale,
            height=img_height * scale,
            mask="auto",
        )
