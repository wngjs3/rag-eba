FROM python:3.12-slim

WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libmagic1 \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    pandoc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# 파이썬 패키지 설치
COPY requirements.txt .
COPY requirements.dev.txt .
RUN pip install --no-cache-dir -r requirements.txt -r requirements.dev.txt

# Jupyter 설정
EXPOSE 8888
ENV PYTHONPATH=/app
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"] 