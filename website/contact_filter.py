"""Function to filter contacts by their seprciality"""
def filter_input(users_input:str) -> list:
    """Function to filter contacts by their seprciality"""
    categories = {
        "Автомобілі": ["водій", "механік", "технік", "машин", "автомобіл", 'фур', 'вантажівк'],
        "Медицина та медичне обладнання": ["лік", 'турнік', 'бинт', 'апечк', 'медицин'],
        "Одяг і амуніція": ["одяг", "амунц", "брон", "штан", "шкарпетки", 'термобілизн', 'куртк'],
        "Сітки": ["сітк"],
        "3D-друк": ["друк", 'пластик', 'принтер', 'дизайн'],
        "Кошти":['гроші', 'збор', 'збір', 'кошти'],
        "Продукти":['м\'ясо', 'продукт', 'риб', 'овоч', 'молочн', 'молочк']
    }

    result = set()
    words = users_input.lower().split()

    for category, keywords in categories.items():
        for word in words:
            for keyword in keywords:
                if keyword in word:
                    result.add(category)
                    break

    return list(result)

