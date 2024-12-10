import os
from src.indexing import OpenSearchClient
from config.opensearch_config import get_default_index_mapping

def main():
    """OpenSearch 인덱스를 생성하는 스크립트"""
    endpoint = os.getenv("OPENSEARCH_ENDPOINT")
    index_name = "rag-index"
    
    client = OpenSearchClient(host=endpoint, index_name=index_name)
    mapping = get_default_index_mapping()
    
    client.create_index(mapping)

if __name__ == "__main__":
    main() 