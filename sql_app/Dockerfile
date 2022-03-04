FROM tiangolo/uvicorn-gunicorn:python3.9

RUN mkdir /sql_app

COPY requirements.txt /sql_app

WORKDIR /sql_app

RUN pip install -r requirements.txt

COPY . /sql_app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]