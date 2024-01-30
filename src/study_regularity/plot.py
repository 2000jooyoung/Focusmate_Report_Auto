import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src import create_week, make_color_transparent
from src.resize_image import resize_image


def get_start_end_scaled_range(df):
    start_ranges = []
    end_ranges = []

    for _, row in df.iterrows():
        start_ranges.append(
            (row["startedAt"].hour * 60 + row["startedAt"].minute) / (24 * 60) * 100
        )
        end_ranges.append(
            (row["endAt"].hour * 60 + row["endAt"].minute) / (24 * 60) * 100
        )

    start_ranges = [e if not np.isnan(e) else 0 for e in start_ranges]
    end_ranges = [e if not np.isnan(e) else 0 for e in end_ranges]

    for _, row in df.iterrows():
        start_ranges.append(
            (row["startedAt"].hour * 60 + row["startedAt"].minute) / (24 * 60) * 100
        )
        end_ranges.append(
            (row["endAt"].hour * 60 + row["endAt"].minute) / (24 * 60) * 100
        )

    start_ranges = [e if not np.isnan(e) else 0 for e in start_ranges]
    end_ranges = [e if not np.isnan(e) else 0 for e in end_ranges]

    return start_ranges, end_ranges


def generate_study_regularity1(df, name):
    start_ranges, end_ranges = get_start_end_scaled_range(df)

    weeks = create_week(df.weekday)

    for start, end, week in zip(start_ranges, end_ranges, weeks):
        source = pd.DataFrame(
            {
                "x": [0, 1],
                "y1": [start - 17, 0],
                "y2": [end - 17, 100],
                "color": ["#9494FF", "#00000000"],
            }
        )

        study_regularity = (
            alt.Chart(source)
            .mark_bar(
                width=30,
                cornerRadius=5,
            )
            .encode(
                x=alt.X("x", axis=None),
                y=alt.Y("y1", axis=None),
                y2=alt.Y2("y2"),
                color=alt.Color("color", scale=None),
            )
        )

        study_regularity = study_regularity.configure_view(stroke="transparent")
        study_regularity.save(f"images/study_regularity_{week}.png", scale_factor=1)
        make_color_transparent(
            f"images/study_regularity_{week}.png", f"images/study_regularity_{week}.png", "#FFFFFF"
        )


def save_공부_규칙성_2(data, name):
    fig, axes = plt.subplots(1, 12, figsize=(20, 20))
    colors = ["#9494FF", "#E7E7FF"]

    type_2_colors = {
        "없음": "#E7E7FF",
        "낮음": "#B5B5FF",
        "보통": "#9494FF",
        "많음": "#5050BB",
    }

    for i, j in zip(
        [i for i in range(4, 24, 2)] + [0, 2], [i for i in range(0, 24, 2)]
    ):
        colors = [type_2_colors[element] for element in data[i : i + 2]]
        ax = axes[j // 2]
        row = [50, 50]
        ax.pie(row, startangle=90, colors=colors)

    fig.subplots_adjust(wspace=0.05)

    plt.savefig(f"images/study_regularity2.png", transparent=True)
    make_color_transparent(f"images/study_regularity2.png", f"images/study_regularity2.png", "#FFFFFF")
    resize_image(f"images/study_regularity2.png", f"images/study_regularity2.png", (2000, 2000))


def generate_study_regularity2(df, name):
    df["timestamp"] = pd.to_datetime(df["startedAt"])
    counts_list = [0] * 24

    for _, row in df.iterrows():
        if not pd.isna(row["timestamp"]):
            interval_index = int(
                (row["timestamp"].hour * 60 + row["timestamp"].minute) / 60
            )
            counts_list[interval_index] += 1

    categories_list = []

    for count in counts_list:
        if count <= 1:
            categories_list.append("없음")
        elif count == 2:
            categories_list.append("낮음")
        elif 3 <= count <= 4:
            categories_list.append("보통")
        else:
            categories_list.append("많음")

    save_공부_규칙성_2(categories_list, name)
    return categories_list
