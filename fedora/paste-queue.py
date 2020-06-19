# You may get an error message that says: “Pyperclip could not find a copy/paste mechanism for your system.
# Please see https://pyperclip.readthedocs.io/en/latest/introduction.html#not-implemented-error for how to fix this.”
#
# In order to work equally well on Windows, Mac, and Linux, Pyperclip uses various mechanisms to do this.
# Currently, this error should only appear on Linux (not Windows or Mac).
# You can fix this by installing one of the copy/paste mechanisms:
#
#    sudo apt-get install xsel to install the xsel utility.
#    sudo apt-get install xclip to install the xclip utility.
#    pip install gtk to install the gtk Python module.
#    pip install PyQt4 to install the PyQt4 Python module.

import clipboard
import keyboard
import queue
import time

q = queue.Queue()
copy = 'ctrl+c'
paste = 'ctrl+v'
esc = 'esc'
first_item = 'first'
just_copied = False

print('Copy hot-key set as : ', copy)
print('Paste hot-key set as : ', paste)
print("Exit hot-key set as : ", esc)


def on_copied():
    time.sleep(0.1)
    global first_item
    global just_copied
    if not just_copied:
        first_item = clipboard.paste()
        q.put(first_item)
    else:
        p = clipboard.paste()
        clipboard.copy(first_item)
        q.put(p)
    just_copied = True


def on_paste():
    time.sleep(0.1)
    global just_copied
    if just_copied:
        q.get()
        just_copied = False
    if not q.empty():
        prev = q.get()
        clipboard.copy(prev)


keyboard.add_hotkey(copy, on_copied)
keyboard.add_hotkey(paste, on_paste)

keyboard.wait(esc)