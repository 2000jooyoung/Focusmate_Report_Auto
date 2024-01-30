FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir Cython==0.29.24
RUN pip3 install --no-cache-dir numpy==1.19.5
RUN pip3 install --no-cache-dir pandas==1.1.5

RUN pip3 install --no-cache-dir -r requirements.txt


# In=
COPY ./report_template ./report_template
COPY ./report_template_new ./report_template_new
COPY ./src ./src
COPY ./main.py ./main.py
COPY ./fonts ./fonts
COPY ./output ./output

CMD ["python3", "main.py"]
