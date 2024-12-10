import json
import boto3
from typing import List
from langchain.embeddings.base import Embeddings

class BedrockEmbeddings(Embeddings):
    def __init__(self, model_id: str = "amazon.titan-embed-text-v2:0"):
        self.client = boto3.client('bedrock-runtime', region_name='ap-northeast-2')
        self.model_id = model_id
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """여러 텍스트의 임베딩을 생성"""
        return [self.embed_query(text) for text in texts]
    
    def embed_query(self, text: str) -> List[float]:
        """단일 텍스트의 임베딩을 생성"""
        body = json.dumps({
            "inputText": text
        })
        
        response = self.client.invoke_model(
            body=body,
            modelId=self.model_id,
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = json.loads(response.get('body').read())
        embedding = response_body.get('embedding')
        
        return embedding 