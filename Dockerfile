FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt --timeout=10000
EXPOSE 8080
CMD ["uvicorn", "fastApp:app", "--host", "0.0.0.0", "--port", "8080"]