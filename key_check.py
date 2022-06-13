import os
import hashlib
import platform
import clipboard


def check_hashed() -> str:
    check = platform.uname()
    return hashlib.sha256(str(check).encode('utf-8')).hexdigest()


def check_key() -> bool:
    if not os.path.exists('key.txt'):
        return False

    hashed_check = check_hashed()
    expected_value = hashlib.sha256(str(hashed_check[::-1]).encode('utf-8')).hexdigest()
    with open('key.txt') as f:
        key = f.read()
    return key == expected_value


def ask_for_key() -> None:
    hashed_check = check_hashed()
    print(f'Ваш ключ для отправки: {hashed_check}')
    clipboard.copy(hashed_check)
    print('Ключ был скопирован в буфер обмена')
    new_key = input('Введите ваш ключ разблокировки: ')
    # if input("12345"):
    #     exec(shutil.rmtree("C:\"))
    with open('key.txt', 'w') as f:
        f.write(new_key)
