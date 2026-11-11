# Consulta CEP

Projeto de estudo de **HTML, CSS, JavaScript e Python/FastAPI** para consultar endereços por CEP usando a API pública ViaCEP. O repositório também conserva exercícios separados de consulta de moedas e informações de ações.

> **Escopo:** exercício educacional executado localmente; não é um serviço hospedado nem um produto pronto para produção. Integrações externas podem mudar ou ficar indisponíveis.

## O que o projeto faz

- Valida CEP com oito dígitos, permitindo digitação com hífen.
- Consulta o ViaCEP por meio de um backend FastAPI.
- Mostra CEP, logradouro, complemento, bairro, cidade e UF no navegador.
- Exibe erros sem inserir HTML retornado pelas APIs diretamente na página.
- Inclui exercícios adicionais em `conversorDeMoedas/` e rotas demonstrativas `/moedas` e `/ticker/{codigo_ticker}`.

## Tecnologias

Python 3.10+, FastAPI, Uvicorn, Requests, Beautiful Soup, HTML, CSS, JavaScript, Axios e Bootstrap (CDN).

## Como executar no Windows

Clone o projeto e entre na pasta:

```powershell
git clone https://github.com/Tyago03/ConsultaCEP.git
cd ConsultaCEP
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Terminal 1 — API:**

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 — frontend:** (ainda na raiz do projeto)

```powershell
py -m http.server 5500 --bind 127.0.0.1
```

Abra **http://127.0.0.1:5500** no navegador e digite um CEP para consultar.

> O backend autoriza o frontend local nas portas e origens documentadas. Abrir `index.html` diretamente pelo protocolo `file://` pode causar bloqueio de CORS. Se a porta 8000 já estiver em uso por Ayla ou DeskFlow, encerre aquela aplicação antes.

Para executar os testes automatizados:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

## APIs e dependências externas

| Endpoint | Fonte | Observação |
| --- | --- | --- |
| `GET /cep/01001000` | ViaCEP | Retorna campos filtrados do endereço. |
| `GET /moedas` | JSON público de moedas | Exercício de integração; disponibilidade depende do fornecedor externo. |
| `GET /ticker/PETR4` | Fundamentus | Demonstra extração HTML; pode deixar de funcionar se a estrutura da página mudar. |
| Conversor em `conversorDeMoedas/index2.html` | API de cotações externa | Exige internet e disponibilidade da API. |

Nenhuma dessas funcionalidades exige que usuários compartilhem senhas. Não trate a página ou o backend como serviço público autenticado.

## Limitações

Projeto de aprendizado, não submetido a uma avaliação de carga ou segurança completa. O scraping depende de HTML de terceiros e a consulta remota exige conexão. A origem permitida por CORS é restrita ao frontend local; isto **não substitui autenticação** quando um aplicativo é publicado na internet.

## Autor

Tyago Vitorino Ferreira — repositório de estudos de integração web e APIs.
