from datetime import timedelta

from src.GenerateFromTemplate import GenerateFromTemplate
from src.brain_bti.plot import *

x, y, coef_x, coef_y, step = 20, 320, 280, -90, 12

# 초반 집중 유형

def 낮은_초반_집중_유형(gen, name):
    gen.addText(f"{name}님의 초반 집중 유형", (x, y), font_size=10)
    gen.addText("초반 10분동안의 두뇌 가동률 변화 추이는 대상이 집중함에 있어 도입부에", (x, y - step * 1), font_size=9)
    gen.addText(f"어떤 자세를 취하는지를 유추 할 수 있습니다. {name}님의 초반 두뇌 가동률 ", (x, y - step * 2), font_size=9)
    gen.addText("변화 추이는 하락을 하는 경향을 보이며, 이는 초반에는 주어진 과제를 분석", (x, y - step * 3), font_size=9)
    gen.addText("하여 적응해나가는 유형입니다.", (x, y - step * 4), font_size=9)
    
def 높은_초반_집중_유형(gen, name):
    gen.addText(f"{name}님의 초반 집중 유형", (x, y), font_size=10)
    gen.addText("초반 10분동안의 두뇌 가동률 변화 추이는 대상이 집중함에 있어 도입부에", (x, y - step * 1), font_size=9)
    gen.addText(f"어떤 자세를 취하는지를 유추 할 수 있습니다. {name}님의 초반 두뇌 가동률 ", (x, y - step * 2), font_size=9)
    gen.addText("변화 추이는 상승을 하는 경향을 보이며, 이는 초반부터 강하게 집중력을 ", (x, y - step * 3), font_size=9)
    gen.addText("끌어올리는 유형입니다.", (x, y - step * 4), font_size=9)
      
# 중반 집중 유형

def 낮은_중반_집중_유형(gen, name):
    gen.addText(f"{name}님의 중반 집중 유형", (x + coef_x, y), font_size=10)
    gen.addText("중반 10분은 실행된 시간에 관계 없이 초반 10분과 후반 10분을 제외한", (x + coef_x, y - step * 1), font_size=9)
    gen.addText("나머지 시간을 10분으로 요약해 나타냅니다. 즉, 중반 10분간의", (x + coef_x, y - step * 2), font_size=9)
    gen.addText(f"두뇌 가동률 변화 추이는 대상의 전체적인 가동률을 대변합니다. {name}님의", (x + coef_x, y - step * 3), font_size=9)
    gen.addText("중반 두뇌 가동률 변화 추이는 하락을 하는 경향을 보이며, 이는 지속성을", (x + coef_x, y - step * 4), font_size=9)
    gen.addText("위해 집중력의 강도를 조절하는 유형입니다.", (x + coef_x, y - step * 5), font_size=9)
    
def 높은_중반_집중_유형(gen, name):
    gen.addText(f"{name}님의 중반 집중 유형", (x + coef_x, y), font_size=10)
    gen.addText("중반 10분은 실행된 시간에 관계 없이 초반 10분과 후반 10분을 제외한", (x + coef_x, y - step * 1), font_size=9)
    gen.addText("나머지 시간을 10분으로 요약해 나타냅니다. 즉, 중반 10분간의", (x + coef_x, y - step * 2), font_size=9)
    gen.addText(f"두뇌 가동률 변화 추이는 대상의 전체적인 가동률을 대변합니다. {name}님의", (x + coef_x, y - step * 3), font_size=9)
    gen.addText("중반 두뇌 가동률 변화 추이는 상승을 하는 경향을 보이며, 이는 집중력의", (x + coef_x, y - step * 4), font_size=9)
    gen.addText("강도를 꾸준히 올리는 유형입니다.", (x + coef_x, y - step * 5), font_size=9)
    
# 후반 집중 유형

def 낮은_후반_집중_유형(gen, name):
    gen.addText(f"{name}님의 후반 집중 유형", (x, y + coef_y), font_size=10)
    gen.addText("후반 10분동안의 두뇌 가동률 변화 추이는 대상이 집중함에 있어 공부", (x, y + coef_y - step * 1), font_size=9)
    gen.addText(f"마무리 단계에서 어떤 자세를 취하는지를 유추 할 수 있습니다.  {name}님의 ", (x, y + coef_y - step * 2), font_size=9)
    gen.addText("후반 두뇌 가동률 변화 추이는 하락을 하는 경향을 보이며, 이는 본인의", (x, y + coef_y - step * 3), font_size=9)
    gen.addText("과제를 점검하며 되돌아보며 마무리 하는 유형입니다.", (x, y + coef_y - step * 4), font_size=9)
    
