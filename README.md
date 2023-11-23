<div id="header" align="center">
  <img src="https://media.sciencemediacenter.de/static/img/logos/smc/smc-logo-typo-bw-big.png" width="300"/>
  <div id="badges" style="padding-top: 20px">
    <a href="https://www.sciencemediacenter.de">
      <img src="https://img.shields.io/badge/Website-orange?style=plastic" alt="Website Science Media Center"/>
    </a>
    <a href="https://lab.sciencemediacenter.de">
      <img src="https://img.shields.io/badge/Website (SMC Lab)-grey?style=plastic" alt="Website Science Media Center Lab"/>
    </a>
    <a href="https://twitter.com/smc_germany_lab">
      <img src="https://img.shields.io/badge/Twitter-blue?style=plastic&logo=twitter&logoColor=white" alt="Twitter SMC Lab"/>
    </a>
  </div>
</div>

# SMC Lab Hackathon | Generative KI im Wissenschaftsjournalismus

Dieses repo beinhaltet alle Bibliotheken, die wir für den Hackathon brauchen, sowie ein paar Beispiele.

## 0. Voraussetzungen

- Docker: https://docs.docker.com/get-docker/
- Dieses repo lokal clonen

## 1. .env Datei

Im repo-root eine neue Datei erstellen, die ".env" heißt. Wir geben euch einen OpenAI API Key, den ihr in der .env Datei als "OPENAI_API_KEY" speichern müsst. Diese Datei wird von docker-compose automatisch geladen.

```
OPENAI_API_KEY=...
```

## 2. Container-Bau

Es gibt zwei Möglichkeiten, den Container zu bauen und zu starten:

### 2.1 Im Terminal diese Kommandos ausführen:

```
docker-compose build
docker-compose up
```

### 2.2 Oder in VS Code:

In VS Code die Docker-Extension von Microsoft installieren und ihre Option "Reopen in Container" mit der docker-compose.yml im repo auswählen.

## 3. Datenbank

Die Vektordatenbank mit den SMC-Angeboten und den vorberechneten Embeddings kann [hier](https://media.sciencemediacenter.de/share/hackathon_2023/chroma_db.zip) heruntergeladen werden. Die ZIP-Datei dann einfach im Unterverzeichnis /data entpacken. Im container folgende Kommandos ausführen:

```
wget -P ./data/ https://media.sciencemediacenter.de/share/hackathon_2023/chroma_db.zip
unzip ./data/chroma_db.zip -d ./data/
# rm ./data/chroma_db.zip
```

[Hier](https://www.jcchouinard.com/wget/) ist eine Einleitung für die Installation von wget.

## Jupyter Notebooks

Wir haben Jupyter Notebooks mit Beispielen vorbereitet. Ihr könnt diese als Grundlage für eure Lösungen nehmen. Die Jupyter Notebooks sind im notebooks/ Ordner. Diese könnt ihr

- in VS Code öffnen und benutzen (wir empfehlen die Jupyter-Extension von Microsoft zu installieren)
- mit dem laufenden Container im Browser öffnen (http://localhost:9999)

## SMC-Blog

Das SMC Lab hat ein eigenes Blog. Unter [diesem Link](https://blog.smclab.io/category/masterclass-medien-triennale-sudwest-2023/) findet ihr Hintergründe zu großen Sprachmodellen. Der Code zu den dort gezeigten Beispiel-Anwendungen befindet sich [hier](https://github.com/sciencemediacenter/lab-masterclass-medientriennale-2023).
