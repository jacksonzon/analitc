# Publicando o dashboard no GitHub Pages (para a TV)

Isso faz o `BaseFeeder.exe` (no seu computador) enviar os dados automaticamente
pro GitHub, e a TV só abre um link público que se atualiza sozinho.

## 1. Instalar o Git (no SEU computador, o que atualiza os dados)
Baixe e instale: https://git-scm.com/downloads/win
(Pode manter todas as opções padrão da instalação.)

## 2. Criar o repositório no GitHub
1. Entre em https://github.com e crie uma conta se ainda não tiver.
2. Clique em **New repository**.
3. Nome sugerido: `dashboard-transportes` (pode ser qualquer nome).
4. Marque como **Public** (o GitHub Pages gratuito exige repositório público,
   a menos que você tenha um plano pago).
5. Não marque "Add a README" — deixe vazio. Clique em **Create repository**.

## 3. Colocar seus arquivos dentro de uma pasta com Git
Na pasta onde estão `feeder.py`, `BaseFeeder.exe`, `index.html` e seus
arquivos `base_*.csv`:

1. Clique na barra de endereço do Explorador de Arquivos, digite `cmd` e
   aperte Enter (ou use o `diagnostico.bat` como referência de como abrir
   um terminal ali).
2. Rode, um de cada vez (troque `SEU-USUARIO` e `SEU-REPO` pelos seus):
   ```
   git init
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git
   git add index.html
   git commit -m "Primeira versao do dashboard"
   git push -u origin main
   ```
3. Na primeira vez, o Windows vai abrir uma janela do navegador pedindo
   pra você logar no GitHub — faça login normalmente. Depois disso, o Git
   guarda o login e os próximos `push` acontecem sem pedir senha de novo
   (é exatamente isso que faz a automação do BaseFeeder funcionar sozinha).

## 4. Ativar o GitHub Pages
1. No repositório, vá em **Settings** → **Pages** (menu à esquerda).
2. Em "Build and deployment" → "Source", escolha **Deploy from a branch**.
3. Em "Branch", escolha **main** e pasta **/ (root)**. Salve.
4. Espere 1-2 minutos. Vai aparecer um link tipo:
   ```
   https://seu-usuario.github.io/seu-repo/
   ```
   Esse é o link que você vai abrir **na TV**.

## 5. Rodar o BaseFeeder normalmente
A partir de agora, sempre que você:
- Ligar o `BaseFeeder.exe` no seu computador, e
- Soltar um arquivo `base_*.csv`/`.xlsx` na pasta,

ele vai gerar `data.json`/`data.js` **e também enviar (`git push`) pro
GitHub automaticamente**. Na janela preta do BaseFeeder você vai ver a
mensagem `[GIT] data.json/data.js publicados no GitHub com sucesso`.

## 6. Na TV
Abra o navegador e acesse `https://seu-usuario.github.io/seu-repo/`.
Deixe em tela cheia (F11). O dashboard já verifica dados novos sozinho a
cada 4 segundos — não precisa mexer em nada na TV depois disso.

**Atenção:** o GitHub Pages pode levar de alguns segundos a ~1 minuto pra
propagar cada atualização (não é instantâneo como era rodando local). Isso
é normal.

## Observações importantes
- Como o repositório fica **público**, os dados dentro do `data.json`
  também ficam públicos (qualquer pessoa com o link consegue ver). Se os
  dados forem sensíveis, isso não é recomendado — nesse caso, me avise
  que existem alternativas (repositório privado + GitHub Pages pago, ou
  outro tipo de hospedagem).
- O `BaseFeeder.exe` só publica se a pasta onde ele está tiver sido
  configurada com `git init` (passo 3). Se você mover os arquivos pra
  outra pasta sem Git, ele simplesmente para de tentar publicar (sem dar
  erro), e continua funcionando local normalmente.
