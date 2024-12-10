import boto3
import requests
from requests_aws4auth import AWS4Auth
from typing import Dict, List
import json

class OpenSearchClient:
    def __init__(self, host: str, index_name: str):
        self.host = host
        self.index_name = index_name
        self.region = "ap-northeast-2"
        self.service = "aoss"
        self.auth = self._get_aws_auth()
        self.headers = {"Content-Type": "application/json"}

    def _get_aws_auth(self) -> AWS4Auth:
        """AWS 인증 객체 생성"""
        credentials = boto3.Session().get_credentials()
        return AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.service,
            session_token=credentials.token
        )

    def create_index(self, mapping: Dict):
        """인덱스 생성"""
        url = f"{self.host}/{self.index_name}"
        response = requests.put(
            url,
            auth=self.auth,
            headers=self.headers,
            json=mapping
        )
        return response.json()

    def index_documents(self, documents: List[Dict]):
        """문서 인덱싱"""
        url = f"{self.host}/{self.index_name}/_doc"
        
        for doc in documents:
            response = requests.post(
                url,
                auth=self.auth,
                headers=self.headers,
                json=doc
            )
            if response.status_code not in (200, 201):
                raise Exception(f"인덱싱 실패: {response.json()}")

    def search_similar(self, query_vector: List[float], k: int = 5) -> List[Dict]:
        """벡터 유사도 검색"""
        url = f"{self.host}/{self.index_name}/_search"
        
        query = {
            "size": k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_vector,
                        "k": k
                    }
                }
            }
        }

        response = requests.post(
            url,
            auth=self.auth,
            headers=self.headers,
            json=query
        )

        if response.status_code != 200:
            raise Exception(f"검색 실패: {response.json()}")

        results = response.json()
        return [hit["_source"] for hit in results["hits"]["hits"]]