from python:3.9-slim
workdir /app
copy . .
run pip install fastapi uvicorn boto3 python-multipart
cmd ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]