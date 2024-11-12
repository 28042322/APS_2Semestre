import pika
from rc5 import RC5  
from coloramacores import Cores, Estilos, Style, Fore

print(Cores.WHITE + Style.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-", end='' + Style.RESET_ALL)
print(Fore.RED + Style.BRIGHT + """     
██████╗  █████╗ ██████╗ ██████╗ ██╗████████╗███╗   ███╗ ██████╗ 
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║╚══██╔══╝████╗ ████║██╔═══██╗
██████╔╝███████║██████╔╝██████╔╝██║   ██║   ██╔████╔██║██║   ██║
██╔══██╗██╔══██║██╔══██╗██╔══██╗██║   ██║   ██║╚██╔╝██║██║▄▄ ██║
██║  ██║██║  ██║██████╔╝██████╔╝██║   ██║   ██║ ╚═╝ ██║╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝   ╚═╝     ╚═╝ ╚══▀▀═╝                                                """ + Style.RESET_ALL)
print(Cores.WHITE + Style.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-" + Style.RESET_ALL)

def ver_mensagens():
    credentials = pika.PlainCredentials('heitor', 'senha')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='15.229.70.251', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    
    def callback(ch, method, properties, body):
        hex_input = body.decode('utf-8')  
        print(Cores.CYAN + Style.BRIGHT + f"Mensagem criptografada recebida: {Cores.WHITE + Style.BRIGHT + hex_input}" + Cores.RESET)

        key = input(Cores.CYAN + Style.BRIGHT + "Digite a chave para descriptografar: " + Cores.RESET)
        key_bytes = key.encode('utf-8')  

        try:
            encrypted = [int(hex_input[i:i + 2], 16) for i in range(0, len(hex_input), 2)]
        except ValueError:
            print(Cores.RED + Style.BRIGHT + "Erro: A entrada deve ser uma sequência de valores hexadecimais válidos." + Cores.RESET)
            return


        rc5_cipher = RC5(w=32, R=12, key=key_bytes)

        decrypted = rc5_cipher.decryptBytes(bytes(encrypted))
        try:
            decrypted_message = decrypted.decode('utf-8', errors='ignore')  
        except UnicodeDecodeError:
            print(Cores.RED + Style.BRIGHT + "Erro ao decodificar a mensagem!" + Cores.RESET)
            decrypted_message = ''

        print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)
        print(Cores.CYAN + Style.BRIGHT + "\nMensagem descriptografada:", Cores.WHITE + Estilos.BRIGHT + decrypted_message + Cores.RESET)
        print(Cores.WHITE + Estilos.BRIGHT + "\n==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)
    print(Cores.CYAN + Style.BRIGHT + "[!] Aguardando mensagens. Para sair, pressione CTRL+C " + Style.RESET_ALL)
    print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)

    channel.start_consuming()

def menu():
    print(Cores.WHITE + Style.BRIGHT + "==-==-==-== ", end='' + Cores.RESET)
    print(Cores.GREEN + Estilos.BRIGHT + "MENU RECEBER", end='' + Cores.RESET)
    print(Cores.WHITE + Style.BRIGHT + " ==-==-==-== " + Cores.RESET)
    print(Cores.CYAN + Estilos.BRIGHT + "1. Ver mensagens\n" + Cores.RESET)   
    print(Cores.CYAN + Estilos.BRIGHT + "[!] Para sair, pressione CTRL+C" + Cores.RESET)

    while True:
        print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)
        escolha = input(Cores.GREEN + Estilos.BRIGHT + "Escolha uma opção: " + Cores.RESET)
        print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)

        if escolha == '1':
            ver_mensagens()
        else:
            print(Cores.RED + Style.BRIGHT + f"\nA opção é inválida, tente novamente!\n" + Cores.RESET)
            print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-== " + Cores.RESET)

if __name__ == '__main__':
    try:
        menu()
    except KeyboardInterrupt:
        print(Cores.WHITE + Estilos.BRIGHT + "\n==-==-==-==-==-==-==-==-==-==-==-==-== " + Cores.RESET)
        print(Cores.RED + Style.BRIGHT + "O programa foi finalizado!" + Cores.RESET)
        print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-== \n" + Cores.RESET)
