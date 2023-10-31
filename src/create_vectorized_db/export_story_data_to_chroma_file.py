import os
import json
import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.config import Settings
from langchain.document_loaders import TextLoader
from typing import Dict, Any

DATA_LOCATION = os.environ.get("DATA_LOCATION")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def fill_teaser_collection(
    metadata: Dict[str, Any], 
    teaser_collection: chromadb.Collection,
    text_splitter: RecursiveCharacterTextSplitter):
    story_no = metadata["story_no"]
    # load the document and split it into chunks
    teaser_loader = TextLoader(f"{DATA_LOCATION}/story_teaser/{story_no}.txt")
    teaser_document = teaser_loader.load()

    teaser_docs = text_splitter.split_documents(teaser_document)

    teaser_metadata = metadata.copy()
    del teaser_metadata["statements_metadata"]
    for i, doc in enumerate(teaser_docs):
        id = f"{story_no}_{i}_teaser"
        doc_metadata = {**doc.metadata, **teaser_metadata}
        print("filling teaser collection with story_no", story_no)
        print("    metadata: ", doc_metadata)
        # print("    page_content: ", doc.page_content)
        print("---")
        print("---")
        # load it into Chroma and export it to a file
        teaser_collection.add(ids=id, metadatas=doc_metadata, documents=doc.page_content)

def fill_statement_collection(
    metadata: Dict[str, Any], 
    statement_collection: chromadb.Collection, 
    text_splitter: RecursiveCharacterTextSplitter
):
    statements_metadata = metadata["statements_metadata"]
    
    for statement in statements_metadata:
        statement_no = statement["statement_no"]
        # load the document and split it into chunks
        statement_loader = TextLoader(f"{DATA_LOCATION}/story_statement/{statement_no}.txt")
        statement_document = statement_loader.load()

        statement_docs = text_splitter.split_documents(statement_document)

        statement_metadata = metadata.copy()
        del statement_metadata["statements_metadata"]
        statement_metadata = {**statement_metadata, **statement}
        for i, doc in enumerate(statement_docs):
            id = f"{statement_no}_{i}_statement"
            doc_metadata = {**doc.metadata, **statement_metadata, "statement_no": id}
            print("filling statement_collection with statement_no", id)
            print("    metadata: ", doc_metadata)
            # print("    page_content: ", doc.page_content)
            print("---")
            print("---")
            # load it into Chroma and export it to a file
            statement_collection.add(ids=id, metadatas=doc_metadata, documents=doc.page_content)

def create_vectorized_db(persistent_client: chromadb.PersistentClient):
    # check if chroma db already exists
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-ada-002"
    )
    teaser_collection = persistent_client.get_or_create_collection("story_teaser", embedding_function=embedding_function)
    statement_collection = persistent_client.get_or_create_collection("story_statement", embedding_function=embedding_function)

    doc_count = teaser_collection.count()
    print("There are", doc_count, "documents in 'teaser_collection'")
            
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000, # characters
        chunk_overlap  = 20,
        length_function = len,
        add_start_index = True,
        # separators=["\n\n\n\n", "\n\n", " ", ""]
    )
    # load story metadata
    with open(f"{DATA_LOCATION}/story_metadata.json", "r") as f:
        story_metadata = json.load(f)

    for metadata in story_metadata:
        print("-----")
        story_no = metadata["story_no"]
        print("processing story_no: ", story_no)
        if doc_count > 0:
            print("Chroma DB already exists")
            docs_of_story = teaser_collection.get(where={"story_no": story_no})
            # print("docs_of_story: ", docs_of_story)
            if len(docs_of_story["ids"]) > 0:
                print("Story", story_no, "is already in the DB. Skipping it.")
                continue
            else:
                print("Story", story_no, "is not in the DB. Filling it.")
                try:
                    fill_teaser_collection(metadata, teaser_collection, text_splitter)
                    fill_statement_collection(metadata, statement_collection, text_splitter)
                except Exception as e:
                    print("Error in story no: ", metadata["story_no"])
                    continue
        else:
            print("Chroma DB was empty. Filling it with story_no: ", story_no)
            try:
                fill_teaser_collection(metadata, teaser_collection, text_splitter)
                fill_statement_collection(metadata, statement_collection, text_splitter)
            except Exception as e:
                print("Error in story no: ", metadata["story_no"])
                continue

    print("---")
    print("---")
    print("Created Chroma DB")

if __name__ == "__main__":
    persistent_client = chromadb.PersistentClient(
        path=f"{DATA_LOCATION}/chroma_db", 
        settings=Settings(allow_reset=True)
    ) # should be created once and passed around
    create_vectorized_db(persistent_client=persistent_client)