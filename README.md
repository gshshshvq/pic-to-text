# pic-to-text
Telegram bot. Turns your pic in to text.

A small but very useful program - assistant. Allows you to copy text from your screenshots or pictures.

*Input* - **image** as **file**! This was done for one purpose - if u send your pic as a photo, Telegram will compress the image, which makes text recognition difficult.
This does not happen with files. So I used the **magic** library to check the **mime** type of the received document:

```python
file = bot.get_file(message.document.file_id)
download_file = bot.download_file(file.file_path)

src = message.document.file_id

with open(src, 'wb') as f:
    f.write(download_file)
    check_format = magic.from_file(src, mime=True)
    
```
After this check, we will know exactly which file the user sent. And depending on the file type starts "reading" of picture, or error. 

*Output* - message with **text** from your **pic**.

![](https://raw.githubusercontent.com/DmitryCherneckiy/pic-to-text/main/examples/example.png)

:white_check_mark: For correct work on Windows system you need a Tesseract program. Download [here](https://digi.bib.uni-mannheim.de/tesseract/), and pytesseract, Pillow libs.

:white_check_mark: The tutorial I used to install Tesseract on my linux machine [here](https://linuxhint.com/install-tesseract-ocr-linux/).

