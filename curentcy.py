import tkinter as tk
from tkinter import messagebox
import requests # type: ignore

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x300")

        # Labels
        tk.Label(root, text="Amount:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(root, text="From Currency:").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(root, text="To Currency:").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(root, text="Result:").grid(row=6, column=0, padx=10, pady=10)
        tk.Label(root, text="exammple: IDR(indonesia ruppiah) to USD (unitide state dolar)").grid(row=4, column=1, padx=20, pady=5)



        # Entry fields
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)
        self.from_currency_entry = tk.Entry(root)
        self.from_currency_entry.grid(row=1, column=1, padx=10, pady=10)
        self.to_currency_entry = tk.Entry(root)
        self.to_currency_entry.grid(row=2, column=1, padx=10, pady=10)

        # Result display
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=6, column=1, padx=10, pady=10)

        # Buttons
        tk.Button(root, text="Convert", command=self.convert_currency).grid(row=5, column=0, padx=10, pady=10)
        tk.Button(root, text="Clear", command=self.clear_fields).grid(row=5, column=1, padx=10, pady=10)
        tk.Button(root, text="Exit", command=root.quit).grid(row=7, column=1, padx=10, pady=10)

    def convert_currency(self):
        amount = self.amount_entry.get()
        from_currency = self.from_currency_entry.get().upper()
        to_currency = self.to_currency_entry.get().upper()

        if not amount or not from_currency or not to_currency:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a numeric value.")
            return

        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)

        if response.status_code != 200:
            messagebox.showerror("Error", "Failed to fetch exchange rates. Please try again later.")
            return

        data = response.json()
        if to_currency not in data['rates']:
            messagebox.showerror("Error", f"Currency {to_currency} not found.")
            return

        rate = data['rates'][to_currency]
        converted_amount = amount * rate
        self.result_label.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")

    def clear_fields(self):
        self.amount_entry.delete(0, tk.END)
        self.from_currency_entry.delete(0, tk.END)
        self.to_currency_entry.delete(0, tk.END)
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
