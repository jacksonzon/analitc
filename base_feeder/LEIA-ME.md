# Base Feeder — como usar

## 1. Gerar o executável (uma vez só)
1. Instale o Python em https://python.org (marque "Add to PATH" na instalação).
2. Dê 2 cliques em `build.bat`.
3. Vai aparecer `dist\BaseFeeder.exe`.

## 2. Usar no seu projeto
1. Copie `BaseFeeder.exe` para dentro da pasta do seu projeto HTML (a mesma pasta do `index.html`).
2. Dê 2 cliques no `BaseFeeder.exe`. Uma janela preta vai abrir e ficar rodando.
3. Ela vai criar automaticamente `data.json` e `data.js` na pasta, com os dados de qualquer
   arquivo que comece com **"base"** (ex: `base_vendas.csv`, `Base_Julho.xlsx`).
4. Abra `http://localhost:8000` no navegador — é a mesma pasta, servida localmente
   (evita erro de CORS que acontece ao abrir o HTML direto com duplo clique).

## 3. Sempre que você jogar um novo arquivo "base..." na pasta
- O BaseFeeder detecta na hora (criação, edição ou remoção do arquivo) e regera
  `data.json` / `data.js` automaticamente. Não precisa reiniciar nada.

## 4. Como o seu HTML deve ler os dados
Duas opções — escolha uma:

**Opção A — variável global (funciona mesmo sem servidor, mais simples):**
```html
<script src="data.js"></script>
<script>
  console.log(window.BASE_DATA); // array com os dados
  // Para reagir quando o arquivo for atualizado, sem precisar recarregar a página:
  window.addEventListener('basedata:updated', (e) => {
    console.log('Dados atualizados:', e.detail);
    // chame aqui a função que redesenha seu dashboard, ex: renderTabela(e.detail)
  });
</script>
```
Nota: `basedata:updated` só dispara se a página já estiver aberta e o `data.js` for
recarregado (ex: com um `setInterval` recarregando o script, ou dando refresh na página).

**Opção B — fetch (requer acessar via http://localhost:8000, não abrir o arquivo direto):**
```html
<script>
async function carregarDados() {
  const resp = await fetch('data.json?_=' + Date.now()); // evita cache
  const dados = await resp.json();
  console.log(dados);
}
carregarDados();
setInterval(carregarDados, 3000); // atualiza a cada 3s sem precisar dar F5
</script>
```

## Formato dos dados
Cada linha do CSV/Excel vira um objeto JSON, por exemplo:
```json
[
  { "VIAGEM ID": "123", "STATUS": "PAGO", "_arquivo_origem": "base_junho.csv" },
  { "VIAGEM ID": "124", "STATUS": "CANCELADO", "_arquivo_origem": "base_junho.csv" }
]
```
O campo `_arquivo_origem` é adicionado automaticamente para você saber de qual
arquivo cada linha veio (útil se tiver mais de um arquivo "base" na pasta).

## Personalizações possíveis (é só pedir)
- Mudar o prefixo do nome do arquivo (hoje é "base...")
- Trocar por sempre usar só o arquivo mais recente, em vez de combinar todos
- Rodar sem a janela do console aparecendo (modo "silencioso")
- Rodar automaticamente ao ligar o Windows
