import yt_dlp
from youtube_search import YoutubeSearch

def download_video(url: str):
    '''
    Procedure allowing to download a video based on it's URL using the ydl_opts library
    Takes a url as an input and return nothing
    '''
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'mp4[ext=mp4][vcodec!=none][acodec!=none]/best',  
        # prend un flux déjà muxé si dispo
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def search_video(query : str):
    '''
    Function allowing to return a list of title, url and image for a given search input
    The function takes a search input as a string as input
    Returns a list of string corresponding to the url and title
    '''
    results = YoutubeSearch(query, max_results=10).to_dict()
    return results

if __name__ == "__main__":
    #download_video("https://www.youtube.com/watch?v=vRZkgpJYSq0")
    results = search_video("nyan cat")
    for result in results:
        url = f"https://youtube.com{result['url_suffix']}"
        title = result['title']
        print(f"{title}: {url}")
        print("")