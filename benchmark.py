"""
Замер времени взлома для разных длин ключей.
Для каждой пары длин ключей (N1, N2):
 - берём случайные p1, p2
 - шифруем известный текст
 - запускаем взлом и замеряем время
"""

import random
from encrypting import encrypt_with_perm
from cracker import crack, PAD_CHAR
from funcs import pad_text

FILE_RESULT = "benchmarks/benchmark_static_4.csv"


# генерация рандомной перестановки
def random_perm(n):
    p = list(range(n))
    random.shuffle(p)
    return tuple(p)


# проводим замеры
def measure(N1, N2, plain):
    # создаем рандомные перестановки
    p1 = random_perm(N1)
    p2 = random_perm(N2)

    # получаем шифр двойной перестановкой
    cipher = encrypt_with_perm(encrypt_with_perm(plain, p1), p2)

    found, time = crack(plain, cipher, N1, N2)  # взламываем

    return found, time


def main():
    plain = "A" * 500 + "b" * 500 + "C" * 500 + "d" * 500 + "E" * 500 + "F" * 500 + "G" * 500 + "h" * 500

    pairs = [
        #(2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9)
       # (3,4), (4,5), (5,6), (6,7), (7,8), (8,9) кат
        (2,9), (3,9), (4,9), (5,9), (6,9)
         #(9,2), (9,3), (9,4), (9,5), (9,6)
    ]

    results = []
    for N1, N2 in pairs:
        print(f"Измерения для: N1={N1}, N2={N2}...")

        p = pad_text(plain, N1, N2, PAD_CHAR)
        found, time = measure(N1, N2, p)
        results.append((N1, N2, time))

        print(f"{'Найдено\n' if found else 'Не найдено\n'}")

    with open(FILE_RESULT, "w", encoding="utf-8") as f:
        f.write("N1,N2,time\n")
        for N1, N2, t in results:
            f.write(f"{N1},{N2},{t}\n")
    print("Результаты сохранены в:", FILE_RESULT)


if __name__ == '__main__':
    main()
