FROM python:3.11

WORKDIR /workspace

COPY . .

RUN pip install -r requirements.txt


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/workspace/src \
    DATA_LOCATION=/workspace/data \
    PYTHONWARNINGS="ignore:Unverified HTTPS request"