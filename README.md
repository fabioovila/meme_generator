# 🎨 Gerador de Memes

Uma ferramenta poderosa de linha de comando para automatizar a criação de memes com templates personalizáveis, posicionamento inteligente de texto e gerenciamento fácil de imagens.

---

## 📋 Visão Geral

**Gerador de Memes** é uma aplicação CLI abrangente desenvolvida como projeto final do curso CS50P de Harvard. Ela simplifica o fluxo de trabalho da criação de memes personalizados, permitindo que usuários baixem templates de imagens da web, configurem o posicionamento e estilo do texto, e gerem imagens polidas com um único comando.

O projeto demonstra proficiência em manipulação de arquivos, requisições web, processamento de imagens e arquitetura de software limpa com práticas abrangentes de testes.

---

## 🛠️ Tecnologias & Linguagens

### **Linguagem Principal**
- **Python 3** - Lógica completa da aplicação e interface CLI

### **Bibliotecas & Dependências Principais**
| Biblioteca | Propósito |
|-----------|-----------|
| **Pillow (PIL)** | Processamento de imagens, renderização de texto e manipulação |
| **Requests** | Requisições HTTP para baixar templates de imagens de URLs |
| **validator-collection** | Validação de URLs e verificações de integridade de dados |
| **pytest** | Testes unitários e execução automatizada de testes |
| **JSON** | Armazenamento leve de configurações e metadados de templates |

### **Tecnologias Adicionais**
- **Operações de Arquivo I/O** - Gerenciamento de diretórios de templates e saída
- **Correspondência de Padrões com Expressões Regulares** - Validação de tipo de arquivo
- **Design Orientado a Objetos** - Estrutura de funções limpa e modular
- **Tratamento de Erros & Gerenciamento de Exceções** - Validação robusta de entrada

---

## ✨ Funcionalidades

* **🌐 Baixar Novos Templates** – Forneça uma URL de imagem e o programa automaticamente a baixa e armazena na pasta `templates/`
* **📍 Configurar Posicionamento de Texto** – Defina as coordenadas X e Y exatas para o posicionamento do texto em cada template
* **🎯 Estilo Personalizável** – Configure tamanho da fonte, selecione cor do texto (preto ou branco) e garanta legibilidade ideal
* **🔒 Validação de Cores** – Validação rigorosa garante que o texto permaneça legível em qualquer fundo
* **⚡ Geração Automatizada** – Leia configurações do JSON, renderize texto e exporte memes finalizados para a pasta `output/`
* **✅ Testes Abrangentes** – Suite completa de testes pytest para funções de validação e formatação de dados

---

## 📁 Estrutura de Arquivos

```
meme_generator/
├── project.py                 # Lógica principal da aplicação
├── test_project.py           # Testes unitários (pytest)
├── templates.json            # Banco de dados de configuração (JSON)
├── ARIALLGT.TTF             # Arquivo de fonte para renderização de texto
├── templates/               # Diretório para imagens de template
├── output/                  # Diretório para memes gerados
└── README.md               # Documentação
```

### **Arquivos Principais**

- **`project.py`** (7,7 KB)
  - Sistema interativo de menu CLI
  - `get_new_img()` – Baixa imagens via HTTP e armazena configurações
  - `add_text_to_img()` – Renderiza texto em templates usando Pillow
  - Validação de URL usando biblioteca `requests`
  - Operações de leitura/escrita JSON para armazenamento persistente
  - Tratamento abrangente de erros e validação de entrada do usuário

- **`test_project.py`** (785 B)
  - `test_validate_color()` – Valida o tratamento de entrada de cores
  - `test_format_template_key()` – Testa a lógica de formatação de string
  - `test_convert_color_to_rgb()` – Verifica a conversão de cores RGB
  - Todos os testes executam com pytest sem bloqueio de terminal

- **`templates.json`**
  - Armazena metadados de template: caminhos de arquivo, coordenadas de texto, tamanhos de fonte, cores
  - 9+ templates pré-configurados com configurações otimizadas
  - Alternativa leve a bancos de dados SQL para este caso de uso

---

## 🏗️ Padrões de Design & Decisões

### **1. Separação de Responsabilidades**
O código separa operações de I/O da lógica de negócios pura, permitindo:
- Testes unitários sem interação com terminal
- Funções reutilizáveis sem dependências externas
- Depuração e manutenção facilitadas

