import psutil
import cpuinfo
import socket
import pickle


def sair():
    print('Sistema finalizado.')
    exit(0)

def processador():
    return {
        'Nome': cpuinfo.get_cpu_info()['brand_raw'],
        'Arquitetura': '{}'.format(cpuinfo.get_cpu_info()['arch']),
        'Palavra (bits)': '{}' .format(cpuinfo.get_cpu_info()['bits']),
        'Frequência Atual': '{:.1f} GHz'.format(psutil.cpu_freq().current / 1000),
        'Núcleos Físicos': psutil.cpu_count(logical=False)
    }

def disco():
    disco = psutil.disk_usage('C:')        
    return {
        'Uso de Disco: (Total': '{:4.2f} GB'.format(disco.total / (1024 * 1024 * 1024))
    }

def memoria():
    mem = psutil.virtual_memory()
    return {
        'Uso de Memória (Total': '{:.2f} GB'.format(mem.total / (1024 * 1024 * 1024)),
        'Memória Disponível': '{:.2f} GB'.format(mem.available / (1024 * 1024 * 1024))
    }

def rede():
    dic_interfaces = psutil.net_if_addrs()
    bytes_resp = pickle.dumps(dic_interfaces)
    socket_cliente.send(bytes_resp)


try:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    host = socket.gethostname()
    porta = 6000
    servidor.bind((host, porta))
    servidor.listen()
    print("Servidor de nome", host, "esperando conexão na porta", porta)
except Exception as ex:
    print('Ocorreu um erro ao iniciar o servidor.')
    print('Erro:', ex)
    sair()
            
while True:
    socket_cliente = servidor.accept()[0]
    msg = socket_cliente.recv(65536).decode('ascii')

    if msg == 'processador':
        print('Enviando informações da CPU.')
        texto = pickle.dumps(processador())
    elif msg == 'disco':
        print('Enviando informações do disco rígido.')
        texto = pickle.dumps(disco())
    elif msg == 'memoria':
        print('Enviando informações da memória.')
        texto = pickle.dumps(memoria())
    elif msg == 'fim':
        socket_cliente.send(pickle.dumps('Servidor finalizado com sucesso.'))
        socket_cliente.close()
        servidor.close()
        sair()
    else:
        print('Comando desconhecido.')
        texto = pickle.dumps('Comando desconhecido.')        

    socket_cliente.send(texto)
    socket_cliente.close()
    









