# gui.py
import os
os.environ.setdefault('DISPLAY', ':0')   # point at HDMI display if needed

import threading
import tkinter as tk

_window = None 

# placeholder until gui thread replaces it
def update(state, door_name=None):
    pass

def _gui_loop():
    window = tk.Tk()
    window.attributes('-fullscreen', True)
    label = tk.Label(window, text='Initializing…', font=('Helvetica', 48))
    label.pack(expand=True)

    def _update(state, door_name=None):
        if state == 'IDLE':
            text = "Idle – Waiting for tag"
        elif state == 'GRANTED':
            text = f"Access Granted\n{door_name}"
        elif state == 'DENIED':
            text = "Access Denied"
        elif state == 'ENROLL':
            text = "Enrollment Mode\nPress door button…"
        elif state == 'SELECT_DOOR':
            text = f"Programming {door_name}\nScan new tag"
        else:
            text = str(state)
        label.config(text=text)

    # bind the real update function
    global update
    update = _update

    # *immediately* switch to IDLE so the label updates
    update('IDLE')

    window.mainloop()

def start():
    t = threading.Thread(target=_gui_loop, daemon=True)
    t.start()

def stop():
    global _window
    if _window:
      _window.quit()
      _window.destroy()
      _window = None
