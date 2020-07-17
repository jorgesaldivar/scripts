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

copied_elements = queue.Queue()
elements_pasted = []
elements_to_undo = []

first_element = ''
last_element = ''
first_element_pasted = False
undo_pasted_elements = False

copy = 'ctrl+c'
cut = 'ctrl+x'
paste = 'ctrl+v'
undo = 'ctrl+z'
esc = 'esc'

print('Copy hot-key set as : ', copy)
print('Cut hot-key set as : ', cut)
print('Paste hot-key set as : ', paste)
print('Undo hot-key set as : ', undo)
print("Exit hot-key set as : ", esc)


def reset_copy_status():
    global elements_pasted
    global elements_to_undo
    global first_element_pasted
    global undo_pasted_elements

    elements_pasted = []
    elements_to_undo = []
    first_element_pasted = False
    undo_pasted_elements = False


def reset_paste_status():
    global first_element
    global elements_to_undo
    global first_element_pasted
    global undo_pasted_elements
    first_element = ''
    first_element_pasted = True
    if elements_to_undo:
        undo_pasted_elements = True
    else:
        undo_pasted_elements = False


def reset_undo_status():
    global first_element_pasted
    global undo_pasted_elements
    first_element_pasted = False
    undo_pasted_elements = True


def on_copied():
    global copied_elements
    global first_element

    time.sleep(0.1)
    reset_copy_status()
    if not first_element:
        copied_elements = queue.Queue()
        first_element = clipboard.paste()

    clipboard_element = clipboard.paste()
    copied_elements.put(clipboard_element)
    clipboard.copy(first_element)
    print("Copy : " + clipboard_element)


def on_paste():
    global last_element
    global elements_pasted
    global first_element_pasted
    global undo_pasted_elements

    time.sleep(0.1)

    if last_element and not elements_to_undo:
        clipboard.copy(last_element)
        print("paste last element, no more elements to undo: " + last_element)
        elements_pasted.append(last_element)
        last_element = ''

    elif undo_pasted_elements:
        if not first_element_pasted and elements_to_undo:
            element = elements_to_undo.pop()
            elements_pasted.append(element)
            print("Next to paste first (undo): " + element)

        if elements_to_undo:
            element = elements_to_undo.pop()
            clipboard.copy(element)
            elements_pasted.append(element)
            print("Next to paste (undo): " + element)
        elif last_element:
            clipboard.copy(last_element)
            print("paste last element, no more elements to undo: " + last_element)
            elements_pasted.append(last_element)
            last_element = ''

    else:
        if not first_element_pasted:
            element = copied_elements.get()
            elements_pasted.append(element)
            print("Pasted : " + element)

        if not copied_elements.empty():
            previous_element = copied_elements.get()
            elements_pasted.append(previous_element)
            clipboard.copy(previous_element)
            print("Next to paste : " + previous_element)
    reset_paste_status()


def on_undo():
    global last_element
    global undo_pasted_elements

    time.sleep(0.1)
    if not undo_pasted_elements and elements_pasted:
        last_element = elements_pasted.pop()
        clipboard.copy(last_element)
        print("Remove next to paste: " + last_element)

    if elements_pasted:
        element = elements_pasted.pop()
        elements_to_undo.append(element)
        clipboard.copy(element)
        print("Undo : " + element)

    reset_undo_status()


keyboard.add_hotkey(copy, on_copied)
keyboard.add_hotkey(cut, on_copied)
keyboard.add_hotkey(paste, on_paste)
keyboard.add_hotkey(undo, on_undo)

keyboard.wait(esc)
