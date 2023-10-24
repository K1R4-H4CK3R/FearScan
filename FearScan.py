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
    print("#   Versão: 2.0                                   #")
    print("#                                                 #")
    print("\033[95m" + "#" * 50)
exibir_banner()

# Função para verificar se uma porta está aberta
def verifica_porta(ip, porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Definir um tempo limite de 1 segundo para a conexão
    resultado = sock.connect_ex((ip, porta))
    sock.close()
    if resultado == 0:
        print("\033[92m[A porta {} está aberta]\033[0m".format(porta))
        return True
    # Suprimir a mensagem de erro do socket
    elif resultado == 10035:  # Código de erro para timeout
        pass
    else:
        pass  # Outros erros de porta

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

# Função para extrair informações do site e salvar em arquivos
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

# IP ou URL do alvo
alvo = input("\033[95m[Digite o Ip ou Url:]\033[0m")

# Especificar o intervalo de portas a serem verificadas
porta_inicio = int(input("Digite a porta de início: "))
porta_fim = int(input("Digite a porta de fim: "))

# Verifica as portas no intervalo especificado
for porta in range(porta_inicio, porta_fim + 1):
    verifica_porta(alvo, porta)  # Verifica a porta

    # URL completa do alvo
    url_alvo = f'http://{alvo}:{porta}'
    # Encontra a página de administração do alvo
    encontra_pagina_admin(url_alvo)
    # Encontra o usuário e senha de administração do alvo
    encontra_user_senha_admin(url_alvo)
    # Extrair e salvar informações do site
    informacoes_salvas = extrair_e_salvar_informacoes(url_alvo)

    # Exibir os arquivos onde as informações foram salvas
    if informacoes_salvas:
        print("Informações extraídas e salvas nos seguintes arquivos:")
        for tipo, arquivo in informacoes_salvas.items():
            print(f"{tipo}: {arquivo}")