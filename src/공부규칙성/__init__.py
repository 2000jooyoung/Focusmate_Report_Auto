from datetime import timedelta
import enum
from src.GenerateFromTemplate import GenerateFromTemplate
from src.공부규칙성.plot import *
from src import create_date_string, create_week

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

            if longest_range is None or (current_range[1] - current_range[0]) > (longest_range[1] - longest_range[0]):
                longest_range = current_range
            current_range = None


    if current_range is not None and (longest_range is None or (current_range[1] - current_range[0]) > (longest_range[1] - longest_range[0])):
        longest_range = current_range

    return longest_range

def generate_공부규칙성(df, name, date):
    date += timedelta(days=7)
    
    labels = {
        0 : "없음",
        1 : "낮음",
        2 : "보통",
        3 : "높음"
    }

    generate_공부규칙성1(df, name)
    규칙성 = generate_공부규칙성2(df, name)
    mapping = {'없음': 0, '낮음': 1, '보통': 2, '높음': 3}

# Convert the Korean words to integers using the mapping
    규칙성_int = [mapping[word] for word in 규칙성]
    
    gen = GenerateFromTemplate("report_template/공부규칙성.pdf")
    gen.addText(date.strftime("%Y년 %m월 %d일"),(130,791), font_size=10)
    gen.addText(name,(510,805), font_size=9)


    공부규칙성_x, 공부규칙성_y = 64, 445
    공부규칙성_step = 28
    공부규칙성_scale = 0.38
    
    weeks = create_week(df.weekday)
    
    for idx, week in enumerate(weeks):
        gen.addGraphics((공부규칙성_x + 공부규칙성_step * idx, 공부규칙성_y), f"{name}/공부규칙성_{week}.png", scale=공부규칙성_scale)
        
    gen.addGraphics((297 ,358), f"{name}/공부규칙성2.png", scale=0.14) # 토
    
    # 높은 시간대 회색 밴드 넣기

    range = find_longest_consecutive_range_of_max(규칙성_int)
    max_val = max(규칙성_int[range[0]: range[1] + 1])
    
    
    if (labels[max_val] != "없음"):
        gen.addText(f"{name}님은 공부 규칙성은 {range[0]}시에서 {range[1] + 1}시 사이에 {labels[max_val]}으로 나타납니다. 꾸준히 높은 규칙성을 유지하시면 효율적인 공부를",(20,300),
                font_size=10)
        gen.addText("하실 수 있을 것입니다.",(20,288 - 2),
                font_size=10)
    else:
        gen.addText(f"{name}님의 공부 규칙성은 없음으로 나타납니다. {name}님만의 공부 습관을 만들어보시면 더 효율적인 공부를 하실 수 있을 것입니다.",(20,300),
                font_size=10)

    for idx, week in enumerate(weeks):
        gen.addColoredText(f"{week}",(72 + 28 * idx, 435), font_size=8, color=(150, 151, 164))
        
    days = create_date_string(df["startedAt"].iloc[0])
    
    for idx, day in enumerate(days):
        gen.addColoredText(f"{day}",(66 + 28 * idx, 425), font_size=8, color=(150, 151, 164))

    gen.merge()
    gen.generate(f"output/{name}_공부규칙성.pdf")
    
    return f"output/{name}_공부규칙성.pdf"