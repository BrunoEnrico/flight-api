# =======================================================
# 🐳 Base Python
# =======================================================
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y git git-lfs curl && git lfs install

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 🔽 Baixa o arquivo de modelo direto do GitHub (via LFS)
RUN curl -L -o voos_pipeline_minimal.joblib \
  https://github.com/BrunoEnrico/flight-api/raw/main/voos_pipeline_minimal.joblib

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
