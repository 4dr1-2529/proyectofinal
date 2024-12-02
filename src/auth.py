import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import random
import string


# Configuración de base de datos
DB_NAME = "password_manager.db"


def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
        # Tabla de contraseñas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT,
                name TEXT,
                username TEXT,
                password TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)


# Funciones de base de datos
def register_user(username, password, email):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False  # Usuario o correo ya existe


def validate_login(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        return user[0] if user else None


def save_password(user_id, category, name, username, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO passwords (user_id, category, name, username, password)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, category, name, username, password))
        conn.commit()


def get_passwords(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category, name, username, password FROM passwords WHERE user_id = ?", (user_id,))
        return cursor.fetchall()


def update_password(user_id, old_password, new_password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE id = ?", (user_id,))
        current_password = cursor.fetchone()
        if current_password and current_password[0] == old_password:
            cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
            conn.commit()
            return True
        return False


# Función para generar contraseñas seguras
def generate_secure_password(base_password):
    length = max(10, len(base_password) + random.randint(4, 6))  # Aseguramos que la contraseña sea suficientemente larga
    characters = string.ascii_letters + string.digits + string.punctuation
    random_chars = ''.join(random.choices(characters, k=length - len(base_password)))
    suggested_password = base_password + random_chars
    suggested_password = ''.join(random.sample(suggested_password, len(suggested_password)))  # Mezclar todo
    return suggested_password


# Funciones de interfaz gráfica
def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()


def login_window(root):
    clear_window(root)
    root.geometry("400x300")
    root.title("Iniciar sesión")

    tk.Label(root, text="Usuario:").pack(pady=10)
    entry_username = tk.Entry(root)
    entry_username.pack(pady=10)

    tk.Label(root, text="Contraseña:").pack(pady=10)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=10)

    def validate():
        username = entry_username.get()
        password = entry_password.get()
        user_id = validate_login(username, password)
        if user_id:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            password_manager_window(root, user_id)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    tk.Button(root, text="Iniciar sesión", command=validate).pack(pady=5)
    tk.Button(root, text="Registrarse", command=lambda: register_window(root)).pack(pady=5)
    tk.Button(root, text="Olvidaste tu contraseña", command=lambda: forgot_password_window(root)).pack(pady=5)


def register_window(root):
    clear_window(root)
    root.geometry("400x350")
    root.title("Registrarse")

    tk.Label(root, text="Usuario:").pack(pady=10)
    entry_username = tk.Entry(root)
    entry_username.pack(pady=10)

    tk.Label(root, text="Contraseña:").pack(pady=10)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=10)

    tk.Label(root, text="Correo electrónico:").pack(pady=10)
    entry_email = tk.Entry(root)
    entry_email.pack(pady=10)

    def register():
        username = entry_username.get()
        password = entry_password.get()
        email = entry_email.get()
        if register_user(username, password, email):
            messagebox.showinfo("Éxito", "Usuario registrado")
            login_window(root)
        else:
            messagebox.showerror("Error", "El usuario o correo ya existen")

    tk.Button(root, text="Registrar", command=register).pack(pady=5)
    tk.Button(root, text="Volver", command=lambda: login_window(root)).pack(pady=5)


def forgot_password_window(root):
    clear_window(root)
    root.geometry("400x300")
    root.title("Recuperar Contraseña")

    tk.Label(root, text="Correo electrónico:").pack(pady=10)
    entry_email = tk.Entry(root)
    entry_email.pack(pady=10)

    def send_password():
        email = entry_email.get()
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            if result:
                messagebox.showinfo("Éxito", f"Tu contraseña es: {result[0]}")
            else:
                messagebox.showerror("Error", "No se encontró un usuario con ese correo electrónico.")

    tk.Button(root, text="Enviar contraseña", command=send_password).pack(pady=5)
    tk.Button(root, text="Volver", command=lambda: login_window(root)).pack(pady=5)


def password_manager_window(root, user_id):
    clear_window(root)
    root.geometry("400x500")
    root.title("Gestor de Contraseñas")

    tk.Label(root, text="Bienvenido al gestor de contraseñas", font=("Helvetica", 14)).pack(pady=10)

    tk.Button(root, text="Ver contraseñas", command=lambda: view_passwords_window(root, user_id)).pack(pady=5)
    tk.Button(root, text="Guardar contraseña", command=lambda: save_password_window(root, user_id)).pack(pady=5)
    tk.Button(root, text="Generar contraseña segura", command=lambda: generate_password_window(root, user_id)).pack(pady=5)
    tk.Button(root, text="Cambiar contraseña", command=lambda: change_password_window(root, user_id)).pack(pady=5)
    tk.Button(root, text="Cerrar sesión", command=lambda: login_window(root)).pack(pady=5)


