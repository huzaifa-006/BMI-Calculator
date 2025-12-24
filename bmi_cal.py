import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import pyttsx3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)

# Global BMI history
bmi_history = []

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()
 
def calculate_bmi():
    try: 
        height_cm = float(entry_height.get())
        weight = float(entry_weight.get())

        if unit_var.get() == "Imperial":
            height_cm *= 30.48  # ft to cm
            weight *= 0.453592  # lbs to kg

        height_m = height_cm / 100
        bmi = round(weight / (height_m ** 2), 2)

        if bmi < 18.5:
            category, color = "Underweight", "#AED6F1"
        elif bmi < 25:
            category, color = "Normal weight", "#A9DFBF"
        elif bmi < 30:
            category, color = "Overweight", "#F9E79F"
        else:
            category, color = "Obese", "#F5B7B1"

        age = entry_age.get()
        gender = gender_var.get()

        details = f"BMI: {bmi} ({category})"
        if age:
            details += f" | Age: {age}"
        if gender:
            details += f" | Gender: {gender}"

        result_label.config(text=details, bg=color)
        speak(f"Your BMI is {bmi}. You are in the {category} category.")

        # Save to history
        bmi_history.append((datetime.now().strftime("%d %b %H:%M"), bmi))

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")
        speak("Please enter valid values.")

def show_bmi_chart():
    chart_window = tk.Toplevel(root)
    chart_window.title("BMI Classification Chart")
    chart_window.geometry("350x250")
    chart_window.configure(bg="#FBFCFC")
    chart_window.resizable(False, False)

    tk.Label(chart_window, text="BMI Classification Chart", font=("Segoe UI", 14, "bold"), bg="#FBFCFC", fg="#154360").pack(pady=10)
    
    chart_data = [
        ("Below 18.5", "Underweight", "#5695BE"),
        ("18.5 - 24.9", "Normal weight", "#8ADEAC"),
        ("25 - 29.9", "Overweight", "#F9E79F"),
        ("30 and above", "Obese", "#D59993"),
    ]

    for bmi_range, label, color in chart_data:
        frame = tk.Frame(chart_window, bg=color)
        frame.pack(fill="x", padx=20, pady=5)
        tk.Label(frame, text=f"{bmi_range}", font=("Segoe UI", 11, "bold"), width=15, bg=color).pack(side="left", padx=5)
        tk.Label(frame, text=f"{label}", font=("Segoe UI", 11), bg=color).pack(side="left")

def show_bmi_trend():
    if not bmi_history:
        messagebox.showinfo("No Data", "No BMI data to show.")
        return

    trend_window = tk.Toplevel(root)
    trend_window.title("BMI Trend")
    trend_window.geometry("500x400")

    dates, bmis = zip(*bmi_history)
    fig, ax = plt.subplots()
    ax.plot(dates, bmis, marker='o', linestyle='-', color='blue')
    ax.set_title("BMI Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("BMI")
    ax.grid(True)
    fig.autofmt_xdate()

    canvas = FigureCanvasTkAgg(fig, master=trend_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

def toggle_units():
    unit = unit_var.get()
    if unit == "Metric":
        height_label.config(text="Height (cm):")
        weight_label.config(text="Weight (kg):")
    else:
        height_label.config(text="Height (ft):")
        weight_label.config(text="Weight (lbs):")

# GUI setup
root = tk.Tk()
root.title("BMI Calculator - Voice Enabled")
root.geometry("420x520")
root.configure(bg="#ECF0F1")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')

tk.Label(root, text="💪 BMI CALCULATOR", font=("Segoe UI", 18, "bold"), fg="#21618C", bg="#ECF0F1").pack(pady=10)

input_frame = tk.Frame(root, bg="#ECF0F1")
input_frame.pack(pady=10)

unit_var = tk.StringVar(value="Metric")
ttk.Label(input_frame, text="Unit System:", background="#ECF0F1", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="e", pady=5)
ttk.Combobox(input_frame, textvariable=unit_var, values=["Metric", "Imperial"], width=17, state="readonly").grid(row=0, column=1, pady=5)
unit_var.trace("w", lambda *args: toggle_units())

height_label = ttk.Label(input_frame, text="Height (cm):", background="#ECF0F1", font=("Segoe UI", 11))
height_label.grid(row=1, column=0, sticky="e", pady=5)
entry_height = ttk.Entry(input_frame, width=20)
entry_height.grid(row=1, column=1, pady=5)

weight_label = ttk.Label(input_frame, text="Weight (kg):", background="#ECF0F1", font=("Segoe UI", 11))
weight_label.grid(row=2, column=0, sticky="e", pady=5)
entry_weight = ttk.Entry(input_frame, width=20)
entry_weight.grid(row=2, column=1, pady=5)

tk.Label(input_frame, text="Age:", bg="#ECF0F1", font=("Segoe UI", 11)).grid(row=3, column=0, sticky="e", pady=5)
entry_age = ttk.Entry(input_frame, width=20)
entry_age.grid(row=3, column=1, pady=5)

tk.Label(input_frame, text="Gender:", bg="#ECF0F1", font=("Segoe UI", 11)).grid(row=4, column=0, sticky="e", pady=5)
gender_var = tk.StringVar()
gender_combo = ttk.Combobox(input_frame, textvariable=gender_var, values=["Male", "Female", "Other"], state="readonly", width=18)
gender_combo.grid(row=4, column=1, pady=5)
gender_combo.set("Select")

ttk.Button(root, text="Calculate BMI", command=calculate_bmi).pack(pady=10)
ttk.Button(root, text="Show BMI Chart", command=show_bmi_chart).pack(pady=5)
ttk.Button(root, text="Show BMI Trend", command=show_bmi_trend).pack(pady=5)

result_label = tk.Label(root, text="", font=("Segoe UI", 12, "bold"), wraplength=380, bg="#ECF0F1")
result_label.pack(pady=15)

root.mainloop()
