from typing import Dict
from pydantic import BaseSettings

class BedrockConfig(BaseSettings):
    model_id: str = "amazon.titan-embed-text-v1"
    
    def get_embedding_params(self) -> Dict:
        return {
            "maxTokenCount": 512,
            "truncate": "RIGHT"
        } 