def view_passwords_window(root, user_id):
    clear_window(root)
    root.geometry("500x400")
    root.title("Ver contraseñas")

    passwords = get_passwords(user_id)

    tree = ttk.Treeview(root, columns=("Categoría", "Nombre", "Usuario", "Contraseña"), show="headings")
    tree.heading("Categoría", text="Categoría")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Usuario", text="Usuario")
    tree.heading("Contraseña", text="Contraseña")

    for pwd in passwords:
        tree.insert("", "end", values=pwd)

    tree.pack(fill="both", expand=True)

    tk.Button(root, text="Volver", command=lambda: password_manager_window(root, user_id)).pack(pady=10)


def generate_password_window(root, user_id):
    clear_window(root)
    root.geometry("400x300")
    root.title("Generar contraseña segura")

    tk.Label(root, text="Contraseña base:").pack(pady=10)
    entry_base_password = tk.Entry(root)
    entry_base_password.pack(pady=10)

    tk.Label(root, text="Contraseña sugerida:").pack(pady=10)
    entry_suggested_password = tk.Entry(root, state="readonly")
    entry_suggested_password.pack(pady=10)

    def generate():
        base_password = entry_base_password.get()
        if len(base_password) >= 4:  # Asegura que la base tenga longitud mínima
            suggested_password = generate_secure_password(base_password)
            entry_suggested_password.config(state="normal")
            entry_suggested_password.delete(0, tk.END)
            entry_suggested_password.insert(0, suggested_password)
            entry_suggested_password.config(state="readonly")
        else:
            messagebox.showerror("Error", "La contraseña base debe tener al menos 4 caracteres.")

    tk.Button(root, text="Generar", command=generate).pack(pady=5)
    tk.Button(root, text="Volver", command=lambda: password_manager_window(root, user_id)).pack(pady=5)


def save_password_window(root, user_id):
    clear_window(root)
    root.geometry("400x400")
    root.title("Guardar contraseña")

    tk.Label(root, text="Categoría:").pack(pady=10)
    entry_category = tk.Entry(root)
    entry_category.pack(pady=10)

    tk.Label(root, text="Nombre del servicio:").pack(pady=10)
    entry_name = tk.Entry(root)
    entry_name.pack(pady=10)

    tk.Label(root, text="Usuario:").pack(pady=10)
    entry_username = tk.Entry(root)
    entry_username.pack(pady=10)

    tk.Label(root, text="Contraseña:").pack(pady=10)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=10)

    def save():
        category = entry_category.get()
        name = entry_name.get()
        username = entry_username.get()
        password = entry_password.get()
        save_password(user_id, category, name, username, password)
        messagebox.showinfo("Éxito", "Contraseña guardada")
        password_manager_window(root, user_id)

    tk.Button(root, text="Guardar", command=save).pack(pady=5)
    tk.Button(root, text="Volver", command=lambda: password_manager_window(root, user_id)).pack(pady=5)


def change_password_window(root, user_id):
    clear_window(root)
    root.geometry("400x300")
    root.title("Cambiar contraseña")

    tk.Label(root, text="Contraseña actual:").pack(pady=10)
    entry_old_password = tk.Entry(root, show="*")
    entry_old_password.pack(pady=10)

    tk.Label(root, text="Nueva contraseña:").pack(pady=10)
    entry_new_password = tk.Entry(root, show="*")
    entry_new_password.pack(pady=10)

    tk.Label(root, text="Confirmar nueva contraseña:").pack(pady=10)
    entry_confirm_password = tk.Entry(root, show="*")
    entry_confirm_password.pack(pady=10)

    def change_password():
        old_password = entry_old_password.get()
        new_password = entry_new_password.get()
        confirm_password = entry_confirm_password.get()
        if new_password == confirm_password:
            if update_password(user_id, old_password, new_password):
                messagebox.showinfo("Éxito", "Contraseña cambiada correctamente.")
                password_manager_window(root, user_id)
            else:
                messagebox.showerror("Error", "La contraseña actual es incorrecta.")
        else:
            messagebox.showerror("Error", "Las nuevas contraseñas no coinciden.")

    tk.Button(root, text="Cambiar contraseña", command=change_password).pack(pady=10)
    tk.Button(root, text="Volver", command=lambda: password_manager_window(root, user_id)).pack(pady=5)


if __name__ == "__main__":
    create_tables()

    root = tk.Tk()
    login_window(root)
    root.mainloop()
