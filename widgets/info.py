import tkinter as tk
from tkinter import ttk

class Info(tk.Frame):
    """Class to create the 'Info' frame with application details."""

    def __init__(self, parent, connection, cursor):
        """Initialize the frame."""
        super().__init__(parent)  # Create a child window in relation to the parent

        # Data for working with the local database
        self.cursor = cursor
        self.connection = connection

        # Configure background color
        self.configure(bg='#0e1621')

        # Text widget to display information about the application
        info_text = tk.Text(self, wrap=tk.WORD, bg='#0e1621', fg='#ffefe1', font=("Arial", 10), borderwidth=0)
        info_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Configure text styles
        info_text.tag_configure("title", font=("Arial", 16, "bold"), foreground="#ffefe1", spacing3=10)
        info_text.tag_configure("subtitle", font=("Arial", 14, "bold"), foreground="#ffefe1", spacing3=10)
        info_text.tag_configure("body", font=("Arial", 11), foreground="#ffefe1", spacing3=10)

        # Insert formatted text into the Text widget
        info_text.insert(tk.END, "Overview\n", "subtitle")
        info_text.insert(tk.END, (
            "This application is designed to allow two people to establish an encrypted communication channel "
            "without the need for server-side code execution. All you need are two users with PCs and a remote database.\n\n"
        ), "body")
        
        info_text.insert(tk.END, "Getting Started\n", "subtitle")
        info_text.insert(tk.END, (
            "To start a conversation with a person, you need to create an account within the application. Then, add a friend in the application "
            "and create a connection. A connection involves providing the credentials to connect to a remote PostgreSQL database. "
            "After these steps, you and your friend can communicate securely.\n\n"
        ), "body")
        
        info_text.insert(tk.END, "Step-by-step Guide:\n", "subtitle")
        info_text.insert(tk.END, "1. Creating an Account\n", "subtitle")
        info_text.insert(tk.END, (
            "Fill in the form to create an account. After creating the account, you need to share your username and public key with your friend, "
            "and your friend must provide you with the same information.\n\n"
        ), "body")
        
        info_text.insert(tk.END, "2. Adding a Friend\n", "subtitle")
        info_text.insert(tk.END, (
            "Complete the form to add a friend by entering the username and public key that your friend has provided to you.\n\n"
        ), "body")
        
        info_text.insert(tk.END, "3. Adding a Connection\n", "subtitle")
        info_text.insert(tk.END, (
            "Provide the connection details to the remote database. Make sure you and your friend agree on a common connection point to connect to the same database.\n\n"
        ), "body")
        
        info_text.insert(tk.END, "Important Note:\n", "subtitle")
        info_text.insert(tk.END, (
            "Ensure that both you and your friend have access to the same remote database endpoint for the application to function correctly.\n\n"
        ), "body")
        
        # Disable editing of the text widget
        info_text.config(state=tk.DISABLED)
