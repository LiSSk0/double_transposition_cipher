"""
Дешифрование метода двойной перестановки.

decrypt() - дешифрование двойного шифрования
decrypt_with_perm() - один прогон расшифровки по готовым перестановкам
"""

from funcs import get_positions


def decrypt_with_perm(cipher: str, p):
    N = len(p)
    bs = N * N

    out = []
    for start in range(0, len(cipher), bs):
        block = cipher[start:start + bs]  # разделяем на блоки

        # заполняем матрицу N x N построчно
        matrix = []
        for r in range(N):
            row = list(block[r * N:(r + 1) * N])  # кусок блока длиной N
            matrix.append(row)  # добавляем строку в матрицу
        # получаем матрицу шифра из одного блока N
        # q w
        # e r

        # при расшифровке порядок обратный:
        # 1) обратная перестановка строк
        new_matrix = [None] * N
        for i in range(N):
            new_matrix[i] = matrix[p[i]]
        matrix = new_matrix

        # 2) обратная перестановка столбцов
        for r in range(N):
            row = matrix[r]
            new_row = [None] * N
            for i in range(N):
                new_row[i] = row[p[i]]
            matrix[r] = new_row

        # считываем построчно
        for r in range(N):
            out.append(''.join(matrix[r]))
    return ''.join(out)


def decrypt(cipher: str, key1: str, key2: str):
    text = decrypt_with_perm(cipher, get_positions(key1))
    text = decrypt_with_perm(text, get_positions(key2))
    return text
