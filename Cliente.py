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
        
        print(pickle.loads(cliente.recv(65536)))
    except Exception as ex:
        print('Ocorreu um erro ao tentar fazer a requisição.')
        print('Erro:', ex)
        sair()
    finally:
        cliente.close()

def processador():

    pos_y=10      
    texto_barra = get_info('processador')
    text = font.render(texto_barra, 1, branco)
    s5.blit(text, (10, pos_y))
    tela1.blit(s5, (0, 0))

    s5.fill(preto)
    num_cpu = len(psutil.cpu_percent(percpu=True))
    x = y = 10
    desl = 10
    alt = s5.get_height() - 2 * y
    larg = (s5.get_width() - 2 * y - (num_cpu + 1) * desl) / num_cpu
    d = x + desl
    for i in (psutil.cpu_percent(percpu=True)):
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
    text = font.render(texto_barra, 1, branco)
    tela2.blit(text, (20, 10))

def memoria():
    mem = psutil.virtual_memory()
    larg = largura_tela - 2 * 20
    tela3.fill(preto)
    pygame.draw.rect(tela3, azul, (20, 50, larg, 70))
    larg = larg * mem.percent / 100
    pygame.draw.rect(tela3, vermelho, (20, 50, larg, 70))
    texto_barra = get_info('memoria')
    text = font.render(texto_barra, 1, branco)
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
                    if pagina < 4:
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
            '''if pagina == 4:
                pid()
            if pagina == 5:
               diretorio()
            if pagina == 6:
                redeLocal()
            if pagina == 7:
                resumo()'''
            controle = 0
            '''if diff < 1:
                print("A tarefa demorou menos de 1 segundos e o clock foi de " + str(
                    round(time.perf_counter(), 1)) + " segundo(s)!")
            elif diff > 59:
                print("A tarefa demorou aproximadamente " + str(
                    round(diff / 60, 1)) + " minuto(s) e o clock foi de " + str(
                    round(time.perf_counter() / 60, 1)) + " minutos(s)!")
            else:
                print("A tarefa demorou " + str(int(diff)) + " segundos e o clock foi de " + str(
                    round(time.perf_counter(), 1)) + " segundo(s)!")'''
        pygame.display.update()
        controle += 1
        CLOCK.tick(HZ)

def __init__():
    print('entrou')
    main()