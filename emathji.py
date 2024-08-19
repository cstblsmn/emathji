import customtkinter as tk
import pyperclip

SYMBOLS = [
    {'key': '01', 'symbol': '∀', 'name': 'for all'},
    {'key': '02', 'symbol': '∂', 'name': 'partial differential'},
    {'key': '03', 'symbol': '∃', 'name': 'there exists'},
    {'key': '04', 'symbol': '∅', 'name': 'empty set'},
    {'key': '05', 'symbol': '∇', 'name': 'nabla (gradient)'},
    {'key': '06', 'symbol': '∈', 'name': 'element of'},
    {'key': '07', 'symbol': '∉', 'name': 'not an element of'},
    {'key': '08', 'symbol': '∋', 'name': 'contains as member'},
    {'key': '09', 'symbol': '∏', 'name': 'n-ary product (product of a sequence)'},
    {'key': '10', 'symbol': '∑', 'name': 'n-ary summation (sum of a sequence)'},
    {'key': '11', 'symbol': '−', 'name': 'minus sign'},
    {'key': '12', 'symbol': '√', 'name': 'square root'},
    {'key': '13', 'symbol': '∛', 'name': 'cube root'},
    {'key': '14', 'symbol': '∝', 'name': 'proportional to'},
    {'key': '15', 'symbol': '∞', 'name': 'infinity'},
    {'key': '16', 'symbol': '∠', 'name': 'angle'},
    {'key': '17', 'symbol': '∧', 'name': 'logical and'},
    {'key': '18', 'symbol': '∨', 'name': 'logical or'},
    {'key': '19', 'symbol': '∩', 'name': 'intersection'},
    {'key': '20', 'symbol': '∪', 'name': 'union'},
    {'key': '21', 'symbol': '∫', 'name': 'integral'},
    {'key': '22', 'symbol': '∬', 'name': 'double integral'},
    {'key': '23', 'symbol': '∭', 'name': 'triple integral'},
    {'key': '24', 'symbol': '∮', 'name': 'contour integral'},
    {'key': '25', 'symbol': '≈', 'name': 'almost equal to'},
    {'key': '26', 'symbol': '≠', 'name': 'not equal to'},
    {'key': '27', 'symbol': '≡', 'name': 'identical to'},
    {'key': '28', 'symbol': '≤', 'name': 'less than or equal to'},
    {'key': '29', 'symbol': '≥', 'name': 'greater than or equal to'},
    {'key': '30', 'symbol': '⊂', 'name': 'subset of'},
    {'key': '31', 'symbol': '⊃', 'name': 'superset of'},
    {'key': '32', 'symbol': '⊆', 'name': 'subset of or equal to'},
    {'key': '33', 'symbol': '⊇', 'name': 'superset of or equal to'},
    {'key': '34', 'symbol': '⊕', 'name': 'direct sum'},
    {'key': '35', 'symbol': '⊥', 'name': 'perpendicular'},
    {'key': '36', 'symbol': '⋅', 'name': 'dot product'},
    {'key': '37', 'symbol': 'ℕ', 'name': 'natural numbers'},
    {'key': '38', 'symbol': 'ℤ', 'name': 'integers'},
    {'key': '39', 'symbol': 'ℚ', 'name': 'rational numbers'},
    {'key': '40', 'symbol': 'ℝ', 'name': 'real numbers'},
    {'key': '41', 'symbol': 'ℂ', 'name': 'complex numbers'},
    {'key': '42', 'symbol': 'ℵ', 'name': 'aleph (cardinality of infinite sets)'},
    {'key': '43', 'symbol': '∂', 'name': 'partial differential'},
    {'key': '44', 'symbol': '∆', 'name': 'increment (difference)'},
    {'key': '45', 'symbol': 'Α', 'name': 'Alpha (uppercase)'},
    {'key': '46', 'symbol': 'α', 'name': 'Alpha (lowercase)'},
    {'key': '47', 'symbol': 'Β', 'name': 'Beta (uppercase)'},
    {'key': '48', 'symbol': 'β', 'name': 'Beta (lowercase)'},
    {'key': '49', 'symbol': 'Γ', 'name': 'Gamma (uppercase)'},
    {'key': '50', 'symbol': 'γ', 'name': 'Gamma (lowercase)'},
    {'key': '51', 'symbol': 'Δ', 'name': 'Delta (uppercase)'},
    {'key': '52', 'symbol': 'δ', 'name': 'Delta (lowercase)'},
    {'key': '53', 'symbol': 'λ', 'name': 'Lambda (lowercase)'},
    {'key': '54', 'symbol': 'π', 'name': 'Pi (lowercase)'},
    {'key': '55', 'symbol': 'φ', 'name': 'Phi (lowercase)'},
    {'key': '56', 'symbol': 'Ω', 'name': 'Omega (uppercase)'},
    {'key': '57', 'symbol': 'ω', 'name': 'Omega (lowercase)'}
]


class MathPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Picker")
        self.root.geometry("250x300")
        self.root.resizable(False, False)

        # Search bar
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.refresh)

        self.search_entry = tk.CTkEntry(self.root, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, padx=10, pady=10)

        self.frame = tk.CTkFrame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        self.canvas = tk.CTkCanvas(self.frame)
        self.scrollbar = tk.CTkScrollbar(self.frame, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set, scrollregion=self.canvas.bbox("all"))

        self.symbol_frame = tk.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.symbol_frame, anchor="nw")

        self.display_symbols(SYMBOLS)

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<MouseWheel>", self.on_mouse_scroll)
        # Buffer for storing recent keystrokes
        self.key_buffer = ""

    def refresh(self, *args):
        search_query = self.search_var.get().lower()
        filtered_symbols = [
            item for item in SYMBOLS if search_query in item['name'].lower()
        ]
        self.display_symbols(filtered_symbols)

    def to_clipboard(self, symbol_char):
        pyperclip.copy(symbol_char)
        self.root.quit()

    def display_symbols(self, symbol_list):
        for widget in self.symbol_frame.winfo_children():
            widget.destroy()

        for i, item in enumerate(symbol_list):
            key, symbol = item["key"], item["symbol"]
            button = tk.CTkButton(
                self.symbol_frame, 
                text=f"{symbol} ({key}) ",
                font=("Arial", 18),
                width=70,
                command=lambda s=symbol: self.to_clipboard(s)
            )
            button.grid(row=i//3, column=i%3, padx=2, pady=2, sticky="nsew")

        for i in range(2):
            self.symbol_frame.grid_columnconfigure(i, weight=1)

        self.symbol_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_key_press(self, event):
        if event.keysym == "Escape":
            self.root.quit()
            return

        if self.root.focus_get() == self.search_entry:
            return
        
        # Update the key buffer with the new key press and keep the last two characters
        self.key_buffer += event.char.lower()
        self.key_buffer = self.key_buffer[-2:]

        # Check if the key buffer matches any key in SYMBOLS
        for item in SYMBOLS:
            if item['key'] == self.key_buffer:
                self.to_clipboard(item['symbol'])
                self.key_buffer = ""  # Clear the buffer after a successful match
                break
    def on_mouse_scroll(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

if __name__ == "__main__":
    tk.set_appearance_mode("system")  # default
    root = tk.CTk()
    app = MathPicker(root)
    root.mainloop()