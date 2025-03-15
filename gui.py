from keemia2 import balance_equation
import tkinter as tk
from tkinter import ttk
import ctypes
scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)/100
ctypes.windll.shcore.SetProcessDpiAwareness(1)


# GUI
def balance_and_display():
    equation = equation_entry.get()
    try:
        balanced_equation = balance_equation(equation)
        result_label.config(text=balanced_equation)
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# Create the main window
root = tk.Tk()
root.tk.call('tk', 'scaling', 3.0)
root.title("Chemical Equation Balancer")
root.geometry("1000x300")

# Create and place the widgets
frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

equation_label = ttk.Label(frame, text="Enter chemical equation (e.g., 'H2 + O2 = H2O' or 'SO2{2-} + O2 -> SO3{2-}'):")
equation_label.pack(pady=(0, 5))

equation_entry = ttk.Entry(frame, width=50)
equation_entry.pack(pady=5)

balance_button = ttk.Button(frame, text="Balance Equation", command=balance_and_display)
balance_button.pack(pady=5)

result_label = ttk.Label(frame, text="Balanced equation will appear here")
result_label.pack(pady=10)



# Start the main loop
root.mainloop()