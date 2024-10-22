from tabnanny import check
from src.study_time import generate_study_time
from src.study_regularity import generate_study_regularity
from src.bor import generate_bor
from src.brain_bti import generate_focus_type
from src.neuroprofile import generate_neuroprofile
from src.sub_neuroprofile import generate_neuroprofile_sub_neuroprofile
from src.mail_sender import send_mail

from src.create_user_df import create_user_df
from datetime import datetime
import pandas as pd
import os
from PyPDF2 import PdfReader, PdfWriter
import pytz
import numpy as np
import shutil


def tmp_create_user_df():
    return pd.read_csv("tmp.csv")


def check_if_abs_brain_energie_exists(df):
    df_without_zeros = df[df["time"] > 0]

    meaned_bor = np.mean(
        [element.mean() for element in df_without_zeros.abs_brain_energies]
    )

    return np.isnan(meaned_bor) == False


def merge_pdfs(output_path, input_paths):
    """
    Merge multiple PDF files into one.

    Parameters:
    - output_path (str): Path to save the merged PDF.
    - input_paths (list): List of paths to the input PDF files.

    Example:
    merge_pdfs("merged_output.pdf", ["file1.pdf", "file2.pdf", "file3.pdf"])
    """
    try:
        output = PdfWriter()

        for input_path in input_paths:
            with open(input_path, "rb") as input_file:
                pdf_reader = PdfReader(input_file)
                output.add_page(pdf_reader.pages[0])

        with open(output_path, "wb") as output_file:
            output.write(output_file)

    except Exception as e:
        print(f"Error: {e}")

    return output_path


def main():
    """
    메인 함수

    Date 를 기준으로 범위 안에 해당되는 모든 유저들의 리포트를 뽑아서 이메일로 전송함
    """

    # 한 유저당 한개의 DF 로 DFS 만드는 과정. 이때 DF 안에서는 이미 필요한 index 들이 다 계산이 되어있다.

    date = datetime(2024, 8, 1)
    # date = datetime(date.year, date.month, date.day)

    utc_plus_9 = pytz.timezone("Asia/Tokyo")
    date = utc_plus_9.localize(date)

    dfs = create_user_df(date)

    condition_funcs = [
        check_if_abs_brain_energie_exists,
    ]

    # 생성된 DFs 들로 리포트를 뽑는 과정
    for df in dfs:
        if not os.path.exists(f"images/"):
            os.makedirs(f"images/")
        # df 가 리포트 생성 조건에 맞는지 확인
        complished_conditions = [
            condition_func(df) for condition_func in condition_funcs
        ]

        if False in complished_conditions:
            continue
        name = df.email.dropna().iloc[0]

        # input paths 에 페이지 하나씩 추가하기. 여기서 페이지를 넣고 빼고를 관리함
        input_paths = []

        # 기본적으로 폴더의 구성이
        # 페이지 이름
        #       -> init.py
        #       -> plot.py
        # 로 구성이 되어있다.
        # plot.py 에서는 그래프라던가 혹은 다른 기타 동적 이미지들을 생성해 "images" 폴더 안에 저장하는 함수들이 작성되어있다
        # init.py 에서는 그려진 이미지들과 동적 텍스트 (날짜나 이름같은) 들의 위치를 pixel 단위로 pdf 에 위치 시키는 함수 / 코드들이 작성되어있다.

        input_paths.append(generate_study_time(df, name, date))
        input_paths.append(generate_bor(df, name, date))
        input_paths.append(generate_study_regularity(df, name, date))
        input_paths.append(generate_focus_type(df, name, date))
        input_paths.append(generate_neuroprofile(df, name, date))
        input_paths.append(generate_neuroprofile_sub_neuroprofile(df, name, date))

        output_path = f"output/{name}_report.pdf"

        # 생성된 모든 페이지를 취합해서 한개의 pdf 로 만드는 과정
        merge_pdfs(output_path, input_paths)

        shutil.rmtree("images")

    # 생성이 완료된 리포트를 이메일로 보내는 과정
    send_mail(
        subject=f"포커스메이트 {name}님 주간 리포트 결과",
        body="The message that you need to send",
        email=name,
        attachments=[output_path],
    )


if __name__ == "__main__":
    main()
