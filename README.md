# FastAPI + postgresql + Streamlit + PLotly + Opencv APP with Docker

## How to start
> Run below
> ```
> $ Docker-compose build
> $ Docker-compose up
> ```


## How to start without Docker
> Uncommentout below line in frontend/main.py
> ```
> backend_url = 'http://127.0.0.1:8000'
> ```
> And commentout 
> ```
> backend_url = 'http://sql_app:8000'
> ```

> Uncommentout below line in sql_app/database.py
> ```
> SQLALCHEMY_DATABASE_URL = 'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/POSTGRES_DB'
> ```
> And commentout 
> ```
> SQLALCHEMY_DATABASE_URL = 'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/POSTGRES_DB'
> ```

> Then, open two shell.
> In one shell, run below
> ```
> cd sql_app
> uvicorn main:app --reload
> ```
> in the other, 
> ```
> streamlit run .\frontend\main.py --server.port 8501
> ```