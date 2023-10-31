import os
import chromadb
# from chromadb.utils import embedding_functions
from chromadb.config import Settings
from create_vectorized_db.export_story_data_to_chroma_file import create_vectorized_db
# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import json

DATA_LOCATION = os.environ.get("DATA_LOCATION")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def query_vectorized_db(persistent_client: chromadb.PersistentClient):
    embedding_function = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-ada-002"
    )
    
    # load from disk
    teaser_db = Chroma(
        client=persistent_client,
        collection_name="story_teaser",
        embedding_function=embedding_function,
    )
    statement_db = Chroma(
        client=persistent_client,
        collection_name="story_statement",
        embedding_function=embedding_function,
    )

    print("There are", teaser_db._collection.count(), "documents in 'teaser_db'")
    print("There are", statement_db._collection.count(), "documents in 'statement_db'")
    
    # QUERY
    query = "umweltfreundliche Stromversorgung" # "Klimawandel und Insektensterben" # "Extremfrühgeburtlichkeit"

    # similarity search
    teaser_results = teaser_db.similarity_search(query)
    statement_results = statement_db.similarity_search(query)
    print("from teaser_db: ", teaser_results)
    print("---")
    print("from statement_db: ", statement_results)

    # retriever options
    # teaser_retriever = teaser_db.as_retriever(search_type="mmr")
    # statement_retriever = statement_db.as_retriever(search_type="mmr")
    # teaser_results = teaser_retriever.get_relevant_documents(query)
    # statements_results = statement_retriever.get_relevant_documents(query)
    # print("from teaser_db: ", teaser_results)
    # print("---")
    # print("from statement_db: ", statements_results)

    # filtering on metadata
    # science_response_teasers = teaser_db.get(where={"type": "Science Response"})
    """teaser_results = teaser_db.query(
        n_results=10,
        where={"type": "Rapid Reaction"},
        where_document={f'"$contains":"{query}"'}
    )
    print("science_response_teasers", teaser_results)"""


if __name__ == "__main__":
    persistent_client = chromadb.PersistentClient(
        path=f"{DATA_LOCATION}/chroma_db", 
        settings=Settings(allow_reset=True)
    ) # should be created once and passed around

    # create_vectorized_db(persistent_client) # needed only once
    query_vectorized_db(persistent_client)