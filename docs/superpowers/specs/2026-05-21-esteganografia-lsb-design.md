# Esteganografia LSB em PNG — Trabalho Prático

**Data:** 2026-05-21
**Autor:** Pedro Casaroti
**Status:** Aprovado pelo usuário, aguardando revisão da spec

## 1. Contexto e objetivo

Trabalho prático da disciplina (Parte 2 — Implementação Prática). O objetivo é demonstrar a aplicação de esteganografia ocultando uma mensagem textual dentro de uma imagem portadora e comprovando que (a) a mensagem pode ser recuperada integralmente e (b) o arquivo portador continua aparentemente íntegro.

### Requisitos do enunciado

Conforme proposta do professor:

1. Escolher uma abordagem entre:
   - Ferramentas de software livre (OpenStego, Steghide, SilentEye), **ou**
   - Linguagens de programação (Python com bibliotecas como `steganography` ou `stepic`).
2. Escolher um arquivo portador (`.png` ou `.bmp`).
3. Ocultar uma mensagem textual (pelo menos 50 palavras) no arquivo.
4. Extrair a mensagem com sucesso e comprovar a integridade do arquivo portador.
5. Documentar o processo: capturas de tela, código-fonte e comandos utilizados.

### Arquivos fornecidos

- `Imagem.png` — portadora (PNG, fornecida pelo professor em `~/Downloads/`).
- `mensagem.txt` — mensagem com 60 palavras (atende o mínimo de 50). Texto explica o conceito de esteganografia.

## 2. Abordagem escolhida

**Python + biblioteca `stepic` + `Pillow`**, exatamente como listado no enunciado.

### Por que stepic

- Citada nominalmente na proposta do professor.
- Implementa LSB (Least Significant Bit) nos canais RGB — um dos métodos clássicos de esteganografia em imagem, didaticamente relevante.
- Saída sempre em PNG (sem perda), o que preserva os bits LSB. (JPEG destruiria a mensagem por compressão com perda.)
- API simples (`stepic.encode`, `stepic.decode`), o que mantém o código curto e legível para a documentação.

### Por que com interface gráfica (Streamlit)

- Permite gerar capturas de tela profissionais para a documentação.
- Demonstra de forma visual a comparação lado-a-lado entre imagem original e imagem com mensagem (mostrando que parecem idênticas).
- Mantém o código Python visível no repositório como código-fonte para o trabalho.
- Streamlit é Python puro — não introduz outras linguagens (HTML/JS/CSS).

## 3. Arquitetura

```
projeto_esteganografia/
├── app.py                    # Interface Streamlit (3 abas)
├── stego.py                  # Lógica pura: ocultar, extrair, integridade
├── Imagem.png                # Cópia da portadora original
├── mensagem.txt              # Cópia da mensagem original
├── Imagem_com_mensagem.png   # Saída gerada pela aba "Ocultar"
├── mensagem_extraida.txt     # Saída gerada pela aba "Extrair"
├── requirements.txt          # streamlit, pillow, stepic
├── capturas/                 # Screenshots para documentação
└── README.md                 # Documentação completa
```

### Separação de responsabilidades

- **`stego.py`** — três funções puras, sem dependência de Streamlit:
  - `ocultar(imagem_path, mensagem_texto, saida_path)` → `PIL.Image`
  - `extrair(imagem_path)` → `str`
  - `verificar_integridade(arquivo_original, arquivo_extraido)` → `dict` com hashes e booleano de igualdade
- **`app.py`** — apenas camada de UI. Consome `stego.py`. Permite que a lógica seja testada independente da interface.

## 4. Interface (Streamlit)

Layout em três abas:

### Aba 1 — Ocultar
- Upload de imagem PNG (com fallback para `Imagem.png` já presente).
- Área de texto com a mensagem (preenchida com `mensagem.txt` por padrão).
- Botão **"Ocultar mensagem"**.
- Após executar: preview lado-a-lado (original vs. com mensagem) + métricas (dimensões, modo, tamanho em bytes) + botão de download do PNG resultante.

### Aba 2 — Extrair
- Upload da imagem com mensagem oculta.
- Botão **"Extrair mensagem"**.
- Mostra o texto recuperado em um bloco destacado + contagem de palavras + botão de download em `.txt`.

### Aba 3 — Integridade
- Upload da mensagem original (`mensagem.txt`) e da mensagem extraída.
- Exibe SHA-256 das duas + indicador visual (✅ idêntico / ❌ divergente).
- Exibe SHA-256 da imagem original e da imagem com mensagem (espera-se que sejam **diferentes** — isso prova que a imagem foi modificada para carregar a mensagem, sem deixar de ser visualmente equivalente).
- Tabela com dimensões e modo de cor das duas imagens (espera-se que sejam idênticos).

