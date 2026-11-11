"""API local de estudo: consulta de CEP e outras integrações externas."""
import re

from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="Consulta CEP (projeto educacional)")

# Frontend de desenvolvimento em http://127.0.0.1:5500 (ou localhost).
# Não são usadas credenciais do navegador, e a API não deve ser exposta publicamente.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/hello")
def read_root():
    return {"msg": "Hello World!"}

@app.get("/cep/{cep}")
def get_cep_info(cep: str):
    if not re.fullmatch(r"\d{8}", cep):
        raise HTTPException(status_code=400, detail="O CEP deve conter oito dígitos.")
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json", timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise HTTPException(status_code=502, detail="Não foi possível consultar o ViaCEP.") from exc
    if not isinstance(data, dict):
        raise HTTPException(status_code=502, detail="Resposta inesperada do ViaCEP.")
    if data.get("erro"):
        raise HTTPException(status_code=404, detail="CEP não encontrado.")
    return {
        "cep": data.get("cep", ""),
        "logradouro": data.get("logradouro", ""),
        "complemento": data.get("complemento", ""),
        "bairro": data.get("bairro", ""),
        "localidade": data.get("localidade", ""),
        "uf": data.get("uf", ""),
    }

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ConsultaCEP study project)"}

@app.get("/ticker/{codigo_ticker}")
def get_ticker_info(codigo_ticker: str):
    if not re.fullmatch(r"[A-Za-z0-9]{1,12}", codigo_ticker):
        raise HTTPException(status_code=400, detail="Código de ticker inválido.")
    try:
        response = requests.get(
            f"https://www.fundamentus.com.br/detalhes.php?papel={codigo_ticker.upper()}",
            headers=HEADERS,
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail="Falha ao consultar o provedor de cotações.") from exc

    soup = BeautifulSoup(response.content, "html.parser")
    td = soup.find("td", class_="data destaque w3")
    span = td.find("span", class_="txt") if td else None
    if not span:
        raise HTTPException(status_code=404, detail="Cotação não encontrada.")
    try:
        cotacao = float(span.get_text(strip=True).replace(".", "").replace(",", "."))
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="Formato de cotação inesperado.") from exc
    return {"ticker": codigo_ticker.upper(), "cotacao": cotacao}

@app.get("/moedas")
def get_moedas():
    url = "https://raw.githubusercontent.com/ourworldincode/currency/main/currencies.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        currencies = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise HTTPException(status_code=502, detail="Não foi possível consultar a lista de moedas.") from exc
    if not isinstance(currencies, dict):
        raise HTTPException(status_code=502, detail="Formato de moedas inesperado.")
    return [
        {"codigo": code, "nome": info.get("name", ""), "simbolo": info.get("symbol", "")}
        for code, info in currencies.items() if isinstance(info, dict)
    ]
