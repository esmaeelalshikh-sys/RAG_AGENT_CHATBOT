def detect_language(text: str) -> str:
    # Arabic Unicode range
    arabic_chars = sum(1 for ch in text if '\u0600' <= ch <= '\u06FF')
    ratio = arabic_chars / len(text)

    if ratio > 0.3:
        return "ar"
    else:
        return "en"