### Estilo visual

- Tema escuro (`.streamlit/config.toml`), paleta sóbria (fundo quase preto, acento ciano).
- Tipografia sans-serif limpa, hierarquia clara.
- Espaçamento generoso, sem poluição visual.
- Métricas em destaque (`st.metric`).
- Feedback claro: `st.success` em integridade OK, `st.error` em divergência.

## 5. Algoritmo (LSB via stepic)

O `stepic` codifica a mensagem usando o **bit menos significativo** de cada canal RGB:

1. A mensagem é convertida para bytes.
2. Cada byte (8 bits) é distribuído entre o LSB dos canais R, G, B de pixels consecutivos.
3. Como o LSB representa a menor variação possível de cor (1/256), a alteração é imperceptível ao olho humano.
4. Na extração, o processo inverso lê os LSBs e reconstrói os bytes.

**Capacidade:** cada pixel armazena 3 bits (1 por canal). Uma imagem 800×600 RGB armazena ~180 mil bytes. A mensagem de 60 palavras (~420 bytes) cabe folgadamente.

## 6. Comprovação de integridade

Duas verificações distintas:

1. **Integridade da mensagem:** SHA-256 de `mensagem.txt` original == SHA-256 de `mensagem_extraida.txt`.
   - Se iguais: a esteganografia foi reversível sem perda — objetivo principal cumprido.
2. **Integridade visual do portador:** as duas imagens (original e com mensagem) devem ter:
   - **Hash SHA-256 diferente** (prova que houve alteração binária — esperado).
   - **Mesmas dimensões e mesmo modo de cor** (RGB → RGB, 800×600 → 800×600).
   - **Aparência visualmente equivalente** (validado pela comparação lado-a-lado na interface).

> Nota: "integridade do arquivo portador" no contexto do enunciado refere-se à integridade *visual/funcional* (o PNG continua válido, abre normalmente, parece a mesma imagem), não à integridade *bit-a-bit* — que necessariamente muda, pois é onde a mensagem foi gravada.

## 7. Documentação (`README.md`)

Conforme exigido pelo professor, o README incluirá:

1. **Introdução** — o que é esteganografia (citando a própria mensagem oculta), diferença para criptografia.
2. **Ferramentas utilizadas** — Python 3.13, `stepic`, `Pillow`, `Streamlit`. Versões fixadas.
3. **Instalação e execução** — comandos exatos:
   ```
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. **Código-fonte comentado** — `stego.py` e `app.py` exibidos com explicações dos blocos principais.
5. **Capturas de tela** — uma por aba (Ocultar, Extrair, Integridade) + comparação lado-a-lado das imagens. Salvas em `capturas/`.
6. **Resultados** — hashes calculados, comprovação de integridade.
7. **Conclusão** — discussão sobre limitações (PNG obrigatório, capacidade limitada pela imagem, detecção por análise estatística).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Usuário tentar salvar saída como JPEG | UI força PNG; README alerta explicitamente. |
| stepic incompatível com Python 3.13 | Validar instalação no primeiro passo; se falhar, plano B é implementar LSB manualmente em ~30 linhas com Pillow (continua atendendo o enunciado, pois "Python com bibliotecas" inclui Pillow). |
| Imagem muito pequena para a mensagem | A mensagem real (~420 bytes) cabe em qualquer PNG razoável; documentar a capacidade no README. |

## 9. Critérios de sucesso

- [ ] `streamlit run app.py` abre a interface sem erros.
- [ ] Aba "Ocultar" gera `Imagem_com_mensagem.png` válida.
- [ ] Aba "Extrair" recupera o texto idêntico a `mensagem.txt`.
- [ ] Aba "Integridade" mostra ✅ para a mensagem e indica que as imagens são visualmente equivalentes.
- [ ] README contém código-fonte, comandos e ao menos 3 capturas de tela.
- [ ] Mensagem oculta tem ≥ 50 palavras (atendido: 60).
- [ ] Arquivo portador é `.png` (atendido).

## 10. Fora de escopo

- Criptografia da mensagem antes de ocultar (esteganografia + criptografia seria uma extensão; o enunciado pede apenas esteganografia).
- Suporte a outros formatos de portador (BMP, áudio, vídeo).
- Detecção de esteganografia (esteganálise).
- Deploy em servidor — a aplicação roda localmente.
