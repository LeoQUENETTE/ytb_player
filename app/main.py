import os, uvicorn

from pydantic import BaseModel
from app.bdd_communication import SupabaseDB
from app.download import search_video, download_audio
from fastapi import FastAPI, Depends, HTTPException
        
        
app = FastAPI(title="My Supabase API", version="1.0")
supabase : SupabaseDB = None

class AudioPayload(BaseModel):
    token: str
    audio_id: str
    title: str
    channel_name: str
    url: str
    duration: str
    
@app.head("/")
def uptime_robot():
    return{"Success" : "200"}

@app.get("/")
def root():
    return{"messages", "TEST EN COURS"}

@app.get("/auth")
def auth(email, password):
    supabase = SupabaseDB()
    success, access_token, refresh_token = supabase.auth_password(email,password)
    if (success and access_token is not None and refresh_token is not None):
        return{"Authentification" : "Success", "AcessToken" : access_token, "RefreshToken" : refresh_token}   
    return{"Authentification", "Failure"}

@app.get("/playlist/getAll")
def playlistGetAll(token : str):
    supabase = SupabaseDB()
    supabase.auth_refresh_token(token)
    return supabase.getAllPlaylist()

@app.get("/playlist/get")
def playlistGetOne(token : str, playlist_name : str):
    supabase = SupabaseDB()
    supabase.auth_refresh_token(token)
    return supabase.getPlaylist(playlist_name)

@app.get("/playlist/delete")
def playlistDelete(token : str,playlist_name : str):
    supabase = SupabaseDB()
    supabase.auth_refresh_token(token)
    return supabase.deletePlaylist(playlist_name)

@app.get("/playlist/deleteAllPlaylist")
def playlistDeleteAll(token : str):
    supabase = SupabaseDB()
    supabase.auth_refresh_token(token)
    return supabase.deleteAllPlaylist()

@app.get("/search")
def searchAudio(token : str,name : str):
    supabase = SupabaseDB()
    supabase.auth_refresh_token(token)
    return search_video(name)

@app.post("/audio/add")
def addAudio(payload: AudioPayload):
    supabase = SupabaseDB()
    supabase.auth_refresh_token(payload.token)
    download_audio(payload.url)
    res, success = supabase.addAudio(payload.title, payload.channel_name, payload.audio_id, payload.url, payload.duration)
    local_path = f"audio/{payload.title}.webm"
    if success and os.path.exists(local_path):
        os.remove(local_path)
        return res
    else:
        return {"error" : res}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)