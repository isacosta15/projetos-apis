import requests
import pandas as pd
import matplotlib.pyplot as plt

CHAVE_API = "SUA_CHAVE_API"
URL = "https://www.omdbapi.com/"

generos = {
    "Ação": "Action",
    "Aventura": "Adventure",
    "Animação": "Animation",
    "Comédia": "Comedy",
    "Crime": "Crime",
    "Drama": "Drama",
    "Fantasia": "Fantasy",
    "Terror": "Horror",
    "Mistério": "Mystery",
    "Romance": "Romance",
    "Ficção Científica": "Sci-Fi",
    "Suspense": "Thriller"
}

filmes_conhecidos = [
    "The Godfather",
    "The Shawshank Redemption",
    "The Dark Knight",
    "Pulp Fiction",
    "Forrest Gump",
    "Fight Club",
    "Inception",
    "Interstellar",
    "The Matrix",
    "Goodfellas",
    "The Green Mile",
    "Gladiator",
    "Titanic",
    "Avatar",
    "Joker",
    "Parasite",
    "Whiplash",
    "The Prestige",
    "The Departed",
    "Django Unchained",
    "The Wolf of Wall Street",
    "Saving Private Ryan",
    "Schindler's List",
    "The Silence of the Lambs",
    "Se7en",
    "The Usual Suspects",
    "American History X",
    "The Pianist",
    "Braveheart",
    "The Intouchables",
    "Back to the Future",
    "Jurassic Park",
    "Star Wars",
    "Avengers",
    "Iron Man",
    "Spider-Man",
    "Deadpool",
    "John Wick",
    "Mad Max",
    "Terminator",
    "Rocky",
    "Top Gun",
    "Die Hard",
    "Mission Impossible",
    "The Hangover",
    "Superbad",
    "Home Alone",
    "The Mask",
    "Groundhog Day",
    "Toy Story",
    "Finding Nemo",
    "The Lion King",
    "Shrek",
    "Frozen",
    "Coco",
    "Up",
    "Inside Out",
    "Harry Potter",
    "The Lord of the Rings",
    "Pirates of the Caribbean",
    "The Hobbit",
    "Pan's Labyrinth",
    "The Conjuring",
    "It",
    "Halloween",
    "Alien",
    "Psycho",
    "Scream",
    "The Exorcist",
    "A Quiet Place",
    "The Notebook",
    "La La Land",
    "The Fault in Our Stars",
    "Pretty Woman",
    "Before Sunrise"
]



teste = requests.get(
    URL,
    params={
        "apikey": CHAVE_API,
        "t": "The Godfather"
    }
)

if teste.status_code != 200:

    print("Erro ao acessar a API.")
    print("Código:", teste.status_code)
    exit()

dados = teste.json()

if dados.get("Response") == "False":

    print("Erro da API:")
    print(dados.get("Error"))
    exit()


# ============================================================
# CABEÇALHO
# ============================================================

print("=" * 60)
print("              RANKING DE FILMES")
print("=" * 60)

print("\nEscolha um gênero:\n")

lista_generos = list(generos.keys())

for numero, genero in enumerate(lista_generos, 1):
    print(f"{numero} - {genero}")


# ESCOLHA DO GÊNERO

while True:

    try:

        opcao = int(
            input("\nDigite o número do gênero: ")
        )

        if 1 <= opcao <= len(lista_generos):
            break

        print("Digite uma opção válida.")

    except ValueError:

        print("Digite apenas números.")


genero_escolhido = lista_generos[opcao - 1]
genero_api = generos[genero_escolhido]

print(
    f"\nProcurando filmes de "
    f"{genero_escolhido}..."
)

print("Aguarde...\n")


# BUSCAR FILMES


filmes = []

