import yt_dlp

def download_video(url: str):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'mp4[ext=mp4][vcodec!=none][acodec!=none]/best',  
        # prend un flux déjà muxé si dispo
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    download_video("https://www.youtube.com/watch?v=vRZkgpJYSq0")