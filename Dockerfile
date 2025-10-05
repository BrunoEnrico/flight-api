# =======================================================
# 🐳 Base Python
# =======================================================
FROM python:3.10-slim

# Evita buffering de logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# =======================================================
# 🧩 Instala dependências do sistema e Git LFS
# =======================================================
RUN apt-get update && apt-get install -y git git-lfs && git lfs install

# Copia requirements e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =======================================================
# 🚀 Copia o app e inicializa
# =======================================================
COPY . .

# Exponha a porta padrão do Uvicorn
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
