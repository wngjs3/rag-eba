import os
import argparse
from src.embeddings import BedrockEmbeddings
from src.indexing import OpenSearchClient

def main():
    parser = argparse.ArgumentParser(description='벡터 유사도 검색')
    parser.add_argument('--query', required=True, help='검색할 쿼리 텍스트')
    parser.add_argument('--k', type=int, default=5, help='반환할 결과 개수')
    args = parser.parse_args()

    # 클라이언트 초기화
    endpoint = os.getenv("OPENSEARCH_ENDPOINT")
    index_name = "rag-index"

    embeddings = BedrockEmbeddings()
    client = OpenSearchClient(host=endpoint, index_name=index_name)

    # 쿼리 텍스트를 임베딩으로 변환
    query_embedding = embeddings.embed_query(args.query)

    # 유사도 검색 수행
    results = client.search_similar(query_embedding, k=args.k)

    # 결과 출력
    print(f"\n검색 쿼리: {args.query}\n")
    for i, result in enumerate(results, 1):
        print(f"결과 {i}:")
        print(f"내용: {result['content'][:200]}...")
        print(f"출처: {result['metadata']['source']}\n")

if __name__ == "__main__":
    main() 