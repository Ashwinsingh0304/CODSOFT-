import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.minsize(320, 400)
        self.root.configure(bg="#1C1C1E")

        self.expression = ""
        self.display_var = tk.StringVar()

        # Display Entry
        self.display = tk.Entry(
            root,
            textvariable=self.display_var,
            font=("Helvetica Neue", 28),
            bg="#1C1C1E",
            fg="white",
            insertbackground="white",
            bd=0,
            highlightthickness=0,
            relief=tk.FLAT,
            justify='right'
        )
        self.display.pack(fill='x', padx=15, pady=(20, 10), ipady=15)

        # Buttons frame
        btns_frame = tk.Frame(root, bg="#2C2C2E")
        btns_frame.pack(fill='both', expand=True, padx=10, pady=10)

        for i in range(5):
            btns_frame.rowconfigure(i, weight=1)
        for j in range(4):
            btns_frame.columnconfigure(j, weight=1)

        # Button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('/', 4, 3),
            ('.', 5, 0), ('⌫', 5, 1), ('(', 5, 2), (')', 5, 3),
        ]

        for (text, row, col) in buttons:
            bg_color = "#3A3A3C"
            fg_color = "white"

            if text == '=':
                bg_color = "#FFD700"
                fg_color = "black"
            elif text in '+-*/()':
                bg_color = "#565656"
            elif text == 'C':
                bg_color = "#FF453A"
            elif text == '⌫':
                bg_color = "#5E5CE6"

            btn = tk.Button(
                btns_frame, text=text,
                font=("Helvetica Neue", 18, "bold"),
                bg=bg_color, fg=fg_color,
                bd=0,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5, ipadx=10, ipady=10)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                result = str(eval(self.expression))
                self.expression = result
            except ZeroDivisionError:
                messagebox.showerror("Error", "Cannot divide by zero")
                self.expression = ""
            except Exception:
                messagebox.showerror("Error", "Invalid input")
                self.expression = ""
        elif char == '⌫':
            self.expression = self.expression[:-1]
        else:
            self.expression += str(char)

        self.display_var.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
