"""file to with functions to check, wether the user's input is valid or no"""
def is_valid_email(email: str) -> bool:
    """checks if the given email is valid.
    It is valid if there is "@" in it, also it should contain a domain, which is 
    being cheked as well.
    """
    if '@' not in email or email.count('@') != 1:
        return False

    local_part, domain_part = email.split('@')

    if not local_part or local_part[0] == '.' or local_part[-1] == '.':
        return False

    if domain_part[0] == '.' or domain_part[-1] == '.':
        return False

    domain_sections = domain_part.split('.')
    if any(not section for section in domain_sections):
        return False

    return True

def is_valid_phone_number(number):
    """Checks if the given phone number is valid. The phone number is valid
    if it's lenght is propper and if there are only allowed symbols in it.
    """
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


def is_name_valid(name: str) -> bool:
    """Function to validate given person name (first or last).
    It checks, wether the first letter of the name is upper, the lenght, then 
    if separators forund in the name, it checks, if they are being used correctly without it's 
    repeating and if the first letter after separator is upper.
    """
    max_length = 150
    if not name or len(name) > max_length:
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

def format_name(name: str) -> str:
    """Робить першу літеру кожної частини імені великою, інші — маленькими."""
    allowed_separators = "-' "
    if len(name) == 1:
        return name.upper()
    result = ''
    i = 0
    while i < len(name):
        if name[i].isalpha():
            result += name[i].upper()
            i += 1
            while i < len(name) and name[i].isalpha():
                result += name[i].lower()
                i += 1
        elif name[i] in allowed_separators:
            result += name[i]
            i += 1
        else:
            return name
    return result


def fix_and_validate_name(name: str) -> str | None:
    name = format_name(name)
    return name if is_name_valid(name) else None

def is_password_incorrect(password: str):
    """function to meke sure user's password is valid.
    It checks if the password is longer, than 7 characters,
    if it has at least one upper case letter and one sybmol, which is not letter or digit.
    if the password is valid function returns False
    """
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    if len(password) < 7:
        return "Password must contain at least 7 characters"

    if ' ' in password:
        return "There can be no spaces in password"

    if not any(ch.isdigit() for ch in password):
        return "Password must include at least one digit"

    if not any(ch.isalpha() for ch in password):
        return "Password must include at least one letter"

    if not any(ch in special_characters for ch in password):
        return "Password must include at least one special character"

    if not all(ch.isalnum() or ch in special_characters for ch in password):
        return "Password can only contain letters, digits and common symbols"

    return False
