import os
from typing import Annotated
import uuid
from fastapi import FastAPI, Response, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontapp-71ja.onrender.com",
        "https://www.frontapp-71ja.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Get public photos for an album
@app.get("/fotos")
async def get_fotos_publicas():
    try:
        fotos = os.listdir(f"imagens")
        fotos = [foto.split(".")[0] for foto in fotos if foto.endswith(".jpg")]

        print(fotos)

        return {"fotos": fotos}
    except Exception as e:
        # Log the exception
        print(str(e))
        return Response(content="Erro ao buscar fotos", status_code=500)


@app.get("/{foto}")
async def get_foto_full_quality(foto: str):
    try:
        image_path = f"imagens/{foto}.jpg"
        if not os.path.exists(image_path):
            return Response(content="Foto não encontrada", status_code=404)

        return FileResponse(image_path, media_type="image/jpg")
    except Exception as e:
        # Log the exception
        print(str(e))
        return Response(content="Foto não encontrada", status_code=404)


# Create a photo for an album
@app.post("/")
async def create_foto(
    foto_file: Annotated[bytes, File()],
):
    try:
        # create unique filename
        foto = str(uuid.uuid4())
        with open(f"imagens/{foto}.jpg", "wb") as f:
            f.write(foto_file)

        return Response(content="Foto criada com sucesso", status_code=201)
    except Exception as e:
        # Log the exception
        print(str(e))
        return Response(content="Erro ao criar foto", status_code=500)
