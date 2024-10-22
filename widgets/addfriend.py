import time
import tkinter as tk
from tkinter import ttk
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from tkinter.messagebox import showerror, showinfo
from dblocal import add_friend

class AddFriend(tk.LabelFrame):
    """Класс для создания фрейма 'Add Friends'."""

    def __init__(self, parent, connection, cursor):
        """Инициализация окна."""
        super().__init__(parent, text="Add a friend", bd=1, relief="groove", bg='#0e1621', fg='#ffefe1')
        self.pack(fill="both", expand=True, ipadx=2, ipady=2)

        # Данные для работы с БД локальной
        self.cursor = cursor
        self.connection = connection

        # Стиль - Поля ввода, кнопка
        entry_style = ttk.Style()
        entry_style.configure("Input.TLabel", foreground="#ffefe1", background="#17212b", padding=5, insertcolor="#ffefe1")
        save_button_style = ttk.Style()
        save_button_style.configure("SaveButtonStyle.TLabel", foreground="#17212b", background="#fcd535", relief='flat', font=("Arial", 10, "bold"))

        # Заголовок Username
        username_label = ttk.Label(self, text="Username:", background='#0e1621', foreground='#ffefe1')
        username_label.pack(anchor='w', pady=(10, 0), padx=(10, 0))

        # Поле ввода Username
        self.username_entry = ttk.Entry(self, style="Input.TLabel", width=40)
        self.username_entry.pack(anchor='w', pady=(0, 5), padx=(10, 0))

        # Заголовок Nickame
        nickname_label = ttk.Label(self, text="Nickame (Only you can see):", background='#0e1621', foreground='#ffefe1')
        nickname_label.pack(anchor='w', pady=(5, 0), padx=(10, 0))

        # Поле ввода Nickame
        self.nickname_entry = ttk.Entry(self, style="Input.TLabel", width=40)
        self.nickname_entry.pack(anchor='w', pady=(0, 5), padx=(10, 0))

        # Заголовок Public Key (RSA):
        public_key_pem_label = ttk.Label(self, text="Public Key (RSA):", background='#0e1621', foreground='#ffefe1')
        public_key_pem_label.pack(anchor='w', pady=(5, 0), padx=(10, 0))

        # Поле ввода Public Key (RSA):
        self.public_key_pem_text = tk.Text(self, wrap='word', height=9, width=64, bg='#17212b', fg='#ffefe1', borderwidth=0, pady=7, padx=7, insertbackground='#ffefe1')
        self.public_key_pem_text.pack(anchor='w', pady=(0, 5), padx=(10, 0))

        # Кнопка "Сохранить"
        self.save_button = ttk.Button(self, style='SaveButtonStyle.TLabel', text="Save", padding=5, command=self.save_friend)
        self.save_button.pack(anchor='w',  pady=(20, 5), padx=(10, 0))

    # Получить данные с формы
    def get_form_data(self):
        username = self.username_entry.get() # Имя друга
        nickname = self.nickname_entry.get() # Никнейм друга
        public_key_pem = self.public_key_pem_text.get("1.0", tk.END) # публичный ключ дурга

        return username, nickname, public_key_pem

    # Обработка кнопки "Сохранить"
    def save_friend(self):
        username, nickname, public_key_pem = self.get_form_data()
        valid_main = self.valid_main(username, nickname, public_key_pem)

        if valid_main:
            res = add_friend(self.connection, self.cursor, {'username': username, 'nickname': nickname, 'public_key': public_key_pem})
            if res:
                showinfo(title="Ready", message="Friend added")
                self.clear_form()
            else:
                showerror(title="Error", message=f"User {username} is already in your friends list")
        else:
            not_valid = self.get_list_not_valid(username, nickname, public_key_pem) 
            showerror(title="Error", message=not_valid)      
            self.claer_not_valid_inputs(username, nickname, public_key_pem) 

    # Валидатор username
    def valid_username(self, username: str):
        """Функция валидации для имени пользователя.
        
        isalpha - Проверка только на английские буквы
        isascii - Проверка что символ с таблицы ASCII

        Строка, длиной 20 символов, которая состоит только из английских букв
        """
        if len(username) == 20 and username.isascii() and username.isalpha():  # Проверка длины и допустимых символов
            return True  
        return False

    # Валидатор nickname
    def valid_nickname(self, nickname: str):
        # Ник нейм не пустой и длина меньше 20 символов
        return bool(nickname) and len(nickname) <= 20
    
    # Валидатор public_key_pem
    def valid_public_key_pem(self, public_key_pem: str) -> bool:
        """
        Проверяет корректность публичного ключа RSA в формате PEM.

        Аргументы:
        pem_key -- строка с публичным ключом в формате PEM.

        Возвращает:
        True, если ключ корректный; иначе False.
        """
        try:
            # Попробуем загрузить ключ из строки PEM
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode(),  # Преобразуем строку в байты
                backend=default_backend()
            )
        
            # Проверяем, что это именно публичный ключ RSA
            if isinstance(public_key, rsa.RSAPublicKey):
                return True
            else:
                return False
        except Exception as e:
            # Если возникло исключение, ключ некорректный
            return False

    # Валидатор Формы
    def valid_main(self, username, nickname, public_key_pem):
        valid_username = self.valid_username(username)
        valid_nickname = self.valid_nickname(nickname)
        valid_public_key_pem = self.valid_public_key_pem(public_key_pem)

        if valid_username and valid_nickname and valid_public_key_pem:
            return True
        return False
    
    # Очистить форму
    def clear_form(self):
        self.username_entry.delete(0, tk.END) 
        self.nickname_entry.delete(0, tk.END)
        self.public_key_pem_text.delete('1.0', tk.END)

    # Получить список не Валидные полей ввода
    def get_list_not_valid(self, username, nickname, public_key_pem):
        not_valid = {
            'Username:': 'Success' if self.valid_username(username) else 'Error',
            'Nickname:': 'Success' if self.valid_nickname(nickname) else 'Error',
            'Public key:': 'Success' if self.valid_public_key_pem(public_key_pem) else 'Error',
        }

        # Преобразование словаря в текст с переносом строки
        return '\n'.join(f"{key} {value}" for key, value in not_valid.items())
    
    # Очистить поля для ввода, котоыре не прошли валидацию
    def claer_not_valid_inputs(self, username, nickname, public_key_pem):
        if not self.valid_username(username):
            self.username_entry.delete(0, tk.END)

        if not self.valid_nickname(nickname):
            self.nickname_entry.delete(0, tk.END)

        if not self.valid_public_key_pem(public_key_pem):
            self.public_key_pem_text.delete("1.0", tk.END)

 



