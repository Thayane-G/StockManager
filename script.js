const API = "http://127.0.0.1:5000/produtos";

let editandoId = null;

/* BOTÃO ENTRAR (AGORA FUNCIONA SEM BUG) */
document.getElementById("btnEntrar").addEventListener("click", entrar);

function entrar() {
    const home = document.getElementById("home");

    home.classList.add("sair");

    setTimeout(() => {
        home.style.display = "none";
        document.getElementById("app").classList.remove("hidden");
        listarProdutos();
    }, 600);
}

/* TOAST */
function toast(msg, tipo = "success") {
    const t = document.getElementById("toast");

    t.innerText = msg;
    t.className = `toast show ${tipo}`;

    setTimeout(() => {
        t.className = "toast hidden";
    }, 2500);
}

/* LISTAR */
async function listarProdutos() {
    try {
        const res = await fetch(API);
        const data = await res.json();

        const tabela = document.getElementById("tabela");
        tabela.innerHTML = "";

        (data.dados || []).forEach(p => {
            tabela.innerHTML += `
                <tr>
                    <td>${p.id}</td>
                    <td>${p.nome}</td>
                    <td>${p.categoria}</td>
                    <td>${p.preco}</td>
                    <td>${p.quantidade}</td>
                    <td>
                        <button onclick="editar(${p.id}, '${p.nome}', '${p.categoria}', ${p.preco}, ${p.quantidade})">
                            Editar
                        </button>

                        <button class="btn-delete" onclick="deletar(${p.id})">
                            Excluir
                        </button>
                    </td>
                </tr>
            `;
        });

    } catch {
        toast("Erro ao carregar dados", "error");
    }
}

/* SALVAR */
document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const produto = {
        nome: nome.value,
        categoria: categoria.value,
        preco: Number(preco.value),
        quantidade: Number(quantidade.value)
    };

    try {
        let url = API;
        let method = "POST";

        const sendoEdicao = editandoId !== null;

        if (sendoEdicao) {
            url = `${API}/${editandoId}`;
            method = "PUT";
        }

        const res = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(produto)
        });

        const data = await res.json();

        if (!res.ok) {
            toast(data.mensagem || "Erro", "error");
            return;
        }

        const mensagem = sendoEdicao
            ? "Editado com sucesso!"
            : "Cadastrado com sucesso!";

        editandoId = null;
        form.reset();
        listarProdutos();

        toast(mensagem);

    } catch {
        toast("Erro de conexão", "error");
    }
});

/* EDITAR */
function editar(id, nomeV, cat, pre, qtd) {
    editandoId = id;

    nome.value = nomeV;
    categoria.value = cat;
    preco.value = pre;
    quantidade.value = qtd;
}

/* DELETE */
async function deletar(id) {
    if (!confirm("Deseja excluir?")) return;

    await fetch(`${API}/${id}`, { method: "DELETE" });

    toast("Produto removido");
    listarProdutos();
}

/* BUSCA */
document.getElementById("busca").addEventListener("input", function () {
    const valor = this.value.toLowerCase();

    document.querySelectorAll("#tabela tr").forEach(tr => {
        tr.style.display = tr.innerText.toLowerCase().includes(valor)
            ? ""
            : "none";
    });
});