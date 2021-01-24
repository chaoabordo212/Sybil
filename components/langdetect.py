# langdetect.py
## Language detection implementation for recognizing lanugages and bulding ?metacriteria? for categorisation of input and
## source material.
from langdetect import detect
from langdetect import detect_langs

def langdet(arg1_input):
    text = arg1_input
    try:
        langdet_result = detect(text)
        return langdet_result

    except Exception as error:
        print(error)
        return "langdet_error"