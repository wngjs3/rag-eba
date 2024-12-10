from typing import List, Dict
from unstructured.partition.auto import partition
from unstructured.documents.elements import Text, Title

class DocumentLoader:
    def __init__(self):
        pass
    
    def load_file(self, file_path: str) -> List[Dict]:
        """
        파일을 로드하고 텍스트 청크로 분할합니다.
        """
        # 파일 파싱
        elements = partition(filename=file_path)
        
        # 텍스트 추출 및 청크 생성
        chunks = []
        current_chunk = ""
        current_metadata = {"source": file_path}
        
        for element in elements:
            if isinstance(element, (Text, Title)):
                text = element.text.strip()
                if text:
                    current_chunk += f"\n{text}" if current_chunk else text
                    
                    # 청크 크기가 일정 이상이면 저장
                    if len(current_chunk) >= 1000:  # 청크 크기는 조절 가능
                        chunks.append({
                            "content": current_chunk,
                            "metadata": current_metadata.copy()
                        })
                        current_chunk = ""
        
        # 마지막 청크 처리
        if current_chunk:
            chunks.append({
                "content": current_chunk,
                "metadata": current_metadata
            })
        
        return chunks 