import strawberry
import typing
from typing import Optional
import requests
from server import url, audioManegement_port

api_url = f'http://{url}:{audioManegement_port}/songs'

@strawberry.type
class Song:
    id: int
    title: str
    publicationDate: str
    lyrics: str
    version: int
    userid: int
    audioid: int
    albumid: int
    image_url: str
    
# Queries
@strawberry.type
class Query:
    # Get song by id
    @strawberry.field    
    def song(self, id: int) -> Song:
        
        # Hacer request en soUNd_AudioManegement_MS
        response = requests.get(f'{api_url}/{id}')
        
        if response.status_code == 200:
            # Devolver los datos obtenidos en formato JSON
            data = response.json()
            
            return Song(
                        id = data.get('id'),
                        title = data.get('title'),
                        publicationDate = data.get('publicationDate'),
                        lyrics = data.get('lyrics'),
                        version = data.get('version'),
                        userid = data.get('userid'),
                        audioid = data.get('audioid'),
                        albumid = data.get('albumid'),
                        image_url = data.get('image_url')
                    )
        else:
            raise Exception(f'Error al obtener la canción con ID {id} desde el microservicio Audio Manegement\nError: {response.status_code}, {response.text}')
        
    # Get all songs
    @strawberry.field    
    def songs(self) -> typing.List[Song]:
        
        # Hacer request en soUNd_AudioManegement_MS
        response = requests.get(api_url)
        
        if response.status_code == 200:
            # Devolver los datos obtenidos en formato JSON
            data = response.json()
            
            return [
                Song(
                    id = song_data.get('id'),
                    title = song_data.get('title'),
                    publicationDate = song_data.get('publicationDate'),
                    lyrics = song_data.get('lyrics'),
                    version = song_data.get('version'),
                    userid = song_data.get('userid'),
                    audioid = song_data.get('audioid'),
                    albumid = song_data.get('albumid'),
                    image_url = song_data.get('image_url')
                )
                for song_data in data
            ]
        else:
            raise Exception(f'Error al obtener las canciones desde el microservicio Audio Manegement\nError: {response.status_code}, {response.text}')
    
# Mutations
@strawberry.type
class Mutation:
    # post song
    @strawberry.mutation
    def create_song(self, title: str, publication_date: str, lyrics: str, version: int, userid: int, audioid: int, albumid: int) -> str:
        
        data = {
            'title': title,
            'publicationDate': publication_date,
            'lyrics': lyrics,
            'version': version,
            'userid': userid,
            'audioid': audioid,
            'albumid': albumid
        }
        
        # Hacer request en soUNd_AudioManegement_MS
        response = requests.post(api_url, json=data)
        
        if response.status_code == 201:
            return response.json()["message"]
        
        else:
            raise Exception(f'Error al crear la canción\nError: {response.status_code}, {response.text}')
    
    # put song
    @strawberry.mutation
    def update_song(self, id:int, title: Optional[str] = None, publication_date: Optional[str] = None, lyrics: Optional[str] = None, version: Optional[int] = None, userid: Optional[int] = None, audioid: Optional[int] = None, albumid: Optional[int] = None) -> Song:
        
        info = {
            'title': title,
            'publicationDate': publication_date,
            'lyrics': lyrics,
            'version': version,
            'userid': userid,
            'audioid': audioid,
            'albumid': albumid
        }
        
        info = {key: value for key, value in info.items() if value is not None}
        
        # Hacer request en soUNd_AudioManegement_MS
        response = requests.put(f'{api_url}/{id}', json=info)
        
        if response.status_code == 200:
            # Devolver los datos obtenidos en formato JSON
            data = response.json()
            
            return Song(
                        id = data.get('id'),
                        title = data.get('title'),
                        publicationDate = data.get('publicationDate'),
                        lyrics = data.get('lyrics'),
                        version = data.get('version'),
                        userid = data.get('userid'),
                        audioid = data.get('audioid'),
                        albumid = data.get('albumid'),
                        image_url = data.get('image_url')
                    )
        else:
            raise Exception(f'Error al actualizar la canción con ID {id} desde el microservicio Audio Manegement\nError: {response.status_code}, {response.text}')
            
    # delete song
    @strawberry.mutation
    def delete_song(self, id: int) -> str:
        # Hacer request en soUNd_AudioManegement_MS
        response = requests.delete(f'{api_url}/{id}')
        
        if response.status_code == 204:
            return f'Canción con id {id} eliminada exitosamente'
        
        else:
            raise Exception(f'Error al eliminar la canción con ID {id} desde el microservicio Audio Manegement\nError: {response.status_code}, {response.text}')