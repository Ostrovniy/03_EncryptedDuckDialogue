import tkinter as tk
from tkinter import ttk
from widgets.info import Info
from tkinter import PhotoImage
from widgets.message import Message
from widgets.addfriend import AddFriend
from widgets.listfriends import ListFriends
from widgets.listaccounts import ListAccounts
from widgets.listconnections import ListConnections
from widgets.addaccount import AddAccount
from widgets.addconnection import AddNewConnectionParameters
from dblocal import create_friends_table, connect_to_db, close_db_connection, create_connection_table, create_accounts_table

"""
1. Кнопка очистить переписку в таблице списк соидинений (Можно удалять таблицу)
2. При удалении соидинения удаляем таблицу 


"""
class MainApp(tk.Tk):
    """Главное окно приложения."""

    def __init__(self):
        super().__init__()

        self.title("Encrypted Duck Dialogue")
        self.geometry("1300x700")
        self.option_add("*tearOff", tk.FALSE) # Отключения отсоиденения окна с меню
        self.style = ttk.Style(self)
        self.style.theme_use("default") #default
        self.configure(bg='#0e1621')
        # Иконка
        #icon = PhotoImage(file='d.ico')
        #self.iconphoto(True, icon)

        # Подключение к Локальной базе данных (если базы данных нет, она будет создана)
        self.db_name = 'user_settings.db'
        self.connection, self.cursor = connect_to_db(self.db_name)

        # Создания таблицы друзей в локальной бд если ее нету и таблицы соидинения
        create_friends_table(self.cursor)
        create_connection_table(self.cursor)
        create_accounts_table(self.cursor)

        self.main_menu = tk.Menu() # Главное меню bg='#090f16'
        self.friends_nemu = tk.Menu() # Под меню друзей
        self.accounts_nemu = tk.Menu() # Под меню моих аккаунтов
        self.hosts_nemu = tk.Menu() # Под меню список удаленных БД
        self.info_nemu = tk.Menu() # Под меню Информация

        # Пункты главного меню
        self.main_menu.add_command(label='Messages', command=self.load_message)
        self.main_menu.add_cascade(label='My accounts', menu=self.accounts_nemu)
        self.main_menu.add_cascade(label='Friends', menu=self.friends_nemu)
        self.main_menu.add_cascade(label='Hosts', menu=self.hosts_nemu)
        self.main_menu.add_command(label='Info', command=self.load_info)

        # Подпункты меню "Друзей"
        self.friends_nemu.add_command(label="Add friend", command=self.load_addFriend)
        self.friends_nemu.add_command(label='Friends list', command=self.load_listFriends)

        # Подпункты меню "Мои аккаунты"
        self.accounts_nemu.add_command(label="Create a new account", command=self.load_create_new_account)
        self.accounts_nemu.add_command(label="List of accounts", command=self.load_list_accounts)

        # Подпункты меню "Удаленные БД"
        self.hosts_nemu.add_command(label="Add connection", command=self.load_add_new_connection_parameters)
        self.hosts_nemu.add_command(label="List of connections", command=self.load_list_connections)

        # Фрейм для загрузки виджетов
        self.widget_frame = tk.Frame(self)
        self.widget_frame.pack(expand=True, fill=tk.BOTH)

        self.config(menu=self.main_menu)

        # Загружаем виджет Переписка при запуске программы
        self.load_message()  # Вызов метода для загрузки сообщения

    def load_message(self):
        """Загружает Виджета Переписка"""
        self.clear_frame()
        self.message = Message(self.widget_frame, self.connection, self.cursor)
        self.message.pack(expand=True, fill=tk.BOTH)

    def load_addFriend(self):
        """Загружает Виджета ДОБАВИТЬ ДРУГА"""
        self.clear_frame()
        self.addFriend = AddFriend(self.widget_frame, self.connection, self.cursor)
        self.addFriend.pack(expand=True, fill=tk.BOTH)

    def load_listFriends(self):
        """Загружает Виджета СПИСОК ДРУЗЕЙ"""
        self.clear_frame()
        self.listFriends = ListFriends(self.widget_frame, self.connection, self.cursor)
        self.listFriends.pack(expand=True, fill=tk.BOTH)

    def load_create_new_account(self):
        """Загружает Виджета СОЗДАНИЯ НОВОГО АККАУНТА"""
        self.clear_frame()
        self.create_new_account = AddAccount(self.widget_frame, self.connection, self.cursor)
        self.create_new_account.pack(expand=True, fill=tk.BOTH)

    def load_list_accounts(self):
        """Загружает Виджета СПИСОК ВСЕХ АККАУНТОВ"""
        self.clear_frame()
        self.list_accounts = ListAccounts(self.widget_frame, self.connection, self.cursor)
        self.list_accounts.pack(expand=True, fill=tk.BOTH)

    def load_add_new_connection_parameters(self):
        """Загружает Виджета ДОБАВЛЕНИЯ НОВОГО ХОСТА"""
        self.clear_frame()
        self.add_new_connection_parameters = AddNewConnectionParameters(self.widget_frame, self.connection, self.cursor)
        self.add_new_connection_parameters.pack(expand=True, fill=tk.BOTH)

    def load_list_connections(self):
        """Загружает Виджета СПИСОК ДОСТУПНЫХ ХОСТОВ"""
        self.clear_frame()
        self.list_connections = ListConnections(self.widget_frame, self.connection, self.cursor)
        self.list_connections.pack(expand=True, fill=tk.BOTH)

    def load_info(self):
        """Загружает Виджета Информация"""
        self.clear_frame()
        self.info = Info(self.widget_frame, self.connection, self.cursor)
        self.info.pack(expand=True, fill=tk.BOTH)            

    def clear_frame(self):
        """Удаляет все виджеты из фрейма для загрузки."""
        for widget in self.widget_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
    close_db_connection(app.connection)
