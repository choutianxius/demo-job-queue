FROM python:3.11

WORKDIR /home/app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["fastapi", "run", "main.py"]

EXPOSE 8000
