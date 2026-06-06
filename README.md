# Sistema RAG de busca e ingestão de documentos

Sistema que permite ingerir documentos PDF, armazená-los com embeddings vetoriais e fazer buscas inteligentes através de uma interface de chat alimentada por IA.

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como desafio do MBA em Inteligência Artificial da FullCycle, implementando um pipeline completo de:

1. **Ingestão de Documentos**: Carregamento e processamento de arquivos PDF
2. **Armazenamento Vetorial**: Persistência de embeddings em banco de dados PostgreSQL com extensão pgvector
3. **Busca por Similaridade**: Recuperação de documentos relevantes através de busca semântica
4. **Chat Inteligente**: Interface conversacional que responde perguntas baseadas apenas no contexto dos documentos ingeridos

## ✨ Funcionalidades

- ✅ **Ingestão de PDF**: Carregue documentos PDF e processe-os automaticamente
- ✅ **Divisão de Chunks**: Divida grandes documentos em pedaços menores com overlap configurável
- ✅ **Embeddings Vetoriais**: Gere embeddings usando OpenAI ou Google Generative AI
- ✅ **Armazenamento Persistente**: Armazene embeddings em PostgreSQL com pgvector
- ✅ **Busca Semântica**: Encontre documentos similares baseado em significado
- ✅ **Chat Contextual**: Interface interativa que responde perguntas usando apenas o contexto dos documentos
- ✅ **Múltiplos Provedores**: Suporte para OpenAI e Google Generative AI

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**: Linguagem principal
- **LangChain**: Framework para construir aplicações com LLMs
- **PostgreSQL 17**: Banco de dados relacional com suporte a vetores
- **pgvector**: Extensão PostgreSQL para operações com vetores
- **OpenAI / Google Generative AI**: Modelos de linguagem e embedding
- **Docker & Docker Compose**: Containerização e orquestração
- **PyPDF**: Carregamento e processamento de arquivos PDF

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.10+**
- **Docker e Docker Compose**
- Conta e API Key de um dos provedores:
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Google Cloud](https://ai.google.dev/tutorials/setup)

## 🚀 Configuração

### 1. Configure as Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas informações:

```env
# Banco de Dados
PG_VECTOR_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documents

# OpenAI
OPENAI_API_KEY=OPENAI-API-KEY
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_LLM_MODEL=gpt-5.4-nano

# Google Generative AI
# GOOGLE_API_KEY=GOOGLE-API-KEY
# GOOGLE_EMBEDDING_MODEL=gemini-embedding-2
# GOOGLE_LLM_MODEL=gemini-2.5-flash

# Caminho para o PDF a ingerir (opcional, padrão: ./document.pdf)
# PDF_PATH=/caminho/para/seu/arquivo.pdf
```

### 2. Inicie o Banco de Dados

Use Docker Compose para iniciar o PostgreSQL com pgvector:

```bash
docker-compose up -d
```

Isso irá:
- Iniciar um container PostgreSQL 17 com pgvector
- Criar o banco de dados `rag`
- Instalar a extensão vector automaticamente

Verifique se está rodando:

```bash
docker-compose ps
```

### 3. Configure o Virtual Environment do Python

Crie um ambiente virtual Python para isolar as dependências do projeto:

```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 4. Instale as Dependências Python

```bash
pip install -r requirements.txt
```

## 📖 Como Usar

### Ingestão de Documentos

Para ingerir um documento PDF:

```bash
python src/ingest.py
```

O script irá:
1. Carregar o arquivo PDF especificado em `PDF_PATH`
2. Dividir o documento em chunks de 1000 caracteres com 150 caracteres de overlap
3. Gerar embeddings para cada chunk
4. Armazenar no PostgreSQL

**Nota**: O arquivo PDF deve estar no caminho especificado em `PDF_PATH` ou no diretório raiz do projeto com o nome `document.pdf`.

### Chat Interativo

Para iniciar a interface de chat:

```bash
python src/chat.py
```

Digite perguntas e o sistema responderá baseado apenas no contexto dos documentos ingeridos:

```
QUAL A SUA PERGUNTA?: Qual é o tema principal do documento?

AQUI ESTÁ SUA RESPOSTA:
[Resposta baseada no contexto do documento]
```

Para sair, pressione `Ctrl+C`.

## 📁 Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── src/
│   ├── ingest.py         # Script para ingerir documentos PDF
│   ├── search.py         # Definição do prompt e chain de busca
│   ├── chat.py           # Interface de chat interativa
│   ├── models.py         # Configuração de modelos de IA
│   └── database.py       # Operações com o banco de dados vetorial
├── docker-compose.yml    # Configuração do PostgreSQL + pgvector
├── .env.example          # Exemplo de variáveis de ambiente
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

### Descrição dos Módulos

- **ingest.py**: Responsável por carregar PDFs, dividir em chunks e armazenar no banco de dados
- **search.py**: Define o template de prompt e cria a chain de busca com o LLM
- **chat.py**: Interface principal que executa um loop de perguntas e respostas
- **models.py**: Factory functions para obter instâncias dos modelos de embedding e LLM
- **database.py**: Interface com o PGVector para armazenar e recuperar documentos

## 🔧 Configuração Avançada

### Ajustar Tamanho dos Chunks

No arquivo `src/ingest.py`, modifique os parâmetros:

```python
chunks = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Aumente para chunks maiores
    chunk_overlap=150     # Aumente para mais sobreposição
).split_documents(document)
```

### Ajustar Número de Documentos na Busca

No arquivo `src/database.py`, modifique o parâmetro `k`:

```python
def similarity_search(question, k=10):  # Aumente para mais resultados
    ...
```

### Trocar Modelo de IA

Modifique as variáveis de ambiente `OPENAI_LLM_MODEL` ou `GOOGLE_LLM_MODEL` de acordo com o modelo desejado.

## 📊 Fluxo de Funcionamento

```
PDF → Loader → Chunks → Embeddings → PGVector → Armazenamento
                                         ↓
                         Similarity Search ← Pergunta do Usuário
                                  ↓
                          LLM + Prompt → Resposta
```

## ⚙️ Troubleshooting

### Erro: "No valid API key found"
- Verifique se as variáveis de ambiente estão configuradas corretamente
- Certifique-se de que está usando `OPENAI_API_KEY` ou `GOOGLE_API_KEY`

### Erro: "Connection refused - PostgreSQL"
- Verifique se o Docker está rodando: `docker-compose ps`
- Inicie o PostgreSQL: `docker-compose up -d`
- Aguarde alguns segundos para o banco inicializar

### Erro: "PDF file not found"
- Coloque o arquivo PDF no caminho especificado em `PDF_PATH`
- Ou configure a variável `PDF_PATH` corretamente no `.env`

## 📝 Licença

Este projeto é parte do desafio do MBA em Inteligência Artificial da FullCycle.

## 👤 Autor

Luis Felipe Dal Molin
