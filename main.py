import yt_dlp, json, requests

ytb_API_URL = "https://www.googleapis.com/youtube/v3/"

def download_video(url: str):
    '''
    Procedure allowing to download a audio based on it's URL using the ydl_opts library
    Takes a url as an input and return nothing
    '''
    ydl_opts = {
        'format': 'bestaudio/best',   # prend le meilleur flux audio dispo
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
    f = open('secrets.json')
    secrets = json.load(f)
    api_key = secrets["API-Key"]
    part = "snippet"
    type="video"
    request_text = f'{ytb_API_URL}search?key={api_key}&part={part}&type={type}&q={query}'
    response = requests.get(request_text)
    if response.status_code >= 300:
        raise Exception(f"ERROR : Status code {response.status_code}")

    return response
        
def info_video(video_id : str):
    '''
    
    '''
    f = open('secrets.json')
    secrets = json.load(f)
    api_key = secrets["API-Key"]
    part = "snippet,contentDetails,statistics"
    request_text = f'{ytb_API_URL}videos?key={api_key}&part={part}&id={video_id}'
    response = requests.get(request_text)
    if response.status_code >= 300:
        raise Exception(f"ERROR : Status code {response.status_code}")

    return response

class Video:
    def __init__(self,title : str, duration : str, channel_title : str, url : str, video_id : str):
        self.duration : str = duration
        self.title : str = title
        self.channel_title : str = channel_title
        self.video_id : str = video_id
        self.url : str = url

if __name__ == "__main__":
    #download_video("https://www.youtube.com/watch?v=vRZkgpJYSq0")
    response = search_video("nyan cat")
    response_dict = eval(response.text)
    v_info_list = response_dict["items"]
    video_ojb_list : list[Video] = [] 
    cpt = 0
    for v_info in v_info_list:
        cpt += 1
        video_id = v_info["id"]["videoId"]
        response_info = info_video(video_id)
        info_supp = response_info.json()
        duration = info_supp["items"][0]["contentDetails"]["duration"].replace("PT", "")
        title = v_info["snippet"]["title"]
        channel_title = v_info["snippet"]["channelTitle"]
        url = f"https://www.youtube.com/watch?v={video_id}&ab_channel={channel_title}"
        new_video = Video(title, duration,channel_title,url, video_id)
        video_ojb_list.append(new_video)
        print(f'{cpt} : {title} by {channel_title} during {duration}')
    video_selected = int(input("Select a video : "))
    video : Video = video_ojb_list[video_selected - 1]
    download_video(video.url)