for titulo in filmes_conhecidos:

    parametros = {
        "apikey": CHAVE_API,
        "t": titulo,
        "type": "movie",
        "plot": "full"
    }

    try:

        resposta = requests.get(
            URL,
            params=parametros,
            timeout=10
        )

    except requests.RequestException:

        continue

    if resposta.status_code != 200:
        continue

    filme = resposta.json()

    if filme.get("Response") == "False":
        continue

    generos_filme = filme.get("Genre", "")

    lista_generos_filme = [
        genero.strip().lower()
        for genero in generos_filme.split(",")
    ]

    if genero_api.lower() not in lista_generos_filme:
        continue

    try:

        nota = float(
            filme.get("imdbRating", "0")
        )

    except (ValueError, TypeError):

        nota = 0.0

    filmes.append({
        "Título": filme.get("Title", "N/A"),
        "Ano": filme.get("Year", "N/A"),
        "Nota": nota,
        "Gênero": filme.get("Genre", "N/A"),
        "Diretor": filme.get("Director", "N/A"),
        "Elenco": filme.get("Actors", "N/A"),
        "Duração": filme.get("Runtime", "N/A"),
        "Sinopse": filme.get("Plot", "N/A"),
        "IMDb": filme.get("imdbID", "N/A")
    })


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(filmes)


if df.empty:

    print("=" * 60)
    print("NENHUM FILME ENCONTRADO")
    print("=" * 60)

else:

    # Ordena pela nota
    df = df.sort_values(
        by="Nota",
        ascending=False
    )

    df = df.reset_index(drop=True)

    # Seleciona os 10 melhores
    top = df.head(10)


    # RANKING

    print("\n" + "=" * 70)
    print(
        f"       TOP 10 FILMES DE "
        f"{genero_escolhido.upper()}"
    )
    print("=" * 70)

    for indice, filme in top.iterrows():

        print(
            f"{indice + 1}. "
            f"{filme['Título']} "
            f"({filme['Ano']}) - "
            f"Nota: {filme['Nota']:.1f}"
        )


    # GRÁFICO

    plt.figure(figsize=(12, 7))

    plt.barh(
        top["Título"][::-1],
        top["Nota"][::-1],
        color="steelblue"
    )

    plt.xlabel("Nota no IMDb")
    plt.ylabel("Filme")

    plt.title(
        f"Top 10 filmes de {genero_escolhido}"
    )

    plt.xlim(0, 10)

    plt.tight_layout()

    plt.show()


    # MENU DE DETALHES

    while True:

        print("\n" + "=" * 60)
        print("Digite o número do filme para ver os detalhes.")
        print("Digite 0 para sair.")
        print("=" * 60)

        try:

            escolha = int(
                input("Escolha: ")
            )

        except ValueError:

            print("Digite apenas números.")
            continue


        if escolha == 0:

            print("\nPrograma encerrado.")
            break


        if escolha < 1 or escolha > len(top):

            print("Filme inválido.")
            continue


        filme = top.iloc[
            escolha - 1
        ]


        # ====================================================
        # DETALHES
        # ====================================================

        print("\n" + "=" * 70)
        print("                 DETALHES DO FILME")
        print("=" * 70)

        print(
            f"\nTítulo: {filme['Título']}"
        )

        print(
            f"Ano: {filme['Ano']}"
        )

        print(
            f"Nota no IMDb: "
            f"{filme['Nota']:.1f}"
        )

        print(
            f"Gênero: {filme['Gênero']}"
        )

        print(
            f"Diretor: {filme['Diretor']}"
        )

        print(
            f"Duração: {filme['Duração']}"
        )


        # ====================================================
        # ELENCO
        # ====================================================

        print("\nElenco:")

        if (
            filme["Elenco"]
            and filme["Elenco"] != "N/A"
        ):

            atores = filme["Elenco"].split(",")

            for ator in atores:

                print(
                    f"- {ator.strip()}"
                )

        else:

            print("Elenco não informado.")


        # SINOPSE

        print("\nSinopse:")

        if (
            filme["Sinopse"]
            and filme["Sinopse"] != "N/A"
        ):

            print(filme["Sinopse"])

        else:

            print("Sinopse não disponível.")


        print(
            f"\nID do IMDb: "
            f"{filme['IMDb']}"
        )

        print("\n" + "=" * 70)
