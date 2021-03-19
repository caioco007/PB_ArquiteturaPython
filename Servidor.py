import psutil
import cpuinfo
import socket
import pickle

class Servidor:
    def sair(self):
        print('Sistema finalizado.')
        exit(0)
    
    def processador(self):
        return {
            'Nome': self.cpu_info['brand_raw'],
            'Arquitetura': '{} ({} bits)'.format(self.cpu_info['arch'], self.cpu_info['bits']),
            'Palavra (bits)': '{}' .format(self.cpu_info['bits']),
            'Frequência Atual': '{:.1f} GHz'.format(psutil.cpu_freq().current / 1000),
            'Núcleos Físicos': psutil.cpu_count(logical=False)
        }

    def disco(self):
        disco = psutil.disk_usage(self.unidade)        
        return {
            'Uso de Disco: (Total': '{:4.2f} GB'.format(disco.total / (1024 * 1024 * 1024))
        }

    def memoria(self):
        mem = psutil.virtual_memory()
        return {
            'Uso de Memória (Total': '{:.2f} GB'.format(mem.total / (1024 * 1024 * 1024)),
            'Memória Disponível': '{:.2f} GB'.format(mem.available / (1024 * 1024 * 1024))
        }
    
    def rede(self):
        dic_interfaces = psutil.net_if_addrs()
        bytes_resp = pickle.dumps(dic_interfaces)
        self.socket_cliente.send(bytes_resp)

    def infoDoServe(self):
        try:
            self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            host = socket.gethostname()
            porta = 5000
            self.servidor.bind((host, porta))
            self.servidor.listen()
            print("Servidor de nome", host, "esperando conexão na porta", porta)
        except Exception as ex:
            print('Ocorreu um erro ao iniciar o servidor.')
            print('Erro:', ex)
            self.sair()
    
    def rodarServe(self):
                 
        while True:
            socket_cliente = self.servidor.accept()[0]
            msg = socket_cliente.recv(2048).decode('UTF-8')

            if msg == 'processador':
                print('Enviando informações da CPU.')
                texto = pickle.dumps(self.processador())
            elif msg == 'disco':
                print('Enviando informações do disco rígido.')
                texto = pickle.dumps(self.disco())
            elif msg == 'memoria':
                print('Enviando informações da memória.')
                texto = pickle.dumps(self.memoria())
            elif msg == 'rede':
                print('Enviando informações da rede.')
                texto = pickle.dumps(self.rede())
            elif msg == 'fim':
                socket_cliente.send(pickle.dumps('Servidor finalizado com sucesso.'))
                socket_cliente.close()
                self.servidor.close()
                self.sair()
            else:
                print('Comando desconhecido.')
                texto = pickle.dumps('Comando desconhecido.')

            socket_cliente.send(texto)
            socket_cliente.close()
        
    def main(self):
        self.infoDoServe()
        self.rodarServe()

    def __init__(self):
        self.cpu_info = cpuinfo.get_cpu_info()
        self.unidade = 'C:'
        self.main()

Servidor()







