from datasets import load_dataset
import re
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import HF_TOKEN

def load_ubuntu_dataset():
    os.system(f"hf auth login --token {HF_TOKEN}")
    dataset = load_dataset("sedthh/ubuntu_dialogue_qa", split="train")
    return dataset

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def preprocess_dataset(dataset):
    questions = []
    answers = []

    for row in dataset:
        q = clean_text(row["INSTRUCTION"])
        a = clean_text(row["RESPONSE"])
        if q and a:
            questions.append(q)
            answers.append(a)

    return questions, answers
