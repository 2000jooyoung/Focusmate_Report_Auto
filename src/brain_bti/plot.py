import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src import make_color_transparent
from src.create_user_df import downsample_list
from src.resize_image import resize_image


def get_summarized_brain_energy(df):
    summarized_brain_energies = []

    for i in np.array(list(df.abs_brain_energies), dtype=object):
        if len(i) == 1:
            continue
        first = i[0:10]
        last = i[-10:]
        middle = i[10:-10]

        middle = downsample_list(middle)

        if last.shape[0] != 0 and middle.shape[0] != 0:
            summarized_brain_energies.append(np.concatenate([first, middle, last]))

    return np.array(summarized_brain_energies)


def generate_bor_change_trend(df, name):
    data_array = get_summarized_brain_energy(df)
    average_values = np.mean(data_array, axis=0)
    std_dev_values = np.std(data_array, axis=0)

    fig, ax = plt.subplots(figsize=(25, 8))
    ax.set_facecolor("#F6F7FF")

    plt.ylim([0, 1])
    plt.plot(average_values, label="Average", color="#6266EA", linewidth=5)

    plt.fill_between(
        range(len(average_values)),
        average_values - std_dev_values,
        average_values + std_dev_values,
        alpha=0.3,
        label="Standard Deviation",
        color="#9494FF",
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.tick_params(axis="both", which="both", length=0)  # Hide ticks

    plt.savefig(f"images/bor_change_trend.png", transparent=True)
    make_color_transparent(f"images/bor_change_trend.png", f"images/bor_change_trend.png", "#FFFFFF")
    resize_image(f"images/bor_change_trend.png", f"images/bor_change_trend.png", (2500, 800))


color_dict = {1: "#6266EA", 2: "#9494FF", 3: "#C084EF", 4: "#E2BEFF"}
text_dict = {
    1: ("R(안정형)", "D(속도형)"),
    2: ("I(변동형)", "E(유지형)"),
    3: ("A(차분형)", "L(뒷심형)"),
    4: ("S(지속형)", "V(변화형)"),
}
idx_2_text_order = {1: "폭발", 2: "유지", 3: "결정", 4: "변화"}


def get_fourth_slope(fourth):
    # std(fourth)가 0.4일 때 1, 0일 때 -1로 기준 잡았을 때.
    # 원래 0.2로 하려 했지만 0.2가 생각보다 작아서 0.4로 늘림
    slope = 5 * fourth - 1
    if slope < -1:
        slope = -1
    if slope > 1:
        slope = 1
    return slope


def build_bbti_graph(slope, number):
    value = round(50 + abs(slope) * 50)

    if slope > 0:
        value_min = 100 - value
        value_max = 100
    else:
        value_min = 0
        value_max = value

    color = color_dict[number]

    source = pd.DataFrame(
        {
            "label": ["first", "first"],
            "background": [100, 0],
            "value": [value_min, value_max],
            "value_text": [f"{value}%", f"{value}%"],
        }
    )

    background = (
        alt.Chart(source)
        .mark_bar(
            cornerRadius=7,
            color="#D9D9D9",
        )
        .encode(x=alt.X("background").axis(None), y=alt.X("label").axis(None))
    )  # properties

    value_chart = (
        alt.Chart(source)
        .mark_bar(
            cornerRadius=7,
            color=color,
        )
        .encode(
            x=alt.X("min(value):Q").axis(None),
            x2="max(value):Q",
            y=alt.X("label").axis(None),
        )
    )

    value_text = (
        alt.Chart(source)
        .mark_text(
            # 텍스트 색깔, 폰트(는 가능하면) 바꾸기
            color="#FFFFF0"
            # size
        )
        .encode(
            x=alt.X("mean(value):Q").axis(None),
            y=alt.X("label").axis(None),
            text="value_text",
        )
    )

    chart = background + value_chart + value_text
    chart = chart.configure_view(stroke="transparent")
    return chart


def build_text(slope, number):
    color = (
        [color_dict[number], "#505265", "#00000000"]
        if slope < 0
        else ["#505265", color_dict[number], "#00000000"]
    )
    source = pd.DataFrame(
        {
            "x": [0, 65, 100],
            "y": [1, 1, 1],
            "value_text": list(text_dict[number]) + [""],
            "color": color,
        }
    )

    value_text = (
        alt.Chart(source)
        .mark_text(
            color="red",
            fontSize=8,
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
    return chart


def plot_and_save_뇌BTI결과(results, name):
    for idx, result in enumerate(results):
        first_chart = build_bbti_graph(result, idx + 1)

        first_chart.save(
            f"images/{idx_2_text_order[idx+1]}.png",
            format="png",
            scale_factor=2,
            background="transparent",
        )
        make_color_transparent(
            f"images/{idx_2_text_order[idx+1]}.png",
            f"images/{idx_2_text_order[idx+1]}.png",
            "#FFFFFF",
        )

        first_text = build_text(result, idx + 1)

        first_text.save(
            f"images/{idx_2_text_order[idx+1]}_text.png",
            format="png",
            scale_factor=8,
            background="transparent",
        )
        make_color_transparent(
            f"images/{idx_2_text_order[idx+1]}_text.png",
            f"images/{idx_2_text_order[idx+1]}_text.png",
            "#FFFFFF",
        )


def generate_뇌BTI결과(df, name):
    data_array = get_summarized_brain_energy(df)
    meaned_data_array = np.mean(data_array, axis=0)
    뇌BTI = ["d", "e", "l", "v"]

    # 1. 10개 단위로 자른다.
    first = meaned_data_array[0:10]
    third = meaned_data_array[-10:]
    second = meaned_data_array[10:-10]
    fourth = np.mean(np.std(data_array, axis=0))

    x = [i / 10 + 0.1 for i in range(10)]

    # 2. 각각의 기울기를 구한다.
    slope_first, _ = np.polyfit(x, first, 1)
    slope_second, _ = np.polyfit(x, second, 1)
    slope_third, _ = np.polyfit(x, third, 1)
    slope_fourth = get_fourth_slope(fourth)

    plot_and_save_뇌BTI결과([slope_first, slope_second, slope_third, slope_fourth], name)

    if slope_first < 0:
        뇌BTI[0] = "r"
    if slope_second < 0:
        뇌BTI[1] = "i"
    if slope_third < 0:
        뇌BTI[2] = "a"
    if slope_fourth < 0:
        뇌BTI[3] = "s"

    return 뇌BTI
