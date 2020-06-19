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
import time

q = []
copy = 'ctrl+c'
paste = 'ctrl+v'
esc = 'esc'
just_copied = False

print('Copy hot-key set as : ', copy)
print('Paste hot-key set as : ', paste)
print("Exit hot-key set as : ", esc)


def on_copied():
    time.sleep(0.1)
    p = clipboard.paste()
    q.append(p)
    global just_copied
    just_copied = True


def on_paste():
    time.sleep(0.1)
    global just_copied
    if just_copied:
        q.pop()
        just_copied = False
    if q:
        prev = q.pop()
        clipboard.copy(prev)


keyboard.add_hotkey(copy, on_copied)
keyboard.add_hotkey(paste, on_paste)

keyboard.wait(esc)