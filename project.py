from PIL import Image, ImageDraw, ImageFont
from validator_collection import validators, checkers
import sys
import os
import requests
import json


def main():

    escolha_usuario = get_escolha_usuario()

    match escolha_usuario:
        case 1:
            novo_template()
        case 2:
            construir_meme()
        case _:
            sys.exit("Error: Invalid option")


def get_escolha_usuario():
    while True:
        try:
            print(
                "\n[1] - Add new img to archive | [2] - Add text to template")
            escolha = int(input("Which option do you want? "))
            if escolha not in [1, 2]:
                print("Invalid option.")
                continue
            return escolha
        except ValueError:
            print("\nError in choice input. Try again.")
        except (EOFError, KeyboardInterrupt):
            sys.exit("\nPrograma encerrado pelo usuario.")


def novo_template():
    url_valida = obter_url_valida()

    nome_arquivo = obter_nome_arquivo()
    caminho_salvamento = os.path.join("templates", f"{nome_arquivo}.jpg")

    conteudo_imagem = baixar_imagem(url_valida)
    if not conteudo_imagem:
        return
    
    configuracoes_texto = obter_configuracoes_texto()
    if not configuracoes_texto:
        return
    
    caminho_arquivo = salvar_imagem(caminho_salvamento, conteudo_imagem)
    if not caminho_arquivo:
        return
    
    registrar_template_json(nome_arquivo, caminho_arquivo, configuracoes_texto)

    print(f"Template '{nome_arquivo}' configurado com sucesso.")


def obter_url_valida():
    while True:
        url_input = input("Type the image URL: ")
        try:
            url_formatada = validators.url(url_input)
            if checkers.is_url(url_formatada):
                return url_formatada
            else:
                print("The URL is invalid. Try again.")
        except ValueError:
            print("The URL is malformed. Try again.")


def obter_nome_arquivo():
    while True:
        nome_arquivo = input("Type the name for the file: ").strip()
        if nome_arquivo:
            return nome_arquivo
        else:
            print("File name cannot be empty. Try again.")


def baixar_imagem(url_valida):
    try:
        response = requests.get(url_valida)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '').lower()
            if not content_type.startswith('image/'):
                print(f"Error: The provided URL does not point to a valid image. (Type: {content_type})")
                return None
            return response.content
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
            return None
    except requests.RequestException:
        print("An error occurred while connecting to the URL.")
        return None


def obter_configuracoes_texto():
    while True:
        try:
            x_pos = int(input("Type the X coordinate for text: "))
            y_pos = int(input("Type the Y coordinate for text: "))
            tamanho_fonte = int(input("Type the font size for text: "))
        except ValueError:
            print("Coordinates and font size must be integers. Try again.")
        else:
            break

    while True:
        cor_input = input("Type the text color (black/white): ").strip().lower()
        try:
            cor_validada = validar_cor(cor_input)
            break
        except ValueError:
            print("Invalid color. Please choose either 'black' or 'white'.")

    return {
        "x": x_pos,
        "y": y_pos,
        "size": tamanho_fonte,
        "color": cor_validada
    }


def salvar_imagem(caminho_salvamento, conteudo_imagem):
    try:
        with open(caminho_salvamento, "wb") as meme_novo:
            meme_novo.write(conteudo_imagem)
        return caminho_salvamento
    except IOError as e:
        print(f"Error saving image: {e}")
        return None


def registrar_template_json(nome_arquivo, caminho_arquivo, configuracoes_texto):
    novo_template_dados = {
        "x": configuracoes_texto["x"],
        "y": configuracoes_texto["y"],
        "tamanho_fonte": configuracoes_texto["tamanho_fonte"],
        "cor_texto": configuracoes_texto["cor_texto"],
        "caminho_template": caminho_arquivo
    }

    dados_json = {}
    if os.path.exists("templates.json"):
        try:
            with open("templates.json", "r") as arquivo_json:
                dados_json = json.load(arquivo_json)
        except json.JSONDecodeError:
            pass

    dados_json[formatar_template_inserido(nome_arquivo)] = novo_template_dados

    with open("templates.json", "w") as arquivo_json:
        json.dump(dados_json, arquivo_json, indent=4)


