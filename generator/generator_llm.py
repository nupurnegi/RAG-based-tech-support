from ibm_watsonx_ai.foundation_models import Model

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import PROJECT_ID, WATSONX_CREDENTIALS, WATSONX_MODEL_ID

def load_llm():
    return Model(
        model_id=WATSONX_MODEL_ID,
        credentials=WATSONX_CREDENTIALS,
        project_id=PROJECT_ID,
        params={
            "temperature": 0.2,
            "max_new_tokens": 50
        }
    )
