import pika
from rc5 import RC5  
from coloramacores import Cores, Estilos, Style, Fore, Back

def ver_mensagens():
    credentials = pika.PlainCredentials('heitor', 'senha')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='15.229.70.251', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    
    def callback(ch, method, properties, body):
        hex_input = body.decode('utf-8')  
        print(f"Mensagem criptografada recebida: {hex_input}")

        key = input("Digite a chave para descriptografar: ")
        key_bytes = key.encode('utf-8')  

        try:
            encrypted = [int(hex_input[i:i + 2], 16) for i in range(0, len(hex_input), 2)]
        except ValueError:
            print("Erro: A entrada deve ser uma sequência de valores hexadecimais válidos.")
            return


        rc5_cipher = RC5(w=32, R=12, key=key_bytes)

        decrypted = rc5_cipher.decryptBytes(bytes(encrypted))
        try:
            decrypted_message = decrypted.decode('utf-8', errors='ignore')  
        except UnicodeDecodeError:
            print("Erro ao decodificar a mensagem!")
            decrypted_message = ''

        print("==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==")
        print(f"\nMensagem descriptografada: {decrypted_message}")
        print("\n==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print("==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==")
    print("[!] Aguardando mensagens. Para sair, pressione CTRL+C ")
    print("==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==")

    channel.start_consuming()

def menu():
    print("==-==-==-== MENU RECEBER ==-==-==-==")
    print("1. Ver mensagens\n")   
    print("[!] Para sair, pressione CTRL+C")

    while True:
        print("==-==-==-==-==-==-==-==-==-==-==-==-==")
        escolha = input("Escolha uma opção: ")
        print("==-==-==-==-==-==-==-==-==-==-==-==-==")

        if escolha == '1':
            ver_mensagens()
        else:
            print(f"\nA opção é inválida, tente novamente!\n")
            print("==-==-==-==-==-==-==-==-==-==-==-==-== ")

if __name__ == '__main__':
    try:
        menu()
    except KeyboardInterrupt:
        print("\n==-==-==-==-==-==-==-==-==-==-==-==-== ")
        print("O programa foi finalizado!")
        print("==-==-==-==-==-==-==-==-==-==-==-==-== \n")
