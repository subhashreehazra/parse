from google.cloud import vision
import io
import os
import sys
from pdf2image import convert_from_path
from PIL import Image
import spacy
import re
nlp = spacy.load("en_core_web_sm")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GCPCredentials/carboxy-f5fc48428989.json"

if len(sys.argv) < 2:
    raise ValueError("Image path argument is not passed")
elif len(sys.argv) > 2:
    raise ValueError("Too many arguments passed")

PDF_PATH = sys.argv[1]


def detect_text(path):
    """Detects text in the file."""
    pages = convert_from_path(path, 500) 
  
    image_counter = 1
  
    for page in pages: 
        filename = "page_"+str(image_counter)+".jpg"
        image_counter = image_counter + 1

    client = vision.ImageAnnotatorClient()
    
    with io.open(filename, 'rb') as image_file:
        content=image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    string=" "
    for text in texts:
        string=string+('\n"{}"'.format(text.description))
        
    return string

def ExtractName(extract):
    string1=extract
    list_of_words=string1.split()    
    next_word=(list_of_words[list_of_words.index("Dr."or"DR.")+1])
    doc=nlp(extract)
    for ent in doc.ents:
        if((ent.label_=="PERSON")and(next_word in ent.text)):
            print("Dr."+(ent.text))

def ExtractAddress(extract):
    string1=extract
    try:
        match = re.search(r"^Full Address : (.*?)[0-9]{6}$", string1,flags=re.MULTILINE|re.DOTALL).group(0)
    except AttributeError:
        match=''  
    print(match)     

extract=detect_text(PDF_PATH)
ExtractName(extract)
ExtractAddress(extract)
