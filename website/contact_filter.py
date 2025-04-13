"""Function to filter contacts by their speciality"""

CATEGORIES = {
    "Автомобілі": [],
    "Медицина та медичне обладнання": [],
    "Одяг і амуніція": [],
    "Сітки": [],
    "3D-друк": [],
    "Кошти": [],
    "Продукти": [],
    "Інше": []
}


def read_files_and_categorize(file_paths:dict):
    """Function to filter contacts by their seprciality"""
    for category, file_path in file_paths.items():
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    CATEGORIES[category].append(word)
    return CATEGORIES
def filter_input(users_input: str) -> list:
    """Function to filter contacts by their speciality"""
    result = set()
    words = users_input.lower().split()
    categories_dict = CATEGORIES

    for category, keywords in categories_dict.items():
        for word in words:
            for keyword in keywords:
                if keyword in word:
                    result.add(category)
                    break

    return list(result) if result else ['Інше']

def does_fit(list1: list, list2: list) -> bool:
    """checks the intersection of two lists"""
    for el in list1:
        if el in list2:
            return True
    return False

file_paths = {'Автомобілі':
    'website/static/files_for_contacts/cars.txt',
    'Медицина та медичне обладнання':
    'website/static/files_for_contacts/medicine.txt',
    'Одяг і амуніція':
    'website/static/files_for_contacts/cloths.txt',
    'Сітки':
    'website/static/files_for_contacts/nets.txt',
    '3D-друк':
    'website/static/files_for_contacts/3d_printing.txt',
    'Кошти':
    'website/static/files_for_contacts/money.txt',
    'Продукти':
    'website/static/files_for_contacts/products.txt'
}

read_files_and_categorize(file_paths)