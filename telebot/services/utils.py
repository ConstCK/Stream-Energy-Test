# Валидация пароля
def valid_password(password: str):
    return 16 > len(password) > 3

# Валидация заноловка и контента для заметок


def valid_text(text: str):
    return len(text) > 0
