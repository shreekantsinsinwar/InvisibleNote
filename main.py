# <----------------InvisibleNote---------------->
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from stegano import lsb
import os

THEME_BG = "#7f0909"  
THEME_FG = "gold"

class InvisibleNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("InvisibleNote - Stealthy Secrets in Sight")
        self.root.geometry("700x500")
        self.root.configure(bg=THEME_BG)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=THEME_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=THEME_BG, foreground=THEME_FG, padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", THEME_FG)], foreground=[("selected", THEME_BG)])

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        self.create_embed_tab()
        self.create_reveal_tab()
        self.create_help_tab()

    def create_embed_tab(self):
        tab = tk.Frame(self.tabs, bg=THEME_BG)
        self.tabs.add(tab, text="📝 Embed Secret")

        tk.Label(tab, text="🔍 Choose Cover Image (.png)", fg=THEME_FG, bg=THEME_BG, font=("Georgia", 12)).pack(pady=5)
        tk.Button(tab, text="Browse Image", command=self.browse_image, bg="gold").pack(pady=5)

        tk.Label(tab, text="✍️ Secret Message", fg=THEME_FG, bg=THEME_BG, font=("Georgia", 12)).pack(pady=5)
        self.secret_entry = tk.Text(tab, height=6, width=60)
        self.secret_entry.pack(pady=5)

        tk.Button(tab, text="✨ Embed Secret", command=self.embed_message, bg="gold").pack(pady=10)
        self.image_path = None

    def create_reveal_tab(self):
        tab = tk.Frame(self.tabs, bg=THEME_BG)
        self.tabs.add(tab, text="🔍 Reveal Secret")

        tk.Label(tab, text="📂 Choose Image with Hidden Message", fg=THEME_FG, bg=THEME_BG, font=("Georgia", 12)).pack(pady=5)
        tk.Button(tab, text="Browse Stego Image", command=self.reveal_message, bg="gold").pack(pady=5)

        self.revealed_text = tk.Text(tab, height=6, width=60, fg="black")
        self.revealed_text.pack(pady=10)

    def create_help_tab(self):
        tab = tk.Frame(self.tabs, bg=THEME_BG)
        self.tabs.add(tab, text="📘 How to Use")

        help_text = """
✨ InvisibleNote - Hide Secrets in Plain Sight!

📝 Embed Secret Tab:
1. Choose a .png image (preferably simple, not too small)
2. Write your secret message
3. Click 'Embed Secret' — your new image will be saved with the hidden message

🔍 Reveal Secret Tab:
1. Load a .png image previously embedded
2. InvisibleNote will extract and reveal the hidden message (if any)

⚠️ Notes:
- Only works with .png images (JPEG corrupts stego data)
- Don't compress or edit images after embedding
- File size of the image limits how much text you can embed
"""
        tk.Label(tab, text=help_text, justify="left", wraplength=650, fg=THEME_FG, bg=THEME_BG, font=("Georgia", 11)).pack(padx=10, pady=10)

    def browse_image(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if path:
            self.image_path = path
            messagebox.showinfo("Image Selected", os.path.basename(path))

    def embed_message(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please select a .png image first.")
            return

        secret_msg = self.secret_entry.get("1.0", tk.END).strip()
        if not secret_msg:
            messagebox.showwarning("Empty Message", "Please enter a secret message to embed.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png", title="Save Stego Image")
        if not save_path:
            return

        try:
            secret_image = lsb.hide(self.image_path, secret_msg)
            secret_image.save(save_path)
            messagebox.showinfo("Success", f"Secret embedded and saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to embed secret: {e}")

    def reveal_message(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if not path:
            return

        try:
            message = lsb.reveal(path)
            if message:
                self.revealed_text.delete("1.0", tk.END)
                self.revealed_text.insert(tk.END, message)
                messagebox.showinfo("Secret Found", "Secret message revealed.")
            else:
                messagebox.showwarning("No Secret", "No hidden message found in this image.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reveal secret: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvisibleNoteApp(root)
    root.mainloop()
