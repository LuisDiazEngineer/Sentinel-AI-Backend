from langchain_core.prompts import PromptTemplate

# Permite crear plantillas de texto (prompts) dinámicas para la IA

from langchain_community.llms import FakeListLLM

# Modelo de IA simulado (no real), devuelve respuestas predefinidas

from langchain_core.output_parsers import StrOutputParser

# Convierte la salida de la IA en texto plano (string)


def analyze_threat_with_ai(ip_address: str, threat_type: str):
    # Función que recibe una IP y tipo de amenaza, y devuelve análisis de IA

    # 1. Definimos el "Prompt"
    template = """
    You are a Cybersecurity Expert at Sentinel-AI.
    Analyze the following threat:
    IP Address: {ip}
    Type of Threat: {threat}
    
    Provide a brief security recommendation in 2 sentences.
    """
    # Texto base que se enviará a la IA
    # {ip} y {threat} son variables dinámicas que se reemplazarán

    prompt = PromptTemplate.from_template(template)
    # Convierte el template en un objeto que LangChain puede usar

    llm = FakeListLLM(
        responses=[
            "Block this IP immediately and check firewall logs.",
            "Low risk, but keep monitoring traffic patterns.",
        ]
    )
    # Crea una IA falsa que devuelve respuestas de una lista
    # Cada vez que se llama, devuelve una de esas respuestas

    # 2. LA CADENA MODERNA (Sin LLMChain)
    # Unimos: Prompt -> LLM -> Parser de texto
    chain = prompt | llm | StrOutputParser()
    # Pipeline:
    # 1. Se genera el prompt con datos reales
    # 2. Se pasa al modelo (llm)
    # 3. Se convierte la salida a string

    # 3. EJECUCIÓN
    # Usamos .invoke en lugar de .run
    response = chain.invoke({"ip": ip_address, "threat": threat_type})
    # Ejecuta la cadena pasando los valores reales
    # Reemplaza {ip} y {threat} en el template

    return response
    # Devuelve el resultado generado por la IA
