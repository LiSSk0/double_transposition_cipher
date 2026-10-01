"""
Взлом шифра двойной перестановки

Известен открытый текст и шифр (P и C):
C = E2(E1(P, p1), p2)
взламываем p1 и p2 (перестановки)
E1, E2 - шифрование перестановкой

Идея (meet-in-the-middle):
1) для каждой p2 считаем M = D2(C, p2), кладём в словарь
2) для каждой p1 считаем M = E1(P, p1), ищем в словаре
Сложность N1! + N2! (полный перебор был бы N1! * N2!)
"""

from itertools import permutations
from time import perf_counter

from encrypting import encrypt_with_perm
from decrypting import decrypt_with_perm
from funcs import pad_text

CRACK_PLAIN_FILE = "files/encrypt_me.txt"  # известный открытый текст
CRACK_CIPHER_FILE = "files/decrypt_me.txt"  # шифро
PAD_CHAR = 'а'


# возвращает (p1, p2) или None и затраченное время
def crack(plain: str, cipher: str, N1: int, N2: int):
    all_p1 = list(permutations(range(N1)))  # все перестановки, для N=3: (0,1,2) (0,2,1) ...
    all_p2 = list(permutations(range(N2)))

    print(f"Перестановок для ключа1 длиной N1={N1}: {len(all_p1)}")
    print(f"Перестановок для ключа2 длиной N2={N2}: {len(all_p2)}")
    print(f"Прямой перебор: {2 * len(all_p1) * len(all_p2)} операций шифрования")
    print(f"Meet-in-the-middle: {len(all_p1) + len(all_p2)} операций шифрования")

    t0 = perf_counter()  # засекаем время

    # 1) дешифруем шифр C для всех перестановок p2
    table = {}  # и записываем в словарь
    for p2 in all_p2:
        M = decrypt_with_perm(cipher, p2)
        if M not in table:
            table[M] = []
        table[M].append(p2)

    # 2) шифруем исходный текст со всеми перестановками p1
    #    пока не найдем совпадение со словарем дешифров
    found = None
    for p1 in all_p1:
        M = encrypt_with_perm(plain, p1)
        if M in table:
            found = (list(p1), list(table[M][0]))
            break

    dt = perf_counter() - t0
    return found, dt


def do_crack(N1, N2, plain, cipher):
    # дополняем открытый текст как при шифровании
    plain = pad_text(plain, N1, N2, PAD_CHAR)

    result, dt = crack(plain, cipher, N1, N2)

    if result is None:
        print(f"Не найдено. Время: {dt:.3f} сек.")
    else:
        p1, p2 = result
        print(f"Найдено. Время: {dt:.3f} сек.")
        print(f"Перестановка 1: {p1}")
        print(f"Перестановка 2: {p2}")

        # проверка: шифруем дважды и сравниваем с имеющимся шифром
        test = encrypt_with_perm(encrypt_with_perm(plain, p1), p2)
        print("Совпадает с шифротекстом:", test == cipher)


def main():
    print("--- Взлом шифра двойная перестановка ---")
    n1 = int(input("Длина ключа 1: ").strip())
    n2 = int(input("Длина ключа 2: ").strip())

    with open(CRACK_PLAIN_FILE, 'r', encoding='utf-8') as f:
        plain = f.read()
    with open(CRACK_CIPHER_FILE, 'r', encoding='utf-8') as f:
        cipher = f.read()

    print("В процессе...")
    try:
        do_crack(n1, n2, plain, cipher)
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()
