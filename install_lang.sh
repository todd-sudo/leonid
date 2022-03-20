#!/bin/bash

sudo apt install tesseract-ocr

wget https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata
wget https://github.com/tesseract-ocr/tessdata/blob/main/rus.traineddata
wget https://github.com/tesseract-ocr/tessdata/blob/main/ukr.traineddata

sudo mv -v rus.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
sudo mv -v eng.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
sudo mv -v ukr.traineddata /usr/share/tesseract-ocr/4.00/tessdata/