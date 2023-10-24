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
    print("#   Versão: 3.0                                   #")
    print("#                                                 #")
    print("\033[95m" + "#" * 50)

def obter_ip(site):
    try:
        ip = socket.gethostbyname(site)
        return ip
    except socket.gaierror:
        print("\033[91m[Erro ao obter o IP do site. Verifique se o site está correto.]\033[0m")
        return None

def verificar_portas(ip, porta_inicio, porta_fim):
    print("\n\033[93m[Verificando as portas no intervalo {} - {} para o site {}]\033[0m".format(porta_inicio, porta_fim, site))
    for porta in range(porta_inicio, porta_fim + 1):
        if verifica_porta(ip, porta):
            print("\033[92m[Porta {} está aberta]\033[0m".format(porta))

def verifica_porta(ip, porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Definir um tempo limite de 1 segundo para a conexão
    resultado = sock.connect_ex((ip, porta))
    sock.close()
    if resultado == 0:
        return True
    elif resultado == 10035:  # Código de erro para timeout
        pass
    else:
        pass

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

def extrair_e_salvar_informacoes(url):
    try:
        pagina = requests.get(url)
        pagina.raise_for_status()
        soup = BeautifulSoup(pagina.content, 'html.parser')
        
        # Extrair texto da página
        texto = soup.get_text()
        
        # Extrair todas as imagens da página
        imagens = [img['src'] for img in soup.find_all('img', src=True)]
        
        # Extrair todos os scripts da página
        scripts = [script['src'] for script in soup.find_all('script', src=True)]
        
        # Criar um diretório para salvar as informações
        site_name = url.split('//')[1].split('/')[0]
        if not os.path.exists(site_name):
            os.makedirs(site_name)
        
        # Salvar informações em arquivos separados
        with open(f"{site_name}/texto.txt", 'w', encoding='utf-8') as file:
            file.write(texto)
        
        with open(f"{site_name}/imagens.txt", 'w', encoding='utf-8') as file:
            for imagem in imagens:
                file.write(imagem + '\n')
        
        with open(f"{site_name}/scripts.txt", 'w', encoding='utf-8') as file:
            for script in scripts:
                file.write(script + '\n')

        return {
            'texto': f"{site_name}/texto.txt",
            'imagens': f"{site_name}/imagens.txt",
            'scripts': f"{site_name}/scripts.txt"
        }
    except requests.exceptions.RequestException as e:
        print("Erro ao acessar o site:", e)
        return {}

exibir_banner()
site = input("\033[95m[Digite o site (URL):]\033[0m")
ip = obter_ip(site)

if ip:
    print("\033[93m[IP do site:]\033[0m", ip)
    porta_inicio = int(input("Digite a porta de início: "))
    porta_fim = int(input("Digite a porta de fim: "))
    
    verificar_portas(ip, porta_inicio, porta_fim)

    url_alvo = f'http://{site}'
    encontra_pagina_admin(url_alvo)
    encontra_user_senha_admin(url_alvo)
    informacoes_salvas = extrair_e_salvar_informacoes(url_alvo)

    if informacoes_salvas:
        print("Informações extraídas e salvas nos seguintes arquivos:")
        for tipo, arquivo in informacoes_salvas.items():
            print(f"{tipo}: {arquivo}")
