from datetime import datetime

import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src import create_week, make_color_transparent


def generate_일별두뇌가동률(df, name):
    weeks = create_week(df.weekday)
    for i, week in enumerate(weeks):
        source = pd.DataFrame(
            {
                "data": [
                    df.iloc[i].veryHighFocus,
                    df.iloc[i].highFocus,
                    df.iloc[i].middleFocus,
                    df.iloc[i].lowFocus,
                ],
                "date": [datetime(2023, 12, 12)] * 4,
                "color": [1, 2, 3, 4],
            }
        )

        custom_colors = ["#E2BEFF", "#DCAFFF", "#9494FF", "#6266EA"]
        custom_colors.reverse()

        일별두되가동률 = (
            alt.Chart(source)
            .mark_bar(
                width=40,
                cornerRadiusTopLeft=5,
                cornerRadiusTopRight=5,
                height=20,
            )
            .encode(
                x=alt.X("date", axis=None),
                y=alt.Y("sum(data)", axis=None),
                color=alt.Color(
                    "color", scale=alt.Scale(range=custom_colors), legend=None
                ),
            )
        )

        일별두되가동률 = 일별두되가동률.configure_view(stroke="transparent")
        일별두되가동률.save(f"{name}/일별두되가동률_{week}.png", scale_factor=1)
        make_color_transparent(
            f"{name}/일별두되가동률_{week}.png", f"{name}/일별두되가동률_{week}.png", "#FFFFFF"
        )


def generate_일별두뇌가동량(df, name):
    days = []
    boas = []
    for _, value in df.iterrows():
        day = value["weekday"]
        boa = np.sum(value["abs_brain_energies"])

        days.append(day)
        boas.append(boa)

    boa_df = pd.DataFrame({"날짜": df["weekday"], "가동량": df["summed_total_boa"]})
    boa_df = boa_df.groupby("날짜").sum().reset_index()
    max_boa = np.max(boa_df["가동량"])
    axis_max_boa = (max_boa // 50 + 1) * 50
    axis_middle_boa = axis_max_boa // 2

    boa_df["plot_가동량"] = (boa_df["가동량"] / axis_max_boa) * 100
    boa_df["Day"] = pd.Categorical(
        boa_df["날짜"], categories=list(df.weekday), ordered=True
    )
    df_sorted = boa_df.copy()
    df_sorted.sort_values(
        by="Day",
        key=lambda x: x.map({day: i for i, day in enumerate(df.weekday)}),
        inplace=True,
    )

    weeks = create_week(df.weekday)
    for week, data in zip(weeks, df_sorted["plot_가동량"]):
        source = pd.DataFrame(
            {
                "label": [1, 2],
                "background": [data, 100],
                "color": ["#686BDC", "#00000000"],
            }
        )

        일별두뇌가동량 = (
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

        일별두뇌가동량 = 일별두뇌가동량.configure_view(stroke="transparent")
        일별두뇌가동량.save(f"{name}/일별두뇌가동량_{week}.png", scale_factor=1)
        make_color_transparent(
            f"{name}/일별두뇌가동량_{week}.png", f"{name}/일별두뇌가동량_{week}.png", "#FFFFFF"
        )

    generate_일별두뇌가동량_text(axis_max_boa, axis_middle_boa, name)


def generate_일별두뇌가동량_text(axis_max_boa, axis_middle_boa, name):
    source = pd.DataFrame(
        {"x": [0], "y": [0], "value_text": [axis_max_boa], "color": ["#9697A4"]}
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
    chart.save(f"{name}/일별두뇌가동량_text_max.png", scale_factor=1)
    make_color_transparent(
        f"{name}/일별두뇌가동량_text_max.png", f"{name}/일별두뇌가동량_text_max.png", "#FFFFFF"
    )

    source = pd.DataFrame(
        {"x": [0], "y": [0], "value_text": [axis_middle_boa], "color": ["#9697A4"]}
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
    chart.save(f"{name}/일별두뇌가동량_text_middle.png", scale_factor=1)
    make_color_transparent(
        f"{name}/일별두뇌가동량_text_middle.png", f"{name}/일별두뇌가동량_text_middle.png", "#FFFFFF"
    )


def generate_평균두뇌활동비율(df, name):
    round(df[df["time"] > 0]["veryHighFocusMean"].mean() * 100)

    values = [
        round(df[df["time"] > 0]["veryHighFocusMean"].mean() * 100),
        round(df[df["time"] > 0]["highFocusMean"].mean() * 100),
        round(df[df["time"] > 0]["middleFocusMean"].mean() * 100),
        round(df[df["time"] > 0]["lowFocusMean"].mean() * 100),
    ]
    values.reverse()

    colors = ["#E2BEFF", "#C084EF", "#9494FF", "#6266EA"]

    wedgeprops = {"width": 0.3, "edgecolor": "w", "lw": 3}
    plt.pie(
        values, startangle=90, counterclock=False, colors=colors, wedgeprops=wedgeprops
    )
    plt.savefig(f"{name}/평균두뇌활동비율.png")
    make_color_transparent(f"{name}/평균두뇌활동비율.png", f"{name}/평균두뇌활동비율.png", "#FFFFFF")
