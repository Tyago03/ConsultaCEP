// Frontend local: dados de APIs externas entram como texto, nunca como HTML.
function consultarCEP() {
    const campo = document.getElementById("CEP");
    const cep = campo.value.replace(/\D/g, "");
    if (!/^\d{8}$/.test(cep)) {
        alert("Digite um CEP válido com 8 dígitos.");
        return;
    }

    axios.get(`http://127.0.0.1:8000/cep/${cep}`, { timeout: 10000 })
        .then(response => mostrarResultados(response.data))
        .catch(error => {
            document.getElementById("resultado").replaceChildren();
            const detail = error.response?.data?.detail;
            alert(typeof detail === "string" ? detail : "Erro ao consultar CEP. Verifique se a API local está ativa.");
        });
}

function mostrarResultados(dados) {
    const tabela = document.getElementById("resultado");
    tabela.replaceChildren();

    const campos = ["cep", "logradouro", "complemento", "bairro", "localidade", "uf"];
    const linha = document.createElement("tr");
    for (const campo of campos) {
        const celula = document.createElement("td");
        celula.textContent = String(dados?.[campo] ?? "");
        linha.appendChild(celula);
    }
    tabela.appendChild(linha);
}
