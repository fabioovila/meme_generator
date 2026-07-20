# Meme Generator

#### Description:
This project is a Command-Line Interface (CLI) tool built in Python designed to easily automate and create customized memes. The main motivation was to have a quick way to overlay text onto images without needing to open heavy image editors or deal with ad-filled websites.

With this program, you can download new templates directly from the internet using a URL, configure the exact X and Y coordinates for the text placement, choose the font size, set the text color (black or white), and instantly generate the final image while keeping everything organized.

---

## Features

* **Save New Templates:** You provide the image URL and the name you want to give it. The program downloads the file and stores it inside the `templates/` folder.
* **Configure Text Settings:** When adding a new image, you define where the text should sit (X and Y axes), the font size, and the default color.
* **Color Validation:** The code strictly accepts "black" or "white" as inputs, ensuring the text remains readable depending on the image background.
* **Automated Generation:** The program reads the saved configurations from a JSON file, renders the text onto the image, and exports the finished meme to the `output/` folder.

---

## File Structure

* **`project.py`**: The main file of the application. It contains the `main()` function, the interactive terminal menu, the download logic using the `requests` library, and the image editing workflow via Pillow (`PIL`).
* **`test_project.py`**: The file containing the automated unit tests to be executed with `pytest`. It tests the pure formatting and validation functions without freezing or waiting for terminal inputs.
* **`templates.json`**: Acts as our lightweight database. It stores each image's file path, X/Y coordinates, font size, and chosen text color.
* **`templates/`**: The directory that stores the clean, downloaded template images.
* **`output/`**: The directory where the finalized memes with text are saved.

---

## Design Choices

### 1. Separating Functions for Pytest
At first, the code mixed terminal `input()` calls directly with the program logic. However, to make `pytest` work smoothly without hanging, I had to separate concerns. I created isolated functions like `validate_color`, `format_template_key`, and `convert_color_to_rgb`. They simply receive data, process it, and return a value (or raise an error), making unit testing incredibly straightforward.

### 2. Using JSON instead of a Relational Database (SQLite)
Since the goal of this project is to be lightweight and practical, using a `.json` file made a lot more sense than setting up a SQLite database. The JSON file perfectly handles reading and writing configuration parameters quickly and directly.

---

## How to Run the Project

First, install the necessary dependencies:
```bash
pip install (pillow validator-collection requests pytest)
