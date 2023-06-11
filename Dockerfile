FROM python:slim-bullseye
LABEL authors="Paulo Miranda"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY ./src .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]