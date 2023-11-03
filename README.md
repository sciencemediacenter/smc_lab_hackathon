# SMC Lab Hackathon

Dieses repo beinhaltet alle Bibliotheken, die wir für den Hackathon brauchen, sowie ein paar Beispiele.

## .env Datei

wir geben euch einen OpenAI API Key, den ihr in einer .env Datei als "OPENAI_API_KEY" speichern müsst. Diese Datei wird von docker-compose automatisch geladen.

```
OPENAI_API_KEY=...
```

## Datenbank

Die Vektordatenbank mit den SMC-Angeboten und den vorberechneten Embeddings kann [hier](https://media.sciencemediacenter.de/share/hackathon_2023/chroma_db.zip) heruntergeladen werden. Die ZIP-Datei dann einfach im Unterverzeichnis /data entpacken.

```
wget -P ./data/ https://media.sciencemediacenter.de/share/hackathon_2023/chroma_db.zip
unzip ./data/chroma_db.zip -d ./data/
# rm ./data/chroma_db.zip
```

## Benutzung

```
docker-compose build
docker-compose up
```

in VS Code "Reopen in Container" und die docker-compose.yml im repo auswählen.

## Jupyter Notebooks

Die Jupyter Notebooks sind in der src/notebooks/ folder. Diese könnt ihr

- in VS Code öffnen und benutzen (wir empfehlen die Jupyter-Extension von Microsoft zu installieren
- mit dem laufenden Container im Browser öffnen (http://localhost:8881)

## Vectorized DB (data/chroma_db/)

Diese Chroma-DB bildet die Basis für unsere Challenges. Wir haben 2 collections in der DB: "story_teaser" und "story_statement".

### Query vectorized data

#### Methoden für Suche innerhalb einer collection:

```
# collection laden
teaser_db = Chroma(
    client=persistent_client,
    collection_name="story_teaser",
    embedding_function=embedding_function,
)

# Suche nach allen Teasern von Stories mit type "Research in Context"
teaser_db.get(where={"type": "Research in Context"})
```

## SMC Lab Data Collection

Die vektorisierte DB haben wir mit unseren öffentlich verfügbaren Daten gemacht. Diese findet ihr hier: https://data.smclab.io/v1/graphql

### Request Story Data

### Hasura example query

```
query getGeneralQuery {
    smc_story_meta(
    where: {type: {\_neq: "Press Briefing"}}
    order_by: {publication_date: desc}
    limit: 10
    ) {
        story_no
        title
        type
        url
        ressort
        publication_date
        expert_statements {
            expert_affiliation
            expert_name
            statement
        }
        smc_content {
            teaser
        }
    }
}
```

### Help function in this repo (get_general_query() in src/graphql/request_gql.py)

```
story_data: List[Dict[str, Any]] = get_general_query(
    table_name="story_meta",
    schema_name="smc",
    return_nodes="""
        story_no,
        title,
        type,
        url,
        ressort,
        publication_date,
        expert_statements {
            expert_affiliation,
            expert_name,
            statement
        },
        smc_content {
            teaser
        }""",
    where_clause='type: {_neq: "Press Briefing"}',
    args_clause="order_by: {publication_date: desc} limit: 10"
    )
```
