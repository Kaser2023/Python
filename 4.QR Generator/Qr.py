import os
import qrcode

img = qrcode.make("https://maps.app.goo.gl/yJtGP3TfGb3u3AQf9")
img.save("aylin.png", "PNG")
