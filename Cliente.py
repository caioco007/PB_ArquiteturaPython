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
tela7 = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Página Inicial")
pygame.display.init()

preto = (0, 0, 0)
azul = (0, 0, 255)
vermelho = (255, 0, 0)
branco = (255, 255, 255)
amarelo = (255, 255, 0)
cinza = (100, 100, 100)

s1 = pygame.Surface((largura_tela, int(altura_tela / 4)))
s2 = pygame.Surface((largura_tela, int(altura_tela / 4)))
s3 = pygame.Surface((largura_tela, int(altura_tela / 4)))
s4 = pygame.Surface((largura_tela, int(altura_tela / 4)))
s5 = pygame.Surface((largura_tela, altura_tela))
s6 = pygame.Surface((largura_tela, int(altura_tela / 3)))
s7 = pygame.Surface((largura_tela, altura_tela))
s8 = pygame.Surface((largura_tela, altura_tela))

def sair():
    pygame.display.quit()
    pygame.quit()
    exit()

def get_info(msg):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    porta = 6000
    try:            
        cliente.connect((host, porta))
        cliente.send(msg.encode('ascii'))        
        return pickle.loads(cliente.recv(65536))
    except Exception as ex:
        print('Ocorreu um erro ao tentar fazer a requisição.')
        print('Erro:', ex)
        sair()
    finally:
        cliente.close()

def processador():

    pos_y=10
    s5.fill(branco)      
    texto_barra = get_info('processador')
    text = font.render(str(texto_barra), 1, preto)    
    topoTexto=5
    for t in texto_barra.keys():
            text = font.render('{}: {}'.format(t, texto_barra[t]), 1, preto)
            s5.blit(text, (24, topoTexto))
            topoTexto += 24
    tela1.blit(s5, (0, 0))

    s5.fill(preto)
    cpu_process= psutil.cpu_percent(percpu=True)
    num_cpu = len(cpu_process)
    x = y = 10
    desl = 10
    alt = s5.get_height() - 2 * y
    larg = (s5.get_width() - 2 * y - (num_cpu + 1) * desl) / num_cpu
    d = x + desl
    for i in (cpu_process):
        pygame.draw.rect(s5, vermelho, (d, y, larg, alt))
        pygame.draw.rect(s5, azul, (d, y, larg, (1 - i / 100) * alt))
        d = d + larg + desl

    # parte mais abaixo da tela e à esquerda
    tela1.blit(s5, (0, altura_tela / 5))

def disco():
    disco = psutil.disk_usage('C:')
    larg = largura_tela - 2 * 20
    tela2.fill(preto)
    pygame.draw.rect(tela2, azul, (20, 50, larg, 70))
    larg = larg * disco.percent / 100
    pygame.draw.rect(tela2, vermelho, (20, 50, larg, 70))
    texto_barra = get_info('disco')
    text = font.render(str(texto_barra), 1, branco)
    for t in texto_barra.keys():
        text = font.render('{}: {}'.format(t, texto_barra[t]), 1, branco)
    tela2.blit(text, (20, 10))

def memoria():
    mem = psutil.virtual_memory()
    larg = largura_tela - 2 * 20
    tela3.fill(preto)
    pygame.draw.rect(tela3, azul, (20, 50, larg, 70))
    larg = larg * mem.percent / 100
    pygame.draw.rect(tela3, vermelho, (20, 50, larg, 70))
    texto_barra = get_info('memoria')
    text = font.render(str(texto_barra), 1, branco)
    for t in texto_barra.keys():
        text = font.render('{}: {}'.format(t, texto_barra[t]), 1, branco)
    tela3.blit(text, (20, 10))

def rede():
    def obter_endereco_ip(family):
        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == family:
                    yield interface, snic.address

    # Função que itera a lista de IPs
    def imprime_ip(lista, surface):
        y = 40
        for address in lista:
            texto = font.render(f"{address}", True, amarelo)
            surface.blit(texto, (20, y))
            y += 20

    ipv4s = list(obter_endereco_ip(socket.AF_INET))
    s6.fill(preto)
    texto_barra = font.render("Endereços IP: ", True, branco)
    s6.blit(texto_barra, (20, 10))
    imprime_ip(ipv4s, s6)
    tela4.fill(preto)
    tela4.blit(s6, (0, 10 + 3 * altura_tela / 5))

