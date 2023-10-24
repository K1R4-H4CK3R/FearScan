import socket
import requests
from bs4 import BeautifulSoup
import os

def exibir_banner():
    print("\033[95m" + "#" * 50)
    print("#  \\  FearScan - Verificação e Análise de Alvo  /  #")
    print("#    ------------------------------------         #")
    print("#                                                 #")
    print("#   Autor: \033[92m[Skull'Xss]\033[0m                            #")
    print("#   Versão: 1.0                                   #")
    print("#                                                 #")
    print("\033[95m" + "#" * 50)
exibir_banner()

# Função para verificar se uma porta está aberta
def verifica_porta(ip, porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Definir um tempo limite de 1 segundo para a conexão
    try:
        resultado = sock.connect_ex((ip, porta))
        sock.close()
        if resultado == 0:
            print("\033[92m[A porta {} está aberta]\033[0m".format(porta))
            return True
        return False
    except socket.gaierror as e:
        print(f"Erro ao resolver o hostname: {e}")
        return False

# Função para encontrar a página de administração de um site e salvar em arquivo
def encontra_pagina_admin(url):
    try:
        pagina = requests.get(url)
        pagina.raise_for_status()
        soup = BeautifulSoup(pagina.content, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            if 'admin' in link.get('href'):
                admin_url = link.get("href")
                print("\033[93m[Página de admin encontrada:]\033[0m {}".format(admin_url))
                # Salva a página de administração em um arquivo com o nome do site
                site_name = url.split('//')[1].split('/')[0]
                with open(f"{site_name}_admin_page.html", 'w', encoding='utf-8') as file:
                    admin_page = requests.get(url + admin_url)
                    file.write(admin_page.text)
    except requests.exceptions.RequestException:
        pass

# Função para encontrar o usuário e senha de administração do site e salvar em arquivo
def encontra_user_senha_admin(url):
    try:
        pagina = requests.get(url)
        pagina.raise_for_status()
        soup = BeautifulSoup(pagina.content, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            inputs = form.find_all('input')
            user_info = {}
            for input in inputs:
                user_info[input.get("name")] = input.get("value")
            if user_info:
                print("\033[91m[Informações de Usuário e Senha Encontradas:]\033[0m")
                for key, value in user_info.items():
                    print(f"\033[91m{key}:\033[0m {value}")
                # Salva informações em um arquivo
                site_name = url.split('//')[1].split('/')[0]
                with open(f"{site_name}_user_info.txt", 'w', encoding='utf-8') as file:
                    for key, value in user_info.items():
                        file.write(f"{key}: {value}\n")
    except requests.exceptions.RequestException:
        pass

# IP ou URL do alvo
alvo = input("\033[95m[Digite o Ip ou Url:]\033[0m")

# Verifica todas as portas entre 1 e 10000 do alvo
for porta in range(1, 10001):
    if verifica_porta(alvo, porta):
        # URL completa do alvo
        url_alvo = f'http://{alvo}:{porta}'
        # Encontra a página de administração do alvo
        encontra_pagina_admin(url_alvo)
        # Encontra o usuário e senha de administração do alvo
        encontra_user_senha_admin(url_alvo)
