from cpuinfo.cpuinfo import main
import psutil 
import pygame
import cpuinfo
import socket
import os
import sys
import sched
import time
from datetime import datetime
import nmap
import subprocess
import pickle
import platform
from psutil._common import bytes2human

class Cliente:
    def sair(self):
        pygame.display.quit()
        pygame.quit()
        exit()
    
    def infoDoCliente(self,msg):
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        porta = 5000

        try:            
            cliente.connect((host, porta))
            cliente.send(msg.encode('UTF-8'))
            return pickle.loads(cliente.recv(65536))
        except Exception as ex:
            print('Ocorreu um erro ao tentar fazer a requisição.')
            print('Erro:', ex)
            self.sair()
        finally:
            cliente.close()

    def configPygame(self):
        pygame.font.init()
        font = pygame.font.Font(None, 32)

        pygame.init()
        CLOCK = pygame.time.Clock()
        HZ = 60

        # Obtém informações da CPU
        info_cpu = cpuinfo.get_cpu_info()

        # Iniciando a janela principal
        largura_tela = 750
        altura_tela = 600
        tela = pygame.display.set_mode((largura_tela, altura_tela))
        tela1 = pygame.display.set_mode((largura_tela, altura_tela))
        tela2 = pygame.display.set_mode((largura_tela, altura_tela))
        tela3 = pygame.display.set_mode((largura_tela, altura_tela))
        tela4 = pygame.display.set_mode((largura_tela, altura_tela))
        tela5 = pygame.display.set_mode((largura_tela, altura_tela))
        tela6 = pygame.display.set_mode((largura_tela, altura_tela))
        pygame.display.set_caption("Página Inicial")
        pygame.display.init()

        self.preto = (0, 0, 0)
        self.azul = (0, 0, 255)
        self.vermelho = (255, 0, 0)
        self.branco = (255, 255, 255)
        self.amarelo = (255, 255, 0)
        self.cinza = (100, 100, 100)

        self.s1 = pygame.Surface((largura_tela, altura_tela / 4))
        self.s2 = pygame.Surface((largura_tela, altura_tela / 4))
        self.s3 = pygame.Surface((largura_tela, altura_tela / 4))
        self.s4 = pygame.Surface((largura_tela, altura_tela / 4))
        self.s5 = pygame.Surface((largura_tela, altura_tela))
        self.s6 = pygame.Surface((largura_tela, altura_tela / 3))
        self.s7 = pygame.Surface((largura_tela, altura_tela))
        self.s8 = pygame.Surface((largura_tela, altura_tela))

    def processador(self):
        i=10
        def mostra_info_cpu():
            self.s5.fill(self.branco)
            text = self.font.render(self.infoDoCliente('processador'), True, self.cinza)
            self.s5.blit(text, (300, i+20))
            self.tela1.blit(self.s5, (0, 0))

        mostra_info_cpu()

        self.s5.fill(self.preto)
        num_cpu = len(psutil.cpu_percent(percpu=True))
        x = y = 10
        desl = 10
        alt = self.s5.get_height() - 2 * y
        larg = (self.s5.get_width() - 2 * y - (num_cpu + 1) * desl) / num_cpu
        d = x + desl
        for i in psutil.cpu_percent(percpu=True):
            pygame.draw.rect(self.s5, self.vermelho, (d, y, larg, alt))
            pygame.draw.rect(self.s5, self.azul, (d, y, larg, (1 - i / 100) * alt))
            d = d + larg + desl

        # parte mais abaixo da tela e à esquerda
        self.tela1.blit(self.s5, (0, self.altura_tela / 5))

    def disco(self):
        disco = psutil.disk_usage('.')
        larg = self.largura_tela - 2 * 20
        self.tela2.fill(self.preto)
        pygame.draw.rect(self.tela2, self.azul, (20, 50, larg, 70))
        larg = larg * disco.percent / 100
        pygame.draw.rect(self.tela2, self.vermelho, (20, 50, larg, 70))
        total = round(disco.total / (1024 * 1024 * 1024), 2)
        texto_barra = "Uso de Disco: (Total: " + str(total) + "GB):"
        text = self.font.render(texto_barra, 1, self.branco)
        self.tela2.blit(text, (20, 10))

    def memoria(self):
        mem = psutil.virtual_memory()
        larg = self.largura_tela - 2 * 20
        self.tela3.fill(self.preto)
        pygame.draw.rect(self.tela3, self.azul, (20, 50, larg, 70))
        larg = larg * mem.percent / 100
        pygame.draw.rect(self.tela3, self.vermelho, (20, 50, larg, 70))
        total = round(mem.total / (1024 * 1024 * 1024), 2)
        texto_barra = "Uso de Memória (Total: " + str(total) + "GB):"
        text = self.font.render(texto_barra, 1, self.branco)
        self.tela3.blit(text, (20, 10))

    def rede(self):
        def obter_endereco_ip(family):
            for interface, snics in psutil.net_if_addrs().items():
                for snic in snics:
                    if snic.family == family:
                        yield interface, snic.address

        # Função que itera a lista de IPs
        def imprime_ip(lista, surface):
            y = 40
            for address in lista:
                texto = self.font.render(f"{address}", True, self.amarelo)
                surface.blit(texto, (20, y))
                y += 20

        ipv4s = list(obter_endereco_ip(socket.AF_INET))
        self.s6.fill(self.preto)
        self.texto_barra = self.font.render("Endereços IP: ", True, branco)
        self.s6.blit(self.texto_barra, (20, 10))
        imprime_ip(ipv4s, self.s6)
        self.tela4.fill(self.preto)
        self.tela4.blit(self.s6, (0, 10 + 3 * altura_tela / 5))   

    def diretorio(self):
        def escrever(top, nome, tamanho, dt_criacao, dt_modificacao):
            fontLista = pygame.font.Font(None, 24)
            colNome = fontLista.render(nome, 1, self.branco)
            colTamanho = fontLista.render(tamanho, 1, self.branco)
            colDtCriacao = fontLista.render(dt_criacao, 1, self.branco)
            colDtModificacao = fontLista.render(dt_modificacao, 1, self.branco)

            self.s7.blit(colNome, (20, top))
            self.s7.blit(colTamanho, (240, top))
            self.s7.blit(colDtCriacao, (400, top))
            self.s7.blit(colDtModificacao, (600, top))
            self.tela5.blit(self.s7, (0, 0))

        top = 24
        escrever(top, 'Nome', 'Tamanho', 'Criação', 'Modificação')

        # Obtém lista de arquivos e diretórios do diretório corrente:
        lista = os.listdir()
        dic = {}  # cria dicionário
        for i in lista:  # Varia na lista dos arquivos e diretórios
            if os.path.isfile(i):  # checa se é um arquivo
                top += 24
                s = '{:.2f} KB'.format(os.stat(i).st_size / 1024)
                dtCriacao = datetime.datetime.fromtimestamp(os.stat(i).st_atime)
                dtModificacao = datetime.datetime.fromtimestamp(os.stat(i).st_mtime)

                escrever(top, i, s,
                        dtCriacao.strftime('%d/%m/%Y - %H:%M:%S'),
                        dtModificacao.strftime('%d/%m/%Y - %H:%M:%S'))

    def pid(self):
        pids = psutil.pids()
        p = psutil.Process(pids[3]);
        altura_topo=20
        perc_mem = '{:.2f}'.format(p.memory_percent())
        mem = '{:.2f}'.format(p.memory_info().rss / 1024 / 1024)

        textNome="Nome: "+p.name()
        textExec = "Executável: "+p.exe()
        textTepCriacao = "Tempo de criação: "+time.ctime(p.create_time())
        textTepUsuario = "Tempo de usuário: "+str(p.cpu_times().user)+"s"
        textTepSistema = "Tempo de sistema: "+str(p.cpu_times().system)+"s"
        textPercCpu = "Percentual de uso de CPU: "+str(p.cpu_percent(interval=1.0))+"%"
        textPercMen = "Percentual de uso de memória: "+str(perc_mem)+"%"
        textMen = "Uso de memória: "+mem+"MB"
        textThreads = "Número de threads: "+str(p.num_threads())
        textClock = "Clock: "+str(time.process_time())

        text1 = self.font.render(textNome, 1, self.branco)
        text2 = self.font.render(textExec, 1, self.branco)
        text3 = self.font.render(textTepCriacao, 1, self.branco)
        text4 = self.font.render(textTepUsuario, 1, self.branco)
        text5 = self.font.render(textTepSistema, 1, self.branco)
        text6 = self.font.render(textPercCpu, 1, self.branco)
        text7 = self.font.render(textPercMen, 1, self.branco)
        text8 = self.font.render(textMen, 1, self.branco)
        text9 = self.font.render(textThreads, 1, self.branco)
        text10 = self.font.render(textClock, 1, self.branco)

        self.s8.blit(text1, (20,altura_topo))
        self.s8.blit(text2, (20, altura_topo*3))
        self.s8.blit(text3, (20, altura_topo*5))
        self.s8.blit(text4, (20, altura_topo*7))
        self.s8.blit(text5, (20, altura_topo*9))
        self.s8.blit(text6, (20, altura_topo*11))
        self.s8.blit(text7, (20, altura_topo*13))
        self.s8.blit(text8, (20, altura_topo*15))
        self.s8.blit(text9, (20, altura_topo*17))
        self.s8.blit(text10, (20, altura_topo*19))
        self.tela6.blit(self.s8, (0, 0))

    def tp6(self):
        def scan_host(host):
            nm = nmap.PortScanner()

            nm.scan(host)
            print(nm[host].hostname())
            for proto in nm[host].all_protocols():
                print('----------')
                print('Protocolo : %s' % proto)

                lport = nm[host][proto].keys()
                # lport.sort()
                for port in lport:
                    print('Porta: %s\t Estado: %s' % (port, nm[host][proto][port]['state']))

        def obter_hostnames(host_validos):
            nm = nmap.PortScanner()
            print("entrando")
            for i in host_validos:
                try:
                    nm.scan(i)
                    print("O IP ", i, "possui o nome", nm[i].hostname())
                except:
                    print("Falhou ", i)
                    pass

        def retorna_codigo_ping(hostname):
            """Usa o utilitario ping do sistema operacional para encontrar   o host. ('-c 5') indica, em sistemas linux, que deve mandar 5   pacotes. ('-W 3') indica, em sistemas linux, que deve esperar 3   milisegundos por uma resposta. Esta funcao retorna o codigo de   resposta do ping """

            plataforma = platform.system()
            args = []
            if plataforma == "Windows":
                args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]

            else:
                args = ['ping', '-c', '1', '-W', '1', hostname]

            ret_cod = subprocess.call(args,
                                    stdout=open(os.devnull, 'w'),
                                    stderr=open(os.devnull, 'w'))
            return ret_cod

        def verifica_hosts(base_ip):
            """Verifica todos os host com a base_ip entre 1 e 255 retorna uma lista com todos os host que tiveram resposta 0 (ativo)"""
            print("Mapeando\r")
            host_validos = []
            return_codes = dict()
            for i in range(1, 255):

                return_codes[base_ip + '{0}'.format(i)] = retorna_codigo_ping(base_ip + '{0}'.format(i))
                if i % 20 == 0:
                    print(".", end="")
                if return_codes[base_ip + '{0}'.format(i)] == 0:
                    host_validos.append(base_ip + '{0}'.format(i))
            print("\nMapping ready...")

            return host_validos

        def escrever():

            # Chamadas
            ip_string = self.host
            print(ip_string)
            ip_lista = ip_string.split('.')
            base_ip = ".".join(ip_lista[0:3]) + '.'
            print("O teste será feito na sub rede: "+ str(base_ip))
            host_validos = verifica_hosts(base_ip)
            print("Os host válidos são: " + ", ".join(host_validos))
            obter_hostnames(host_validos)
            scan_host(ip_string)

        escrever()

    def redeInterface(self):
            af_map = {
                socket.AF_INET: 'IPv4',
                socket.AF_INET6: 'IPv6',
                psutil.AF_LINK: 'MAC',
            }

            duplex_map = {
                psutil.NIC_DUPLEX_FULL: "full",
                psutil.NIC_DUPLEX_HALF: "half",
                psutil.NIC_DUPLEX_UNKNOWN: "?",
            }

            stats = psutil.net_if_stats()
            io_counters = psutil.net_io_counters(pernic=True)
            for nomes, addrs in psutil.net_if_addrs().items():
                
                print("%s:" % (nomes))
                if nomes in stats:
                    st = stats[nomes]
                    print("    stats          : ", end='')
                    print("speed=%sMB, duplex=%s, mtu=%s, up=%s" % (
                        st.speed, duplex_map[st.duplex], st.mtu,
                        "yes" if st.isup else "no"))
                if nomes in io_counters:
                    io = io_counters[nomes]
                    print("    Enviados       : ", end='')
                    print("bytes=%s, pacotes=%s, erros=%s, drop=%s" % (
                        bytes2human(io.bytes_sent), io.packets_sent, io.errin,
                        io.dropin))
                    print("    Recebidos      : ", end='')
                    print("bytes=%s, pacotes=%s, erros=%s, drop=%s" % (
                        bytes2human(io.bytes_recv), io.packets_recv, io.errout,
                        io.dropout))
                for addr in addrs:
                    print("    %-4s" % af_map.get(addr.family, addr.family), end="")
                    print(" address   : %s" % addr.address)
                    if addr.broadcast:
                        print("         broadcast : %s" % addr.broadcast)
                    if addr.netmask:
                        print("        Máscara    : %s" % addr.netmask)
                    if addr.ptp:
                        print("      p2p       : %s" % addr.ptp)
                print("")         

    def main(self):

        controle = 60
        pagina = 0
        while True:
            for event in pygame.event.get():
                if event.type == quit:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if pagina > 0:
                            pagina -= 1
                    if event.key == pygame.K_RIGHT:
                        if pagina < 8:
                            pagina += 1
                    if event.key == pygame.K_SPACE:
                        pagina = 7

            if controle == 60:
                if pagina == 0:
                    self.processador()
                if pagina == 1:
                    self.memoria()
                if pagina == 2:
                    self.disco()
                if pagina == 3:
                    self.rede()
                if pagina == 4:
                    self.pid()
                if pagina == 5:
                    self.diretorio()
                
                controle = 0
                
            pygame.display.update()
            controle += 1
            self.CLOCK.tick(self.HZ)


Cliente()
    




