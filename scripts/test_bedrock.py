import os
from src.llm.bedrock_claude import BedrockClaude
from src.embeddings import BedrockEmbeddings

def test_embedding():
    """임베딩 테스트"""
    print("\n=== 임베딩 테스트 ===")
    embeddings = BedrockEmbeddings()
    text = "이것은 테스트 텍스트입니다."
    
    try:
        embedding = embeddings.embed_query(text)
        print(f"성공: 임베딩 차원 = {len(embedding)}")
    except Exception as e:
        print(f"실패: {str(e)}")

def test_claude():
    """Claude 생성 테스트"""
    print("\n=== Claude 테스트 ===")
    claude = BedrockClaude()
    prompt = "블랙홀을 8살짜리 꼬마에게 설명하듯이 알려줘"
    
    try:
        response = claude.generate(prompt)
        print(f"성공: Claude의 응답:\n{response}")
    except Exception as e:
        print(f"실패: {str(e)}")

if __name__ == "__main__":
    # 임베딩 테스트
    test_embedding()
    
    # Claude 테스트
    test_claude() 