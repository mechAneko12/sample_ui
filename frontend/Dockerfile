FROM python:3.9

RUN mkdir /frontend

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev

COPY requirements.txt /frontend

WORKDIR /frontend

RUN pip install -r requirements.txt

COPY . /frontend

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port", "8501"]