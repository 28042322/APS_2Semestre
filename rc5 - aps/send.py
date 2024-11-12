import pika
from rc5 import RC5  
from coloramacores import Cores, Estilos, Style, Fore, Back


print(Cores.WHITE + Style.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-", end='' + Style.RESET_ALL)
print(Fore.RED + Style.BRIGHT + """     
██████╗  █████╗ ██████╗ ██████╗ ██╗████████╗███╗   ███╗ ██████╗ 
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║╚══██╔══╝████╗ ████║██╔═══██╗
██████╔╝███████║██████╔╝██████╔╝██║   ██║   ██╔████╔██║██║   ██║
██╔══██╗██╔══██║██╔══██╗██╔══██╗██║   ██║   ██║╚██╔╝██║██║▄▄ ██║
██║  ██║██║  ██║██████╔╝██████╔╝██║   ██║   ██║ ╚═╝ ██║╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝   ╚═╝     ╚═╝ ╚══▀▀═╝                                                """ + Style.RESET_ALL)
print(Cores.WHITE + Style.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-" + Style.RESET_ALL)


def enviar_mensagem():
    try:
        credentials = pika.PlainCredentials('heitor', 'senha')  
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='15.229.70.251', credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='hello')


        mensagem = input(Cores.CYAN + Estilos.BRIGHT + "Digite a mensagem que deseja enviar: " + Cores.RESET)

        if len(mensagem) > 128:
            print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-== " + Cores.RESET)
            print(Cores.RED +  Style.BRIGHT + "\nEssa mensagem não pode ser criptografada!\n" + Cores.RESET)
            print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-== " + Cores.RESET)
        else:
            key = input(Cores.CYAN + Estilos.BRIGHT + "Chave para criptografar: " + Cores.RESET)
            rc5 = RC5(w=32, R=12, key=key.encode('utf-8'))  

            encrypted = rc5.encryptBytes(mensagem.encode('utf-8'))  
            hex_encrypted = [format(byte, '02x') for byte in encrypted]

            channel.basic_publish(exchange='', routing_key='hello', body=''.join(hex_encrypted))
            print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-== " + Cores.RESET)
            print(Cores.CYAN + Style.BRIGHT + f"\nMensagem enviada: {Cores.WHITE + Style.BRIGHT + ''.join(hex_encrypted)} \n" + Style.RESET_ALL)
            print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-== \n" + Cores.RESET)

    except Exception as e:
        print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)
        print(Cores.RED +  Style.BRIGHT + f"\nOcorreu um erro: {str(e)}\n" + Cores.RESET)
        print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)
    finally:
        connection.close()  

def menu():
    while True:
        print(Cores.WHITE + Style.BRIGHT + "==-==-==-== ", end='' + Cores.RESET)
        print(Cores.GREEN + Estilos.BRIGHT + "MENU MENSAGENS", end='' + Cores.RESET)
        print(Cores.WHITE + Style.BRIGHT + " ==-==-==-==" + Cores.RESET)
        print(Cores.CYAN + Estilos.BRIGHT + "1. Enviar mensagem" + Cores.RESET)  
        print(Cores.CYAN + Estilos.BRIGHT + "2. Sair" + Cores.RESET)                

        print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)
        escolha = input(Cores.GREEN + Estilos.BRIGHT + "Escolha uma opção: " + Cores.RESET)
        print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)

        if escolha == '1':
            enviar_mensagem()
        elif escolha == '2':
            print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)
            print(Cores.RED +  Style.BRIGHT + "\nO programa foi finalizado!\n" + Cores.RESET)
            print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)
            break
        else:
            print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)
            print(Cores.RED +  Style.BRIGHT + f"\nA opção é inválida, tente novamente!" + Cores.RESET)
            print(Cores.WHITE + Estilos.BRIGHT + "==-==-==-==-==-==-==-==-==-==-==-==-==" + Cores.RESET)

if __name__ == "__main__":
    menu()
