from src import create_date_string
from src.GenerateFromTemplate import GenerateFromTemplate
from src.공부시간.plot import *
import numpy as np
from datetime import datetime, timedelta

def generate_공부시간(df, name, date):
    date += timedelta(days=7)

    generate_일별공부시간(df, name)
    generate_목표시간대비공부시간(df, name)
    
    gen = GenerateFromTemplate("report_template/공부시간.pdf")
    gen.addText(date.strftime("%Y년 %m월 %d일"),(130,791), font_size=10)
    gen.addText(name,(510,805), font_size=9)

    xs = [70, 100, 130, 161, 191, 222, 252]
    weeks = create_week(df.weekday)
    
    for x, week in zip(xs, weeks):
        gen.addGraphics((x, 467), f"{name}/일별공부시간_{week}.png", scale=0.3)

    gen.addGraphics((542, 431), f"{name}/목표시간대비공부시간_text_max.png", scale=0.1)
    gen.addGraphics((481, 431), f"{name}/목표시간대비공부시간_text_middle.png", scale=0.1)


    gen.addText("-",(323,444), font_size=6)
    gen.addText("-",(377,444), font_size=6)


    gen.addGraphics((321, 431), f"{name}/목표시간대비공부시간_text_max.png", scale=0.1)
    gen.addGraphics((373, 431), f"{name}/목표시간대비공부시간_text_middle.png", scale=0.1)
    
    df_without_zeros = df[df["time"] > 0]

    평균_주간_공부시간 = (datetime(2000, 3, 17, 0) + timedelta(seconds=np.mean(df_without_zeros.time)))
    최대_주간_공부시간 = (datetime(2000, 3, 17, 0) + timedelta(seconds=np.max(df_without_zeros.time)))
    최소_주간_공부시간 = (datetime(2000, 3, 17, 0) + timedelta(seconds=np.min(df_without_zeros.time)))
    공부_시간_변화량 = np.diff(df.time)
    
    generate_평균공부시간(평균_주간_공부시간.hour, 평균_주간_공부시간.minute, name)
    gen.addGraphics((380, 600), f"{name}/평균공부시간.png", scale=0.4)
    gen.addText("평균 공부 시간",(485,710), font_size=9)
    if 평균_주간_공부시간.hour == 0:
        gen.addText(f"{평균_주간_공부시간.minute}분",(502,690), font_size=10)
    else:
        gen.addText(f"{평균_주간_공부시간.hour}시간 {평균_주간_공부시간.minute}분",(485,690), font_size=10)
    
    
    gen.addText(f"{name}님의 주간 평균 공부 시간은 {str(평균_주간_공부시간.hour) + '시간' if 평균_주간_공부시간.hour != 0 else ''} {평균_주간_공부시간.minute} 분입니다. 최단 시간은 {str(최소_주간_공부시간.hour) + '시간' if 최소_주간_공부시간.hour != 0 else ''}",(20,330), font_size=9)
    gen.addText(f"{최소_주간_공부시간.minute}분이었으며, 최장 공부시 시간은 {str(최대_주간_공부시간.hour) + '시간' if 최대_주간_공부시간.hour != 0 else ''} {최대_주간_공부시간.minute}분이었습니다.",(20,318), font_size=9)

    gen.addText(f"{name}님의 목표 시간 대비 공부 시간은 평균적으로 {abs(round(np.mean(df_without_zeros.goalProportion) / 60))}분 {'많았' if np.mean(df_without_zeros.goalProportion) > 0 else '적었'}습니다.",(305,330), font_size=9)
    gen.addText(f"최저 시간 기록일에는 목표 대비 {abs(round(np.min(df_without_zeros.goalProportion) / 60))}분 적었으며, 최고 기록일에는",(305,318), font_size=9)
    gen.addText(f"목표 대비 {abs(round(np.min(df_without_zeros.goalProportion) / 60))}분 많았습니다. 전반적으로 목표치보다 {abs(round(np.mean(df_without_zeros.goalProportion) / 60))}분만큼,",(305,306), font_size=9)
    gen.addText(f"목표 시간을 {'줄이시' if np.mean(df_without_zeros.goalProportion) < 0  else '늘리시'}는 것이 공부에 도움이 될 수 있습니다.",(305,294), font_size=9)

    gen.addText(f"{name}님의 공부 시간의 평균 변화량은 {round(np.mean(공부_시간_변화량))}분으로, {'증가' if np.mean(공부_시간_변화량) else '감소'}하는 양상을 보였습",(20,230), font_size=9)
    gen.addText("니다.",(20,218), font_size=9)

    gen.addText(f"7일 중 목표한 공부 시간을 달성한 날은 {(df.goalProportion > 0).sum()}일이었으며, 달성하지 못한 날은",(305,230), font_size=9)
    gen.addText(f"{7 - (df.goalProportion > 0).sum()}일 입니다. ",(305,218), font_size=9)


    gen.addGraphics((342, 420), f"{name}/목표시간대비공부시간.png", scale=0.33) # 칸당 15y

    gen.addGraphics((12, 540), f"{name}/일별공부시간_text_1.png", scale=0.12)
    gen.addGraphics((12, 540 - 25), f"{name}/일별공부시간_text_2.png", scale=0.12)
    gen.addGraphics((12, 540 - 46), f"{name}/일별공부시간_text_3.png", scale=0.12)
    gen.addGraphics((12, 540 - 69), f"{name}/일별공부시간_text_4.png", scale=0.12)
    
    
    for idx, week in enumerate(weeks):
        gen.addColoredText(f"{week}",(324,552 - 15 * idx), font_size=8, color=(150, 151, 164))

    for idx, week in enumerate(weeks):
        gen.addColoredText(f"{week}",(75 + 30.5 * idx, 455), font_size=8, color=(150, 151, 164))
    
    days = create_date_string(df["startedAt"].iloc[0])
    
    for idx, day in enumerate(days):
        gen.addColoredText(f"{day}",(69 + 30.5 * idx, 445), font_size=8, color=(150, 151, 164))
    
    gen.merge()
    gen.generate(f"output/{name}_공부시간.pdf")
    return f"output/{name}_공부시간.pdf"