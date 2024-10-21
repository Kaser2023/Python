from pytubefix import YouTube
from pytubefix.cli import on_progress
 
url = "https://www.youtube.com/watch?v=TNAu6DvB9Ng"
 
yt = YouTube(url, on_progress_callback = on_progress)
print(yt.title)

ys = yt.streams.get_lowest_resolution()

ys.download()

