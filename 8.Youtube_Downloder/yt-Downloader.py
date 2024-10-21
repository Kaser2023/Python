from pytubefix import YouTube
from pytubefix.cli import on_progress


# ----------------------------------------------------------------
# Coded by: Abdullah Alqurashi.
# ----------------------------
# Git-Hub: https://github.com/Kaser2023
# Linked-In: https://www.linkedin.com/in/abdullah-alqurashi-a3777a224/
# Date: 18.Rabi'a Alakhir. 1446 -  2024.Oct.21
# ----------------------------------------------------------------


url = "https://www.youtube.com/watch?v=TNAu6DvB9Ng"
 
yt = YouTube(url, on_progress_callback = on_progress)
print(yt.title)

ys = yt.streams.get_lowest_resolution()

ys.download()

