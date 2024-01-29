from datetime import timedelta

from src.GenerateFromTemplate import GenerateFromTemplate

def generate_뉴로프로필_부록(df, name, date):

    gen = GenerateFromTemplate("report_template_new/뉴로프로필_부록.pdf")
    gen.addText(date.strftime("%Y년 %m월 %d일"), (129, 790), font_size=9)
    gen.addText(
        (date + timedelta(days=6)).strftime(" ~ %Y년 %m월 %d일"), (200, 790), font_size=9
    )
    gen.addText(name, (510, 805), font_size=9)
    
    gen.merge()
    gen.generate(f"output/{name}_뇌BTI_부록.pdf")

    return f"output/{name}_뇌BTI_부록.pdf"
