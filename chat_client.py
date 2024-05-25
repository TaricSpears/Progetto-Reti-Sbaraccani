#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt
from tkinter import ttk

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkt.END, msg)
            msg_list.yview(tkt.END)
        except OSError:
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    try:
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.close()
            finestra.quit()
    except Exception as e:
        print(f"Errore nell'invio del messaggio: {e}")
        client_socket.close()
        finestra.quit()

def request_list(event=None):
    try:
        client_socket.send(bytes("/list", "utf8"))
    except Exception as e:
        print(f"Errore nell'invio del comando /list: {e}")

def send_private_message(event=None):
    try:
        client_socket.send(bytes("/pvt", "utf8"))
    except Exception as e:
        print(f"Errore nell'invio del comando /pvt: {e}")

def on_closing(event=None):
    my_msg.set("{quit}")
    send()

finestra = tkt.Tk()
finestra.title("Chat Laboratorio")

# Style configuration
finestra.configure(background='white')
finestra.attributes("-alpha", 0.95)

style = ttk.Style()
style.theme_use('clam')

style.configure("TFrame", background="white", bordercolor="#00ff00", relief="solid")
style.configure("TButton", background="#4CAF50", foreground="white", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12), background="#e0e0e0")
style.configure("TLabel", font=("Helvetica", 12), background="white")
style.configure("TScrollbar", background="#e0e0e0")

messages_frame = ttk.Frame(finestra)
my_msg = tkt.StringVar()
my_msg.set("Scrivi qui i tuoi messaggi.")
scrollbar = tkt.Scrollbar(messages_frame)

msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set, bg="white", font=("Helvetica", 12))
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH, expand=True)
messages_frame.pack(pady=10, padx=10)

entry_field = ttk.Entry(finestra, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack(pady=5, padx=10, fill=tkt.BOTH)

button_frame = ttk.Frame(finestra)
button_frame.pack(pady=5, padx=10, fill=tkt.BOTH)

send_button = ttk.Button(button_frame, text="Invio", command=send)
send_button.pack(side=tkt.LEFT, padx=5)

list_button = ttk.Button(button_frame, text="Lista Utenti", command=request_list)
list_button.pack(side=tkt.LEFT, padx=5)

pvt_button = ttk.Button(button_frame, text="Messaggio Privato", command=send_private_message)
pvt_button.pack(side=tkt.RIGHT, padx=5)

finestra.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input('Inserire il Server host: ')

while True:
    try:
        PORT = int(input('Inserire la porta del server host: '))
        if PORT <= 0 or PORT > 65535:
            raise ValueError
        break
    except ValueError:
        print("Porta non valida. Inserisci un numero tra 1 e 65535.")

BUFSIZ = 1024
ADDR = (HOST, PORT)

try:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
except Exception as e:
    print(f"Errore di connessione: {e}")
    finestra.quit()

receive_thread = Thread(target=receive)
receive_thread.start()

tkt.mainloop()
