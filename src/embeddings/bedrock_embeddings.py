import json
import boto3
from typing import List
from langchain.embeddings.base import Embeddings
from langchain.embeddings import BedrockEmbeddings
from utils import bedrock, print_ww
from utils.bedrock import bedrock_info

llm_emb = BedrockEmbeddings(
    client=boto3_bedrock,
    model_id=bedrock_info.get_model_id(
        model_name="Titan-Text-Embeddings-V2"
    )
)
dimension = 1024
llm_emb

# class BedrockEmbeddings(Embeddings):
#     def __init__(self, model_id: str = "amazon.titan-embed-text-v2:0"):
#         self.client = boto3.client('bedrock-runtime', region_name='ap-northeast-2')
#         self.model_id = model_id
    
#     def embed_documents(self, texts: List[str]) -> List[List[float]]:
#         """여러 텍스트의 임베딩을 생성"""
#         return [self.embed_query(text) for text in texts]
    
#     def embed_query(self, text: str) -> List[float]:
#         """단일 텍스트의 임베딩을 생성"""
#         body = json.dumps({
#             "inputText": text
#         })
        
#         response = self.client.invoke_model(
#             body=body,
#             modelId=self.model_id,
#             accept='application/json',
#             contentType='application/json'
#         )
        
#         response_body = json.loads(response.get('body').read())
#         embedding = response_body.get('embedding')
        
#         return embedding 