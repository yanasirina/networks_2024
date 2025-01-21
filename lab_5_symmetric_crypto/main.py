from typing import Protocol
import random
import string


class EncryptionProtocol(Protocol):
    def encrypt(self, text: str, key: int | str) -> str:
        """Шифрует текст с использованием указанного ключа."""
        pass

    def decrypt(self, text: str, key: int | str) -> str:
        """Дешифрует текст с использованием указанного ключа."""
        pass


class CaesarCipher(EncryptionProtocol):
    """Обобщённый шифр Цезаря."""

    def encrypt(self, text: str, key: int) -> str:
        encrypted_text = []
        for char in text:
            if 'A' <= char <= 'Z':  # Латиница (заглавные)
                encrypted_text.append(chr((ord(char) - ord('A') + key) % 26 + ord('A')))
            elif 'a' <= char <= 'z':  # Латиница (строчные)
                encrypted_text.append(chr((ord(char) - ord('a') + key) % 26 + ord('a')))
            elif 'А' <= char <= 'Я':  # Кириллица (заглавные)
                encrypted_text.append(chr((ord(char) - ord('А') + key) % 32 + ord('А')))
            elif 'а' <= char <= 'я':  # Кириллица (строчные)
                encrypted_text.append(chr((ord(char) - ord('а') + key) % 32 + ord('а')))
            else:
                encrypted_text.append(char)  # Прочие символы без изменений
        return ''.join(encrypted_text)

    def decrypt(self, text: str, key: int) -> str:
        return self.encrypt(text, -key)  # Дешифрование обратное


class VernamCipher(EncryptionProtocol):
    """Шифр Вернама."""

    def encrypt(self, text: str, key: str) -> str:
        if len(text) != len(key):
            raise ValueError("Длина текста и ключа должны совпадать.")
        encrypted = ''.join(chr(ord(t) ^ ord(k)) for t, k in zip(text, key))
        return encrypted

    def decrypt(self, text: str, key: str) -> str:
        return self.encrypt(text, key)  # XOR симметричен


def brute_force_caesar(cipher_text: str):
    """Расшифровка текста, зашифрованного шифром Цезаря, перебором ключей."""
    caesar = CaesarCipher()
    possible_results = []
    for shift in range(1, 33):  # Перебираем сдвиги от 1 до 32
        decrypted = caesar.decrypt(cipher_text, shift)
        possible_results.append((shift, decrypted))
    return possible_results


def main():
    """Тестирование всех реализованных функций."""
    text = "Привет, мир! Hello world!"

    # Пример с шифром Цезаря
    caesar = CaesarCipher()
    key_caesar = 5

    print("Шифр Цезаря:")
    encrypted_caesar = caesar.encrypt(text, key_caesar)
    decrypted_caesar = caesar.decrypt(encrypted_caesar, key_caesar)
    print(f"Оригинальный текст: {text}")
    print(f"Зашифрованный текст: {encrypted_caesar}")
    print(f"Расшифрованный текст: {decrypted_caesar}")

    # Расшифровка шифра Цезаря грубым перебором
    print("\nПеребор ключей для шифра Цезаря:")
    brute_force_results = brute_force_caesar(encrypted_caesar)
    for key, result in brute_force_results:
        print(f"Ключ {key}: {result}")

    # Пример с шифром Вернама
    vernam = VernamCipher()
    key_vernam = ''.join(random.choice(string.ascii_letters) for _ in range(len(text)))

    print("\nШифр Вернама:")
    encrypted_vernam = vernam.encrypt(text, key_vernam)
    decrypted_vernam = vernam.decrypt(encrypted_vernam, key_vernam)
    print(f"Оригинальный текст: {text}")
    print(f"Ключ: {key_vernam}")
    print(f"Зашифрованный текст: {encrypted_vernam}")
    print(f"Расшифрованный текст: {decrypted_vernam}")


if __name__ == "__main__":
    main()
