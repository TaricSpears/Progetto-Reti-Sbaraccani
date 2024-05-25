#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accetta_connessioni_in_entrata():
    while True:
        try:
            client, client_address = SERVER.accept()
            print("%s:%s si è collegato." % client_address)
            client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
            indirizzi[client] = client_address
            Thread(target=gestice_client, args=(client,)).start()
        except Exception as e:
            print(f"Errore durante l'accettazione di una connessione: {e}")

def gestice_client(client):
    try:
        nome = client.recv(BUFSIZ).decode("utf8")
        benvenuto = 'Benvenuto %s! Se vuoi lasciare la Chat, scrivi {quit} per uscire.' % nome
        client.send(bytes(benvenuto, "utf8"))
        msg = "%s si è unito alla chat!" % nome
        broadcast(bytes(msg, "utf8"))
        clients[client] = nome
        
        while True:
            msg = client.recv(BUFSIZ)
            if msg == bytes("{quit}", "utf8"):
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf8"))
                break
            elif msg == bytes("/list", "utf8"):
                lista_utenti = "Utenti connessi: " + ", ".join(clients.values())
                client.send(bytes(lista_utenti, "utf8"))
            elif msg == bytes("/pvt", "utf8"):
                client.send(bytes("Inserisci il nome del destinatario:", "utf8"))
                destinatario = client.recv(BUFSIZ).decode("utf8")
                if destinatario == nome:
                    client.send(bytes("Non puoi inviare messaggi privati a te stesso.", "utf8"))
                elif destinatario not in clients.values():
                    client.send(bytes("Utente non trovato o offline.", "utf8"))
                else:
                    client.send(bytes("Inserisci il tuo messaggio:", "utf8"))
                    messaggio_privato = client.recv(BUFSIZ).decode("utf8")
                    for c, n in clients.items():
                        if n == destinatario:
                            c.send(bytes("[PVT da %s]: %s" % (nome, messaggio_privato), "utf8"))
                            break
            else:
                broadcast(msg, nome+": ")
    except Exception as e:
        print(f"Errore nella gestione del client {client}: {e}")
        client.close()
        if client in clients:
            del clients[client]

def broadcast(msg, prefisso=""):
    for utente in clients:
        try:
            utente.send(bytes(prefisso, "utf8") + msg)
        except Exception as e:
            print(f"Errore nell'invio del messaggio a {clients[utente]}: {e}")
            utente.close()
            if utente in clients:
                del clients[utente]

clients = {}
indirizzi = {}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
