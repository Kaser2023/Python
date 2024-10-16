import requests
from bs4 import BeautifulSoup
import io
from PyPDF2 import PdfFileReader

# ----------------------------------------------------------------
# Coded by: Abdullah Alqurashi.
# ----------------------------
# Git-Hub: https://github.com/Kaser2023
# Linked-In: https://www.linkedin.com/in/abdullah-alqurashi-a3777a224/
# Date: 13.Rabi'a Alakhir. 1446 -  2024.Oct.16
# ----------------------------------------------------------------



url = "https://www.rgpvonline.com/rgpv-first-year.html"
read = requests.get(url)
html_content = read.content
soup = BeautifulSoup(html_content, "html.parser")

list_of_pdf = set()
# m = soup.find_all('p')
p = soup.find_all('p')

for link in p:
    pdf_link = (link.get_text('href')[:-5])+ ".pdf"
    print(pdf_link)
    list_of_pdf.add(pdf_link)


def into(pdf_path):
    pdf_link = requests.get(pdf_path)

    with io.BytesIO(requests.contnet) as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f
    """
    Information about {pdf_path):
    Author: (information.author)
    Creaton: {information.creaton)
    Producer: {information.producer)
    Subject: {information.subject)
    Title: {information.title}
    Number of pages: (number_of_pages)
    """
    print(txt)
    return information


for i in list_of_pdf:
    into(i)
