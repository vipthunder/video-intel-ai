# from langchain_chroma import Chroma
# from src.embedding import embeddings




# def create_vector_store(chunks, video_name):

#     metadatas = [
#         {"video_name": video_name}
#         for _ in chunks                              
        
# ####Chroma only allows collection names that:

# # Are 3–512 characters long
# # Contain only:
# # a-z
# # A-Z                                            this code is not fully correct like i am not convert  alphnumeric to alphbets or text
# # 0-9
# # .
# # _
# # -
# # Must start and end with an alphanumeric character

# # Your filename contains invalid characters:
#     ]

#     vector_store = Chroma.from_texts(
#         texts=chunks,
#         embedding=embeddings,
#         persist_directory="chroma_db",
#         collection_name=video_name,
#         metadatas=metadatas
#     )

#     return vector_store



# --- -------------------------------------

# this method will handle the special characters in the video name and create a valid collection name for chroma

from langchain_chroma import Chroma
from src.embedding import embeddings
import uuid


COLLECTION_NAME = "video_knowledge_base"


def create_vector_store(chunks, video_name):
    """
    Add video transcript chunks to ChromaDB.

    Args:
        chunks (list[str]): Text chunks from transcript.
        video_name (str): Original video filename/title.

    Returns:
        Chroma: Chroma vector store instance.
    """

    # Metadata for each chunk
    metadatas = [
        {
            "video_name": video_name
        }
        for _ in chunks
    ]

    # Unique IDs for each chunk
    ids = [str(uuid.uuid4()) for _ in chunks]

    # Load/Create collection
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory="chroma_db"
    )

    # Add chunks to collection
    vector_store.add_texts(
        texts=chunks,
        metadatas=metadatas,
        ids=ids
    )

    return vector_store