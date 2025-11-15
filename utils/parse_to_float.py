#TODO: put this in a utils folder:
def parse_to_float(text: str) -> float:
    _str = ""
    for ch in text:
        if ch.isdigit() or ch == ".":
            _str += ch
    return float(_str)    
