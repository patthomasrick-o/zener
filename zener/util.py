from typing import List


def word_wrap(value: str, character_length: int =2000) -> List[str]:
    """
    Wrap something according to character limits.
    """

    words = value.split()
    wrapped_lines: List[str] = []
    current_line: str = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= character_length:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            wrapped_lines.append(current_line)
            current_line = word

    if current_line:
        wrapped_lines.append(current_line)

    return wrapped_lines
