import yt_dlp

url = 'https://www.youtube.com/watch?v=iTHtXgnhqfM'


ydl_opts = {
    'format': 'bestaudio/best',  
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',  
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(url)
    