def 높은_후반_집중_유형(gen, name):
    gen.addText(f"{name}님의 후반 집중 유형", (x, y + coef_y), font_size=10)
    gen.addText("후반 10분동안의 두뇌 가동률 변화 추이는 대상이 집중함에 있어 공부", (x, y + coef_y - step * 1), font_size=9)
    gen.addText(f"마무리 단계에서 어떤 자세를 취하는지를 유추 할 수 있습니다.  {name}님의 ", (x, y + coef_y - step * 2), font_size=9)
    gen.addText("후반 두뇌 가동률 변화 추이는 상승을 하는 경향을 보이며, 이는 높은", (x, y + coef_y - step * 3), font_size=9)
    gen.addText("퍼포먼스로 집중을 마무리 하는 유형입니다.", (x, y + coef_y - step * 4), font_size=9)
    
# 두뇌 가동률 변화 유형

def 낮은_두뇌_가동률_변화_유형(gen, name):
    gen.addText(f"{name}님의 두뇌 가동률 변화량 유형", (x + coef_x, y + coef_y), font_size=10)
    gen.addText("변화량은 두뇌 가동률 변화 추이 표준 편차라고도 표현합니다. 가동률 ", (x + coef_x, y + coef_y - step * 1), font_size=9)
    gen.addText("변화량은 각각의 사용마다 일정한 가동률이 발현되었는지를 알려주는", (x + coef_x, y + coef_y - step * 2), font_size=9)
    gen.addText(f"지표입니다. {name}님의 변화량은 낮음으로, 일정한 난도의 상황에서", (x + coef_x, y + coef_y - step * 3), font_size=9)
    gen.addText("집중을 하였습니다.", (x + coef_x, y + coef_y - step * 4), font_size=9)

def 높은_두뇌_가동률_변화_유형(gen, name):
    gen.addText(f"{name}님의 두뇌 가동률 변화량 유형", (x + coef_x, y + coef_y), font_size=10)
    gen.addText("변화량은 두뇌 가동률 변화 추이 표준 편차라고도 표현합니다. 가동률 ", (x + coef_x, y + coef_y - step * 1), font_size=9)
    gen.addText("변화량은 각각의 사용마다 일정한 가동률이 발현되었는지를 알려주는", (x + coef_x, y + coef_y - step * 2), font_size=9)
    gen.addText(f"지표입니다. {name}님의 변화량은 높음으로, 다양한 난도의 상황에서", (x + coef_x, y + coef_y - step * 3), font_size=9)
    gen.addText("집중을 하였습니다.", (x + coef_x, y + coef_y - step * 4), font_size=9)


def generate_focus_type_list(df):
    data_array = get_summarized_brain_energy(df)
    meaned_data_array = np.mean(data_array, axis=0)
    focus_type = ["높음", "높음", "높음", "높음"]

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

    if slope_first < 0:
        focus_type[0] = "낮음"
    if slope_second < 0:
        focus_type[1] = "낮음"
    if slope_third < 0:
        focus_type[2] = "낮음"
    if slope_fourth < 0:
        focus_type[3] = "낮음"

    return focus_type

유형_plot_dict = [
    {
        "낮음" : 낮은_초반_집중_유형,
        "높음" : 높은_초반_집중_유형,
    },
    {
        "낮음" : 낮은_중반_집중_유형,
        "높음" : 높은_중반_집중_유형,
    },
    {
        "낮음" : 낮은_후반_집중_유형,
        "높음" : 높은_후반_집중_유형,
    },
    {
        "낮음" : 낮은_두뇌_가동률_변화_유형,
        "높음" : 높은_두뇌_가동률_변화_유형,
    },
]

def generate_focus_type(df, name, date):
    
    generate_bor_change_trend(df, name)
    gen = GenerateFromTemplate("./report_template_new/focus_type.pdf")
    gen.addText(date.strftime("%Y년 %m월 %d일"), (129, 790), font_size=9)
    gen.addText(
        (date + timedelta(days=6)).strftime(" ~ %Y년 %m월 %d일"), (200, 790), font_size=9
    )
    gen.addText(name, (510, 805), font_size=9)

    study_regularity_x, study_regularity_y = -53, 425
    study_regularity_step = 28
    study_regularity_scale = 0.29
        
    gen.addGraphics(
        (study_regularity_x + study_regularity_step * 0, study_regularity_y),
        f"images/bor_change_trend.png",
        scale=study_regularity_scale,
    )

    focus_type = generate_focus_type_list(df)

    for i, func in enumerate(유형_plot_dict):
        func[focus_type[i]](gen, name)


    gen.merge()
    gen.generate(f"output/{name}_focus_type.pdf")

    pdf_path = f"output/{name}_focus_type.pdf"

    return pdf_path