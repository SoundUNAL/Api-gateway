from fastapi import APIRouter, HTTPException, File, UploadFile
import requests
from server import url, audioManegement_port

song_img = APIRouter()

""" Cambiar datos de una canción (Uso exclusivo para agregar la imagen a una canción
    para cambiar otros datos ya se tiene establecida la petición con graphql) """
@song_img.put("/upload_image/{song_id}")
async def upload_image(song_id: int, image: UploadFile = File(...)):

    api_url = f'http://{url}:{audioManegement_port}/songs/{song_id}'

    files = {"image": (image.filename, image.file)}

    try:
        # Petición a la api de audio manegement
        response = requests.put(api_url, files=files)
        
        response.raise_for_status()
        return {"message": "Image uploaded successfully"}
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")