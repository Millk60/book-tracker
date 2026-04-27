import tkinter as tk
from tkinter import messagebox, ttk
import json

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("650x500")
        
        self.books = []
        self.load_from_json()
        
        # Поля ввода
        tk.Label(root, text="Название книги:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(root, text="Автор:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.author_entry = tk.Entry(root, width=30)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(root, text="Жанр:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.genre_entry = tk.Entry(root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(root, text="Кол-во страниц:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.pages_entry = tk.Entry(root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Кнопки
        tk.Button(root, text="Добавить книгу", command=self.add_book, bg="green", fg="white").grid(row=4, column=0, columnspan=2, pady=10)
        
        # Фильтрация
        filter_frame = tk.Frame(root)
        filter_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        tk.Label(filter_frame, text="Фильтр по жанру:").pack(side="left", padx=5)
        self.genre_filter = tk.Entry(filter_frame, width=15)
        self.genre_filter.pack(side="left", padx=5)
        
        tk.Label(filter_frame, text="Страниц >").pack(side="left", padx=5)
        self.pages_filter = tk.Entry(filter_frame, width=8)
        self.pages_filter.pack(side="left", padx=5)
        
        tk.Button(filter_frame, text="Фильтровать", command=self.filter_books).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Сбросить", command=self.show_all).pack(side="left", padx=5)
        
        # Таблица
        self.tree = ttk.Treeview(root, columns=("Название", "Автор", "Жанр", "Страницы"), show="headings", height=12)
        self.tree.heading("Название", text="Название")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страницы", text="Страницы")
        self.tree.column("Название", width=180)
        self.tree.column("Автор", width=120)
        self.tree.column("Жанр", width=100)
        self.tree.column("Страницы", width=80)
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        
        # Кнопка удаления
        tk.Button(root, text="Удалить выбранную", command=self.delete_book, bg="red", fg="white").grid(row=7, column=0, columnspan=2, pady=5)
        
        self.show_all()
    
    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()
        
        # Валидация
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        
        try:
            pages = int(pages)
            if pages <= 0:
                messagebox.showerror("Ошибка", "Страниц должно быть больше 0!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return
        
        # Добавление
        self.books.append({
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        })
        
        self.save_to_json()
        self.show_all()
        
        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", "Книга добавлена!")
    
    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите книгу для удаления!")
            return
        
        # Получаем название книги из выбранной строки
        item = self.tree.item(selected[0])
        title = item["values"][0]
        
        # Удаляем из списка
        for i, book in enumerate(self.books):
            if book["title"] == title:
                self.books.pop(i)
                break
        
        self.save_to_json()
        self.show_all()
        messagebox.showinfo("Успех", "Книга удалена!")
    
    def filter_books(self):
        genre = self.genre_filter.get().strip().lower()
        pages_threshold = self.pages_filter.get().strip()
        
        filtered = self.books.copy()
        
        if genre:
            filtered = [b for b in filtered if genre in b["genre"].lower()]
        
        if pages_threshold:
            try:
                threshold = int(pages_threshold)
                filtered = [b for b in filtered if b["pages"] > threshold]
            except ValueError:
                messagebox.showerror("Ошибка", "Фильтр страниц должен быть числом!")
                return
        
        self.update_table(filtered)
    
    def show_all(self):
        self.genre_filter.delete(0, tk.END)
        self.pages_filter.delete(0, tk.END)
        self.update_table(self.books)
    
    def update_table(self, books_list):
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Заполняем
        for book in books_list:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))
    
    def save_to_json(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)
    
    def load_from_json(self):
        try:
            with open("books.json", "r", encoding="utf-8") as f:
                self.books = json.load(f)
        except:
            self.books = []

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()