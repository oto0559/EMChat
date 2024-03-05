import socket  # Hlavní modul pro funkci serveru
import time
from tkinter import *
from threading import Thread  # Více procesů zároveň
from datetime import datetime  # Pro zaznamenání času odeslání zprávy


def recv(conn, address):
    print("Připojil se: " + str(address))
    while True:
        try:
            data = conn.recv(1024).decode()  # Zkouší obdržet zprávu
            txt.insert(END, "\n" + data)
            f = open('chatlog.txt', 'a', encoding='utf-8')
            f.write(str(data) + '\n')  # Zapisuje zprávu do logu

        except ConnectionError:
            txt.insert(END, f"Spojení s klientem {address} bylo ztraceno.")  # Pokud klient spadne, server může zůstat zapnutý a čeká znovupřipojení
            time.sleep(1)
            txt.insert(END, f"Čekám na opětovné připojení...")
            return


def send(conn, address):
    while True:
        message = e.get()  # Pošli zprávu
        txt.insert(END, "\n" + message)
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Zaznamenání času odeslání zprávy
        message = f"[{date_now}] {name}: {message}"  # Formátování zprávy
        f = open('chatlog.txt', 'a', encoding='utf-8')
        f.write(message + '\n')  # Zapisuje zprávu do logu
        conn.send(message.encode())  # Odesílá zprávu klientovi


def server_program():
    server_socket.bind((SERVER_HOST, SERVER_PORT))  # Spojí host adresu a port dohromady
    server_socket.listen(2)  # Poslouchá pro 'x' zařízení
    print(f"[*] Čekám na připojení {SERVER_HOST}:{SERVER_PORT}")
    while True:
        conn, address = server_socket.accept()  # Přijme nové připojení
        Thread(target=send, args=(conn, address)).start()  # Zapne thready s odesíláním a přijímáním zpráv
        Thread(target=recv, args=(conn, address)).start()


if __name__ == '__main__':
    root = Tk()
    root.title("Komunikace")

    # IP adresa serveru
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5002
    name = 'MCC'  # Jméno zobrazené u zprávy (Mission Control Center)
    server_socket = socket.socket()  # Pouze přejmenované na server pro lepší vyznání


    BG_GRAY = "#ABB2B9"
    BG_COLOR = "#17202A"
    TEXT_COLOR = "#EAECEE"

    FONT = "Helvetica 14"
    FONT_BOLD = "Helvetica 13 bold"

    lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0)

    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=1, column=0, columnspan=2)
    txt.insert(END, 'ahoj')
    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)

    e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    e.grid(row=2, column=0)

    sendni = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1)
    server_program()  # Spustí celý program
    root.mainloop()
