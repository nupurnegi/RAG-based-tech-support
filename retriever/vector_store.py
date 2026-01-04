from langchain_community.vectorstores import Milvus
from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL_NAME, COLLECTION_NAME, MILVUS_URL, MILVUS_TOKEN

def get_vectorstore():
    embedding_fn = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )

    vectorstore = Milvus(
        embedding_function=embedding_fn,
        collection_name=COLLECTION_NAME,
        connection_args={
            "uri": MILVUS_URL,
            "token": MILVUS_TOKEN
        },
        vector_field="embedding",
        text_field="question"
    )

    return vectorstore
