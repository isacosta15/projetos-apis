from flask import Flask, request, render_template_string
import requests
import webbrowser
import threading

# CONFIGURAÇÃO

app = Flask(__name__)

API_KEY = "Sua_chave_api"

URL_API = "https://api.openweathermap.org/data/2.5/weather"


# HTML + CSS

HTML = """
<!DOCTYPE html>

<html lang="pt-br">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <link rel="preconnect" href="https://fonts.googleapis.com">

    <link
        rel="preconnect"
        href="https://fonts.gstatic.com"
        crossorigin
    >

    <link
        href="https://fonts.googleapis.com/css2?family=Lobster&family=Open+Sans:wght@300;500;700&family=Roboto:ital,wght@0,100;0,300;0,400;1,300&display=swap"
        rel="stylesheet"
    >

    <title>Previsão do Tempo</title>


    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Open Sans', sans-serif;
        }


        body {

            height: 100vh;
            width: 100vw;

            display: flex;

            justify-content: center;

            align-items: center;

            background-color: rgb(97, 97, 97);

        }


        .caixa-maior {

            background: #000000;

            opacity: 0.8;

            border-radius: 25px;

            padding: 20px;

            width: 95%;

            max-width: 450px;

        }


        .input-city {

            border: none;

            outline: none;

            padding: 10px;

            border-radius: 25px;

            font-size: 20px;

            background-color: #7c7c7c2b;

            color: #ffffff;

            width: calc(100% - 70px);

        }


        .input-city::placeholder {

            color: #cccccc;

        }


        .button-search-city {

            border: none;

            outline: none;

            padding: 10px;

            border-radius: 50px;

            background-color: #7c7c7c2b;

            cursor: pointer;

            float: right;

        }


        .button-search-city:hover {

            background-color: #555555;

        }


        .img-search {

            width: 20px;

        }


        .caixa-media {

            margin-top: 30px;

        }


        .cidade {

            color: #ffffff;

            font-size: 28px;

            font-weight: 300;

        }


        .temp {

            font-size: 20px;

            color: #ffffff;

            margin-top: 20px;

        }


        .caixa-menor {

            display: flex;

            align-items: center;

            margin-top: 20px;

        }


        .img-previsao {

            width: 50px;

        }


        .texto-previsao {

            color: #ffffff;

            margin-left: 20px;

            text-transform: capitalize;

        }


        .umidade {

            color: #ffffff;

            margin-top: 20px;

        }


        .erro {

            color: #ff6b6b;

            margin-top: 20px;

        }

    </style>

</head>


<body>


    <div class="caixa-maior">


        <form method="POST">


            <input
                class="input-city"
                name="cidade"
                placeholder="Digite o nome da cidade"
                value="{{ cidade }}"
                required
            >


            <button
                class="button-search-city"
                type="submit"
            >

                <img
                    class="img-search"
                    alt="busca"
                    src="https://www.svgrepo.com/show/488200/find.svg"
                >

            </button>


        </form>


        {% if erro %}

            <p class="erro">
                {{ erro }}
            </p>

        {% endif %}


        {% if dados %}

            <div class="caixa-media">


                <h2 class="cidade">

                    Clima em {{ dados.name }}

                </h2>


                <p class="temp">

                    {{ dados.main.temp | round | int }}°C

                </p>


                <div class="caixa-menor">


                    <img
                        class="img-previsao"
                        alt="icone"
                        src="https://openweathermap.org/img/wn/{{ dados.weather[0].icon }}.png"
                    >


                    <p class="texto-previsao">

                        {{ dados.weather[0].description }}

                    </p>


                </div>


                <p class="umidade">

                    Umidade: {{ dados.main.humidity }}%

                </p>


            </div>

        {% endif %}


    </div>


</body>

</html>
"""


# ROTA PRINCIPAL

@app.route("/", methods=["GET", "POST"])
def clima():

    dados = None

    erro = None

    cidade = ""

    # QUANDO O USUÁRIO PESQUISAR

    if request.method == "POST":

        cidade = request.form.get("cidade", "").strip()


        if cidade == "":

            erro = "Digite uma cidade."

        else:

            parametros = {

                "q": cidade,

                "appid": API_KEY,

                "lang": "pt_br",

                "units": "metric"

            }


            try:

                resposta = requests.get(

                    URL_API,

                    params=parametros,

                    timeout=10

                )


                if resposta.status_code == 200:

                    dados = resposta.json()


                elif resposta.status_code == 401:

                    erro = "API Key inválida."


                elif resposta.status_code == 404:

                    erro = "Cidade não encontrada."


                else:

                    erro = (
                        f"Erro da API: "
                        f"{resposta.status_code}"
                    )


            except requests.exceptions.RequestException as e:

                erro = f"Erro de conexão: {e}"


    return render_template_string(

        HTML,

        dados=dados,

        erro=erro,

        cidade=cidade

    )


# ABRIR O CHROME AUTOMATICAMENTE

def abrir_navegador():

    webbrowser.open(
        "http://127.0.0.1:5000"
    )


# EXECUÇÃO

if __name__ == "__main__":

    threading.Timer(
        1,
        abrir_navegador
    ).start()


    app.run(
        debug=False
    )