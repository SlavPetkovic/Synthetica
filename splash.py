from tkinter import *

def center_window(window, width=1100, height=580):
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

def fade_in(window):
    alpha = window.attributes('-alpha')
    if alpha < 1:
        alpha += 0.05
        window.attributes('-alpha', alpha)
        # Call this function again to increase transparency
        window.after(50, lambda: fade_in(window))

def fade_out(window):
    alpha = window.attributes('-alpha')
    if alpha > 0:
        alpha -= 0.05
        window.attributes('-alpha', alpha)
        # Call this function again to decrease transparency
        window.after(50, lambda: fade_out(window))
    else:
        show_main_window()

def show_main_window():
    splash_root.destroy()
    root = Tk()
    root.title('OpenAI')
    root.iconbitmap('assets/Dalle.png')
    center_window(root)

    main_label = Label(root, text="Main Screen", font=("Helvetica", 18))
    main_label.pack(pady=20)

splash_root = Tk()
splash_root.title("OpenAI")
center_window(splash_root)
splash_root.overrideredirect(True)
# Start with a completely transparent window
splash_root.attributes('-alpha', 0.0)
# Begin the fade in effect
fade_in(splash_root)

splash_label = Label(splash_root, text="OpenAI", font=("Helvetica", 18))
splash_label.pack(pady=20)

# Instead of directly calling main_window, start fade-out after 5000ms
splash_root.after(5000, lambda: fade_out(splash_root))
mainloop()
