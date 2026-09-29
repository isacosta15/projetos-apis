# Trabalho de Estrutura de Dados

## 👥 Grupo

- Andrey
- Diego
- Fernanda
- Isabela
- Juliana
- Kauã
- Maria Eduarda

## 📚 Sobre o projeto

Este repositório contém três projetos desenvolvidos para a disciplina de **Estrutura de Dados**, utilizando Python e APIs externas.

### 🌤️ 1. Dashboard de Previsão do Tempo (dash_previsaotempo)

Utiliza a API **OpenWeatherMap** para consultar informações como temperatura, umidade, pressão e previsão do tempo.

### 🎬 2. Ranking de Filmes e Séries (rank_filmes)

Utiliza a API **The Movie Database (TMDb)** para consultar filmes, avaliações, gêneros, elenco e outras informações.

### 📰 3. Sistema de Notícias (sistemas_noticias)

Utiliza a **NewsAPI** para coletar manchetes, contar a frequência das palavras e gerar uma nuvem de palavras. Inclui ranking em tabela e separação das notícias por data, região e tema.

Configuração & Uso:
1. Renomeie o arquivo `.env.example` para `.env` e coloque sua chave da NewsAPI
2. Instale: `pip install requests python-dotenv nltk matplotlib wordcloud pandas`
3. Execute: `python sistemas_noticias.py`

## 🛠️ Tecnologias

- Python
- Requests
- Pandas
- Matplotlib
- JSON
- NLTK
- Flask

## ▶️ Como executar

Para executar os projetos, é necessário ter o **Python** instalado.

Também é necessário criar uma chave (**API Key**) nas APIs utilizadas e colocar a sua chave no código correspondente antes de executar o projeto.

> ⚠️ Não compartilhe ou publique sua API Key no GitHub.

Depois de configurar a chave, execute o arquivo `.py` do projeto desejado:

```bash
python nome_do_arquivo.py
