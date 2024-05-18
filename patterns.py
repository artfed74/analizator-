keywords = ["машинист поезда", "слушаю вас", "ДНЦ", "понятно", "машинист", "верно"]
unwanted_words = ["здравствуйте", "спасибо", "пожалуйста", "хорошо"]

def check_keywords_presence(text, keywords, unwanted_words):
    text_lower = text.lower()
    missing_keywords = []
    found_unwanted_words = []

    for keyword in keywords:
        if keyword.lower() not in text_lower:
            missing_keywords.append(keyword)

    for unwanted_word in unwanted_words:
        if unwanted_word.lower() in text_lower:
            found_unwanted_words.append(unwanted_word)

    return missing_keywords, found_unwanted_words

import re

pattern = r"^Машинист поезда [0-9]+ .+ Слушаю Вас, машинист поезда №[0-9]+ .+ ДНЦ .+ Понятно, .+ Верно|Верно выполняйте$"

def check_text_structure(text, pattern):
    if re.match(pattern, text, re.IGNORECASE):
        return True
    else:
        return False
