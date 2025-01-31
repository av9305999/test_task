FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY requirements.txt .

RUN apt-get update -y --fix-missing && \
    apt-get upgrade -y --fix-missing && \
    pip install --upgrade pip && \
    pip install --root-user-action=ignore -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "main.py", "run_server"]