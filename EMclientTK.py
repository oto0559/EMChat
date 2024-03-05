import socket # Hlavní modul pro funkci serveru
import sys
from tkinter import *
from threading import Thread # Více procesů zároveň
from datetime import datetime # Pro zaznamenání času odeslání zprávy


def recv():
    while True:
        data = client_socket.recv(1024).decode() # Zkouší obdržet zprávu
        if not data:
            sys.exit(0)
        txt.insert(str(data))


def send():
    while True:
        message = e.get()  # Pošli zprávu
        txt.insert(END, "\n" + message)
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"[{date_now}] {name}: {message}" # Formátování zprávy
        client_socket.send(message.encode()) # Odesílá zprávu klientovi


def client_program():
    print(f"[*] Připojuji se k {SERVER_HOST}:{SERVER_PORT}...")

    client_socket.connect((SERVER_HOST, SERVER_PORT))  # Připojení k serveru
    print("[*] Připojeno.")

    Thread(target=send).start() # Zapne thready s odesíláním a přijímáním zpráv
    Thread(target=recv).start()


if __name__ == '__main__':
    # IP adresa serveru, zjistíte pomocí Win+R -> ipconfig -> IPv4 Address
    # 127.0.0.1 pro local server
    root = Tk()
    root.title("Komunikace")
    BG_GRAY = "#ABB2B9"
    BG_COLOR = "#17202A"
    TEXT_COLOR = "#EAECEE"

    FONT = "Helvetica 14"
    FONT_BOLD = "Helvetica 13 bold"

    lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
        row=0)

    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=1, column=0, columnspan=2)

    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)

    e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    e.grid(row=2, column=0)
    sendni = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1)
    client_socket = socket.socket()  # Pouze přejmenované na client pro lepší vyznání
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 5002

    name = 'Posádka' # Jméno zobrazené u zprávy


    client_program() # Spustí celý program

    root.mainloop()