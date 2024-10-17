from datetime import datetime 
import customtkinter as ctk
from tkcalendar import Calendar
from database_repair import DatabaseRepair

class CalendarWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Календарь")
        self.geometry("400x400")
        self.resizable(False, False)

        self.attributes('-topmost', True)

        today = datetime.today()
        current_year = today.year
        current_month = today.month
        current_day = today.day

        self.calendar = Calendar(self, selectmode='day', year=current_year, month=current_month, day=current_day)
        self.calendar.pack(padx=10, pady=10)

        self.task_entry = ctk.CTkEntry(self, placeholder_text="Введите задачу")
        self.task_entry.pack(pady=10)

        # Use CTkButton instead of CTkEntry for buttons with commands
        save_button = ctk.CTkButton(self, text="Добавить задачу", command=self.add_task)
        save_button.pack(pady=(0, 5))

        delete_button = ctk.CTkButton(self, text="Удалить задачу", command=self.delete_task)
        delete_button.pack(pady=(0, 10))

        self.tasks_listbox = ctk.CTkTextbox(self, width=300, height=150)
        self.tasks_listbox.pack(padx=10, pady=10)
        self.tasks_listbox.configure(state='normal')

        self.calendar.bind("<Double-1>", self.open_task_window)
        self.calendar.bind("<<CalendarSelected>>", self.load_tasks)

        close_button = ctk.CTkButton(self, text="Закрыть", command=self.destroy)
        close_button.pack(pady=(0, 10))

        self.database = DatabaseRepair()
        self.load_tasks()

    def load_tasks(self, event=None):
        self.tasks_listbox.configure(state='normal')
        self.tasks_listbox.delete(1.0, 'end')
        selected_date = self.calendar.get_date()
        tasks = self.database.get_all_tasks()
        for task in tasks:
            if task['task_date'] == selected_date:
                self.tasks_listbox.insert('end', f"{task['task']}\n")
        self.tasks_listbox.configure(state='disabled')

    def add_task(self):
        task = self.task_entry.get()
        selected_date = self.calendar.get_date()
        if task:
            self.database.add_task(task, selected_date)
            self.load_tasks(None)
            self.task_entry.delete(0, 'end')

    def delete_task(self):
        selected_task = self.tasks_listbox.get('active')
        if selected_task:
            self.database.delete_task(selected_task)
            self.load_tasks(None)

    def open_task_window(self, event):
        selected_date = self.calendar.get_date()
        TaskWindow(self, selected_date, self.database)


class TaskWindow(ctk.CTkToplevel):
    def __init__(self, parent, date, database):
        super().__init__(parent)
        self.title("Создание задачи")
        self.geometry("300x200")
        self.resizable(False, False)

        date_label = ctk.CTkLabel(self, text=f"Выбранная дата: {date}")
        date_label.pack(pady=10)

        self.task_entry = ctk.CTkEntry(self, placeholder="Введите задачу")
        self.task_entry.pack(pady=10)

        save_button = ctk.CTkButton(self, text="Сохранить", command=lambda: self.save_task(date))
        save_button.pack(pady=10)

        self.database = database

    def save_task(self, date):
        """ Метод для сохранения задачи. """
        task = self.task_entry.get()
        if task:
            self.database.add_task(date, task)
            print(f"Задача на {date}: '{task}' создана!")
        self.destroy()