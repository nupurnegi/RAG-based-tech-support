from sentence_transformers import SentenceTransformer

from data_loader import load_ubuntu_dataset, preprocess_dataset

from app.config import EMBEDDING_MODEL_NAME

embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)


dataset = load_ubuntu_dataset()
questions, answers = preprocess_dataset(dataset)
print(max(len(q) for q in questions))
print(max(len(a) for a in answers))

# questions = questions

embeddings = embedder.encode(
    questions,   #embedding only the question i.e. the instruction column.
    show_progress_bar=True,
    convert_to_numpy=True
)

print("Embedding shape:", embeddings.shape)
