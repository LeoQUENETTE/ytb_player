import os
import yt_dlp, json, requests

ytb_API_URL = "https://www.googleapis.com/youtube/v3/"

class Audio:
    def __init__(self,title : str, duration : str, channel_title : str, url : str):
        self.title : str = title
        self.channel_title : str = channel_title
        self.duration : str = duration
        self.url : str = url

def download_audio(url: str):
    '''
    Procedure allowing to download a audio based on it's URL using the ydl_opts library
    Takes a url as an input and return nothing
    '''
    ydl_opts = {
        'format': 'bestaudio/best', 
        'outtmpl': 'audio/%(title)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def search_video(query : str):
    '''
    Function allowing to return a list of title, url and image for a given search input
    The function takes a search input as a string as input
    Returns a list of string corresponding to the url and title
    '''
    api_key = os.getenv("API_KEY")
    part = "snippet"
    type="video"
    request_text = f'{ytb_API_URL}search?key={api_key}&part={part}&type={type}&q={query}'
    response = requests.get(request_text)
    if response.status_code >= 300:
        raise Exception(f"ERROR : Status code {response.status_code}")
    
    audio_list = eval(response.text)
    audio_object_list = []
    for audio in audio_list["items"]:
        audio_info_supp_dict = info_video(audio["id"]["videoId"])
        duration = audio_info_supp_dict["items"][0]["contentDetails"]["duration"]
        new_audio = Audio(
            title=audio["snippet"]["title"],
            duration=duration,
            channel_title=audio["snippet"]["channelTitle"],
            url="https://www.youtube.com/watch?"+"v=" + audio["id"]["videoId"]+"&abChannel="+ audio["snippet"]["channelTitle"] 
        )
        audio_object_list.append(new_audio.__dict__)
    return {"data": audio_object_list}
        
def info_video(audio_id : str):
    '''
    
    '''
    api_key = os.getenv("API_KEY")
    part = "snippet,contentDetails,statistics"
    request_text = f'{ytb_API_URL}videos?key={api_key}&part={part}&id={audio_id}'
    response = requests.get(request_text)
    if response.status_code >= 300:
        raise Exception(f"ERROR : Status code {response.status_code}")
    return json.loads(response.text)