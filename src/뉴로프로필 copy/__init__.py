from datetime import timedelta

from src.GenerateFromTemplate import GenerateFromTemplate
from src.neuroprofile.plot import *

font_size = 9
mbti_coef = 90


def text_for_e(gen, name):
    gen.addText(
        "E", (130 + mbti_coef * 0, 600), font_size=81, font_family="NotoSansKR-Bold"
    )

    gen.addText("E", (40, 480), font_size=40, font_family="NotoSansKR-Bold")

    x, y, coef_y = 35, 400, 11

    gen.addText(
        f"{name}님의 일별 총 공부 시간은 불규칙한 양상을 띕니다. 본인에게 ",
        (x, y - coef_y * 0),
        font_size=font_size,
    )
    gen.addText(
        "맞는 공부 타이밍과 시간을 찾아 공부하는 데에 유리한 유형입니다.", (x, y - coef_y * 1), font_size=font_size
    )


def text_for_i(gen, name):
    gen.addText(
        "I", (150 + mbti_coef * 0, 600), font_size=81, font_family="NotoSansKR-Bold"
    )

    gen.addText("I", (40, 480), font_size=40, font_family="NotoSansKR-Bold")

    x, y, coef_y = 35, 400, 11

    gen.addText(
        f"{name}님의 일별 총 공부 시간은 일정한 양상을 띕니다.", (x, y - coef_y * 0), font_size=font_size
    )
    gen.addText(
        "꾸준하게 일정한 강도로 집중력을 유지하는 데에 유리한 유형입니다.", (x, y - coef_y * 1), font_size=font_size
    )


def text_for_h(gen, name):
    gen.addText(
        "H", (130 + mbti_coef * 1, 600), font_size=81, font_family="NotoSansKR-Bold"
    )

    gen.addText("H", (320, 480), font_size=40, font_family="NotoSansKR-Bold")

    x, y, coef_y = 320, 400, 11

    gen.addText(
        f"{name}님의 주간 평균 두뇌 가동률은 높았습니다. 이는 적절한",
        (x, y - coef_y * 0),
        font_size=font_size,
    )
    gen.addText(
        "난이도의 과제를 수행했다는 것을 의미합니다. 높은 두뇌가동률이 ", (x, y - coef_y * 1), font_size=font_size
    )
    gen.addText(
        "지속될 경우, 쉽게 지칠 수 있음을 염두에 두는 것이 좋습니다.", (x, y - coef_y * 2), font_size=font_size
    )


def text_for_d(gen, name):
    gen.addText(
        "D", (130 + mbti_coef * 1, 600), font_size=81, font_family="NotoSansKR-Bold"
    )

    gen.addText("D", (320, 480), font_size=40, font_family="NotoSansKR-Bold")

    x, y, coef_y = 320, 400, 11

    gen.addText(
        f"{name}님의 주간 평균 두뇌 가동률은 낮았습니다. 이는 낮은", (x, y - coef_y * 0), font_size=font_size
    )
    gen.addText(
        "난이도의 과제를 수행했다는 것을 의미합니다. 지속될 경우, 본인의", (x, y - coef_y * 1), font_size=font_size
    )
    gen.addText(
        "능력을 더 발휘할 기회를 놓칠 수 있음을 염두해 두는것이 좋습니다.",
        (x, y - coef_y * 2),
        font_size=font_size,
    )


def text_for_c(gen, name):

    gen.addText(
        "C", (130 + mbti_coef * 2, 600), font_size=81, font_family="NotoSansKR-Bold"
    )

    gen.addText("C", (40, 280), font_size=40, font_family="NotoSansKR-Bold")

    x, y, coef_y = 35, 200, 11

    gen.addText(
        f"{name}님은 공부 규칙성이 높은 유형입니다. 공부 규칙성이 높다는 것은 ",
        (x, y - coef_y * 0),
        font_size=font_size,
    )
    gen.addText(
        "계획적인 경향을 띤다는 것을 의미합니다. 일정한 시간대에 공부하는", (x, y - coef_y * 1), font_size=font_size
    )
    gen.addText(
        "습관을 들이고 할 일들을 해결해 나가는 것에 유리한 유형입니다.", (x, y - coef_y * 2), font_size=font_size
    )


