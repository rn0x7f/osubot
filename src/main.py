import re
from config import connection

osu_nick, irc = connection.conn()

# Regex para capturar el autor y el mensaje de tipo PRIVMSG
privmsg_pattern = re.compile(rf"^:([^!]+)!.* PRIVMSG {osu_nick} :(.*)", re.MULTILINE)

# Handling private messages in a loop
while True:
    response = irc.recv(2048).decode(errors="ignore").strip()
    if not response:
        continue  # Skip empty responses
    print(f"Received response: {response}")  # Debugging received response

    if response.find('PING') != -1:  # Check if 'PING' is found
        irc.send(('PONG ' + response.split()[1] + '\r\n').encode())  # Send PONG to keep the connection alive

    # Verificamos que la respuesta sea PRIVMSG
    if f'PRIVMSG {osu_nick} :' in response:  # Asegurarnos de que solo estamos procesando los PRIVMSG
        # Usamos la expresión regular para buscar mensajes PRIVMSG
        match = privmsg_pattern.search(response)
        if match:
            sender = match.group(1)  # Nombre del remitente
            message = match.group(2).strip()  # Contenido del mensaje, eliminando espacios extras

            print(f"Sender: {sender}, Message: {message}")  # Debugging

            # Aseguramos que el mensaje sea exactamente '!hi'
            if message == '!hi':  
                irc.send(f'PRIVMSG {sender} :Hello, {sender}! \r\n'.encode())  # Respondemos al autor
                print(f'Message sent to {sender}!')  # Debugging sent message
            else:
                irc.send(f'PRIVMSG {sender} :Use !hi \r\n'.encode())
                print(f"Message '{message}' not handled.")  # Depuración de mensajes no reconocidos
    else:
        print(f"Not a PRIVMSG to {osu_nick}.")
