from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_cep_valido(monkeypatch):
    mock = Mock()
    mock.json.return_value = {
        "cep": "01001-000", "logradouro": "Praça da Sé",
        "bairro": "Sé", "localidade": "São Paulo", "uf": "SP",
    }
    monkeypatch.setattr("main.requests.get", lambda *args, **kwargs: mock)
    response = client.get("/cep/01001000")
    assert response.status_code == 200
    assert response.json()["localidade"] == "São Paulo"

def test_cep_com_formato_invalido():
    response = client.get("/cep/abc")
    assert response.status_code == 400

def test_cep_inexistente(monkeypatch):
    mock = Mock()
    mock.json.return_value = {"erro": True}
    monkeypatch.setattr("main.requests.get", lambda *args, **kwargs: mock)
    assert client.get("/cep/00000000").status_code == 404

def test_via_cep_fora_do_ar(monkeypatch):
    import requests
    def raise_timeout(*args, **kwargs):
        raise requests.Timeout("simulado")
    monkeypatch.setattr("main.requests.get", raise_timeout)
    response = client.get("/cep/01001000")
    assert response.status_code == 502
    assert "simulado" not in response.text

def test_cors_restrito():
    ok = client.get("/hello", headers={"Origin": "http://127.0.0.1:5500"})
    assert ok.headers.get("access-control-allow-origin") == "http://127.0.0.1:5500"
    denied = client.get("/hello", headers={"Origin": "https://example.org"})
    assert "access-control-allow-origin" not in denied.headers
