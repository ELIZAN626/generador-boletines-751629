from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import boto3
import uuid
import json

app = FastAPI()

# configuracion
bucket_nombre = "practica-4-751629"
cola_url = "https://sqs.us-east-1.amazonaws.com/515162739424/cola-boletines"
region = "us-east-1"

s3 = boto3.client("s3", region_name=region)
sqs = boto3.client("sqs", region_name=region)

@app.post("/boletines", status_code=201)
async def crear_boletin(
    correo: str = Form(...),
    mensaje: str = Form(...),
    archivo: UploadFile = File(...)
):
    try:
        # subimos un archivo a s3
        file_name = f"{uuid.uuid4()}-{archivo.filename}"
        s3.upload_fileobj(archivo.file, bucket_nombre, file_name)
        file_url = f"https://{bucket_nombre}.s3.amazonaws.com/{file_name}"

        # enviar mensaje a sqs
        contenido_sqs = {
            "correo": correo,
            "mensaje": mensaje,
            "url_imagen": file_url
        }
        sqs.send_message(
            QueueUrl=cola_url,
            MessageBody=json.dumps(contenido_sqs)
        )

        return {"status": "boletin enviado a cola", "s3_url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))