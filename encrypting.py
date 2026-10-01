"""
Шифрование метода двойной перестановки.

encrypt() - шифрование двойной перестановкой
encrypt_with_perm() - один прогон шифрования по готовым перестановкам
"""


from funcs import pad_text, get_positions


# Шифрование текста с известными позициями ключа
def encrypt_with_perm(text: str, p):
    N = len(p)
    bs = N * N  # размер блока

    out = []
    for start in range(0, len(text), bs):
        # выделяем блок текста
        # если bs=4, то "qwertyuiop" -> "qwer", "tyui", "opXX"
        block = text[start:start + bs]

        # заполняем матрицу N x N построчно
        matrix = []
        for r in range(N):
            row = list(block[r * N:(r + 1) * N])  # кусок блока длиной N
            matrix.append(row)  # добавляем строку в матрицу
        # получим
        # q w
        # e r

        # 1) переставляем столбцы
        for r in range(N):
            row = matrix[r]
            new_row = [None] * N
            for i in range(N):
                new_row[p[i]] = row[i]
            matrix[r] = new_row

        # 2) переставляем строки
        new_matrix = [None] * N
        for i in range(N):
            new_matrix[p[i]] = matrix[i]
        matrix = new_matrix

        # считываем построчно
        for r in range(N):
            out.append(''.join(matrix[r]))
    return ''.join(out)


# Шифрование двойной перестановкой
def encrypt(text: str, key1: str, key2: str, pad_char):
    text = pad_text(text, len(key1), len(key2), pad_char)  # дополняем текст до длины, кратной НОК размеров обоих блоков

    # делаем два прогона шифрования
    text = encrypt_with_perm(text, get_positions(key1))
    text = encrypt_with_perm(text, get_positions(key2))
    return text