def construir_meme():
    template_desejado, texto_meme = selecionar_template_texto()

    x_position, y_position, tamanho_fonte, cor_texto, template_escolhido = carregar_template(template_desejado)

    if template_escolhido:
        criar_arquivo_output(template_escolhido, texto_meme, tamanho_fonte, cor_texto, x_position, y_position)
        print(f"\n{template_desejado} meme successfully created!\n")
    else:
        print("Could not create meme due to missing template configurations.")


def selecionar_template_texto():
    pasta_templates = "templates"
    if not os.path.exists(pasta_templates):
        os.makedirs(pasta_templates)

    arquivos = os.listdir(pasta_templates)
    templates_disponiveis = []

    for arquivo in arquivos:
        if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            nome_sem_extensao = os.path.splitext(arquivo)[0]
            nome_formatado = nome_sem_extensao.replace("_", " ").title()
            templates_disponiveis.append(nome_formatado)

    if not templates_disponiveis:
        sys.exit("Error: Sem templates disponíveis. Adicione um template primeiro.")
    templates_disponiveis.sort()

    while True:
        try:
            print(templates_disponiveis)
            template_desejado = input("Which template you wish to use? ")

            if not template_desejado.strip().lower().title() in templates_disponiveis:
                print("Unavailable template. Select one of the following: ")
                continue
            else:
                template_desejado = template_desejado.strip().lower().title()
                print(f"\n{template_desejado} template selected!\n")

        except (EOFError, KeyboardInterrupt):
            sys.exit("\nPrograma encerrado pelo usuario.")

        while True:
            try:
                texto_meme = input("What text you wish to put into the selected template? ")
                if input(f"\nOk, so you wish to write '{texto_meme}' into the {template_desejado} template?[y/n] ").strip().lower() in ['y', "ye", "yes"]:
                    return (template_desejado, texto_meme)
                else:
                    break
            except EOFError:
                print("Input error. Try again")


def carregar_template(template_desejado):
    chave_template = formatar_template_inserido(template_desejado)
    caminho_configuracoes = "templates.json"

    if not os.path.exists(caminho_configuracoes):
        print(f"Error: {caminho_configuracoes} not found.")
        return (None, None, None, None, None)

    try:
        with open(caminho_configuracoes, "r") as arquivo_configuracoes:
            dados = json.load(arquivo_configuracoes)
            if chave_template in dados:
                t = dados[chave_template]
                # Se os templates antigos não tiverem a chave "color", o padrão assume "black"
                cor = t.get("color", "black")
                return (t["x"], t["y"], t["size"], cor, t["caminho_template"])
            else:
                print(f"Error: '{template_desejado}' coordinates not found in JSON file.")
    except json.JSONDecodeError:
        print(f"Error: '{caminho_configuracoes}' is corrupted or poorly formatted.")

    return (None, None, None, None, None)


def criar_arquivo_output(template_escolhido, text, tamanho_fonte, cor_texto, x_position, y_position):
    with Image.open(template_escolhido) as arquivo_template:
        draw = ImageDraw.Draw(arquivo_template)
        font = ImageFont.truetype("ARIALLGT.TTF", size=tamanho_fonte)

        rgb_color = converter_cor_para_rgb(cor_texto)
        draw.text((x_position, y_position), text, fill=rgb_color, font=font)

        nome_arquivo = os.path.basename(template_escolhido)
        nome_sem_extensao = os.path.splitext(nome_arquivo)[0]

        if not os.path.exists("output"):
            os.makedirs("output")

        caminho_salvamento = os.path.join("output", f"{nome_sem_extensao}_meme.jpg")
        arquivo_template.save(caminho_salvamento)


def validar_cor(cor_input):
    cor_formatada = cor_input.strip().lower()
    if cor_formatada not in ["black", "white"]:
        raise ValueError("Color must be 'black' or 'white'")
    return cor_formatada


def formatar_template_inserido(template_inserido):
    return template_inserido.strip().lower().replace(" ", "_")


def converter_cor_para_rgb(cor_texto):
    if cor_texto == "white":
        return (255, 255, 255)
    return (0, 0, 0)


if __name__ == "__main__":
    main()
