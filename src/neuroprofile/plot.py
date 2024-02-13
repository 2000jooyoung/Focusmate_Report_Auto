import re
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src import make_color_transparent
from src.create_user_df import downsample_list
from src.resize_image import resize_image
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties


def get_summarized_brain_energy_f_m_l(df):
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

    return first, middle, last


def get_summarized_brain_energy(df):
    summarized_brain_energies = []

    for i in np.array(list(df.abs_brain_energies)):
        if len(i) == 1:
            continue
        first = i[0:10]
        last = i[-10:]
        middle = i[10:-10]

        middle = downsample_list(middle)

        if last.shape[0] != 0 and middle.shape[0] != 0:
            summarized_brain_energies.append(np.concatenate([first, middle, last]))

    return np.array(summarized_brain_energies)


def get_daily_total_study_time_proportion(df):
    std = np.std(df[df["time"] > 0]["time"]) / 60

    norm = 30

    result = (std - norm) * (100 / norm)
    if result > 100:
        result = 100
    return round(50 + result / 2)


def plot_and_save_평균두뇌활동비율(df, name):
    values = [
        round(df[df["time"] > 0]["veryHighFocusMean"].mean() * 100),
        round(df[df["time"] > 0]["highFocusMean"].mean() * 100),
        round(df[df["time"] > 0]["middleFocusMean"].mean() * 100),
        round(df[df["time"] > 0]["lowFocusMean"].mean() * 100),
    ]
    values.reverse()

    colors = ["#E2BEFF", "#C084EF", "#9494FF", "#6266EA"]

    wedgeprops = {"width": 0.3, "edgecolor": "w", "lw": 3}

    fig, ax = plt.subplots(figsize=(4, 3))

    ax.pie(
        values, startangle=90, counterclock=False, colors=colors, wedgeprops=wedgeprops
    )
    plt.tight_layout()
    plt.savefig(f"images/meaned_bor_proportion.png")
    make_color_transparent(
        f"images/meaned_bor_proportion.png",
        f"images/meaned_bor_proportion.png",
        "#FFFFFF",
    )
    resize_image(
        f"images/meaned_bor_proportion.png",
        f"images/meaned_bor_proportion.png",
        (640, 480),
    )

    plt.close()

    df_without_zeros = df[df["time"] > 0]
    평균bor = np.mean([element.mean() for element in df_without_zeros.abs_brain_energies])

    if round(round(평균bor * 100)) <= 45:
        return "i"
    else:
        return "e"


def plot_and_save_daily_total_study_time(df, name):
    session_time_mean = df.session_time_mean.mean()
    
    if session_time_mean >= 30 * 60:
        return "l"
    else:
        return "s"


def plot_and_save_study_regularity(df, name):
    df["timestamp"] = pd.to_datetime(df["startedAt"])
    counts_list = [0] * 24

    for _, row in df.iterrows():
        if not pd.isna(row["timestamp"]):
            interval_index = int(
                (row["timestamp"].hour * 60 + row["timestamp"].minute) / 60
            )
            counts_list[interval_index] += 1
    custom_font_path = "fonts/Noto_Sans_KR/static/NotoSansKR-Light.ttf"

    # Define a FontProperties object with the custom font
    custom_font = FontProperties(fname=custom_font_path)

    # Update Matplotlib rcParams to use the custom font globally
    rcParams["font.family"] = custom_font.get_name()
    rcParams["font.weight"] = "light"

    fig, ax = plt.subplots(figsize=(10, 5))
    x = 1
    bars = ax.bar(range(24), counts_list, color="#686BDC")

    max_index = counts_list.index(max(counts_list))

    ax.text(
        max_index,
        max(counts_list) + 0.2,
        f"{max_index}시 ~ {max_index + x}시",
        ha="center",
        va="bottom",
        color="#686BDC",
        fontsize=12,
        fontproperties=custom_font,
    )

    plt.ylim([0, 6])
    ax.set_xticks([0, 6, 12, 18, 24])
    ax.set_yticks([0, 1, 2, 3, 4, 5, 6], ["0", "1", "2", "3", "4", "5", "5+"])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlabel("시간 (hours)", fontproperties=custom_font, fontsize=20, labelpad=10)
    ax.set_ylabel("횟수", fontproperties=custom_font, fontsize=20, labelpad=10)

    plt.tight_layout()

    plt.savefig(f"images/study_regularity.png")
    make_color_transparent(
        f"images/study_regularity.png", f"images/study_regularity.png", "#FFFFFF"
    )

    plt.close()

    if max(counts_list) <= 4:
        return "r"
    else:
        return "c"


def plot_and_save_focus_type(df, name):
    custom_font_path = "fonts/Noto_Sans_KR/static/NotoSansKR-Light.ttf"

    # Define a FontProperties object with the custom font
    custom_font = FontProperties(fname=custom_font_path)

    # Update Matplotlib rcParams to use the custom font globally
    rcParams["font.family"] = custom_font.get_name()
    rcParams["font.weight"] = "light"

    first, middle, last = get_summarized_brain_energy_f_m_l(df)
    data = np.concatenate([first, middle, last])

    x = [i / 10 + 0.1 for i in range(15)]

    first = data[:15]
    last = data[15:]

    first_slope, _ = np.polyfit(x, first, 1)
    last_slope, _ = np.polyfit(x, last, 1)

    first_y = np.array([i * first_slope for i in range(15)])
    first_x = np.array([i for i in range(15)])
    last_y = np.array([i * last_slope + first_slope * 14 for i in range(15)])
    last_x = np.array([i + 14 for i in range(15)])

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.tick_params(axis="both", which="both", length=0)
    ax.set_yticks([])

    ax.set_xticks(range(30))
    xticklabel = ["" for i in range(30)]
    xticklabel[4] = "5"
    xticklabel[9] = "10"
    xticklabel[14] = "15"
    xticklabel[19] = "20"
    xticklabel[24] = "25"
    xticklabel[29] = "30"

    ax.set_xticklabels(xticklabel)

    ax.plot(first_x, first_y, label="frfff", color="#6266EA", linewidth=6)
    ax.plot(last_x, last_y, label="fffffff", color="#C084EF", linewidth=6)
    ax.axvline(14, linestyle="dashed", color="gray")

    plt.xlabel("분 (minutes)", fontproperties=custom_font, fontsize=20, labelpad=10)
    plt.ylabel("bor 추이", fontproperties=custom_font, fontsize=20, labelpad=10)

    fig.savefig(f"images/focus_type.png")
    make_color_transparent(
        f"images/focus_type.png", f"images/focus_type.png", "#FFFFFF"
    )

    plt.close()

    if first_slope < last_slope:
        return "t"
    else:
        return "h"


def generate_neuroprofile_list(df, name):
    뇌BTI = ["l", "i", "c", "h"]

    뇌BTI[0] = plot_and_save_daily_total_study_time(df, name)
    뇌BTI[1] = plot_and_save_평균두뇌활동비율(df, name)
    뇌BTI[2] = plot_and_save_study_regularity(df, name)
    뇌BTI[3] = plot_and_save_focus_type(df, name)

    return 뇌BTI
