import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet


class EncryptPad(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("EncryptPad")
        self.pack(fill=tk.BOTH, expand=1)

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=1)

        self.textarea = tk.Text(main_frame, undo=True, bg='black', fg='#00ff00', font=('Courier', 14))
        self.textarea.pack(fill=tk.BOTH, expand=1)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        save_button = tk.Button(button_frame, text="Save", command=self.save_file)
        save_button.pack(side=tk.LEFT, padx=10, pady=5)

        load_button = tk.Button(button_frame, text="Load", command=self.open_file)
        load_button.pack(side=tk.LEFT, padx=10, pady=5)

        key_frame = tk.Frame(main_frame)
        key_frame.pack(side=tk.TOP, fill=tk.X)

        self.key_var = tk.StringVar()
        self.key_var.set("vyJpTGa-ebn9GJdKvzY1I_RQ2n0xMxWQf_wLPBkC-zc=")
        key_label = tk.Label(key_frame, text="Key:")
        key_label.pack(side=tk.LEFT, padx=5)
        self.key_entry = tk.Entry(key_frame, textvariable=self.key_var, width=50)
        self.key_entry.pack(side=tk.LEFT, padx=5)

        key_button_frame = tk.Frame(key_frame)
        key_button_frame.pack(side=tk.RIGHT, padx=5, pady=5)

        new_key_frame = tk.Frame(key_frame)
        new_key_frame.pack(side=tk.RIGHT, padx=2, pady=5)

        generate_key_button = tk.Button(new_key_frame, text="Generate New Key", command=self.generate_key)
        generate_key_button.pack(side=tk.LEFT, padx=1)

        key_label_frame = tk.Frame(main_frame)
        key_label_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.key_label_var = tk.StringVar()
        self.key_label_var.set("Encryption Key: " + self.key_var.get())
        self.key_label = tk.Label(key_label_frame, textvariable=self.key_label_var)
        self.key_label.pack(side=tk.LEFT, padx=5)

        encrypt_button = tk.Button(button_frame, text="Encrypt", command=self.encrypt_file)
        encrypt_button.pack(side=tk.LEFT, padx=10, pady=5)

        decrypt_button = tk.Button(button_frame, text="Decrypt", command=self.decrypt_file)
        decrypt_button.pack(side=tk.LEFT, padx=10, pady=5)


    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                text = self.textarea.get(1.0, tk.END)
                file.write(text)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                text = file.read()
                self.textarea.delete(1.0, tk.END)
                self.textarea.insert(tk.END, text)

    def encrypt_file(self):
        key = self.key_var.get().encode()
        f = Fernet(key)
        encrypted_text = f.encrypt(self.textarea.get(1.0, tk.END).encode())
        self.textarea.delete(1.0, tk.END)
        self.textarea.insert(tk.END, encrypted_text.decode())

    def decrypt_file(self):
        key = self.key_var.get().encode()
        f = Fernet(key)
        decrypted_text = f.decrypt(self.textarea.get(1.0, tk.END).encode())
        self.textarea.delete(1.0, tk.END)
        self.textarea.insert(tk.END, decrypted_text.decode())


    def generate_key(self):
        # Generate a new key
        key = Fernet.generate_key()

        # Set the key variable
        self.key_var.set(key.decode())

        # Update the key label
        self.key_label_var.set("Encryption Key: " + self.key_var.get())


if __name__ == '__main__':
    root = tk.Tk()
    app = EncryptPad(master=root)
    root.geometry("700x600")
    root.mainloop()
