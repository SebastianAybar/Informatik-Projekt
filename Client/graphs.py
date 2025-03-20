import sys
import tkinter as tk
import matplotlib.pyplot as plt
import tkcalendar as cal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from SensorData import SensordataList


options = ["jumps", "walkingSteps", "squats", "situps", "pushups", "averageSpeed"]
root = tk.Tk()
figure = None
listing = SensordataList()

def writeData(data):
    listing.writeData(data)

def display():
    root.title("Jump")
    root.geometry("1000x600")
    root.configure(bg="#99aab5")
    return root

def beenden():
    root.destroy()
    sys.exit()

def on_select_activity(activity,frame_bottom, diagramFrame):
    if diagramFrame:
        diagramFrame.destroy() 
    selecting(activity.get(), frame_bottom, diagramFrame)

def show_chart(canvas_bottom):
        for widget in canvas_bottom.winfo_children():
            widget.destroy()  
        canvas = FigureCanvasTkAgg(figure, master=canvas_bottom)
        canvas.draw()
        canvas.get_tk_widget().pack()
        return canvas

def hide_chart(canvas_bottom):
    for widget in canvas_bottom.winfo_children():
        widget.destroy()        

def setup():
    
    display()

    # left Side 
    frame = tk.Frame(root)
    frame.configure(bg="#99aab5")
    frame.pack(side = tk.LEFT, padx= 20)

    # Right Side
    diagramm = tk.Frame(root)
    diagramm.configure(bg="#99aab5")
    diagramm.pack(side= tk.RIGHT, padx= 20)

    calender = cal.Calendar(frame, selectmode = 'day',
               year = 2020, month = 5,
               day = 22)
    calender.pack(pady=20)

    dropdown_label = tk.Label(frame, text="Wähle aktivität", font=("Arial", 12),bg="#99aab5")
    dropdown_label.pack(pady=0)


    selected_activity = tk.StringVar()
    selected_activity.set(options[0])
    selected_activity.trace_add("write", lambda *args: on_select_activity(selected_activity, frame_bottom, diagramm))

    dropdown_menu = tk.OptionMenu(frame, selected_activity, *options)
    dropdown_menu.pack(pady= 10)

    beendenknopf = tk.Button(frame, text="Beenden", width=25, command=beenden)
    beendenknopf.pack(pady=10)

    # Display Jumps as default in the bottom canvas on startup
    display_jumps(diagramm)

    # Display the data for the selected activity

    root.mainloop()

def selecting(activity , frame_bottom, diagramFrame):
    if activity == "averageSpeed":
        display_average_speed(diagramFrame ,frame_bottom)
    elif activity == "jumps":
        display_jumps(diagramFrame,frame_bottom)
    elif activity == "walkingSteps":
        display_walking_steps(diagramFrame,frame_bottom)
    elif activity == "squats":
        display_squats(diagramFrame,frame_bottom)
    elif activity == "situps":
        display_situps(diagramFrame,frame_bottom)
    elif activity == "pushups":
        display_pushups(diagramFrame,frame_bottom)


