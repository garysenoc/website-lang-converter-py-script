from bs4 import BeautifulSoup
from googletrans import Translator
import os
import httpx
import time

# specify the input HTML file
input_file = "/scrap/www.classcentral.com/index.html"

# specify the output directory for the translated files
output_directory = "output/"

# create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# create a translator object with a longer timeout period
# create a translator object
translator = Translator()

# create a Timeout object with the timeout value
timeout = httpx.Timeout(timeout=10.0)


# create a translator object with the Timeout object
translator = Translator(timeout=timeout)
# read the input HTML file
with open(input_file, "rb") as f:
    html = f.read()

# parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# find all the text inside HTML tags, excluding CSS and JS code
text_tags = soup.find_all(string=True, recursive=True)
for tag in text_tags:
    if tag.parent.name in ['style', 'script', 'noscript', 'comment']:
        continue
    text = tag.strip()
    if text:
        print(text)
        translated_text = None
        while not translated_text:
            try:
                translated_text = translator.translate(text, src="en", dest="hi").text
            except:
                print(text + ' no translate')
                time.sleep(2) # wait for 2 seconds before trying again
                continue
        tag.replace_with(translated_text)

# save the translated HTML file to the output directory
output_file = os.path.join(output_directory, "output.html")
with open(output_file, "w",encoding="utf-8") as f:
    f.write(str(soup))
