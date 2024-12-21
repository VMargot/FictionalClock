# Étape 1 : Utiliser une image Python comme base
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./requirements.txt
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
