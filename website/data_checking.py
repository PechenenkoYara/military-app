"""file to with functions to check, wether the user's input is valid or no"""
def is_valid_email(email: str) -> bool:
    """checks if the given email is valid"""
    if '@' not in email or email.count('@') != 1:
        return False

    local_part, domain_part = email.split('@')

    if not local_part or local_part[0] == '.' or local_part[-1] == '.':
        return False

    if '.' not in domain_part:
        return False

    if domain_part[0] == '.' or domain_part[-1] == '.':
        return False

    domain_sections = domain_part.split('.')
    if any(not section for section in domain_sections):
        return False

    return True

def is_valid_phone_number(number):
    """Checks if the given phone number is valid"""
    if not (number.startswith("+") or number.startswith("0")):
        return False
    if len(number) < 10 or len(number) > 15:
        return False
    allowed = "+-#()*0123456789"
    elements = '+-#*()'
    for el in number:
        if el not in allowed:
            return False
    for i in range(len(number) - 1):
        if number[i] in elements and number[i+1] == number[i]:
            return False
    return True

def is_valid_name(name: str) -> bool:
    """Checks if the given name is valid"""
    if name[0].islower():
        return False
    if len(name) == 1 and name.isupper():
        return True

    if not name or len(name) > 150:
        return False

    allowed_separators = "-' "
    for ch in name:
        if not (ch.isalpha() or ch in allowed_separators):
            return False

    parts = name.replace("-", " ").replace("'", " ").split()
    for part in parts:
        if len(part) < 2:
            return False
    return True


def is_valid_last_name(last_name: str) -> bool:
    """Checks if the given last name is valid"""
    if last_name[0].islower():
        return False
    if not last_name or len(last_name) > 50:
        return False

    allowed_separators = "-' "
    prev_char = ""
    for ch in last_name:
        if not (ch.isalpha() or ch in allowed_separators):
            return False
        if ch in allowed_separators and prev_char in allowed_separators:
            return False
        prev_char = ch

    parts = last_name.replace("-", " ").replace("'", " ").split()
    for part in parts:
        if len(part) == 1:
            if not part.isupper():
                return False
        elif not part[0].isupper() or not part[1:].islower():
            return False

    return True

def is_name_valid(name: str) -> bool:
    return True

def is_password_incorrect(password: str) -> bool | str:
    return 0