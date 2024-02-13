from datetime import timedelta

from src import create_date_string, create_week, eng_week_2_korean_week
from src.GenerateFromTemplate import GenerateFromTemplate
from src.bor.plot import *


def generate_bor(df, name, date):

    generate_일별bor(df, name)
    generate_daily_boa(df, name)
    generate_평균두뇌활동비율(df, name)

    gen = GenerateFromTemplate("./report_template_new/bor.pdf")
    gen.addText(date.strftime("%Y년 %m월 %d일"), (129, 790), font_size=9)
    gen.addText(
        (date + timedelta(days=6)).strftime(" ~ %Y년 %m월 %d일"), (200, 790), font_size=9
    )
    gen.addText(name, (510, 805), font_size=9)

    daily_bor_x, daily_bor_y = 16, 445
    daily_bor_step = 30
    daily_bor_scale = 0.32

    일별두되가동량_x, 일별두되가동량_y = 344, 448
    일별두되가동량_step = 30
    일별두되가동량_scale = 0.32

    weeks = create_week(df.weekday)

    for idx, week in enumerate(weeks):
        gen.addGraphics(
            (daily_bor_x + daily_bor_step * idx, daily_bor_y),
            f"images/daily_bor_{week}.png",
            scale=daily_bor_scale,
        )
        gen.addGraphics(
            (일별두되가동량_x + 일별두되가동량_step * idx, 일별두되가동량_y),
            f"images/daily_boa_{week}.png",
            scale=일별두되가동량_scale,
        )

    gen.addGraphics((308, 525), f"images/daily_boa_text_max.png", scale=0.1)
    gen.addGraphics((308, 480), f"images/daily_boa_text_middle.png", scale=0.1)

    gen.addText("매우 높음은 뇌의 인지기능을 많이 사용하고 있는 상태로 어려운 과제 수행을", (20, 315), font_size=9)
    gen.addText(f"할 때 나타납니다. {name} 님의 주간 평균 두놔가동률이 매우 높은 상태로", (20, 303), font_size=9)
    gen.addText(
        f"나타나는 시간은 전체 공부시간의 {round(df[df['time'] > 0]['veryHighFocusMean'].mean() * 100)}%입니다.",
        (20, 291),
        font_size=9,
    )

    gen.addText(f"보통은 일상적인 생활을 할 때 나타나는 수준의 인지 사용량을 의미합니다.", (305, 315), font_size=9)
    gen.addText(f"{name} 님의 주간 평균 두놔가동률이 보통 수준으로 나타나는 시간은 전체", (305, 303), font_size=9)
    gen.addText(
        f"공부시간의 {round(df[df['time'] > 0]['highFocusMean'].mean() * 100)}%입니다.",
        (305, 291),
        font_size=9,
    )

    gen.addText(f"높음은 뇌의 인지기능을 적절하게 사용하고 있는 상태로 적절한 난이도의 ", (20, 230), font_size=9)
    gen.addText(f"과제 수행을 의미합니다. {name} 님의 주간 평균 두놔가동률이 높음 상태로", (20, 218), font_size=9)
    gen.addText(
        f"나타나는 시간은 전체 공부시간의 {round(df[df['time'] > 0]['middleFocusMean'].mean() * 100)}% 입니다",
        (20, 206),
        font_size=9,
    )

    gen.addText("낮음은 뇌의 활동이 낮은 상태로 졸음과 같이 인지 사용량이 적은 상태를 ", (305, 230), font_size=9)
    gen.addText(f"의미합니다. {name} 님의 주간 평균 두놔가동률이 낮음 상태로 나타나는", (305, 218), font_size=9)
    gen.addText(
        f"시간은 전체 공부시간의 {round(df[df['time'] > 0]['lowFocusMean'].mean() * 100)}%입니다. ",
        (305, 206),
        font_size=9,
    )

    df_without_zeros = df[df["time"] > 0]

    평균bor = np.mean([element.mean() for element in df_without_zeros.abs_brain_energies])

    gen.addGraphics((420, 630), f"images/meaned_bor_proportion.png", scale=0.3)
    gen.addColoredText(
        f"매우 높음 ({round(df_without_zeros['veryHighFocusMean'].mean() * 100)}%)",
        (475, 635),
        font_size=7,
        color=(98, 102, 234),
    )
    gen.addColoredText(
        f"높음 ({round(df_without_zeros['highFocusMean'].mean() * 100)}%)",
        (475, 623),
        font_size=7,
        color=(148, 148, 255),
    )
    gen.addColoredText(
        f"보통 ({round(df_without_zeros['middleFocusMean'].mean() * 100)}%)",
        (540, 635),
        font_size=7,
        color=(192, 132, 239),
    )
    gen.addColoredText(
        f"낮음 ({round(df_without_zeros['lowFocusMean'].mean() * 100)}%)",
        (540, 623),
        font_size=7,
        color=(220, 175, 255),
    )

    gen.addText("평균", (513, 715), font_size=7)
    gen.addText("두놔가동률", (503, 705), font_size=7)
    gen.addText(f"{round(평균bor * 100)}%", (513, 695), font_size=7)

    for idx, week in enumerate(eng_week_2_korean_week(weeks)):  # 한글로 바꾸기
        gen.addColoredText(
            f"{week}", (61 + 30.2 * idx, 432), font_size=9, color=(150, 151, 164)
        )

    for idx, week in enumerate(eng_week_2_korean_week(weeks)):  # 한글로 바꾸기
        gen.addColoredText(
            f"{week}", (350 + 29.8 * idx, 432), font_size=9, color=(150, 151, 164)
        )

    days = create_date_string(df["startedAt"].dropna().iloc[0])

    for idx, day in enumerate(days):
        gen.addColoredText(
            f"{day}", (55 + 30.2 * idx, 422), font_size=9, color=(150, 151, 164)
        )

    for idx, day in enumerate(days):
        gen.addColoredText(
            f"{day}", (344 + 29.8 * idx, 422), font_size=9, color=(150, 151, 164)
        )

    gen.merge()
    gen.generate(f"output/{name}_bor.pdf")

    return f"output/{name}_bor.pdf"
