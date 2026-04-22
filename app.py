import sqlite3
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, ttk


@dataclass
class Client:
    full_name: str
    phone: str
    group_name: str


class Database:
    def __init__(self, db_path: str = "clients.db") -> None:
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    group_name TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add_client(self, client: Client) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clients (full_name, phone, group_name) VALUES (?, ?, ?)",
                (client.full_name, client.phone, client.group_name),
            )
            conn.commit()

    def get_all_clients(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name, phone, group_name FROM clients")
            return cursor.fetchall()


class ClientService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def add_client(self, full_name: str, phone: str, group_name: str) -> bool:
        if not full_name.strip() or not phone.strip() or not group_name.strip():
            return False

        new_client = Client(
            full_name=full_name.strip(),
            phone=phone.strip(),
            group_name=group_name.strip(),
        )
        self.database.add_client(new_client)
        return True

    def list_clients(self):
        return self.database.get_all_clients()


class ClientApp:
    def __init__(self, root: tk.Tk, service: ClientService) -> None:
        self.root = root
        self.service = service

        self.root.title("Система учета клиентов")
        self.root.geometry("700x450")

        self._build_ui()
        self._refresh_table()

    def _build_ui(self) -> None:
        form_frame = tk.LabelFrame(self.root, text="Добавить клиента", padx=10, pady=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(form_frame, text="ФИО:").grid(row=0, column=0, sticky="w")
        self.full_name_entry = tk.Entry(form_frame, width=40)
        self.full_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Телефон:").grid(row=1, column=0, sticky="w")
        self.phone_entry = tk.Entry(form_frame, width=40)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Группа:").grid(row=2, column=0, sticky="w")
        self.group_entry = tk.Entry(form_frame, width=40)
        self.group_entry.grid(row=2, column=1, padx=5, pady=5)

        add_button = tk.Button(
            form_frame, text="Добавить клиента", command=self._on_add_client
        )
        add_button.grid(row=3, column=1, sticky="e", padx=5, pady=10)

        table_frame = tk.LabelFrame(self.root, text="Список клиентов", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        columns = ("id", "full_name", "phone", "group_name")
        self.table = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=10
        )

        self.table.heading("id", text="ID")
        self.table.heading("full_name", text="ФИО")
        self.table.heading("phone", text="Телефон")
        self.table.heading("group_name", text="Группа")

        self.table.column("id", width=50, anchor="center")
        self.table.column("full_name", width=240)
        self.table.column("phone", width=170)
        self.table.column("group_name", width=170)

        self.table.pack(fill="both", expand=True)

    def _on_add_client(self) -> None:
        full_name = self.full_name_entry.get()
        phone = self.phone_entry.get()
        group_name = self.group_entry.get()

        added = self.service.add_client(full_name, phone, group_name)
        if not added:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        self.full_name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.group_entry.delete(0, tk.END)

        self._refresh_table()
        messagebox.showinfo("Готово", "Клиент добавлен")

    def _refresh_table(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)

        clients = self.service.list_clients()
        for client in clients:
            self.table.insert("", tk.END, values=client)


def main() -> None:
    database = Database()
    service = ClientService(database)

    root = tk.Tk()
    ClientApp(root, service)
    root.mainloop()


if __name__ == "__main__":
    main()