def text_for_r(gen, name):

    gen.addText(
        "R", (130 + mbti_coef * 2, 600), font_size=81, font_family="NotoSansKR-Bold"
    )

    gen.addText("R", (40, 280), font_size=40, font_family="NotoSansKR-Bold")

    x, y, coef_y = 35, 200, 11

    gen.addText(
        f"{name}님은 공부 규칙성이 낮은 유형입니다. 공부 규칙성이 낮다는 것은 ",
        (x, y - coef_y * 0),
        font_size=font_size,
    )
    gen.addText(
        "즉흥적인 경향을 띤다는 것을 의미합니다. 일정한 시간대에 공부하는", (x, y - coef_y * 1), font_size=font_size
    )
    gen.addText(
        "것에는 불리하지만 오히려 집중할 때 불태울 수 있는 유형입니다.", (x, y - coef_y * 2), font_size=font_size
    )


def text_for_b(gen, name):

    gen.addText(
        "B", (130 + mbti_coef * 3, 600), font_size=81, font_family="NotoSansKR-Bold"
    )

    gen.addText("B", (320, 280), font_size=40, font_family="NotoSansKR-Bold")

    x, y, coef_y = 320, 200, 11

    gen.addText(
        f"{name}님의 집중 유형은 초반에 가동률이 높게 올라가는 초반형입니다.",
        (x, y - coef_y * 0),
        font_size=font_size,
    )
    gen.addText(
        "이 유형은 중반 이전까지 두뇌 가동률이 상승하는 게 특징이며, ", (x, y - coef_y * 1), font_size=font_size
    )
    gen.addText("자신의 최대 집중력 도달 속도가 빠른 유형입니다.", (x, y - coef_y * 2), font_size=font_size)


def text_for_l(gen, name):

    gen.addText(
        "L", (130 + mbti_coef * 3, 600), font_size=81, font_family="NotoSansKR-Bold"
    )

    gen.addText("L", (320, 280), font_size=40, font_family="NotoSansKR-Bold")

    x, y, coef_y = 320, 200, 11

    gen.addText(
        f"{name}님의 집중 유형은 후반에 가동률이 높게 올라가는 후반형입니다.",
        (x, y - coef_y * 0),
        font_size=font_size,
    )
    gen.addText(
        "이 유형은 중반 이후에 두뇌 가동률이 상승하는 게 특징이며, ", (x, y - coef_y * 1), font_size=font_size
    )
    gen.addText("높은 퍼포먼스로 공부를 마무리하는 유형입니다.", (x, y - coef_y * 2), font_size=font_size)


bti_2_function = {
    "i": text_for_i,
    "e": text_for_e,
    "h": text_for_h,
    "d": text_for_d,
    "c": text_for_c,
    "r": text_for_r,
    "b": text_for_b,
    "l": text_for_l,
}


def get_neuroprofile(df):
    profile = []


def generate_neuroprofile(df, name, date):
    neuroprofile = generate_neuroprofile_list(df, name)

    gen = GenerateFromTemplate("./report_template_new/뉴로프로필.pdf")
    gen.addText(date.strftime("%Y년 %m월 %d일"), (129, 790), font_size=9)
    gen.addText(
        (date + timedelta(days=6)).strftime(" ~ %Y년 %m월 %d일"), (200, 790), font_size=9
    )
    gen.addText(name, (510, 805), font_size=9)

    for letter in neuroprofile:
        bti_2_function[letter](gen, "김주영")

    gen.addText("규칙적이고 빠른 집중", (250, 560), font_size=12)

    # 일별 총 공부시간
    gen.addGraphics((80, 450), f"images/일별총공부시간.png", scale=0.5)

    # 두뇌가동률

    gen.addGraphics((350, 400), f"images/meaned_bor_proportion.png", scale=0.3)
    gen.addText("평균", (439, 482), font_size=10)
    gen.addText("두뇌 가동률", (424, 467), font_size=10)
    gen.addText("77%", (439, 452), font_size=11)  # mmecoco 퍼센트 가져오기

    # 공부규칙성
    gen.addGraphics((70, 214), f"images/공부규칙성.png", scale=0.2)

    # 집중유형
    gen.addGraphics((355, 220), f"images/집중유형.png", scale=0.2)

    gen.merge()
    gen.generate(f"output/{name}_bbti.pdf")

    return f"output/{name}_bbti.pdf"
