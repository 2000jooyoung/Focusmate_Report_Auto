import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src import create_week, make_color_transparent


def generate_daily_study_time(df, name):
    duration = df.summed_total_duration
    max_length = (max(duration) // 3600 + 1) * 60
    coef = max(duration) / 60

    weeks = create_week(df.weekday)

    daily_study_time들 = []

    for target in duration / (max_length * 60) * max_length:
        source = pd.DataFrame(
            {
                "label": [1, 2],
                "background": [target, max_length],
                "color": ["#9494FF", "#00000000"],
                # "color": ["#9494FF", "red"],
            }
        )

        background = (
            alt.Chart(source)
            .mark_bar(
                width=40,
                cornerRadiusTopLeft=5,
                cornerRadiusTopRight=5,
            )
            .encode(
                x=alt.X("label", axis=None),
                y=alt.Y("background", axis=None),
                color=alt.Color("color", scale=None),
            )
        )

        background = background.configure_view(stroke="transparent")
        daily_study_time들.append(background)

    for pngs, week in zip(daily_study_time들, weeks):
        pngs.save(f"images/daily_study_time_{week}.png", scale_factor=1)
        make_color_transparent(
            f"images/daily_study_time_{week}.png", f"images/daily_study_time_{week}.png", "#FFFFFF"
        )

    generate_daily_study_time_text(duration, name)


def generate_daily_study_time_text(duration, name):
    axis_max_duration = (max(duration) // 3600 + 1) * 60

    for idx, target in enumerate(
        [(axis_max_duration - ((axis_max_duration // 4) * i)) / 60 for i in range(4)]
    ):
        source = pd.DataFrame(
            {"x": [0], "y": [0], "text": [str(target)], "color": ["#9697A4"]}
        )
        value_text = (
            alt.Chart(source)
            .mark_text(
                fontSize=70,
            )
            .encode(
                x=alt.X("x", axis=None),
                y=alt.Y("y", axis=None),
                text=alt.Text("text"),
                color=alt.Color("color", scale=None),
            )
        )
        chart = value_text
        chart = chart.configure_view(stroke="transparent")
        chart.save(f"images/daily_study_time_text_{idx + 1}.png", scale_factor=1)
        make_color_transparent(
            f"images/daily_study_time_text_{idx + 1}.png",
            f"images/daily_study_time_text_{idx + 1}.png",
            "#FFFFFF",
        )


def generate_goal_relational_study_time(df, name):
    target = np.array(df.summed_goal_proportion)
    original_abs_max = max(abs(target))

    def scale_to_color_bar(original_values, new_max, original_abs_max):
        norm_scale = 2400
        original_min = -original_abs_max
        original_max = original_abs_max

        # Define the new range
        new_min = 0

        # Proportionally scale the values to the new range
        scaled_values = (
            (original_values - original_min) / (original_max - original_min)
        ) * (new_max - new_min) + new_min

        scaled_values = scaled_values * (norm_scale / new_max)
        return list(scaled_values)

    target = target / max(abs(target)) * max(abs(target))
    index = [i + 1 for i in range(9)]
    index.reverse()
    max_boa = np.max(target)
    axis_max_boa = (max_boa // 50 + 1) * 50
    # 최대값이 2400으로 맞춰져있어서 이걸 기준으로 그려야함
    norm_scale = 2400

    source_df = pd.DataFrame(
        {
            "x": [norm_scale // 2] * 9,
            "x2": scale_to_color_bar(target, axis_max_boa, original_abs_max)
            + [0, norm_scale],
            "index": index,
            "color": [
                "#9494FF" if t > norm_scale // 2 else "#E2BEFF"
                for t in scale_to_color_bar(target, axis_max_boa, original_abs_max)
            ]
            # + ["red", "red"], DEBUG
            + ["#00000000", "#00000000"],
        }
    )

    color_bar_left = (
        alt.Chart(source_df[source_df["x2"] >= norm_scale // 2])
        .mark_bar(
            cornerRadiusTopRight=5,
            cornerRadiusBottomRight=5,
            height=30,
            color="#E2BEFF",
        )
        .encode(
            x=alt.X("x").title(None).axis(None),
            x2=alt.X2("x2"),
            y=alt.Y("index").title(None).axis(None),
            color=alt.Color("color", scale=None),
        )
    )

    color_bar_right = (
        alt.Chart(source_df[source_df["x2"] <= norm_scale // 2])
        .mark_bar(
            cornerRadiusTopLeft=5, cornerRadiusBottomLeft=5, height=30, color="#E2BEFF"
        )
        .encode(
            x=alt.X("x").title(None).axis(None),
            x2=alt.X2("x2"),
            y=alt.Y("index").title(None).axis(None),
            color=alt.Color("color", scale=None),
        )
    )

    goal_relational_study_time = (
        (color_bar_left + color_bar_right)
        .configure_axis(grid=False, domain=False)
        .configure_view(stroke=None)
        .properties(
            width=300 * 2,  # Set the width of the chart
            height=450,  # Set the height of the chart
        )
    )

    goal_relational_study_time.save(f"images/goal_relational_study_time.png", scale_factor=1)
    make_color_transparent(
        f"images/goal_relational_study_time.png", f"images/goal_relational_study_time.png", "#FFFFFF"
    )

    generate_goal_relational_study_time_text(target, name)


def generate_goal_relational_study_time_text(target, name):
    max_boa = np.max(abs(target))
    axis_max_boa = ((((max_boa // 60) + 1) // 5) + 1) * 5  # 5분단위라

    source = pd.DataFrame(
        {
            "x": [0],
            "y": [0],
            "value_text": [str(int(axis_max_boa // 2)) + "분"],
            "color": ["#9697A4"],
        }
    )

    value_text = (
        alt.Chart(source)
        .mark_text(
            fontSize=70,
        )
        .encode(
            x=alt.X("x", axis=None),
            y=alt.Y("y", axis=None),
            text=alt.Text("value_text"),
            color=alt.Color("color", scale=None),
        )
    )
    chart = value_text
    chart = chart.configure_view(stroke="transparent")
    chart.save(f"images/goal_relational_study_time_text_middle.png", scale_factor=1)
    make_color_transparent(
        f"images/goal_relational_study_time_text_middle.png",
        f"images/goal_relational_study_time_text_middle.png",
        "#FFFFFF",
    )

    source = pd.DataFrame(
        {
            "x": [0],
            "y": [0],
            "value_text": [str(int(axis_max_boa)) + "분"],
            "color": ["#9697A4"],
        }
    )

    value_text = (
        alt.Chart(source)
        .mark_text(
            fontSize=70,
        )
        .encode(
            x=alt.X("x", axis=None),
            y=alt.Y("y", axis=None),
            text=alt.Text("value_text"),
            color=alt.Color("color", scale=None),
        )
    )
    chart = value_text
    chart = chart.configure_view(stroke="transparent")
    chart.save(f"images/goal_relational_study_time_text_max.png", scale_factor=1)
    make_color_transparent(
        f"images/goal_relational_study_time_text_max.png", f"images/goal_relational_study_time_text_max.png", "#FFFFFF"
    )


def generate_평균study_time(hour, minute, name):
    total_time = 6 * 60  # 임의로 6시간으로 정함
    current_time = hour * 60 + minute
    values = [current_time, total_time]
    colors = ["#9494FF", "#EFEFFA"]

    wedgeprops = {"width": 0.3, "edgecolor": "w", "lw": 3}
    plt.pie(
        values, startangle=90, counterclock=False, colors=colors, wedgeprops=wedgeprops
    )
    plt.savefig(f"images/study_time.png")
    make_color_transparent(f"images/study_time.png", f"images/study_time.png", "#FFFFFF")
