# 🎨 Meme Generator

A powerful command-line tool for automating meme creation with customizable templates, intelligent text placement, and easy image management.

---

## 📋 Overview

**Meme Generator** is a comprehensive CLI application built as the final project for Harvard's CS50P course. It streamlines the workflow of creating custom memes by allowing users to download image templates from the web, configure text positioning and styling, and generate polished output images with a single command.

The project demonstrates proficiency in file manipulation, web requests, image processing, and clean software architecture with comprehensive testing practices.

---

## 🛠️ Technologies & Languages

### **Core Language**
- **Python 3** - Full application logic and CLI interface

### **Key Libraries & Dependencies**
| Library | Purpose |
|---------|---------|
| **Pillow (PIL)** | Image processing, text rendering, and manipulation |
| **Requests** | HTTP requests for downloading image templates from URLs |
| **validator-collection** | URL validation and data integrity checks |
| **pytest** | Unit testing and automated test execution |
| **JSON** | Lightweight configuration storage and template metadata |

### **Additional Technologies**
- **File I/O Operations** - Managing templates and output directories
- **Regular Expression Pattern Matching** - File type validation
- **Object-Oriented Design** - Clean, modular function structure
- **Error Handling & Exception Management** - Robust input validation

---

## ✨ Features

* **🌐 Download New Templates** – Provide an image URL and the program automatically downloads and stores it in the `templates/` folder
* **📍 Configure Text Placement** – Define exact X and Y coordinates for text positioning on each template
* **🎯 Customizable Styling** – Set font size, select text color (black or white), and ensure optimal readability
* **🔒 Color Validation** – Strict validation ensures text remains readable against any background
* **⚡ Automated Generation** – Read configurations from JSON, render text, and export finished memes to `output/` folder
* **✅ Comprehensive Testing** – Full pytest test suite for validation functions and data formatting

---

## 📁 File Structure

```
meme_generator/
├── project.py                 # Main application logic
├── test_project.py           # Unit tests (pytest)
├── templates.json            # Configuration database (JSON)
├── ARIALLGT.TTF             # Font file for text rendering
├── templates/               # Directory for template images
├── output/                  # Directory for generated memes
└── README.md               # Documentation
```

### **Core Files**

- **`project.py`** (7.7 KB)
  - Interactive CLI menu system
  - `get_new_img()` – Downloads images via HTTP and stores configurations
  - `add_text_to_img()` – Renders text onto templates using Pillow
  - URL validation using `requests` library
  - JSON read/write operations for persistent storage
  - Comprehensive error handling and user input validation

- **`test_project.py`** (785 B)
  - `test_validate_color()` – Validates color input handling
  - `test_format_template_key()` – Tests string formatting logic
  - `test_convert_color_to_rgb()` – Verifies RGB color conversion
  - All tests execute with pytest without terminal blocking

- **`templates.json`**
  - Stores template metadata: file paths, text coordinates, font sizes, colors
  - 9+ pre-configured templates with optimized settings
  - Lightweight alternative to SQL databases for this use case

---

## 🏗️ Design Patterns & Decisions

### **1. Separation of Concerns**
The codebase separates I/O operations from pure business logic, enabling:
- Unit testing without terminal interaction
- Reusable functions without external dependencies
- Easy debugging and maintenance

### **2. JSON Configuration Over Relational Databases**
Chosen for:
- **Simplicity** – No database setup required
- **Portability** – Easy to share and version control
- **Readability** – Human-editable configuration files
- **Lightweight** – Minimal dependencies for a personal project

### **3. Robust Input Validation**
- URL validation using `validator-collection` library
- Type checking for coordinates and font sizes
- Content-type verification to prevent invalid image uploads
- Graceful error messages for user guidance

### **4. Modular Function Design**
Small, testable functions with single responsibilities:
- `validate_color()` – Color string validation
- `format_template_key()` – String formatting
- `convert_color_to_rgb()` – Color conversion
- `text_placement()` – Configuration retrieval

---

## 🚀 How to Run

### **Prerequisites**
```bash
pip install pillow validator-collection requests pytest
```

### **Installation**
```bash
git clone https://github.com/fabioovila/meme_generator.git
cd meme_generator
```

### **Running the Application**
```bash
python project.py
```

**Menu Options:**
1. **Add new template** – Provide a URL to download and configure a new meme template
2. **Generate meme** – Select a template and add custom text to create a meme

### **Running Tests**
```bash
pytest test_project.py -v
```

---

## 📸 Example Workflow

```
$ python project.py

[1] - Add new img to archive | [2] - Add text to template
Which option do you want? 1

Type the image URL: https://example.com/meme_template.jpg
Type the name to the file: my_template
Type the X coordinate for text: 100
Type the Y coordinate for text: 150
Type the font size for text: 24
Type the text color (black/white): white

Template 'my_template' successfully added and configured!

[1] - Add new img to archive | [2] - Add text to template
Which option do you want? 2

Which template you wish to use? ['My Template']
What text you wish to put into the selected template? Hello World!
Ok, so you wish to write 'Hello World!' into the My Template template?[y/n] y

My Template meme successfully created!
```

---

## 🧪 Testing & Quality Assurance

The project includes a comprehensive test suite using **pytest**:

```bash
$ pytest test_project.py -v
test_project.py::test_validate_color PASSED
test_project.py::test_format_template_key PASSED
test_project.py::test_convert_color_to_rgb PASSED
```

**Test Coverage:**
- ✅ Color validation (valid/invalid inputs)
- ✅ String formatting with whitespace handling
- ✅ RGB color conversion logic
- ✅ Edge cases and error conditions

---

## 📚 Learning Outcomes & Skills Demonstrated

This project showcases proficiency in:

- **Python Programming** – Advanced function design, error handling, file operations
- **Web Development** – HTTP requests, URL validation, content-type verification
- **Image Processing** – Using PIL/Pillow for image manipulation and text rendering
- **Data Persistence** – JSON file management and configuration storage
- **Test-Driven Development** – pytest framework, unit testing best practices
- **Software Architecture** – Clean code principles, separation of concerns, modularity
- **CLI Development** – User-friendly menu systems, input validation, error messages
- **Git & Version Control** – Proper repository structure and documentation

---

## 🎓 Course Context

This project was created as the **final capstone project for Harvard's CS50P** (Introduction to Programming with Python), demonstrating mastery of:
- File I/O operations
- API integration with external web services
- Image processing libraries
- Automated testing frameworks
- Professional software development practices

---

## 📝 License

This project is open source and available for educational and personal use.

---

## 🤝 Contributing

Suggestions and improvements are welcome! Feel free to fork, create issues, or submit pull requests.

---

**Created by:** [Fábio Vila](https://github.com/fabioovila)  
**GitHub Repository:** [fabioovila/meme_generator](https://github.com/fabioovila/meme_generator)
