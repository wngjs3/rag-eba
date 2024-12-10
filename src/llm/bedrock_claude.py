import json
import boto3
from typing import Dict, Optional

class BedrockClaude:
    def __init__(
        self, 
        model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0",
        max_tokens: int = 300,
        temperature: float = 0.1,
        top_p: float = 0.9
    ):
        self.client = boto3.client('bedrock-runtime', region_name='ap-northeast-2')
        self.model_id = model_id
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
    
    def generate(self, prompt: str, **kwargs) -> str:
        """텍스트 생성"""
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": kwargs.get('max_tokens', self.max_tokens),
            "temperature": kwargs.get('temperature', self.temperature),
            "top_p": kwargs.get('top_p', self.top_p)
        })
        
        response = self.client.invoke_model(
            body=body,
            modelId=self.model_id,
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = json.loads(response.get('body').read())
        return response_body.get('content')[0].get('text') 