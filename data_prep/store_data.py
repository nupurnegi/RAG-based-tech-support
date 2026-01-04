from config import MILVUS_TOKEN, MILVUS_URL, COLLECTION_NAME

from pymilvus import (
    connections, FieldSchema, CollectionSchema, DataType, Collection
)

from data_loader import load_ubuntu_dataset
from data_embedding import embeddings

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=2048)

]

schema = CollectionSchema(fields, description="Ubuntu RAG chatbot")

connections.connect(
  uri=MILVUS_TOKEN,
  token=MILVUS_URL
)

collection = Collection(
    name=COLLECTION_NAME,
    schema=schema
)


collection.insert([
    load_ubuntu_dataset["instruction"].tolist(),
    embeddings.tolist(),
    load_ubuntu_dataset["response"].tolist()
])