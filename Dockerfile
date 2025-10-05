# =======================================================
# 🐳 Base Python
# =======================================================
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# =======================================================
# 🧩 Instala dependências e Git LFS
# =======================================================
RUN apt-get update && apt-get install -y git git-lfs && git lfs install

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =======================================================
# 📥 Copia os arquivos do projeto
# =======================================================
COPY . .

# 🔽 Puxa o modelo do Git LFS (ESSENCIAL!)
RUN git lfs pull

# =======================================================
# 🚀 Start
# =======================================================
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
