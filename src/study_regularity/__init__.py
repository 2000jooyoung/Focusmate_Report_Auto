import enum
from datetime import timedelta
from glob import glob

from src import create_date_string, create_week, eng_week_2_korean_week
from src.GenerateFromTemplate import GenerateFromTemplate
from src.study_regularity.plot import *


def find_longest_consecutive_range_of_max(lst):
    max_value = max(lst)

    longest_range = None
    current_range = None

    for i, value in enumerate(lst):
        if value == max_value:
            if current_range is None:
                current_range = (i, i)
            else:
                current_range = (current_range[0], i)
        elif current_range is not None:
            if longest_range is None or (current_range[1] - current_range[0]) > (
                longest_range[1] - longest_range[0]
            ):
                longest_range = current_range
            current_range = None

    if current_range is not None and (
        longest_range is None
        or (current_range[1] - current_range[0]) > (longest_range[1] - longest_range[0])
    ):
        longest_range = current_range

    return longest_range


def generate_study_regularity(df, name, date):
    labels = {0: "없음", 1: "낮음", 2: "보통", 3: "높음"}

    generate_study_regularity1(df, name)
    규칙성 = generate_study_regularity2(df, name)
    mapping = {"없음": 0, "낮음": 1, "보통": 2, "높음": 3}

    # Convert the Korean words to integers using the mapping
    규칙성_int = [mapping[word] for word in 규칙성]

    gen = GenerateFromTemplate("./report_template/study_regularity.pdf")
    gen.addText(date.strftime("%Y년 %m월 %d일"), (129, 790), font_size=9)
    gen.addText(
        (date + timedelta(days=6)).strftime(" ~ %Y년 %m월 %d일"), (200, 790), font_size=9
    )
    gen.addText(name, (510, 805), font_size=9)

    study_regularity_x, study_regularity_y = 64, 432
    study_regularity_step = 28
    study_regularity_scale = 0.38

    weeks = create_week(df.weekday)

    for idx, week in enumerate(df.weekday):
        for file_path in glob(f"images/{week}/*.png"):
            gen.addGraphics(
                (study_regularity_x + study_regularity_step * idx, study_regularity_y),
                file_path,
                scale=study_regularity_scale,
            )

    gen.addGraphics((297, 358), f"images/study_regularity2.png", scale=0.14)  # 토

    # 높은 시간대 회색 밴드 넣기

    range = find_longest_consecutive_range_of_max(규칙성_int)
    max_val = max(규칙성_int[range[0] : range[1] + 1])

    if labels[max_val] != "없음":
        gen.addText(
            f"{name} 님은 공부 규칙성은 {range[0]}시에서 {range[1] + 1}시 사이에 {labels[max_val]}으로 나타납니다. 꾸준히 높은 규칙성을 유지하시면 효율적인 공부를",
            (20, 300),
            font_size=10,
        )
        gen.addText("하실 수 있을 것입니다.", (20, 288 - 2), font_size=10)
    else:
        gen.addText(
            f"{name} 님의 공부 규칙성은 없음으로 나타납니다. {name} 님만의 공부 습관을 만들어보시면 더 효율적인 공부를 하실 수 있을 것입니다.",
            (20, 300),
            font_size=10,
        )

    for idx, week in enumerate(eng_week_2_korean_week(weeks)):
        gen.addColoredText(
            f"{week}", (72 + 28 * idx, 435), font_size=8, color=(150, 151, 164)
        )

    days = create_date_string(df["startedAt"].iloc[0])

    for idx, day in enumerate(days):
        gen.addColoredText(
            f"{day}", (66 + 28 * idx, 425), font_size=8, color=(150, 151, 164)
        )

    gen.merge()
    gen.generate(f"output/{name}_study_regularity.pdf")

    return f"output/{name}_study_regularity.pdf"
