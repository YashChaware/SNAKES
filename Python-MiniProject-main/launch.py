import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from game import run_game
from database_manager import dm

dm.initialize_database()

# Tkinter app
def login():
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()
        user = dm.get_user(username, password)
        if user:
            remember = remember_radio.get()
            dm.update_remember(username, remember)
            messagebox.showinfo("Success", "Login successful!")
            root.destroy()
            run_game(username)  # Run Game after successful login
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def signup():
        username = username_entry.get()
        password = password_entry.get()
        if username == "" or password == "":
            messagebox.showerror("Error", "Username and password cannot be empty")
            return
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return
        if username == password:
            messagebox.showerror("Error", "Username and password cannot be same")
            return
        dm.set_user(username, password);
        dm.update_remember(username, remember_radio.get());
        messagebox.showinfo("Success", "Signup successful!")
        root.destroy()
        run_game(username)  # Run Game after successful signup

    def select_user(event):
        selected_user = user_dropdown.get()
        if selected_user:
            username_entry.delete(0, "end")
            password_entry.delete(0, "end")
            username_entry.insert(0, selected_user)
            password, remember = dm.get_selected_data(selected_user)
            password_entry.insert(0, password)
            remember_radio.set("Once" if remember == 0 else "Always")
            enable_radio_checkbutton.state(["!selected"])

    def toggle_radio_state():
        if enable_radio_var.get() == 1:
            once_radio.configure(state="normal")
            always_radio.configure(state="normal")
        else:
            once_radio.configure(state="disabled")
            always_radio.configure(state="disabled")

    root = tk.Tk()
    root.title("Login")

    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Username label
    username_label = ttk.Label(root, text="Username:")
    username_label.pack(anchor="w", padx=10, pady=(10, 0))

    # Username entry
    username_entry = ttk.Entry(root)
    username_entry.pack(fill="x", padx=10)

    # Password label
    password_label = ttk.Label(root, text="Password:")
    password_label.pack(anchor="w", padx=10, pady=(10, 0))

    # Password entry
    password_entry = ttk.Entry(root, show="*")
    password_entry.pack(fill="x", padx=10)

    # Enable radio buttons checkbutton
    enable_radio_var = tk.IntVar()
    enable_radio_checkbutton = ttk.Checkbutton(
        root,
        text="Remember Me",
        variable=enable_radio_var,
        command=toggle_radio_state,
    )
    enable_radio_checkbutton.pack(anchor="w", padx=10, pady=(10, 0))

    # Remember radio buttons
    remember_frame = ttk.Frame(root)
    remember_frame.pack(anchor="w", padx=10, pady=(10, 0))

    remember_radio = tk.StringVar(value="Always")

    once_radio = ttk.Radiobutton(
        remember_frame,
        text="Once",
        variable=remember_radio,
        value="Once",
        state="disabled",
    )
    once_radio.pack(side="left")

    always_radio = ttk.Radiobutton(
        remember_frame,
        text="Always",
        variable=remember_radio,
        value="Always",
        state="disabled",
    )
    always_radio.pack(side="left")

    # User dropdown
    user_dropdown = ttk.Combobox(root, state="readonly")
    user_dropdown.set("Select User to Auto Fill")
    user_dropdown.pack(fill="x", padx=10, pady=(10, 0))
    user_dropdown.bind("<<ComboboxSelected>>", select_user)

    # Button frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Login button
    login_button = ttk.Button(button_frame, text="Login", command=validate_login)
    login_button.pack(side="left", padx=10)

    # Signup button
    signup_button = ttk.Button(button_frame, text="Signup", command=signup)
    signup_button.pack(side="left", padx=10)

    # Forgot Password link
    def show_forgot_password():
        def forgot_password():
            username = username_entry_fp.get()
            new_password = new_password_entry.get()
            dm.update_password(username, new_password)
            messagebox.showinfo("Password Updated", "Your password has been updated.")
            forgot_password_window.destroy()

        forgot_password_window = tk.Toplevel(root)
        forgot_password_window.title("Forgot Password")
        forgot_password_window.geometry("300x150")

        username_label = ttk.Label(forgot_password_window, text="Username:")
        username_label.pack(anchor="w", padx=10, pady=(10, 0))

        username_entry_fp = ttk.Entry(forgot_password_window)
        username_entry_fp.pack(fill="x", padx=10)

        new_password_label = ttk.Label(forgot_password_window, text="New Password:")
        new_password_label.pack(anchor="w", padx=10, pady=(10, 0))

        new_password_entry = ttk.Entry(forgot_password_window, show="*")
        new_password_entry.pack(fill="x", padx=10)

        update_button = ttk.Button(
            forgot_password_window, text="Update Password", command=forgot_password
        )
        update_button.pack(pady=10)

        forgot_password_window.mainloop()

    forgot_password_link = tk.Label(
        root, text="Forgot Password?", fg="blue", cursor="hand2"
    )
    forgot_password_link.pack(pady=10)
    forgot_password_link.bind("<Button-1>", lambda event: show_forgot_password())

    user_dropdown["values"] = dm.get_remembered_users()

    root.mainloop()


login()

dm.close_database()
