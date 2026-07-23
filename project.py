import os
import json
import sys

from PIL import Image, ImageDraw, ImageFont
import requests
from validator_collection import validators, checkers


PASTA_TEMPLATES = "templates"
PASTA_OUTPUT = "output"
ARQUIVO_CONFIG_JSON = "templates.json"
FONTE_PADRAO = "ARIALLGT.TTF"


def main() -> None:

    escolha_usuario = get_escolha_usuario()

    match escolha_usuario:
        case 1:
            novo_template()
        case 2:
            construir_meme()
        case _:
            sys.exit("Erro: Opção inválida. Programa encerrado.")


def get_escolha_usuario() -> int:
    while True:
        try:
            print(
                "\n[1] - Criar novo template para memes | [2] - Criar novo meme")
            escolha = int(input("Qual função deseja utilizar? "))
            if escolha not in [1, 2]:
                print("Opção inválida.")
                continue
            return escolha
        except ValueError:
            print("\nErro: Entrada inválida. Digite um número inteiro (1 ou 2).")
        except (EOFError, KeyboardInterrupt):
            sys.exit("\nPrograma encerrado pelo usuario.")


def novo_template() -> None:
    url_valida = obter_url_valida()

    nome_arquivo = obter_nome_arquivo()
    caminho_salvamento = os.path.join(PASTA_TEMPLATES, f"{nome_arquivo}.jpg")

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


def obter_url_valida() -> str:
    while True:
        url_input = input("Digite o URL da imagem que deseja usar como template: ")
        try:
            url_formatada = validators.url(url_input)
            if checkers.is_url(url_formatada):
                return url_formatada
            else:
                print("O URL é inválido. Tente novamente.")
        except ValueError:
            print("A URL está desformatada. Tente novamente.")


def obter_nome_arquivo() -> str:
    while True:
        nome_arquivo = input("Digite o nome desejado para o novo arquivo: ").strip()
        if nome_arquivo:
            return nome_arquivo
        else:
            print("O nome do arquivo não pode estar vazio. Tente novamente.")


def baixar_imagem(url_valida: str) -> bytes | None:
    try:
        response = requests.get(url_valida, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '').lower()
            if not content_type.startswith('image/'):
                print(f"Erro: A URL fornecida não aponta para uma imagem válida. (Tipo: {content_type})")
                return None
            return response.content
        else:
            print(f"Erro: Falha ao recuperar a imagem. Código de status: {response.status_code}")
            return None
    except requests.RequestException:
        print("Erro: Ocorreu um erro ao conectar-se à URL.")
        return None


def obter_configuracoes_texto() -> dict[str, int | str] | None:
    while True:
        try:
            x_pos = int(input("Digite a coordenada X para o texto: "))
            y_pos = int(input("Digite a coordenada Y para o texto: "))
            tamanho_fonte = int(input("Digite o tamanho da fonte para o texto: "))
        except ValueError:
            print("As coordenadas e o tamanho da fonte devem ser números inteiros. Tente novamente.")
        except (EOFError, KeyboardInterrupt):
            sys.exit("\nPrograma encerrado pelo usuario.")
        else:
            break

    while True:
        cor_input = input("Digite a cor do texto (black/white): ").strip().lower()
        try:
            cor_validada = validar_cor(cor_input)
            break
        except ValueError:
            print("Cor inválida. Por favor, escolha entre 'black' ou 'white'.")

    return {
        "x": x_pos,
        "y": y_pos,
        "tamanho_fonte": tamanho_fonte,
        "cor_texto": cor_validada
    }


def salvar_imagem(caminho_salvamento: str, conteudo_imagem: bytes) -> str | None:
    try:
        with open(caminho_salvamento, "wb") as meme_novo:
            meme_novo.write(conteudo_imagem)
        return caminho_salvamento
    except IOError as e:
        print(f"Erro ao salvar imagem: {e}")
        return None


def registrar_template_json(nome_arquivo: str, caminho_arquivo: str, configuracoes_texto: dict[str, int | str]) -> None:
    novo_template_dados = {
        "x": configuracoes_texto["x"],
        "y": configuracoes_texto["y"],
        "tamanho_fonte": configuracoes_texto["tamanho_fonte"],
        "cor_texto": configuracoes_texto["cor_texto"],
        "caminho_template": caminho_arquivo
    }

    dados_json = {}
    if os.path.exists(ARQUIVO_CONFIG_JSON):
        try:
            with open(ARQUIVO_CONFIG_JSON, "r") as arquivo_json:
                dados_json = json.load(arquivo_json)
        except json.JSONDecodeError:
            pass

    dados_json[formatar_template_inserido(nome_arquivo)] = novo_template_dados

    with open(ARQUIVO_CONFIG_JSON, "w") as arquivo_json:
        json.dump(dados_json, arquivo_json, indent=4)


