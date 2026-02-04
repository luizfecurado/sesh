const API_URL = "http://127.0.0.1:8000";

// Função Principal: Busca dados e desenha na tela
async function carregarDados() {
    try {
        // 1. O Fetch vai até o seu Python buscar os dados
        const response = await fetch(`${API_URL}/itens`);
        const dadosJson = await response.json();
        
        // 2. Chama a função que atualiza a lista visual
        renderizarLista(dadosJson.dados);
        
        // 3. Atualiza os números do topo (calculamos simples aqui ou chamamos /estatisticas)
        atualizarStats(dadosJson.dados);

    } catch (erro) {
        console.error("Erro ao buscar dados:", erro);
        alert("Erro ao conectar com a API. O Uvicorn está rodando?");
    }
}

// Atualize esta função
function renderizarLista(itens) {
    const listaElemento = document.getElementById("lista-itens");
    listaElemento.innerHTML = "";

    itens.forEach(item => {
        const li = document.createElement("li");
        
        // Adicionamos o botão de lixeira (🗑️) no final
        li.innerHTML = `
            <div class="item-info">
                <span class="tag ${item.categoria}">${item.categoria}</span>
                <strong>${item.titulo}</strong>
            </div>
            <div class="item-meta">
                <span class="nota">⭐ ${item.nota ? item.nota : '-'}</span>
                <button class="btn-delete" onclick="deletarItem(${item.id})">🗑️</button>
            </div>
        `;
        listaElemento.appendChild(li);
    });
}

function atualizarStats(itens) {
    document.getElementById("total-count").innerText = itens.length;
    
    // Filtra só quem tem nota para calcular a média
    const itensComNota = itens.filter(i => i.nota !== null);
    const soma = itensComNota.reduce((acc, curr) => acc + curr.nota, 0);
    const media = itensComNota.length ? (soma / itensComNota.length).toFixed(1) : "0.0";
    
    document.getElementById("media-nota").innerText = media;
}

async function deletarItem(id) {
    if (confirm("Tem certeza que quer apagar este item?")) {
        try {
            // Chama a rota DELETE do seu Python
            const response = await fetch(`${API_URL}/itens/${id}`, {
                method: "DELETE"
            });

            if (response.ok) {
                // Se deu certo, recarrega a lista para sumir com o item
                carregarDados();
            } else {
                alert("Erro ao excluir");
            }
        } catch (erro) {
            console.error("Erro:", erro);
        }
    }
} 

// Carrega tudo assim que a página abrir
document.addEventListener("DOMContentLoaded", carregarDados);