from PIL import Image, ImageDraw, ImageFont
from validator_collection import validators, checkers
import sys
import os
import requests
import json


def main():

    user_response = menu()

    match user_response:
        case 1:
            get_new_img()
        case 2:
            add_text_to_img()
        case _:
            print("Invalid option")


def menu():
    while True:
        try:
            print(
                "\n[1] - Add new img to archive | [2] - Add text to template")
            response = int(input("Which option do you want? "))
            if response not in [1, 2]:
                print("Invalid option.")
                continue
            return response
        except (ValueError, EOFError):
            print("\nError in choice input. Try again.")


def get_new_img():
    while True:
        image_url = input("Type the image URL: ")
        try:
            valid_url = validators.url(image_url)
            if checkers.is_url(valid_url):
                break
            else:
                print("The URL is invalid. Try again.")
        except ValueError:
            print("The URL is malformed. Try again.")

    archive_name = input("Type the name to the file: ").strip()
    caminho_salvamento = os.path.join("templates", f"{archive_name}.jpg")

    try:
        response = requests.get(valid_url)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '').lower()
            if not content_type.startswith('image/'):
                sys.exit(
                    f"Error: The provided URL does not point to a valid image. (Type: {content_type})")
                return
            else:
                while True:
                    try:
                        x_pos = int(input("Type the X coordinate for text: "))
                        y_pos = int(input("Type the Y coordinate for text: "))
                        font_size = int(input("Type the font size for text: "))
                        break
                    except ValueError:
                        print("Coordinates and font size must be integers. Try again.")

                while True:
                    cor_input = input("Type the text color (black/white): ").strip().lower()
                    try:
                        cor_input = validate_color(cor_input)
                        break
                    except ValueError:
                        print("Invalid color. Please choose either 'black' or 'white'.")

            with open(caminho_salvamento, "wb") as file:
                file.write(response.content)

            chave_json = format_template_key(archive_name)
            novo_template_dados = {
                "x": x_pos,
                "y": y_pos,
                "size": font_size,
                "color": cor_input,
                "file": caminho_salvamento
            }

            dados_json = {}
            if os.path.exists("templates.json"):
                try:
                    with open("templates.json", "r") as file:
                        dados_json = json.load(file)
                except json.JSONDecodeError:
                    pass

            dados_json[chave_json] = novo_template_dados

            with open("templates.json", "w") as file:
                json.dump(dados_json, file, indent=4)

            print(f"Template '{archive_name}' successfully added and configured!")
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
    except requests.RequestException:
        print("An error occurred while connecting to the URL.")

def add_text_to_img():
    wished_template, text = get_user_input()

    x_position, y_position, font_size, text_color, template_file = text_placement(
        wished_template)

    if template_file:
        output_image(template_file, text, font_size, text_color, x_position, y_position)
        print(f"\n{wished_template} meme successfully created!\n")
    else:
        print("Could not create meme due to missing template configurations.")


def get_user_input():
    pasta_templates = "templates"
    if not os.path.exists(pasta_templates):
        os.makedirs(pasta_templates)

    arquivos = os.listdir(pasta_templates)
    available_templates = []
    for arquivo in arquivos:
        if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            nome_sem_extensao = os.path.splitext(arquivo)[0]
            nome_formatado = nome_sem_extensao.replace("_", " ").title()
            available_templates.append(nome_formatado)

    available_templates.sort()

    while True:
        try:
            print(available_templates)
            wished_template = input("Which template you wish to use? ")

            if not wished_template.strip().lower().title() in available_templates:
                print("Unavailable template. Select one of the following: ")
                continue
            else:
                wished_template = wished_template.strip().lower().title()
                print(f"\n{wished_template} template selected!\n")

        except EOFError:
            print("Input error. Try again")
            continue

        while True:
            try:
                input_text = input("What text you wish to put into the selected template? ")
                if input(f"\nOk, so you wish to write '{input_text}' into the {wished_template} template?[y/n] ").strip().lower() in ['y', "ye", "yes"]:
                    return (wished_template, input_text)
                else:
                    break
            except EOFError:
                print("Input error. Try again")


def text_placement(wished_template):
    chave_template = format_template_key(wished_template)
    config_file = "templates.json"

    if not os.path.exists(config_file):
        print(f"Error: {config_file} not found.")
        return (None, None, None, None, None)

    try:
        with open(config_file, "r") as file:
            dados = json.load(file)
            if chave_template in dados:
                t = dados[chave_template]
                # Se os templates antigos não tiverem a chave "color", o padrão assume "black"
                cor = t.get("color", "black")
                return (t["x"], t["y"], t["size"], cor, t["file"])
            else:
                print(f"Error: '{wished_template}' coordinates not found in JSON file.")
    except json.JSONDecodeError:
        print(f"Error: '{config_file}' is corrupted or poorly formatted.")

    return (None, None, None, None, None)


def output_image(template_file, text, font_size, text_color, x_position, y_position):
    with Image.open(template_file) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("ARIALLGT.TTF", size=font_size)

        rgb_color = convert_color_to_rgb(text_color)
        draw.text((x_position, y_position), text, fill=rgb_color, font=font)

        nome_arquivo = os.path.basename(template_file)
        nome_sem_extensao = os.path.splitext(nome_arquivo)[0]

        if not os.path.exists("output"):
            os.makedirs("output")

        caminho_salvamento = os.path.join("output", f"{nome_sem_extensao}_meme.jpg")
        img.save(caminho_salvamento)


def validate_color(color_string):
    clean_color = color_string.strip().lower()
    if clean_color not in ["black", "white"]:
        raise ValueError("Color must be 'black' or 'white'")
    return clean_color


def format_template_key(name_string):
    return name_string.strip().lower().replace(" ", "_")


def convert_color_to_rgb(color_name):
    if color_name == "white":
        return (255, 255, 255)
    return (0, 0, 0)


if __name__ == "__main__":
    main()
