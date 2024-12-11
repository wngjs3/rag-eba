# RAG Project

AWS Bedrock과 OpenSearch Serverless를 활용한 RAG 시스템

## 개발 환경 설정

1. 환경 변수 설정
   - `.env.example`을 `.env`로 복사하고 필요한 값들을 설정합니다.
   - 또는 `scripts/setup_dev_env.sh`를 실행합니다.

2. 개발 환경 실행

## Docker 관리 스크립트

개발 환경 관리를 위한 편리한 스크립트들이 제공됩니다:

```bash
./scripts/docker-build.sh   # 도커 이미지 빌드
./scripts/docker-start.sh   # 개발 환경 시작
./scripts/docker-stop.sh    # 개발 환경 중지
./scripts/docker-logs.sh    # 로그 확인
./scripts/docker-shell.sh   # 컨테이너 쉘 접속
./scripts/docker-restart.sh # 개발 환경 재시작
```

처음 실행 시에는 스크립트들을 실행 가능하게 만들어야 합니다:
```bash
./scripts/make-scripts-executable.sh
```


apt-get update && apt-get install -y \
    libmagic1 \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    pandoc