# Methods for each activity (with bar chart functionality)
def display_jumps(window):
    label = tk.Label(window, text="Displaying Jump Data...", font=("Arial", 12), bg="#99aab5")
    label.pack(pady= 20)

    # Example data for jumps
    days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
    jumps = [30, 25, 35, 28, 33]  # Example jumps data

    # Create a bar chart for the jumps data
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(days, jumps, color='blue')

    ax.set_xlabel('Days')
    ax.set_ylabel('Jumps')
    ax.set_title('Jumps per Day')
    global figure
    figure = fig

    for widget in window.winfo_children():
        widget.destroy()  
        canvas = FigureCanvasTkAgg(figure, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    

    # Adding labels and entry fields below the chart for additional inputs
    # Label for Anzahl Schritte pro Woche (Steps per week)
    """
    steps_label = tk.Label(window, text="Anzahl Schritte pro Woche", font=("Arial", 12), bg="#99aab5")
    steps_label.pack(pady=20)

    steps_label2 = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    steps_label2.pack(pady=20)


    # Label for test1
    test1_label = tk.Label(window, text="8", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.pack(pady=20)
    test1_label = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.pack(pady=20)


    test2_label = tk.Label(window, text="test2", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test2_label.pack(pady=20)
    test1_label = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.pack(pady=20)
    """


def display_walking_steps(window, canvas_bottom):
    label = tk.Label(window, text="Displaying Walking Steps Data...", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    label.pack(pady=10)

    # Example data for walking steps
    days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
    steps = [1000, 1500, 1200, 1700, 1800]
    steps_label = tk.Label(window, text="Anzahl Schritte pro Woche", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    steps_label.place(x=350, y=80)

    steps_label2 = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    steps_label2.place(x=350, y=120)

    # Label for test1
    test1_label = tk.Label(window, text="8", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=600, y=80)
    test1_label = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=600, y=120)

    test2_label = tk.Label(window, text="test2", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test2_label.place(x=750, y=80)
    test1_label = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=810, y=120)
    # Create a bar chart for the walking steps data
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(days, steps, color='green')

    ax.set_xlabel('Days')
    ax.set_ylabel('Steps')
    ax.set_title('Walking Steps per Day')

    # Show and hide functions for the chart
    def show_chart():
        canvas = FigureCanvasTkAgg(fig, master=canvas_bottom)
        canvas.draw()
        canvas.get_tk_widget().pack()
        return canvas

    def hide_chart():
        for widget in canvas_bottom.winfo_children():
            widget.destroy()

    # Buttons for Show and Hide functionality
    show_button = tk.Button(window, text="Show", width=25, command=show_chart)
    show_button.place(x=50, y=130)

    hide_button = tk.Button(window, text="Hide", width=25, command=hide_chart)
    hide_button.place(x=50, y=230)

def display_squats(window, canvas_bottom):
    label = tk.Label(window, text="Displaying Squats Data...", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    label.pack(pady=10)

    steps_label = tk.Label(window, text="Anzahl Steps pro Woche", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    steps_label.place(x=350, y=80)

    steps_label2 = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    steps_label2.place(x=350, y=120)


    test1_label = tk.Label(window, text="8", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=600, y=80)
    test1_label = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=600, y=120)

    test2_label = tk.Label(window, font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test2_label.place(x=750, y=80)
    test1_label = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=810, y=120)

    # Example data for squats
    days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
    squats = [50, 40, 60, 55, 45]  # Example squats data

    # Create a bar chart for the squats data
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(days, squats, color='purple')

    ax.set_xlabel('Days')
    ax.set_ylabel('Squats')
    ax.set_title('Squats per Day')


    def show_chart():
        canvas = FigureCanvasTkAgg(fig, master=canvas_bottom)
        canvas.draw()
        canvas.get_tk_widget().pack()
        return canvas

    def hide_chart():
        for widget in canvas_bottom.winfo_children():
            widget.destroy()


    show_button = tk.Button(window, text="Show", width=25, command=show_chart)
    show_button.place(x=50, y=130)

    hide_button = tk.Button(window, text="Hide", width=25, command=hide_chart)
    hide_button.place(x=50, y=230)

def display_situps(window, canvas_bottom):
    label = tk.Label(window, text="Displaying Situps Data...", font=("Arial", 12), bg="#99aab5")
    label.pack(pady=10)

    # Example data for situps
    days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
    situps = [40, 60, 55, 45, 50]  # Example situps data
    # Adding labels and entry fields below the chart for additional inputs
    # Label for Anzahl Schritte pro Woche (Steps per week)
    steps_label = tk.Label(window, text="Anzahl Situps pro Woche", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    steps_label.place(x=350, y=80)

    steps_label2 = tk.Label(window, text="7",font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    steps_label2.place(x=350, y=120)

    # Label for test1
    test1_label = tk.Label(window, text="8",font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=600, y=80)
    test1_label = tk.Label(window, text="7",font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=600, y=120)

    test2_label = tk.Label(window, text="test2", font=("Arial", 12), bg="#99aab5")
    test2_label.place(x=750, y=80)
    test1_label = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=810, y=120)
    # Create a bar chart for the situps data
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(days, situps, color='orange')

    ax.set_xlabel('Days')
    ax.set_ylabel('Situps')
    ax.set_title('Situps per Day')

    # Show and hide functions for the chart
    def show_chart():
        canvas = FigureCanvasTkAgg(fig, master=canvas_bottom)
        canvas.draw()
        canvas.get_tk_widget().pack()
        return canvas

    def hide_chart():
        for widget in canvas_bottom.winfo_children():
            widget.destroy()

    # Buttons for Show and Hide functionality
    show_button = tk.Button(window, text="Show", width=25, command=show_chart)
    show_button.place(x=50, y=130)

    hide_button = tk.Button(window, text="Hide", width=25, command=hide_chart)
    hide_button.place(x=50, y=230)

def display_pushups(window, canvas_bottom):
    label = tk.Label(window, text="Displaying Pushups Data...", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    label.pack(pady=10)

    # Example data for pushups
    days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
    pushups = [20, 25, 30, 28, 35]  # Example pushups data
    # Adding labels and entry fields below the chart for additional inputs
    # Label for Anzahl Schritte pro Woche (Steps per week)
    steps_label = tk.Label(window, text="Anzahl Schritte pro Woche", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    steps_label.place(x=350, y=80)

    steps_label2 = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    steps_label2.place(x=350, y=120)

    # Label for test1
    test1_label = tk.Label(window, text="8", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=600, y=80)
    test1_label = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=600, y=120)

    test2_label = tk.Label(window, text="test2", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test2_label.place(x=750, y=80)
    test1_label = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=810, y=120)
    # Create a bar chart for the pushups data
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(days, pushups, color='red')

    ax.set_xlabel('Days')
    ax.set_ylabel('Pushups')
    ax.set_title('Pushups per Day')

    # Show and hide functions for the chart
    def show_chart():
        canvas = FigureCanvasTkAgg(fig, master=canvas_bottom)
        canvas.draw()
        canvas.get_tk_widget().pack()
        return canvas

    def hide_chart():
        for widget in canvas_bottom.winfo_children():
            widget.destroy()


    show_button = tk.Button(window, text="Show", width=25, command=show_chart)
    show_button.place(x=50, y=130)

    hide_button = tk.Button(window, text="Hide", width=25, command=hide_chart)
    hide_button.place(x=50, y=230)

def display_average_speed(window, canvas_bottom):
    label = tk.Label(window, text="Displaying Average Speed Data per Day...", font=("Arial", 12), bg="#99aab5")
    label.pack(pady=10)

    days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
    avg_speed = [5.1, 4.8, 6.0, 5.5, 5.9]  # Example average speeds (km/h)
    # Adding labels and entry fields below the chart for additional inputs
    # Label for Anzahl Schritte pro Woche (Steps per week)
    steps_label = tk.Label(window, text="Anzahl Schritte pro Woche", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    steps_label.place(x=350, y=80)

    steps_label2 = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    steps_label2.place(x=350, y=120)


    test1_label = tk.Label(window, text="8", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=600, y=80)
    test1_label = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=600, y=120)

    test2_label = tk.Label(window, text="test2", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test2_label.place(x=750, y=80)
    test1_label = tk.Label(window, text="7", font=("Comic Sans MS", 12, 'bold'), bg="white", fg="green")
    test1_label.place(x=810, y=120)

    # Create a bar chart for the average speed per day
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(days, avg_speed, color='blue')

    ax.set_xlabel('Days')
    ax.set_ylabel('Geschwindigkeit (km/h)')
    ax.set_title('Average Speed per Day')

    # Show and hide functions for the chart
    def show_chart():
        canvas = FigureCanvasTkAgg(fig, master=canvas_bottom)
        canvas.draw()
        canvas.get_tk_widget().pack()
        return canvas

    def hide_chart():
        for widget in canvas_bottom.winfo_children():
            widget.destroy()


    show_button = tk.Button(window, text="Show", width=25, command=show_chart)
    show_button.place(x=50, y=130)

    hide_button = tk.Button(window, text="Hide", width=25, command=hide_chart)
    hide_button.place(x=50, y=230)



