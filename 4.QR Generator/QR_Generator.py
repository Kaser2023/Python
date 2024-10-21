import os
import qrcode

# ----------------------------------------------------------------
# Coded by: Abdullah Alqurashi.
# ----------------------------
# Git-Hub: https://github.com/Kaser2023
# Linked-In: https://www.linkedin.com/in/abdullah-alqurashi-a3777a224/
# Date: 18.Rabi'a Alakhir. 1446 -  2024.Oct.21
# ----------------------------------------------------------------


img = qrcode.make("https://github.com/Kaser2023")
img.save("kaser-Abdullah.png", "PNG")