def construir_meme() -> None:
    template_desejado, texto_meme = selecionar_template_texto()

    pos_x, pos_y, tamanho_fonte, cor_texto, template_escolhido = carregar_template(template_desejado)

    if template_escolhido:
        criar_arquivo_output(template_escolhido, texto_meme, tamanho_fonte, cor_texto, pos_x, pos_y)
        print(f"\nMeme do template {template_desejado} criado com sucesso!\n")
    else:
        print("Não foi possível criar o meme devido à ausência de configurações de template.")


def selecionar_template_texto() -> tuple[str, str]:
    pasta_templates = PASTA_TEMPLATES
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
        sys.exit("Erro: Sem templates disponíveis. Adicione um template primeiro.")
    templates_disponiveis.sort()

    while True:
        try:
            print(templates_disponiveis)
            template_desejado = input("Qual template você deseja usar? ")

            if not template_desejado.strip().lower().title() in templates_disponiveis:
                print("Template indisponível. Selecione um dos seguintes: ")
                continue
            else:
                template_desejado = template_desejado.strip().lower().title()
                print(f"\nTemplate '{template_desejado}' selecionado!\n")

        except (EOFError, KeyboardInterrupt):
            sys.exit("\nPrograma encerrado pelo usuario.")

        while True:
            try:
                texto_meme = input("Qual texto você deseja colocar no template selecionado? ")
                if input(f"\nOk, então você deseja escrever '{texto_meme}' no template {template_desejado}? [y/n] ").strip().lower() in ['y', "ye", "yes"]:
                    return (template_desejado, texto_meme)
                else:
                    break
            except EOFError:
                print("Erro: Entrada inválida. Tente novamente.")


def carregar_template(template_desejado: str) -> tuple[int | None, int | None, int | None, str | None, str | None]:
    chave_template = formatar_template_inserido(template_desejado)
    caminho_configuracoes = ARQUIVO_CONFIG_JSON

    if not os.path.exists(caminho_configuracoes):
        print(f"Erro: {caminho_configuracoes} não encontrado.")
        return (None, None, None, None, None)

    try:
        with open(caminho_configuracoes, "r") as arquivo_configuracoes:
            dados = json.load(arquivo_configuracoes)
            if chave_template in dados:
                t = dados[chave_template]
                # Se os templates antigos não tiverem a chave "cor_texto", o padrão assume "black"
                cor = t.get("cor_texto", "black")
                return (t["x"], t["y"], t["tamanho_fonte"], cor, t["caminho_template"])
            else:
                print(f"Erro: Coordenadas do template '{template_desejado}' não encontradas no arquivo JSON.")
    except json.JSONDecodeError:
        print(f"Erro: '{caminho_configuracoes}' está corrompido ou desformatado.")

    return (None, None, None, None, None)


def criar_arquivo_output(template_escolhido: str, text: str, tamanho_fonte: int, cor_texto: str, pos_x: int, pos_y: int) -> None:
    with Image.open(template_escolhido) as arquivo_template:
        draw = ImageDraw.Draw(arquivo_template)
        try:
            font = ImageFont.truetype(FONTE_PADRAO, size=tamanho_fonte)
        except OSError:
            print(f"Erro: Fonte '{FONTE_PADRAO}' não encontrada. Fonte padrão selecionada.")
            font = ImageFont.load_default()

        cor_em_rgb = converter_cor_para_rgb(cor_texto)
        draw.text((pos_x, pos_y), text, fill=cor_em_rgb, font=font)

        nome_arquivo = os.path.basename(template_escolhido)
        nome_sem_extensao = os.path.splitext(nome_arquivo)[0]

        if not os.path.exists(PASTA_OUTPUT):
            os.makedirs(PASTA_OUTPUT)

        caminho_salvamento = os.path.join(PASTA_OUTPUT, f"{nome_sem_extensao}_meme.jpg")
        arquivo_template.save(caminho_salvamento)


def validar_cor(cor_input: str) -> str:
    cor_formatada = cor_input.strip().lower()
    if cor_formatada not in ["black", "white"]:
        raise ValueError("A cor deve ser 'black' ou 'white'")
    return cor_formatada


def formatar_template_inserido(template_inserido: str) -> str:
    return template_inserido.strip().lower().replace(" ", "_")


def converter_cor_para_rgb(cor_texto: str) -> tuple[int, int, int]:
    if cor_texto == "white":
        return (255, 255, 255)
    return (0, 0, 0)


if __name__ == "__main__":
    main()