def diretorio():
    def escrever(top, nome, tamanho, dt_criacao, dt_modificacao):
        fontLista = pygame.font.Font(None, 24)
        colNome = fontLista.render(nome, 1, branco)
        colTamanho = fontLista.render(tamanho, 1, branco)
        colDtCriacao = fontLista.render(dt_criacao, 1, branco)
        colDtModificacao = fontLista.render(dt_modificacao, 1, branco)

        s7.blit(colNome, (20, top))
        s7.blit(colTamanho, (240, top))
        s7.blit(colDtCriacao, (400, top))
        s7.blit(colDtModificacao, (600, top))
        tela5.blit(s7, (0, 0))

    top = 24
    escrever(top, 'Nome', 'Tamanho', 'Criação', 'Modificação')

    # Obtém lista de arquivos e diretórios do diretório corrente:
    lista = os.listdir()
    dic = {}  # cria dicionário
    for i in lista:  # Varia na lista dos arquivos e diretórios
        if os.path.isfile(i):  # checa se é um arquivo
            top += 24
            s = '{:.2f} KB'.format(os.stat(i).st_size / 1024)
            dtCriacao = datetime.fromtimestamp(os.stat(i).st_atime)
            dtModificacao = datetime.fromtimestamp(os.stat(i).st_mtime)

            escrever(top, i, s,
                     dtCriacao.strftime('%d/%m/%Y - %H:%M:%S'),
                     dtModificacao.strftime('%d/%m/%Y - %H:%M:%S'))

def pid():
    pids = psutil.pids()
    p = psutil.Process(pids[3])
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

    text1 = font.render(textNome, 1, branco)
    text2 = font.render(textExec, 1, branco)
    text3 = font.render(textTepCriacao, 1, branco)
    text4 = font.render(textTepUsuario, 1, branco)
    text5 = font.render(textTepSistema, 1, branco)
    text6 = font.render(textPercCpu, 1, branco)
    text7 = font.render(textPercMen, 1, branco)
    text8 = font.render(textMen, 1, branco)
    text9 = font.render(textThreads, 1, branco)
    text10 = font.render(textClock, 1, branco)

    s8.blit(text1, (20,altura_topo))
    s8.blit(text2, (20, altura_topo*3))
    s8.blit(text3, (20, altura_topo*5))
    s8.blit(text4, (20, altura_topo*7))
    s8.blit(text5, (20, altura_topo*9))
    s8.blit(text6, (20, altura_topo*11))
    s8.blit(text7, (20, altura_topo*13))
    s8.blit(text8, (20, altura_topo*15))
    s8.blit(text9, (20, altura_topo*17))
    s8.blit(text10, (20, altura_topo*19))
    tela6.blit(s8, (0, 0))

def info_dispositivos_rede(ip):
    rede = '{0}.{1}.{2}.'.format(*ip.split('.'))
    ip_lista = []
    
    # Coloquei até 15 pra não demorar tanto, mas o correto é 254 (broadcast (255) não deve ser incluso)
    for i in range(1, 15):
        ip_remoto = rede + str(i)
        args = ['ping', '-n', '1', '-l', '1', '-w', '10', ip_remoto]
        if subprocess.call(args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w')) == 0:
            ip_lista.append(ip_remoto)

    return ip_lista

def redeLocal():
    rede_local = {}
    if rede_local == {}:
        host = socket.gethostname()
        ip = socket.gethostbyname(host)
        portasInfo = []

        ip_na_rede = info_dispositivos_rede(ip)

        n = nmap.PortScanner()
        n.scan(ip)

        for protoco in n[ip].all_protocols():
            for porta in n[ip][protoco].keys():
                portasInfo.append('{}: {}'.format(porta, n[ip][protoco][porta]['state']))

        msg = {
            'Nome do computador': host,
            'IP': ip,
            'Portas': portasInfo,
            'Outros IP nesta rede:': ip_na_rede
        }
        
        rede_local = msg
    text = font.render(str(rede_local), 1, preto)    
    topoTexto=5
    for t in rede_local.keys():
            text = font.render('{}: {}'.format(t, rede_local[t]), 1, branco)         
    tela7.blit(text, (20, 10))

def main():
    controle = 60
    pagina = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair()
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
                processador()
            if pagina == 1:
                memoria()
            if pagina == 2:
                disco()
            if pagina == 3:
                rede()
            if pagina == 4:
                pid()
            if pagina == 5:
               diretorio()
            if pagina == 6:
                redeLocal()
            if pagina == 7:
                resumo()
            controle = 0            
        pygame.display.update()
        controle += 1
        CLOCK.tick(HZ)

print('entrou')
main()