### **2. Configuração JSON em vez de Bancos de Dados Relacionais**
Escolhido por:
- **Simplicidade** – Sem necessidade de configuração de banco de dados
- **Portabilidade** – Fácil de compartilhar e controlar versões
- **Legibilidade** – Arquivos de configuração editáveis por humanos
- **Leveza** – Dependências mínimas para um projeto pessoal

### **3. Validação Robusta de Entrada**
- Validação de URL usando biblioteca `validator-collection`
- Verificação de tipo para coordenadas e tamanhos de fonte
- Verificação de tipo de conteúdo para evitar uploads de imagens inválidas
- Mensagens de erro graciosas para orientação do usuário

### **4. Design Modular de Funções**
Funções pequenas e testáveis com responsabilidades únicas:
- `validate_color()` – Validação de string de cor
- `format_template_key()` – Formatação de string
- `convert_color_to_rgb()` – Conversão de cor
- `text_placement()` – Recuperação de configuração

---

## 🚀 Como Executar

### **Pré-requisitos**
```bash
pip install pillow validator-collection requests pytest
```

### **Instalação**
```bash
git clone https://github.com/fabioovila/meme_generator.git
cd meme_generator
```

### **Executando a Aplicação**
```bash
python project.py
```

**Opções de Menu:**
1. **Adicionar novo template** – Forneça uma URL para baixar e configurar um novo template de meme
2. **Gerar meme** – Selecione um template e adicione texto personalizado para criar um meme

### **Executando os Testes**
```bash
pytest test_project.py -v
```

---

## 📸 Exemplo de Fluxo de Trabalho

```
$ python project.py

[1] - Add new img to archive | [2] - Add text to template
Which option do you want? 1

Type the image URL: https://example.com/meme_template.jpg
Type the name to the file: meu_template
Type the X coordinate for text: 100
Type the Y coordinate for text: 150
Type the font size for text: 24
Type the text color (black/white): white

Template 'meu_template' successfully added and configured!

[1] - Add new img to archive | [2] - Add text to template
Which option do you want? 2

Which template you wish to use? ['Meu Template']
What text you wish to put into the selected template? Olá Mundo!
Ok, so you wish to write 'Olá Mundo!' into the Meu Template template?[y/n] y

Meu Template meme successfully created!
```

---

## 🧪 Testes & Garantia de Qualidade

O projeto inclui uma suite abrangente de testes usando **pytest**:

```bash
$ pytest test_project.py -v
test_project.py::test_validate_color PASSED
test_project.py::test_format_template_key PASSED
test_project.py::test_convert_color_to_rgb PASSED
```

**Cobertura de Testes:**
- ✅ Validação de cores (entradas válidas/inválidas)
- ✅ Formatação de string com tratamento de espaços em branco
- ✅ Lógica de conversão de cor RGB
- ✅ Casos extremos e condições de erro

---

## 📚 Resultados de Aprendizado & Habilidades Demonstradas

Este projeto demonstra proficiência em:

- **Programação em Python** – Design avançado de funções, tratamento de erros, operações de arquivo
- **Desenvolvimento Web** – Requisições HTTP, validação de URL, verificação de tipo de conteúdo
- **Processamento de Imagens** – Uso de PIL/Pillow para manipulação de imagens e renderização de texto
- **Persistência de Dados** – Gerenciamento de arquivos JSON e armazenamento de configurações
- **Desenvolvimento Orientado por Testes** – Framework pytest, práticas recomendadas de testes unitários
- **Arquitetura de Software** – Princípios de código limpo, separação de responsabilidades, modularidade
- **Desenvolvimento de CLI** – Sistemas de menu amigáveis, validação de entrada, mensagens de erro
- **Git & Controle de Versão** – Estrutura adequada de repositório e documentação

---

## 🎓 Contexto do Curso

Este projeto foi criado como o **projeto capstone final do CS50P de Harvard** (Introdução à Programação com Python), demonstrando domínio de:
- Operações de I/O de arquivo
- Integração de API com serviços web externos
- Bibliotecas de processamento de imagens
- Frameworks de testes automatizados
- Práticas profissionais de desenvolvimento de software

---

## 📝 Licença

Este projeto é de código aberto e disponível para uso educacional e pessoal.

---

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas! Sinta-se livre para fazer fork, criar issues ou enviar pull requests.

---

**Criado por:** [Fábio Vila](https://github.com/fabioovila)  
**Repositório GitHub:** [fabioovila/meme_generator](https://github.com/fabioovila/meme_generator)
