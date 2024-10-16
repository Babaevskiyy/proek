import customtkinter as ctk
from tkinter import messagebox
from database_repair import DatabaseRepair

class AddConsumableWindow(ctk.CTkToplevel):
    def __init__(self, parent,):
        self.parent = parent 
        self.title("Добавитьь расходник")
        self.geometry("300x300")
        self.resizable(False, False)

        self.label_name = ctk.CTkLabel(self, text="Название расходника:")
        self.label_name.pack(pady=10)

        self.entry_name = ctk.CTkEntry(self)
        self.entry_name.pack(pady=5)

        self.label_quantity = ctk.CTkLabel(self, text="Количество:")
        self.label_quantity.pack(pady=10)

        self.entry_quantity = ctk.CTkEntry(self)
        self.entry_quantity.pack(pady=5)

        self.add_button = ctk.CTkButton(self, text="Добавить", command=self.add_consumable)
        self.add_button.pack(pady=20)

        self.clear_button = ctk.CTkButton(self, text="Очистить", command=self.clear_fields)
        self.clear_button.pack(pady=5)

    def add_consumable(self):
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()

        if name and quantity.isdigit():
            quantity = int(quantity)
            self.parent.database.add_consumable(name, quantity)
            messagebox.showinfo("Успех", f"Расходник '{name}' добавлен.")
            self.parent.update_consumables_list()
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")

    def clear_fields(self):
        self.parent.database.delete_all_consumables()
        messagebox.showinfo("Успех", "Все расходники успешно удалены.")

        self.parent.update_consumables_list()

        self.entry_name.delete(0, 'end')
        self.entry_quantity.delete(0, 'end')
