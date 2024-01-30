from src.study_time import generate_study_time
from src.study_regularity import generate_study_regularity
from src.bor import generate_bor
from src.brain_bti import generate_focus_type
from src.neuroprofile import generate_neuroprofile
from src.sub_neuroprofile import generate_neuroprofile_sub_neuroprofile

from src.create_user_df import create_user_df
from datetime import datetime
import pandas as pd
import os
from PyPDF2 import PdfReader, PdfWriter
import pytz


def tmp_create_user_df():
    return pd.read_csv("tmp.csv")


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

# os.system("ls")
print("report_template")
os.system("ls report_template")

date = datetime(2023, 12, 21)
utc_plus_9 = pytz.timezone("Asia/Tokyo")
date = utc_plus_9.localize(date)

df = create_user_df("6541eb349113bf9e08eaaab3", date)
# df = create_user_df("65819928109bf12162aa1aab", date)
# df = tmp_create_user_df()

name = "김선형"


if not os.path.exists(f"images/"):
    os.makedirs(f"images/")

input_paths = []
input_paths.append(generate_study_time(df, name, date))
input_paths.append(generate_bor(df, name, date))
input_paths.append(generate_study_regularity(df, name, date))
input_paths.append(generate_focus_type(df, name, date))
input_paths.append(generate_neuroprofile(df, name, date))
input_paths.append(generate_neuroprofile_sub_neuroprofile(df, name, date))

output_path = f"output/{name}_report.pdf"

merge_pdfs(output_path, input_paths)
