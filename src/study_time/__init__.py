from datetime import datetime, timedelta

import numpy as np

from src import create_date_string, eng_week_2_korean_week
from src.GenerateFromTemplate import GenerateFromTemplate
from src.study_time.plot import *


def generate_study_time(df, name, date):

    generate_daily_study_time(df, name)
    generate_goal_relational_study_time(df, name)

    gen = GenerateFromTemplate("./report_template/study_time.pdf")
    gen.addText(date.strftime("%Y년 %m월 %d일"), (129, 790), font_size=9)
    gen.addText(
        (date + timedelta(days=6)).strftime(" ~ %Y년 %m월 %d일"), (200, 790), font_size=9
    )
    gen.addText(name, (510, 805), font_size=9)

    xs = [70, 100, 130, 161, 191, 222, 252]
    weeks = create_week(df.weekday)

    for x, week in zip(xs, weeks):
        gen.addGraphics((x, 467), f"images/daily_study_time_{week}.png", scale=0.3)

    gen.addGraphics(
        (542, 431), f"images/goal_relational_study_time_text_max.png", scale=0.1
    )
    gen.addGraphics(
        (481, 431), f"images/goal_relational_study_time_text_middle.png", scale=0.1
    )

    gen.addText("-", (323, 444), font_size=6)
    gen.addText("-", (377, 444), font_size=6)

    gen.addGraphics(
        (321, 431), f"images/goal_relational_study_time_text_max.png", scale=0.1
    )
    gen.addGraphics(
        (373, 431), f"images/goal_relational_study_time_text_middle.png", scale=0.1
    )

    df_without_zeros = df[df["time"] > 0]

    평균_주간_study_time = datetime(2000, 3, 17, 0) + timedelta(
        seconds=np.mean(df_without_zeros.summed_time)
    )
    최대_주간_study_time = datetime(2000, 3, 17, 0) + timedelta(
        seconds=np.max(df_without_zeros.summed_time)
    )
    최소_주간_study_time = datetime(2000, 3, 17, 0) + timedelta(
        seconds=np.min(df_without_zeros.summed_time)
    )
    공부_시간_변화량 = np.diff(df.summed_total_duration)

    generate_평균study_time(평균_주간_study_time.hour, 평균_주간_study_time.minute, name)
    gen.addGraphics((380, 600), f"images/study_time.png", scale=0.4)
    gen.addText("평균 공부 시간", (485, 710), font_size=9)
    if 평균_주간_study_time.hour == 0:
        gen.addText(f"{평균_주간_study_time.minute}분", (502, 690), font_size=10)
    else:
        gen.addText(
            f"{평균_주간_study_time.hour}시간 {평균_주간_study_time.minute}분",
            (485, 690),
            font_size=10,
        )

    gen.addText(
        f"{name} 님의 주간 평균 공부 시간은 {str(평균_주간_study_time.hour) + '시간' if 평균_주간_study_time.hour != 0 else ''} {평균_주간_study_time.minute} 분입니다. 최단 시간은 {str(최소_주간_study_time.hour) + '시간' if 최소_주간_study_time.hour != 0 else ''}",
        (20, 330),
        font_size=9,
    )
    gen.addText(
        f"{최소_주간_study_time.minute}분이었으며, 최장 공부 시간은 {str(최대_주간_study_time.hour) + '시간' if 최대_주간_study_time.hour != 0 else ''} {최대_주간_study_time.minute}분이었습니다.",
        (20, 318),
        font_size=9,
    )

    gen.addText(
        f"{name} 님의 목표 시간 대비 공부 시간은 평균적으로 {abs(round(np.mean(df_without_zeros.summed_goal_proportion) / 60))}분 {'많았' if np.mean(df_without_zeros.goalProportion) > 0 else '적었'}습니다.",
        (305, 330),
        font_size=9,
    )
    gen.addText(
        f"최저 시간 기록일에는 목표 대비 {abs(round(np.min(df_without_zeros.summed_goal_proportion) / 60))}분 적었으며, 최고 기록일에는",
        (305, 318),
        font_size=9,
    )
    gen.addText(
        f"목표 대비 {abs(round(np.min(df_without_zeros.summed_goal_proportion) / 60))}분 많았습니다. 전반적으로 목표치보다 {abs(round(np.mean(df_without_zeros.goalProportion) / 60))}분만큼,",
        (305, 306),
        font_size=9,
    )
    gen.addText(
        f"목표 시간을 {'줄이시' if np.mean(df_without_zeros.summed_goal_proportion) < 0  else '늘리시'}는 것이 공부에 도움이 될 수 있습니다.",
        (305, 294),
        font_size=9,
    )

    gen.addText(
        f"{name} 님의 공부 시간의 평균 변화량은 {round(np.mean(공부_시간_변화량) // 60)}분으로, {'증가' if np.mean(공부_시간_변화량) // 60 >= 0 else '감소'}하는 양상을",
        (20, 230),
        font_size=9,
    )
    gen.addText("보였습니다.", (20, 218), font_size=9)

    gen.addText(
        f"7일 중 목표한 공부 시간을 달성한 날은 {(df.summed_goal_proportion > 0).sum()}일이었으며, 달성하지 못한 날은",
        (305, 230),
        font_size=9,
    )
    gen.addText(
        f"{7 - (df.summed_goal_proportion > 0).sum()}일 입니다. ", (305, 218), font_size=9
    )

    gen.addGraphics(
        (342, 420), f"images/goal_relational_study_time.png", scale=0.33
    )  # 칸당 15y

    gen.addGraphics((12, 540), f"images/daily_study_time_text_1.png", scale=0.12)
    gen.addGraphics((12, 540 - 25), f"images/daily_study_time_text_2.png", scale=0.12)
    gen.addGraphics((12, 540 - 46), f"images/daily_study_time_text_3.png", scale=0.12)
    gen.addGraphics((12, 540 - 69), f"images/daily_study_time_text_4.png", scale=0.12)

    for idx, week in enumerate(eng_week_2_korean_week(weeks)):
        gen.addColoredText(
            f"{week}", (324, 552 - 15 * idx), font_size=8, color=(150, 151, 164)
        )

    for idx, week in enumerate(eng_week_2_korean_week(weeks)):
        gen.addColoredText(
            f"{week}", (75 + 30.5 * idx, 455), font_size=8, color=(150, 151, 164)
        )

    days = create_date_string(df["startedAt"].iloc[0])

    for idx, day in enumerate(days):
        gen.addColoredText(
            f"{day}", (69 + 30.5 * idx, 445), font_size=8, color=(150, 151, 164)
        )

    gen.merge()
    gen.generate(f"output/{name}_study_time.pdf")
    return f"output/{name}_study_time.pdf"
