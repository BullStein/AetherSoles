# 🛍️ Tênis Store - E-commerce Inteligente

Um e-commerce moderno de tênis com sistema de recomendações personalizadas baseado no comportamento do usuário.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Funcionalidades Principais

- **🎯 Sistema de Recomendações Inteligente** - Aprende suas preferências por marcas
- **❤️ Sistema de Favoritos** - Salve e gerencie seus produtos preferidos
- **👤 Perfil Personalizado** - Estatísticas e preferências individuais
- **🛒 Carrinho de Compras Completo** - Experiência completa de e-commerce
- **⚙️ Painel Administrativo** - Gerenciamento de produtos e usuários
- **🎨 Design Responsivo** - Funciona em todos os dispositivos

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Instalação e Execução

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/tenis-store.git
cd tenis-store
Instale as dependências


pip install flask
Execute a aplicação


python app.py
Acesse no navegador


http://localhost:5000
👤 Credenciais de Teste
Administrador:

Usuário: admin

Senha: admin123

Usuário comum: Registre-se gratuitamente na aplicação

🎯 Sistema de Recomendações
O sistema aprende automaticamente suas preferências baseado em:

Ação	Peso	Descrição
👁️ Visualizar produto	1	Quando você vê detalhes de um produto
🛒 Adicionar ao carrinho	2	Quando você adiciona um item ao carrinho
❤️ Favoritar produto	3	Quando você marca um produto como favorito
Marcas suportadas: Nike, Adidas, Puma, New Balance, Mizuno, Jordan, Vans

🌐 Acesso em Rede Local
Para permitir que outros dispositivos na mesma rede acessem:

bash
python app.py --host=0.0.0.0 --port=5000
Outras pessoas podem acessar via: http://SEU_IP:5000

📁 Estrutura do Projeto
text
tenis-store/
├── app.py                 # Aplicação principal Flask
├── database.json          # Banco de dados JSON
├── templates/             # Templates HTML
│   ├── base.html          # Layout base
│   ├── index.html         # Página inicial
│   ├── profile.html       # Perfil do usuário
│   ├── preferences.html   # Preferências
│   ├── cart.html          # Carrinho de compras
│   ├── login.html         # Login
│   ├── register.html      # Registro
│   └── admin/             # Painel administrativo
└── README.md              # Este arquivo
🛠️ Tecnologias Utilizadas
Backend: Python + Flask

Frontend: HTML5, CSS3, JavaScript

Banco de Dados: JSON (simulado)

Ícones: Font Awesome

Fontes: Google Fonts (Inter)

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

👨‍💻 Desenvolvimento
Projeto desenvolvido com foco em:

Experiência do usuário intuitiva

Sistema de recomendações inteligente

Interface moderna e responsiva

Fácil manutenção e extensibilidade

⭐ Se este projeto foi útil, deixe uma estrela no repositório!



