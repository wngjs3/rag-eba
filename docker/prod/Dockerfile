FROM python:3.9-slim

WORKDIR /app

# 프로덕션 종속성만 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY src/ src/

# 애플리케이션 실행
CMD ["python", "-m", "src"] 