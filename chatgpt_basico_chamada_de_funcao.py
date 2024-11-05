import json
from openai import OpenAI  # pip install openai
from dotenv import load_dotenv
load_dotenv()

modelo = "gpt-4o-mini"

client = OpenAI()

historico = []

ferramentas = [
    {
        "type": "function",
        "function": {
            "name": "que_horas_sao",
            "description": "Diz as horas atuais quando o usuário perguntar sobre o horário de acordo com a cidade desejada.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cidade": {
                        "type": "string",
                        "description": "A cidade desejada.",
                    },
                },
                "required": ["cidade"],
                "additionalProperties": False,
            },
        }
    }
]

def que_horas_sao(cidade):
    return f"Em {cidade} são 10:00. Na verdade este é só um exemplo de chamada de função."

def generate_answer(messages, modelo="gpt-4o-mini"):
    try:
        historico.append({"role": "user", "content": messages})
        response = client.chat.completions.create(
            model=modelo,
            messages=historico,
            tools=ferramentas,
            tool_choice="auto"
        )

        historico.append({"role": "assistant", "content": response.choices[0].message.content})

        # Verifica se a razão do término da resposta é devido a chamadas de ferramentas
        if response.choices[0].finish_reason == "tool_calls":
            # Itera sobre todas ferramentas chamadas na mensagem da resposta
            for tool_call in response.choices[0].message.tool_calls:
                # Verifica se o nome da função chamada é "que_horas_sao"
                if tool_call.function.name == "que_horas_sao":
                    # Extrai a cidade dos argumentos da função em formato JSON
                    cidade = json.loads(tool_call.function.arguments)["cidade"]
                    # Retorna a resposta da função que_horas_sao com a cidade extraída
                    return que_horas_sao(cidade)
        else:
            return response.choices[0].message.content
    except Exception as e:
        print("Erro", e)
        return e

while True:
    pergunta = input("Você ('x'): ")

    if pergunta.lower() == 'x':
        break

    answer = generate_answer(pergunta, modelo=modelo)

    print(f"Chat ({modelo}):", answer)


