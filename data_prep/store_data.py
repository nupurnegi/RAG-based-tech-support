import sys
import os

# Adding the parent directory to the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import MILVUS_TOKEN, MILVUS_URL, COLLECTION_NAME

from pymilvus import (
    connections, FieldSchema, CollectionSchema, DataType, Collection, utility
)

# from data_loader import load_ubuntu_dataset
from data_embedding import questions, answers
# dataset=load_ubuntu_dataset()
# dataset.head()

from data_embedding import embeddings

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=2048)

]

schema = CollectionSchema(fields, description="Ubuntu RAG chatbot")

connections.connect(
  uri=MILVUS_URL,
  token=MILVUS_TOKEN
)

if utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)

collection = Collection(
    name=COLLECTION_NAME,
    schema=schema
)

print(embeddings.shape)
print(collection.schema)


collection.insert([
    questions,
    embeddings.astype("float32").tolist(),
    answers
])

collection.flush()

print(collection.num_entities)

index_params = {
    "index_type": "HNSW",
    "metric_type": "IP",   # cosine similarity
    "params": {
        "M": 16,
        "efConstruction": 200
    }
}

collection.create_index(
    field_name="embedding",
    index_params=index_params
)

collection.load()
print("Index created")
