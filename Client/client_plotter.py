import tkinter as tk
import random

# Hauptfenster erstellen
root = tk.Tk()
root.title("Receiver")
root.geometry("1000x600")
root.configure(bg="#99aab5")


# Funktion zum Beenden des Programms
def beenden():
    root.destroy()


# Array mit Sensordaten (hier als Beispiel mit Zufallswerten, du kannst diese durch deine echten Daten ersetzen)
# Sensordaten für 24 Stunden vorübergehend (0 Uhr bis 23 Uhr)
mywords = [random.randint(1, 20) for _ in range(24)]

# Buttons mit genauer Platzierung
button1 = tk.Button(root, text="Show", width=25)
button1.place(x=50, y=130)  # X und Y Position festlegen

button2 = tk.Button(root, text="Hide", width=25)
button2.place(x=50, y=230)

button3 = tk.Button(root, text="Beenden", width=25, command=beenden)
button3.place(x=50, y=330)

# Canvas (Zeichenbereich) mit genauer Positionierung - knallweiß
canvas = tk.Canvas(root, width=700, height=400, bg="#FFFFFF")
canvas.place(x=250, y=50)  # Platziert das Canvas rechts


# Funktion zum Zeichnen der Achsen
def zeichne_achsen():
    width = 700  # Breite des Canvas
    height = 400  # Höhe des Canvas
    x_offset = 50  # Abstand der Punkte von der linken Kante
    y_offset = 350  # Abstand der Punkte von der unteren Kante

    # Zeichne die Achsen (X- und Y-Achse)
    canvas.create_line(x_offset, y_offset, x_offset + width,
                       y_offset, arrow=tk.LAST, width=2, fill="black")  # X-Achse
    canvas.create_line(x_offset, y_offset, x_offset, y_offset -
                       height, arrow=tk.LAST, width=2, fill="black")  # Y-Achse

    # Zeit auf der X-Achse hinzufügen (0 Uhr bis 23 Uhr)
    for i in range(24):
        x = x_offset + i * (width // 24)
        if i % 4 == 0:  # Alle 4 Stunden (0, 4, 8, ..., 20)
            canvas.create_text(
                x, y_offset + 20, text=f"{i}h", anchor=tk.N, font=("Times New Roman", 15))

    # Optionale horizontale Linien für den Bereich der Y-Achse
    for i in range(5):
        y_line = y_offset - (i / 4) * height
        canvas.create_line(x_offset, y_line, x_offset + width,
                           y_line, dash=(2, 2), fill="gray")


# Funktion zum Zeichnen der Punkte
def zeichne_punkte():
    max_wert = max(mywords)
    min_wert = min(mywords)

    width = 700  # Breite des Canvas
    height = 400  # Höhe des Canvas
    x_offset = 50  # Abstand der Punkte von der linken Kante
    y_offset = 350  # Abstand der Punkte von der unteren Kante

    # Zeichne die Punkte für jede Stunde (0 bis 23 Uhr)
    for i in range(24):
        x = x_offset + i * (width // 24)  # X-Position der Punkte
        # Y-Position der Punkte basierend auf den Werten in mywords
        y = y_offset - (mywords[i] / max_wert) * height
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                           fill="blue", outline="blue")  # Punkt zeichnen


# Funktion zum Umschalten der Sichtbarkeit der Punkte
def toggle_punkte():
    # Wenn der "Show"-Button geklickt wird, zeichne die Punkte
    zeichne_punkte()
    # Deaktiviere den Show-Button, wenn er gedrückt wurde
    button1.config(state=tk.DISABLED)
    button2.config(state=tk.NORMAL)  # Aktiviere den Hide-Button


# Funktion zum Ausblenden der Punkte
def hide_punkte():
    canvas.delete("all")  # Lösche alles auf dem Canvas
    zeichne_achsen()  # Zeichne nur die Achsen
    button1.config(state=tk.NORMAL)  # Aktiviere den Show-Button
    button2.config(state=tk.DISABLED)  # Deaktiviere den Hide-Button


# Zeichne die Achsen zu Beginn
zeichne_achsen()

# Button-Event Handler
button1.config(command=toggle_punkte)  # Show-Button zeigt die Punkte
button2.config(command=hide_punkte)  # Hide-Button versteckt die Punkte

# Hauptfenster starten
root.mainloop()
