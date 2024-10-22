import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, showwarning
from dblocal import add_account
from cripto import create_username, generate_rsa_keys

class AddAccount(tk.LabelFrame):
    """Класс для создания фрейма 'Создайть новый аккаунт'."""
    def __init__(self, parent, connection, cursor):
        """Инициализация окна."""
        super().__init__(parent, text="Create a new account", bd=1, relief="groove", bg='#0e1621', fg='#ffefe1')
        self.pack(fill="both", expand=True, ipadx=2, ipady=2)

        # Данные для работы с БД локальной
        self.cursor = cursor
        self.connection = connection

        self.username = create_username() # Генерация 20-и сивольного рандомного имени пользователя
        self.private_key_rsa, self.public_key_rsa = generate_rsa_keys() # Генерация пары ключей RSA

        # Стиль - Кнопка "Сохранить" и "Сгенерировать еще раз Ключи и Имя пользователя"
        save_btn_style = ttk.Style()
        save_btn_style.configure("SaveBtnStyle.TLabel", foreground="#17212b", background="#fcd535", relief='flat', font=("Arial", 10, "bold"))

        # Заголовок nickname
        nickname_label = ttk.Label(self, text="Nickame (Only you can see):", background='#0e1621', foreground='#ffefe1')
        nickname_label.pack(anchor='w', pady=(10, 0), padx=(10, 0)) # Top 10, down 5 // left 10, Right 0

        # Поле ввода nickname
        nickname_entry_style = ttk.Style()
        nickname_entry_style.configure("Input.TLabel", foreground="#ffefe1", background="#17212b", padding=5, insertcolor="#ffefe1")
        self.nickname_entry = ttk.Entry(self, style="Input.TLabel", width=40)
        self.nickname_entry.pack(anchor='w', pady=(0, 5), padx=(10, 0))

        # Заголовок и Поле для вывода username
        self.username_text = self.create_readonly_text(self, "Username:", self.username)

        # Заголовок и Поле для вывода private_key_rsa
        self.private_key_rsa_text = self.create_readonly_text(self, "Private Key (RSA):", self.private_key_rsa, height=15)
        
        # Заголовок и Поле для вывода public_key_rsa
        self.public_key_rsa_text = self.create_readonly_text(self, "Public Key (RSA):", self.public_key_rsa, height=8)

        # Кнопка "Сгенерировать еще раз Ключи и Имя пользователя"
        self.private_button = ttk.Button(self, style='SaveBtnStyle.TLabel', text="Update parameters RSA", padding=5, command=self.generete_privat_data)
        self.private_button.pack(anchor='w',  pady=(20, 5), padx=(10, 0))

        # Кнопка "Сохранить" - Сохранения данных в БД
        self.save_button = ttk.Button(self, style='SaveBtnStyle.TLabel', text="Save", padding=5, command=self.save_account)
        self.save_button.pack(anchor='w',  pady=(0, 5), padx=(10, 0))

    # Конструктор для Имени пользоватлея, двух пар ключей
    def create_readonly_text(self, parent, label_text, content, height=1, width=64):
        """
        Функция для создания поля вывода текста с невозможностью редактирования.

        Аргументы:
        parent -- родительский элемент (фрейм).
        label_text -- заголовок перед полем.
        content -- текстовое содержание для отображения.
        height -- высота текстового поля.
        width -- ширина текстового поля.
        """
        # Заголовок поля
        label = ttk.Label(parent, text=label_text, background='#0e1621', foreground='#ffefe1')
        label.pack(anchor='w', pady=(5, 0), padx=(10, 0))
    
        # Поле ввода
        text_widget = tk.Text(parent, wrap='word', height=height, width=width, bg='#17212b', fg='#ffefe1', borderwidth=0, pady=7, padx=7)  # Устанавливаем фиксированную ширину
        text_widget.pack(anchor='w', pady=(0, 5), padx=(10, 0)) 
        text_widget.insert('1.0', content)
        text_widget.config(state='disabled')  # Запрещаем редактирование
        return text_widget

    # Обработка кнопки "Сохранить"
    def save_account(self):
        nickname = self.nickname_entry.get() # Получить введенный никнейм с поля ввода
        # Проверка ник нейма на пустоту
        if nickname != "" and len(nickname) > 1:
            # Добавить новый аккаунт в базу данных
            res = add_account(self.connection, self.cursor, self.username, nickname, self.private_key_rsa, self.public_key_rsa)
            # Проверка на успешность добавления аккаунта в БД
            if res:
                showinfo(title="Ready", message='New User added to DB')
                self.clear_form()# Очистить поле ввода
            else:
                showerror(title="Error", message='Attempt to record duplicate')
        else:
            showwarning(title="Error", message='Nickname must not be empty and must contain at least 2 characters')

    # Обработка кнопки "Сгенерировать еще раз Ключи и Имя пользователя"
    def generete_privat_data(self):
        # Сгенерировать данные для обновления
        self.username = create_username()
        self.private_key_rsa, self.public_key_rsa = generate_rsa_keys()

        # Имя пользователя
        self.username_text.config(state='normal')           # Разрешаем редактирование
        self.username_text.delete('1.0', tk.END)            # Удалить все данные с поля
        self.username_text.insert('1.0', self.username)     # Записать новые данные в поле
        self.username_text.config(state='disabled')         # Запрещаем редактирование

        # Приватный ключ
        self.private_key_rsa_text.config(state='normal')
        self.private_key_rsa_text.delete('1.0', tk.END)
        self.private_key_rsa_text.insert('1.0', self.private_key_rsa)
        self.private_key_rsa_text.config(state='disabled')

        # Публичный ключ
        self.public_key_rsa_text.config(state='normal')
        self.public_key_rsa_text.delete('1.0', tk.END)
        self.public_key_rsa_text.insert('1.0', self.public_key_rsa)
        self.public_key_rsa_text.config(state='disabled')

        self.update()  # Обновляем интерфейс 

    # Очистить форму ввода
    def clear_form(self):
        # Никнейм
        self.nickname_entry.delete(0, tk.END)

        # Имя пользователя
        self.username_text.config(state='normal')       # Разрешаем редактирование
        self.username_text.delete('1.0', tk.END)        # Очищаем текстовое поле
        self.username_text.config(state='disabled')     # Запрещаем редактирование

        # Приватный ключ
        self.private_key_rsa_text.config(state='normal')
        self.private_key_rsa_text.delete('1.0', tk.END)
        self.private_key_rsa_text.config(state='disabled')

        # Публичный ключ
        self.public_key_rsa_text.config(state='normal')
        self.public_key_rsa_text.delete('1.0', tk.END)
        self.public_key_rsa_text.config(state='disabled')

        self.update()  # Обновляем интерфейс      

        

        
        
        
