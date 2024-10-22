import io

from PyPDF2 import PdfReader, PdfWriter, Transformation
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

font_path = "fonts/Noto_Sans_KR/static/NotoSansKR-Light.ttf"

pdfmetrics.registerFont(TTFont("NotoSansKR", font_path))

font_path = "fonts/Noto_Sans_KR/static/NotoSansKR-Bold.ttf"

pdfmetrics.registerFont(TTFont("NotoSansKR-Bold", font_path))  # mmecoco 폰트 관리 코드 작성


def drawText(c, text, x, y, font_size):
    contents = text.split("\n")

    for content in contents:
        alpha = 0.5

        modified_color = c._color(80, 82, 101, alpha)

        c.setFillColor(modified_color)
        c.drawString(x, y, content)
        y = y - font_size


class GenerateFromTemplate:
    """
    PDF 를 쉽게 편집할 수 있도록 만든 클래스

    사용법은
    1. generator를 pdf template path 를 통해서 로드 한다
    ex. gen = GenerateFromTemplate("./report_template_new/study_time.pdf")

    2. 택스트 혹은 이미지를 삽입한다
    ex text. gen.addText(name, (510, 805), font_size=9)
    ex image. gen.addGraphics((x, 467), f"images/daily_study_time_{week}.png", scale=0.3)

    3. 편집이 완료가 된 변경사항을 merge 하고 저장할 수 있다
    ex.  gen.merge()
         gen.generate(f"output/{name}_study_time.pdf")
    """

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
