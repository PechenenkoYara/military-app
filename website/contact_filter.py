"""Function to filter contacts by their seprciality"""

CATEGORIES = {
    "Автомобілі": ["водій", "механік", "технік", "машин", "автомобіл", 'фур', 'вантажівк'],
    "Медицина та медичне обладнання": ["лік", 'турнік', 'бинт', 'апечк', 'медицин'],
    "Одяг і амуніція": ["одяг", "амунц", "брон", "штан", "шкарпетки", 'термобілизн', 'куртк'],
    "Сітки": ["сітк"],
    "3D-друк": ["друк", 'пластик', 'принтер', 'дизайн'],
    "Кошти":['гроші', 'збор', 'збір', 'кошти'],
    "Продукти":['м\'ясо', 'продукт', 'риб', 'овоч', 'молочн', 'молочк'],
    "Інше": []
}

def filter_input(users_input:str) -> list:
    """Function to filter contacts by their seprciality"""
    CATEGORIES = {
        "Автомобілі": ["водій", "механік", "технік", "машин", "автомобіл", 'фур', 'вантажівк', 'шин'],
        "Медицина та медичне обладнання": ["лік", 'турнік', 'бинт', 'апечк', 'медицин', 'медик'],  #added some key words
        "Одяг і амуніція": ["одяг", "амунц", "брон", "штан", "шкарпетк", 'термобілизн', 'куртк'],
        "Сітки": ["сітк"],
        "3D-друк": ["друк", 'пластик', 'принтер', 'дизайн'],
        "Кошти":['гроші', 'збор', 'збір', 'кошти'],
        "Продукти":['м\'ясо', 'продукт', 'риб', 'овоч', 'молочн', 'молочк']
    }

    result = set()
    words = users_input.lower().split()

    for category, keywords in CATEGORIES.items():
        for word in words:
            for keyword in keywords:
                if keyword in word:
                    result.add(category)
                    break

    return list(result) if result else ['Інше']

def does_fit(list1: list, list2: list) -> bool:
    'checcks the intersection of two lests'
    for el in list1:
        if el in list2:
            return True
    return False
