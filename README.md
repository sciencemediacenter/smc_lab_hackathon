# SMC Lab Hackathon | Generative KI im Wissenschaftsjournalismus

Dieses repo beinhaltet alle Bibliotheken, die wir für den Hackathon brauchen, sowie ein paar Beispiele.

## 1. .env Datei

Wir geben euch einen OpenAI API Key, den ihr in einer .env Datei als "OPENAI_API_KEY" speichern müsst. Diese Datei wird von docker-compose automatisch geladen.

```
OPENAI_API_KEY=...
```

## 2. Datenbank

Die Vektordatenbank mit den SMC-Angeboten und den vorberechneten Embeddings kann [hier](https://media.sciencemediacenter.de/share/hackathon_2023/chroma_db.zip) heruntergeladen werden. Die ZIP-Datei dann einfach im Unterverzeichnis /data entpacken.

```
wget -P ./data/ https://media.sciencemediacenter.de/share/hackathon_2023/chroma_db.zip
unzip ./data/chroma_db.zip -d ./data/
# rm ./data/chroma_db.zip
```

## 3. Container-Bau

Es gibt zwei Möglichkeiten, den Container zu bauen und zu starten:

### 3.1 Im Terminal diese Kommandos ausführen:

```
docker-compose build
docker-compose up
```

### 3.2 Oder in VS Code:

in VS Code "Reopen in Container" und die docker-compose.yml im repo auswählen.

## Jupyter Notebooks

Wir haben Jupyter Notebooks mit Beispielen vorbereitet. Ihr könnt diese als Grundlage für eure Lösungen nehmen. Die Jupyter Notebooks sind im notebooks/ Ordner. Diese könnt ihr

- in VS Code öffnen und benutzen (wir empfehlen die Jupyter-Extension von Microsoft zu installieren)
- mit dem laufenden Container im Browser öffnen (http://localhost:8888)

## SMC-Blog

Das SMC Lab hat ein eigenes Blog. Unter [diesem Link](https://blog.smclab.io/category/masterclass-medien-triennale-sudwest-2023/) findet ihr Hintergründe zu großen Sprachmodellen.
