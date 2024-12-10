#!/bin/bash

# 개발 환경 설정 스크립트

# .env 파일이 없으면 예제에서 복사
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from example. Please update with your credentials."
fi

# 도커 개발 환경 실행
docker-compose -f docker-compose.dev.yml up --build 