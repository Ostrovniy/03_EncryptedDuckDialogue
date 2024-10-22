import hashlib
import random
import string
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Зашыфровать текст ПУБЛИЧНЫМ ключем
def encrypt_with_pem_public_key(pem_key: str, plaintext: str) -> bytes:
    # Загрузка публичного ключа из PEM
    public_key = serialization.load_pem_public_key(
        pem_key.encode()
    )

    # Преобразование текста в байты
    plaintext_bytes = plaintext.encode()

    # Шифрование текста с использованием публичного ключа
    ciphertext = public_key.encrypt(
        plaintext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext

# Разшифровать текст Приватным ключем
def decrypt_with_pem_private_key(pem_key: str, ciphertext: str) -> str:
    # Загрузка приватного ключа из PEM
    private_key = load_pem_private_key(
        pem_key.encode(),
        password=None
    )

    # Преобразование строки ciphertext из hex в байты
    if ciphertext.startswith('\\x'):
        # Удаляем '\\x' и преобразуем из hex в байты
        ciphertext_bytes = bytes.fromhex(ciphertext[2:])
    else:
        raise ValueError("Неверный формат строки для ciphertext")

    # Расшифрование текста с использованием приватного ключа
    plaintext_bytes = private_key.decrypt(
        ciphertext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Преобразование байт в строку
    plaintext = plaintext_bytes.decode()

    return plaintext

# Сгенерировать Приватный и Публичный ключ
def generate_rsa_keys():
    # Генерация пары ключей
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    # Сериализация ключей в формат PEM
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Возврат ключей в виде строк
    return private_key_pem.decode('utf-8'), public_key_pem.decode('utf-8')

# Хешырование текста
def get_hesh(text: str):
    # Создание хэша ключа
    bytes_text = text.encode()  # Преобразование строки в байты
    return hashlib.sha256(bytes_text).hexdigest()

# Проверка двух Хешей на равность
def is_hesh_equal(hash1: str, hash2: str):
    return hash1 == hash2

# Создать уникальное имя пользователя длиной 20 символов
def create_username(length=20):
    """
    Генерирует случайное имя длиной length символов, состоящее из английских букв.

    Возвращает:
    Случайное имя в виде строки
    """
    length=20
    characters = string.ascii_letters  # Все английские буквы (A-Z, a-z)
    username = ''.join(random.choice(characters) for _ in range(length))
    
    return username

# Зашыфровать сообщения для друга
def data_to_encryptdata(text, public_key_friend):
    # (1) Получить хеш сообщения
    hesh_text = get_hesh(text)
    # (2) Зашыфровка сообщения публичным ключем отправителя
    encrypt_text = encrypt_with_pem_public_key(public_key_friend, text)
    # (3) Зашыфровка хеша публичным ключем отправилея
    encrypt_hesh = encrypt_with_pem_public_key(public_key_friend, hesh_text)

    return encrypt_text, encrypt_hesh