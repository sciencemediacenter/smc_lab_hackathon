FROM python:3.11

WORKDIR /workspace

COPY . .

# https://stackoverflow.com/questions/61364113/dockerfile-how-to-download-a-file-using-curl-and-copy-into-the-container
# RUN wget -np -P ./data/chroma_db/ -r https://media.sciencemediacenter.de/hackathon_2023/chroma_db/
# RUN cp ./data/chroma_db/ /workspace/data/

RUN pip install -r requirements.txt


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/workspace/src \
    DATA_LOCATION=/workspace/data 