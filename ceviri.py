import cv2
import os
import pytesseract
# Used for converting images to text.
from translate import Translator
from googletrans import LANGUAGES

pytesseract.pytesseract.tesseract_cmd = r'/Users/ahmeteminguney/homebrew/Cellar/tesseract/5.3.3/bin/tesseract'
os.environ['TESSDATA_PREFIX'] = '/Users/ahmeteminguney/homebrew/Cellar/tesseract/5.3.3/share/tessdata'

# reading the image
image_path = '/Users/ahmeteminguney/Desktop/TARA.png'
image = cv2.imread(image_path)

# RGB format
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

text = pytesseract.image_to_string(image_rgb)

print("\nSupported Languages:")
for code, language in LANGUAGES.items():
    print(f"{code}: {language}")

targetLng = input("\n\n Enter the language code you want to translate to: ")

if targetLng.lower() in LANGUAGES:
    #translate library is limited to 500 characters unlike googletranslate
    #so we figured out a way to create chunks of 500 characters and combine them in the end
    chunkLimit = 500
    textChunk = [text[i:i + chunkLimit] for i in range(0, len(text), chunkLimit)]

    translatedChunks = []
    translator = Translator(to_lang=targetLng)

    for chunk in textChunk:
        translated_chunk = translator.translate(chunk)
        translatedChunks.append(translated_chunk)

    # join chunks with no space between them
    translatedText = ''.join(translatedChunks)

    # Print the translated text
    print(f"\nTranslated Text ({LANGUAGES[targetLng]}):")
    print(translatedText)

    fileOutput = 'tara1.txt'
    with open(fileOutput, 'w', encoding='utf-8') as file:
        file.write(f"Translated Text ({LANGUAGES[targetLng]}):\n{translatedText}")
else:
    print("Invalid language code. Please enter a valid language code.")