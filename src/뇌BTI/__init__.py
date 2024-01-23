from datetime import timedelta

from src.GenerateFromTemplate import GenerateFromTemplate
from src.뇌BTI.plot import *


def draw_D(gen):
    gen.addText("D(Dash)는 속도형입니다. 속도형의 사람들은 공부 초반에 두뇌 가동률이", (20, 310), font_size=9)
    gen.addText(f"상승하는 경향을 보이며, 자신의 역량을 끌어 올리려는 성향이", (20, 298), font_size=9)
    gen.addText("있습니다. ", (20, 286), font_size=9)


def draw_R(gen):
    gen.addText("R(Relax)는 안정형입니다. 안정형의 사람들은 공부 초반에 두뇌 가동률이", (20, 310), font_size=9)
    gen.addText("감소하는 경향을 보이며, 주어진 과제를 탐색하고 적응해가는 성향이", (20, 298), font_size=9)
    gen.addText("있습니다. ", (20, 286), font_size=9)


def draw_E(gen):
    gen.addText("E(kEep)는 유지형입니다. 유지형의 사람들은 공부 중반에 두뇌 가동률이", (20, 270), font_size=9)
    gen.addText("유지 혹은 상승하는 경향을 보이며,  공부 페이스를 끌어 올리는 성향이", (20, 258), font_size=9)
    gen.addText("있습니다. ", (20, 246), font_size=9)


def draw_I(gen):
    gen.addText(
        "I(Imbalance)는 변동형입니다. 변동형의 사람들은 공부 중반에 두뇌 가동률이 ", (20, 270), font_size=9
    )
    gen.addText("감소하는 경향을 보이며, 공부 페이스를 조절하는 성향이", (20, 260), font_size=9)
    gen.addText("있습니다. ", (20, 246), font_size=9)


def draw_L(gen):
    gen.addText("L(Late)는 뒷심형입니다. 뒷심형의 사람들은 후반에 두뇌 가동이", (20, 230), font_size=9)
    gen.addText("상승하는 경향을 보이며, 높은 퍼포먼스로", (20, 218), font_size=9)
    gen.addText("공부를 마무리합니다.", (20, 206), font_size=9)


def draw_A(gen):
    gen.addText("A(eArly)는 차분형입니다. 차분형의 사람들은 후반에 두뇌 가동이", (20, 230), font_size=9)
    gen.addText("감소하는 경향을 보이며, 자신이 했던 공부를 점검하고", (20, 218), font_size=9)
    gen.addText("되돌아보며 마무리하는 성향이 있습니다.", (20, 206), font_size=9)


def draw_V(gen):
    gen.addText("V(Various)는 변화형입니다. 변화형의 사람들은 전체적인 두뇌 가동 변화의", (20, 190), font_size=9)
    gen.addText("표준 편차가 큽니다. 다양한 난이도의 공부를 한다고 볼 수 있습니다.", (20, 178), font_size=9)


def draw_S(gen):
    gen.addText("S(Stable)은 지속형입니다. 지속형의 사람들은 전체적인 두뇌 가동 변화의", (20, 190), font_size=9)
    gen.addText("표준 편차가 작습니다. 일정한 난이도의 공부를 한다고 볼 수 있습니다.", (20, 178), font_size=9)


bti_2_function = {
    "d": draw_D,
    "r": draw_R,
    "e": draw_E,
    "i": draw_I,
    "l": draw_L,
    "a": draw_A,
    "v": draw_V,
    "s": draw_S,
}


def generate_두뇌가동유형(df, name, date):
    mbti = generate_뇌BTI결과(df, name)
    generate_두뇌가동률변화추이(df, name)

    gen = GenerateFromTemplate("report_template/뇌BTI.pdf")
    gen.addText(date.strftime("%Y년 %m월 %d일"), (129, 790), font_size=9)
    gen.addText(
        (date + timedelta(days=6)).strftime(" ~ %Y년 %m월 %d일"), (200, 790), font_size=9
    )
    gen.addText(name, (510, 805), font_size=9)

    공부규칙성_x, 공부규칙성_y = -53, 425
    공부규칙성_step = 28
    공부규칙성_scale = 0.29

    gen.addGraphics(
        (공부규칙성_x + 공부규칙성_step * 0, 공부규칙성_y),
        f"{name}/두뇌가동률변화추이.png",
        scale=공부규칙성_scale,
    )  # 일

    mbti_x, mbti_y = 300, 160
    mbti_step = 50
    mbti_scale = 0.4

    gen.addGraphics(
        (mbti_x, mbti_y + mbti_step * 3), f"{name}/폭발.png", scale=mbti_scale
    )
    gen.addGraphics(
        (mbti_x, mbti_y + mbti_step * 2), f"{name}/유지.png", scale=mbti_scale
    )
    gen.addGraphics(
        (mbti_x, mbti_y + mbti_step * 1), f"{name}/결정.png", scale=mbti_scale
    )
    gen.addGraphics(
        (mbti_x, mbti_y + mbti_step * 0), f"{name}/변화.png", scale=mbti_scale
    )

    mbti_x, mbti_y = 305, -150
    mbti_step = 50
    mbti_scale = 0.125

    gen.addGraphics(
        (mbti_x, mbti_y + mbti_step * 3), f"{name}/폭발_text.png", scale=mbti_scale
    )
    gen.addGraphics(
        (mbti_x, mbti_y + mbti_step * 2), f"{name}/유지_text.png", scale=mbti_scale
    )
    gen.addGraphics(
        (mbti_x, mbti_y + mbti_step * 1), f"{name}/결정_text.png", scale=mbti_scale
    )
    gen.addGraphics(
        (mbti_x, mbti_y + mbti_step * 0), f"{name}/변화_text.png", scale=mbti_scale
    )

    title_x, title_y = 410, 335
    title_step = 50

    gen.addText("폭발", ((title_x, title_y - title_step * 0)), font_size=9)
    gen.addText("유지", ((title_x, title_y - title_step * 1)), font_size=9)
    gen.addText("결정", ((title_x, title_y - title_step * 2)), font_size=9)
    gen.addText("변화", ((title_x, title_y - title_step * 3)), font_size=9)

    gen.drawText(
        f"{name} 님의 두뇌 유형은 {''.join(mbti).upper()}형입니다.", (20, 325), font_size=10
    )

    for letter in mbti:
        bti_2_function[letter](gen=gen)

    gen.merge()
    gen.generate(f"output/{name}_뇌BTI.pdf")

    return f"output/{name}_뇌BTI.pdf"
