from config.config import Config
import socket

def conn():
    # Configuración de la cuenta de osu!
    osu_nick = Config.NICKNAME
    osu_pass = Config.SERVER_PASS

    # Conectar a IRC
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect(("irc.ppy.sh", 6667))
    irc.send(f"PASS {osu_pass}\r\n".encode())
    irc.send(f"NICK {osu_nick}\r\n".encode())
    irc.send(f"USER {osu_nick} 0 * :{osu_nick}\r\n".encode())

    # Esperar la respuesta del servidor
    authenticated = False

    while True:
        response = irc.recv(2048).decode(errors="ignore").strip()
        for line in response.split("\r\n"):
            if not line:
                continue
            
            print(line)  # Imprimir la respuesta para depuración

            if "464" in line:
                print("Error: Contraseña incorrecta.")
                irc.close()
                exit(1)
            
            if f":{osu_nick}!" in line or "001" in line:
                authenticated = True  # Recibió el código de bienvenida 001

        if authenticated:
            print("Conectado al IRC de osu!")
            break  # Salimos del loop de espera y seguimos con el programa

    return osu_nick, irc