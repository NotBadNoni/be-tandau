def parse_language(accept_language: str) -> str:
    for lang in accept_language.lower().split(","):
        code = lang.strip().split(";")[0]
        if code in {"kk", "ru", "en"}:
            return code
    return "en"
