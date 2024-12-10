import os
import argparse
from typing import List, Dict
from src.indexing import OpenSearchClient
from src.embeddings import BedrockEmbeddings
from src.loader.document_loader import DocumentLoader

def load_documents(file_path: str) -> List[Dict]:
    """문서 로드 및 청크 생성"""
    loader = DocumentLoader()
    chunks = loader.load_file(file_path)
    return chunks

def main():
    parser = argparse.ArgumentParser(description='문서 인덱싱 스크립트')
    parser.add_argument('--input', required=True, help='인덱싱할 문서 파일 경로')
    args = parser.parse_args()
    
    # 클라이언트 초기화
    endpoint = os.getenv("OPENSEARCH_ENDPOINT")
    index_name = "rag-index"
    
    embeddings = BedrockEmbeddings()
    client = OpenSearchClient(host=endpoint, index_name=index_name)
    
    # 문서 로드 및 청크 생성
    chunks = load_documents(args.input)
    
    # 각 청크에 대해 임베딩 생성
    for chunk in chunks:
        embedding = embeddings.embed_query(chunk["content"])
        chunk["embedding"] = embedding
    
    # OpenSearch에 인덱싱
    client.index_documents(chunks)

if __name__ == "__main__":
    main() 