from typing import Dict

def get_default_index_mapping() -> Dict:
    return {
        "mappings": {
            "properties": {
                "content": {
                    "type": "text"
                },
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 1536,  # Titan 임베딩 차원
                    "method": {
                        "name": "hnsw",
                        "space_type": "l2",
                        "engine": "nmslib"
                    }
                },
                "metadata": {
                    "type": "object"
                }
            }
        }
    }