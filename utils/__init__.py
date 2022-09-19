def fa_to_en(fa_text: str) -> str:
    fa_digit_range = range(ord('۰'), ord('۹') + 1)
    diff = abs(ord('۰') - ord('0'))
    for char in fa_text:
        if ord(char) in fa_digit_range:
            fa_text = fa_text.replace(char, chr(ord(char) - diff))

    return fa_text
