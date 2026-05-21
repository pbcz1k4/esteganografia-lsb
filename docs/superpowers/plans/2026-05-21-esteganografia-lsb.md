# Esteganografia LSB Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir uma aplicação Python com interface Streamlit que oculta uma mensagem textual dentro de uma imagem PNG usando esteganografia LSB (via biblioteca `stepic`), permite extrair a mensagem de volta e comprova a integridade do processo via hashes SHA-256.

**Architecture:** Separação em duas camadas — `stego.py` com funções puras (ocultar, extrair, verificar_integridade) testáveis isoladamente via pytest, e `app.py` como camada Streamlit que consome `stego.py` em três abas. Documentação em `README.md` com código-fonte, comandos e capturas de tela conforme exigido pelo professor.

**Tech Stack:** Python 3.13, Streamlit, stepic, Pillow, pytest, hashlib (stdlib).

---

## File Structure

```
projeto_esteganografia/
├── app.py                    # Interface Streamlit (criar — Task 5)
├── stego.py                  # Lógica pura (criar — Task 3)
├── tests/
│   └── test_stego.py         # Testes pytest (criar — Task 3)
├── .streamlit/
│   └── config.toml           # Tema escuro (criar — Task 2)
├── Imagem.png                # Portadora (copiar do Downloads — Task 2)
├── mensagem.txt              # Mensagem (copiar do Downloads — Task 2)
├── requirements.txt          # Dependências (criar — Task 2)
├── .gitignore                # Ignorar artefatos (criar — Task 2)
├── capturas/                 # Screenshots (criar — Task 6)
└── README.md                 # Documentação final (criar — Task 6)
```

**Caminho absoluto base:** `C:\Users\Pedro Casaroti\projeto_esteganografia\`

**Python:** `C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe`

Comandos no plano assumem que o diretório de trabalho é o do projeto. Quando relevante, comandos serão dados com caminho absoluto.

---

### Task 1: Setup inicial — requirements, git, gitignore, config Streamlit

**Files:**
- Create: `projeto_esteganografia/requirements.txt`
- Create: `projeto_esteganografia/.gitignore`
- Create: `projeto_esteganografia/.streamlit/config.toml`

- [ ] **Step 1.1: Criar `requirements.txt`**

Conteúdo exato:
```
streamlit==1.40.2
stepic==0.5.0
Pillow==11.0.0
pytest==8.3.4
```

- [ ] **Step 1.2: Criar `.gitignore`**

Conteúdo exato:
```
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/
Imagem_com_mensagem.png
mensagem_extraida.txt
```

> Os artefatos gerados (`Imagem_com_mensagem.png`, `mensagem_extraida.txt`) ficam fora do versionamento porque são saídas reprodutíveis. Os screenshots em `capturas/` permanecem versionados (são entregáveis).

- [ ] **Step 1.3: Criar `.streamlit/config.toml`**

Conteúdo exato:
```toml
[theme]
base = "dark"
primaryColor = "#00d4ff"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#161b22"
textColor = "#e6edf3"
font = "sans serif"

[server]
headless = false
```

- [ ] **Step 1.4: Inicializar repositório git**

```powershell
cd "C:\Users\Pedro Casaroti\projeto_esteganografia"
git init
git add .gitignore requirements.txt .streamlit/config.toml docs/
git commit -m "chore: setup inicial — requirements, gitignore, tema Streamlit, specs"
```

Expected: `[master (root-commit) <hash>] chore: setup inicial...`

---

### Task 2: Copiar arquivos do Downloads e instalar dependências

**Files:**
- Copy: `~/Downloads/Imagem.png` → `projeto_esteganografia/Imagem.png`
- Copy: `~/Downloads/mensagem.txt` → `projeto_esteganografia/mensagem.txt`

- [ ] **Step 2.1: Copiar `Imagem.png` e `mensagem.txt`**

```powershell
Copy-Item "C:\Users\Pedro Casaroti\Downloads\Imagem.png" "C:\Users\Pedro Casaroti\projeto_esteganografia\Imagem.png"
Copy-Item "C:\Users\Pedro Casaroti\Downloads\mensagem.txt" "C:\Users\Pedro Casaroti\projeto_esteganografia\mensagem.txt"
```

- [ ] **Step 2.2: Confirmar que arquivos chegaram**

```powershell
Get-ChildItem "C:\Users\Pedro Casaroti\projeto_esteganografia\" -Include Imagem.png,mensagem.txt -Recurse
```

Expected: lista mostrando os dois arquivos com tamanhos > 0.

- [ ] **Step 2.3: Instalar dependências**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt
```

Expected: `Successfully installed ... stepic-0.5.0 streamlit-1.40.2 ...`

- [ ] **Step 2.4: Validar imports**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -c "import stepic, PIL, streamlit; print('OK', stepic.__file__)"
```

Expected: `OK <caminho do stepic>`. Se falhar (incompatibilidade Python 3.13), pular para Task 3-Alt no final do plano.

- [ ] **Step 2.5: Commit**

```powershell
git add Imagem.png mensagem.txt
git commit -m "chore: adicionar arquivos portador e mensagem fornecidos pelo professor"
```

---

### Task 3: Implementar `stego.ocultar()` com TDD

**Files:**
- Create: `projeto_esteganografia/tests/__init__.py` (vazio)
- Create: `projeto_esteganografia/tests/test_stego.py`
- Create: `projeto_esteganografia/stego.py`

- [ ] **Step 3.1: Criar `tests/__init__.py` vazio**

Arquivo sem conteúdo (`New-Item -ItemType File tests/__init__.py`).

- [ ] **Step 3.2: Escrever o teste falho de `ocultar`**

Criar `tests/test_stego.py` com:
```python
import os
from pathlib import Path
from PIL import Image
import pytest

import stego


@pytest.fixture
def imagem_portadora(tmp_path):
    img = Image.new("RGB", (200, 200), color=(120, 130, 140))
    caminho = tmp_path / "portadora.png"
    img.save(caminho, "PNG")
    return caminho


@pytest.fixture
def mensagem_curta():
    return "Mensagem de teste com mais de cinquenta palavras: " + ("palavra " * 60)


def test_ocultar_gera_png_valido(imagem_portadora, mensagem_curta, tmp_path):
    saida = tmp_path / "com_mensagem.png"

    stego.ocultar(str(imagem_portadora), mensagem_curta, str(saida))

    assert saida.exists(), "arquivo de saída não foi criado"
    img_saida = Image.open(saida)
    assert img_saida.format == "PNG"
    assert img_saida.size == (200, 200)
    assert img_saida.mode == "RGB"


def test_ocultar_modifica_bits_da_imagem(imagem_portadora, mensagem_curta, tmp_path):
    saida = tmp_path / "com_mensagem.png"
    stego.ocultar(str(imagem_portadora), mensagem_curta, str(saida))

    bytes_original = imagem_portadora.read_bytes()
    bytes_saida = saida.read_bytes()
    assert bytes_original != bytes_saida, "imagem não foi modificada — mensagem não foi inserida"
```

- [ ] **Step 3.3: Rodar o teste e confirmar que falha**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -m pytest tests/test_stego.py -v
```

Expected: `ModuleNotFoundError: No module named 'stego'` (ou `ImportError`).

- [ ] **Step 3.4: Implementar `ocultar` em `stego.py`**

Criar `stego.py`:
```python
"""Módulo de esteganografia LSB para imagens PNG."""
from PIL import Image
import stepic


def ocultar(imagem_path: str, mensagem: str, saida_path: str) -> str:
    """Oculta `mensagem` na imagem em `imagem_path` via LSB e salva em `saida_path`.

    Retorna o caminho da imagem resultante. A saída é sempre PNG (sem perda),
    porque JPEG destruiria os bits LSB.
    """
    portadora = Image.open(imagem_path).convert("RGB")
    com_mensagem = stepic.encode(portadora, mensagem.encode("utf-8"))
    com_mensagem.save(saida_path, "PNG")
    return saida_path
```

- [ ] **Step 3.5: Rodar o teste e confirmar que passa**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -m pytest tests/test_stego.py -v
```

Expected: `2 passed`.

- [ ] **Step 3.6: Commit**

```powershell
git add stego.py tests/
git commit -m "feat: implementar stego.ocultar via stepic LSB"
```

---

### Task 4: Implementar `stego.extrair()` e `stego.verificar_integridade()` com TDD

**Files:**
- Modify: `projeto_esteganografia/tests/test_stego.py` (adicionar testes)
- Modify: `projeto_esteganografia/stego.py` (adicionar funções)

- [ ] **Step 4.1: Adicionar testes falhos de `extrair` e `verificar_integridade`**

Adicionar ao final de `tests/test_stego.py`:
```python
def test_extrair_retorna_mensagem_original(imagem_portadora, mensagem_curta, tmp_path):
    saida = tmp_path / "com_mensagem.png"
    stego.ocultar(str(imagem_portadora), mensagem_curta, str(saida))

    recuperada = stego.extrair(str(saida))

    assert recuperada == mensagem_curta


def test_extrair_de_imagem_sem_mensagem_levanta(imagem_portadora):
    with pytest.raises(Exception):
        stego.extrair(str(imagem_portadora))


def test_verificar_integridade_mensagem_identica(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("conteudo identico", encoding="utf-8")
    b.write_text("conteudo identico", encoding="utf-8")

    resultado = stego.verificar_integridade(str(a), str(b))

    assert resultado["iguais"] is True
    assert resultado["hash_original"] == resultado["hash_comparado"]
    assert len(resultado["hash_original"]) == 64  # SHA-256 em hex


def test_verificar_integridade_mensagem_diferente(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("um", encoding="utf-8")
    b.write_text("outro", encoding="utf-8")

    resultado = stego.verificar_integridade(str(a), str(b))

    assert resultado["iguais"] is False
    assert resultado["hash_original"] != resultado["hash_comparado"]
```

- [ ] **Step 4.2: Rodar os testes novos e confirmar que falham**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -m pytest tests/test_stego.py -v
```

Expected: 4 testes novos com `AttributeError: module 'stego' has no attribute 'extrair'` / `verificar_integridade`.

- [ ] **Step 4.3: Implementar `extrair` e `verificar_integridade` em `stego.py`**

Adicionar ao `stego.py` (no topo, ajustar imports):
```python
"""Módulo de esteganografia LSB para imagens PNG."""
import hashlib
from pathlib import Path

from PIL import Image
import stepic


def ocultar(imagem_path: str, mensagem: str, saida_path: str) -> str:
    """Oculta `mensagem` na imagem em `imagem_path` via LSB e salva em `saida_path`.

    Retorna o caminho da imagem resultante. A saída é sempre PNG (sem perda),
    porque JPEG destruiria os bits LSB.
    """
    portadora = Image.open(imagem_path).convert("RGB")
    com_mensagem = stepic.encode(portadora, mensagem.encode("utf-8"))
    com_mensagem.save(saida_path, "PNG")
    return saida_path


def extrair(imagem_path: str) -> str:
    """Lê a mensagem oculta em `imagem_path` e retorna o texto decodificado em UTF-8."""
    img = Image.open(imagem_path).convert("RGB")
    bytes_msg = stepic.decode(img)
    if isinstance(bytes_msg, bytes):
        return bytes_msg.decode("utf-8")
    return bytes_msg


def _sha256_de_arquivo(caminho: str) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def verificar_integridade(arquivo_original: str, arquivo_comparado: str) -> dict:
    """Compara dois arquivos por SHA-256. Retorna dict com hashes e booleano `iguais`."""
    hash_a = _sha256_de_arquivo(arquivo_original)
    hash_b = _sha256_de_arquivo(arquivo_comparado)
    return {
        "hash_original": hash_a,
        "hash_comparado": hash_b,
        "iguais": hash_a == hash_b,
    }
```

- [ ] **Step 4.4: Rodar todos os testes e confirmar verde**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -m pytest tests/test_stego.py -v
```

Expected: `6 passed`.

- [ ] **Step 4.5: Commit**

```powershell
git add stego.py tests/test_stego.py
git commit -m "feat: implementar stego.extrair e stego.verificar_integridade"
```

---

### Task 5: Validação fim-a-fim com a imagem real do professor

**Files:**
- Modify: `projeto_esteganografia/tests/test_stego.py` (adicionar teste de integração com arquivos reais)

- [ ] **Step 5.1: Adicionar teste de integração**

Adicionar ao final de `tests/test_stego.py`:
```python
def test_fluxo_completo_com_arquivos_reais(tmp_path):
    """Smoke test usando os arquivos reais Imagem.png e mensagem.txt do projeto."""
    base = Path(__file__).resolve().parent.parent
    imagem_real = base / "Imagem.png"
    mensagem_real = base / "mensagem.txt"

    if not imagem_real.exists() or not mensagem_real.exists():
        pytest.skip("arquivos do professor não estão presentes")

    texto_original = mensagem_real.read_text(encoding="utf-8")
    saida_imagem = tmp_path / "Imagem_com_mensagem.png"
    saida_texto = tmp_path / "mensagem_extraida.txt"

    stego.ocultar(str(imagem_real), texto_original, str(saida_imagem))
    extraido = stego.extrair(str(saida_imagem))
    saida_texto.write_text(extraido, encoding="utf-8")

    integridade = stego.verificar_integridade(str(mensagem_real), str(saida_texto))
    assert integridade["iguais"], (
        f"mensagem corrompida! hash original={integridade['hash_original']} "
        f"extraido={integridade['hash_comparado']}"
    )

    # imagem com mensagem deve ser diferente da original (em bytes)
    integridade_img = stego.verificar_integridade(str(imagem_real), str(saida_imagem))
    assert not integridade_img["iguais"], "imagem com mensagem é idêntica à original — algo deu errado"
```

- [ ] **Step 5.2: Rodar e confirmar**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -m pytest tests/test_stego.py -v
```

Expected: `7 passed`. Esse teste é a prova de que o fluxo do trabalho funciona com os arquivos do professor.

- [ ] **Step 5.3: Commit**

```powershell
git add tests/test_stego.py
git commit -m "test: validação fim-a-fim com Imagem.png e mensagem.txt reais"
```

---

### Task 6: Interface Streamlit — Aba "Ocultar"

**Files:**
- Create: `projeto_esteganografia/app.py`

- [ ] **Step 6.1: Criar `app.py` com layout base e aba "Ocultar"**

Criar `app.py`:
```python
"""Interface Streamlit para esteganografia LSB."""
import io
from pathlib import Path

import streamlit as st
from PIL import Image

import stego


st.set_page_config(
    page_title="Esteganografia LSB",
    page_icon="🔐",
    layout="wide",
)

st.title("🔐 Esteganografia LSB em PNG")
st.caption(
    "Trabalho prático — ocultar e extrair mensagens em imagens via bit menos significativo (LSB). "
    "Biblioteca: stepic + Pillow."
)

aba_ocultar, aba_extrair, aba_integridade = st.tabs(
    ["1 · Ocultar", "2 · Extrair", "3 · Integridade"]
)

# ---------- Aba 1: Ocultar ----------
with aba_ocultar:
    st.subheader("Ocultar mensagem em uma imagem PNG")

    col_a, col_b = st.columns(2)
    with col_a:
        arquivo_img = st.file_uploader(
            "Imagem portadora (.png)", type=["png"], key="up_ocultar_img"
        )
        if arquivo_img is None:
            padrao = Path("Imagem.png")
            if padrao.exists():
                st.info(f"Usando `{padrao.name}` por padrão (faça upload para trocar).")
                bytes_img = padrao.read_bytes()
            else:
                bytes_img = None
        else:
            bytes_img = arquivo_img.read()

    with col_b:
        padrao_msg = Path("mensagem.txt")
        texto_default = padrao_msg.read_text(encoding="utf-8") if padrao_msg.exists() else ""
        mensagem = st.text_area(
            "Mensagem a ocultar (mín. 50 palavras)",
            value=texto_default,
            height=200,
            key="ta_ocultar_msg",
        )
        n_palavras = len(mensagem.split())
        st.metric("Palavras", n_palavras, delta=n_palavras - 50, delta_color="normal")

    if st.button("Ocultar mensagem", type="primary", disabled=bytes_img is None or not mensagem):
        entrada_tmp = Path("_entrada_tmp.png")
        entrada_tmp.write_bytes(bytes_img)
        saida = Path("Imagem_com_mensagem.png")
        stego.ocultar(str(entrada_tmp), mensagem, str(saida))
        entrada_tmp.unlink()

        st.success(f"Mensagem ocultada com sucesso em `{saida.name}`.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Imagem original**")
            st.image(bytes_img, use_container_width=True)
        with col2:
            st.markdown("**Imagem com mensagem oculta**")
            st.image(str(saida), use_container_width=True)

        with open(saida, "rb") as f:
            st.download_button(
                "Baixar imagem com mensagem",
                data=f.read(),
                file_name="Imagem_com_mensagem.png",
                mime="image/png",
            )

# ---------- Aba 2: Extrair ----------
with aba_extrair:
    st.subheader("Em construção (próxima task)")

# ---------- Aba 3: Integridade ----------
with aba_integridade:
    st.subheader("Em construção (próxima task)")
```

- [ ] **Step 6.2: Rodar Streamlit e validar a aba 1 manualmente**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -m streamlit run app.py
```

Expected: abre `http://localhost:8501` no navegador. Validar visualmente:
- Título e descrição aparecem.
- Imagem `Imagem.png` carrega no preview.
- Mensagem preenchida com o conteúdo de `mensagem.txt`.
- Métrica de palavras mostra ≥ 50.
- Botão "Ocultar mensagem" gera arquivo `Imagem_com_mensagem.png` e exibe lado a lado.
- Botão de download funciona.

Parar com `Ctrl+C` no terminal após validar.

- [ ] **Step 6.3: Commit**

```powershell
git add app.py
git commit -m "feat: interface Streamlit — aba Ocultar"
```

---

### Task 7: Aba "Extrair" e aba "Integridade"

**Files:**
- Modify: `projeto_esteganografia/app.py`

- [ ] **Step 7.1: Substituir os blocos "Em construção" pelas abas reais**

Substituir o bloco `# ---------- Aba 2: Extrair ----------` até o final do arquivo por:

```python
# ---------- Aba 2: Extrair ----------
with aba_extrair:
    st.subheader("Extrair mensagem oculta de uma imagem")

    arquivo_com_msg = st.file_uploader(
        "Imagem com mensagem oculta (.png)", type=["png"], key="up_extrair_img"
    )
    if arquivo_com_msg is None:
        padrao = Path("Imagem_com_mensagem.png")
        if padrao.exists():
            st.info(f"Usando `{padrao.name}` por padrão.")
            bytes_extr = padrao.read_bytes()
        else:
            bytes_extr = None
    else:
        bytes_extr = arquivo_com_msg.read()

    if st.button("Extrair mensagem", type="primary", disabled=bytes_extr is None):
        entrada_tmp = Path("_entrada_extrair_tmp.png")
        entrada_tmp.write_bytes(bytes_extr)
        try:
            texto = stego.extrair(str(entrada_tmp))
        except Exception as e:
            st.error(f"Não foi possível extrair: {e}")
            texto = None
        finally:
            entrada_tmp.unlink(missing_ok=True)

        if texto is not None:
            saida_txt = Path("mensagem_extraida.txt")
            saida_txt.write_text(texto, encoding="utf-8")
            st.success("Mensagem extraída com sucesso.")
            st.metric("Palavras recuperadas", len(texto.split()))
            st.text_area("Texto recuperado", value=texto, height=200, key="ta_extraido")
            st.download_button(
                "Baixar mensagem extraída",
                data=texto.encode("utf-8"),
                file_name="mensagem_extraida.txt",
                mime="text/plain",
            )


# ---------- Aba 3: Integridade ----------
with aba_integridade:
    st.subheader("Comprovação de integridade")
    st.caption(
        "Comparamos a mensagem original com a extraída (devem ser idênticas) e a imagem original "
        "com a imagem modificada (devem ter hashes diferentes, mas mesmas dimensões e modo)."
    )

    col_e, col_d = st.columns(2)
    with col_e:
        st.markdown("**Mensagens**")
        msg_orig = st.file_uploader("mensagem.txt original", type=["txt"], key="up_msg_orig")
        msg_extr = st.file_uploader("mensagem_extraida.txt", type=["txt"], key="up_msg_extr")

        # fallback nos arquivos do projeto
        if msg_orig is None and Path("mensagem.txt").exists():
            msg_orig_path = "mensagem.txt"
        elif msg_orig is not None:
            msg_orig_path = "_msg_orig_tmp.txt"
            Path(msg_orig_path).write_bytes(msg_orig.read())
        else:
            msg_orig_path = None

        if msg_extr is None and Path("mensagem_extraida.txt").exists():
            msg_extr_path = "mensagem_extraida.txt"
        elif msg_extr is not None:
            msg_extr_path = "_msg_extr_tmp.txt"
            Path(msg_extr_path).write_bytes(msg_extr.read())
        else:
            msg_extr_path = None

        if msg_orig_path and msg_extr_path:
            res = stego.verificar_integridade(msg_orig_path, msg_extr_path)
            st.code(f"SHA-256 original : {res['hash_original']}\nSHA-256 extraída : {res['hash_comparado']}")
            if res["iguais"]:
                st.success("✅ Mensagens são idênticas — integridade preservada.")
            else:
                st.error("❌ Mensagens diferem — algo corrompeu o processo.")

    with col_d:
        st.markdown("**Imagens (portador)**")
        img_orig_path = "Imagem.png" if Path("Imagem.png").exists() else None
        img_mod_path = "Imagem_com_mensagem.png" if Path("Imagem_com_mensagem.png").exists() else None

        if img_orig_path and img_mod_path:
            res_img = stego.verificar_integridade(img_orig_path, img_mod_path)
            st.code(
                f"SHA-256 original    : {res_img['hash_original']}\n"
                f"SHA-256 com mensagem: {res_img['hash_comparado']}"
            )
            if not res_img["iguais"]:
                st.success(
                    "✅ Imagens têm hashes diferentes — esperado, pois a mensagem foi gravada nos LSBs."
                )
            else:
                st.warning("⚠️ Hashes iguais — nenhuma alteração foi feita.")

            # Verificar dimensões e modo
            im_a = Image.open(img_orig_path)
            im_b = Image.open(img_mod_path)
            st.write(
                {
                    "dimensoes_original": im_a.size,
                    "dimensoes_modificada": im_b.size,
                    "modo_original": im_a.mode,
                    "modo_modificada": im_b.mode,
                    "estruturalmente_equivalentes": (im_a.size == im_b.size and im_a.mode == im_b.mode),
                }
            )
        else:
            st.info("Gere `Imagem_com_mensagem.png` na aba 1 antes de comparar.")
```

- [ ] **Step 7.2: Rodar e validar manualmente**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -m streamlit run app.py
```

Roteiro de validação:
1. Aba "Ocultar" → clicar "Ocultar mensagem" → confirmar que gera `Imagem_com_mensagem.png`.
2. Aba "Extrair" → clicar "Extrair mensagem" → texto recuperado deve ser idêntico à mensagem original.
3. Aba "Integridade" → mensagens devem mostrar ✅; imagens devem mostrar hashes diferentes mas mesmas dimensões/modo.

Parar com `Ctrl+C`.

- [ ] **Step 7.3: Commit**

```powershell
git add app.py
git commit -m "feat: abas Extrair e Integridade na interface Streamlit"
```

---

### Task 8: Capturas de tela

**Files:**
- Create: `projeto_esteganografia/capturas/01-aba-ocultar.png`
- Create: `projeto_esteganografia/capturas/02-aba-ocultar-resultado.png`
- Create: `projeto_esteganografia/capturas/03-aba-extrair.png`
- Create: `projeto_esteganografia/capturas/04-aba-integridade.png`

> Esses arquivos são gerados manualmente pelo usuário com a ferramenta de captura do Windows (`Win+Shift+S`). O plano não pode automatizar isso, mas pode orientar.

- [ ] **Step 8.1: Rodar a app**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -m streamlit run app.py
```

- [ ] **Step 8.2: Capturar 4 telas**

Usar `Win+Shift+S` (ferramenta de captura do Windows) e salvar em `projeto_esteganografia/capturas/`:

1. `01-aba-ocultar.png` — aba "Ocultar" com a imagem e mensagem carregadas, **antes** de clicar no botão.
2. `02-aba-ocultar-resultado.png` — depois de clicar, com as duas imagens lado a lado e a mensagem de sucesso.
3. `03-aba-extrair.png` — aba "Extrair" com a mensagem recuperada visível.
4. `04-aba-integridade.png` — aba "Integridade" mostrando os SHA-256 e as caixinhas verdes ✅.

- [ ] **Step 8.3: Commit**

```powershell
git add capturas/
git commit -m "docs: capturas de tela das 3 abas para o relatório"
```

---

### Task 9: Escrever `README.md` com o formato exigido pelo professor

**Files:**
- Create: `projeto_esteganografia/README.md`

- [ ] **Step 9.1: Coletar os hashes reais para incluir no README**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -c "import stego; print(stego.verificar_integridade('Imagem.png', 'Imagem_com_mensagem.png'))"
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -c "import stego; print(stego.verificar_integridade('mensagem.txt', 'mensagem_extraida.txt'))"
```

Anotar os 4 hashes — serão colados no README no Step 9.2.

- [ ] **Step 9.2: Criar `README.md`**

Conteúdo (substituir `<HASH_X>` pelos valores reais do Step 9.1):

````markdown
# Esteganografia LSB em Imagens PNG

**Trabalho prático — Parte 2: Implementação**
Autor: Pedro Casaroti

## 1. Introdução

A esteganografia é uma técnica utilizada para ocultar informações dentro de arquivos aparentemente comuns, como imagens, áudios ou vídeos. Diferentemente da criptografia, que protege o conteúdo da mensagem, a esteganografia busca esconder a própria existência da informação.

Este trabalho implementa esteganografia pelo método **LSB (Least Significant Bit)** — o bit menos significativo de cada canal de cor (R, G, B) de cada pixel é usado para armazenar bits da mensagem. Como o LSB altera a cor em apenas 1/256, a modificação é imperceptível ao olho humano, mas pode ser revertida bit a bit por quem conhece o algoritmo.

## 2. Ferramentas utilizadas

| Ferramenta | Versão | Uso |
|---|---|---|
| Python | 3.13 | Linguagem |
| stepic | 0.5.0 | Codificação/decodificação LSB |
| Pillow | 11.0.0 | Manipulação de imagens |
| Streamlit | 1.40.2 | Interface gráfica |
| pytest | 8.3.4 | Testes automatizados |

A escolha por **Python + stepic** segue exatamente a opção sugerida pelo enunciado ("Linguagens de programação — por exemplo, Python com bibliotecas como steganography ou stepic").

## 3. Arquivos do trabalho

- `Imagem.png` — arquivo portador (PNG fornecido).
- `mensagem.txt` — mensagem textual a ser ocultada (60 palavras, > 50 exigidas).
- `Imagem_com_mensagem.png` — saída gerada pelo programa.
- `mensagem_extraida.txt` — texto recuperado a partir da imagem com mensagem.

## 4. Instalação e execução

```powershell
# 1. Clonar/extrair o projeto e entrar na pasta
cd projeto_esteganografia

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar a interface
streamlit run app.py
```

A interface abre automaticamente em `http://localhost:8501`.

Para rodar os testes automatizados:
```powershell
pytest tests/ -v
```

## 5. Código-fonte

### `stego.py` — Lógica de esteganografia

Três funções puras, testáveis isoladamente:

- **`ocultar(imagem_path, mensagem, saida_path)`** — abre a imagem, chama `stepic.encode()` para gravar a mensagem nos LSBs dos canais RGB e salva o resultado como PNG (formato sem perda; JPEG destruiria os bits).
- **`extrair(imagem_path)`** — chama `stepic.decode()` na imagem e retorna o texto em UTF-8.
- **`verificar_integridade(arquivo_a, arquivo_b)`** — calcula SHA-256 dos dois arquivos e retorna um dicionário indicando se são iguais.

O código completo está em [`stego.py`](stego.py).

### `app.py` — Interface Streamlit

Três abas:
1. **Ocultar** — upload da imagem + área de texto da mensagem → gera `Imagem_com_mensagem.png`.
2. **Extrair** — upload da imagem com mensagem → mostra texto recuperado.
3. **Integridade** — compara hashes SHA-256 e mostra ✅/❌.

Código completo em [`app.py`](app.py).

## 6. Capturas de tela

### 6.1 Aba "Ocultar" — antes da execução

![Aba Ocultar](capturas/01-aba-ocultar.png)

### 6.2 Aba "Ocultar" — depois da execução (comparação lado a lado)

![Resultado da ocultação](capturas/02-aba-ocultar-resultado.png)

### 6.3 Aba "Extrair" — mensagem recuperada

![Aba Extrair](capturas/03-aba-extrair.png)

### 6.4 Aba "Integridade" — hashes SHA-256

![Aba Integridade](capturas/04-aba-integridade.png)

## 7. Resultados — comprovação de integridade

### 7.1 Integridade da mensagem

Comparação SHA-256 entre `mensagem.txt` original e `mensagem_extraida.txt`:

```
SHA-256 original : <HASH_MSG_ORIGINAL>
SHA-256 extraída : <HASH_MSG_EXTRAIDA>
Iguais? ✅ SIM
```

Conclusão: a mensagem foi recuperada **sem qualquer perda** — bit por bit idêntica ao original. A esteganografia é totalmente reversível.

### 7.2 Integridade do arquivo portador

Comparação entre `Imagem.png` e `Imagem_com_mensagem.png`:

```
SHA-256 original    : <HASH_IMG_ORIGINAL>
SHA-256 com mensagem: <HASH_IMG_MODIFICADA>
Iguais? ❌ NÃO (esperado — a mensagem foi gravada nos LSBs)

Dimensões original   : (largura, altura) — igual à modificada
Modo de cor original : RGB — igual à modificada
```

Conclusão: a imagem foi alterada em bytes (era preciso, para carregar a mensagem), mas:
- Continua sendo um PNG válido;
- Mantém exatamente as mesmas dimensões e modo de cor;
- É **visualmente equivalente** à original (ver capturas 6.2).

A integridade visual/funcional do portador foi preservada, que é o objetivo prático da esteganografia.

## 8. Discussão

- **Formato obrigatório PNG:** usamos PNG porque a compressão é sem perda. Salvar a saída como JPEG destruiria os bits LSB e a mensagem se perderia.
- **Capacidade:** cada pixel armazena 3 bits (1 por canal RGB). Uma imagem de 200×200 RGB armazena ~15.000 bytes; nossa mensagem de ~420 bytes cabe folgadamente.
- **Limitações:** o método LSB é detectável por análise estatística (esteganálise). Em cenários reais, costuma-se combinar com criptografia antes de ocultar, para que mesmo a detecção não revele o conteúdo.

## 9. Conclusão

O trabalho demonstrou, com código próprio e interface gráfica, que é possível ocultar uma mensagem textual em uma imagem PNG via LSB e recuperá-la integralmente. A integridade da mensagem foi comprovada por SHA-256 (idênticos), e a integridade visual do portador foi comprovada pela equivalência de dimensões/modo/aparência — apesar da diferença esperada em bytes brutos.
````

- [ ] **Step 9.3: Substituir os placeholders `<HASH_*>` pelos valores reais**

Editar `README.md` e trocar:
- `<HASH_MSG_ORIGINAL>` e `<HASH_MSG_EXTRAIDA>` pelos hashes do Step 9.1.
- `<HASH_IMG_ORIGINAL>` e `<HASH_IMG_MODIFICADA>` pelos hashes do Step 9.1.
- `(largura, altura)` pelas dimensões reais da `Imagem.png`.

- [ ] **Step 9.4: Commit**

```powershell
git add README.md
git commit -m "docs: README com introdução, código, capturas, resultados e conclusão"
```

---

### Task 10: Verificação final

**Files:** nenhuma alteração — apenas validação.

- [ ] **Step 10.1: Rodar suite de testes completa**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -m pytest tests/ -v
```

Expected: `7 passed`.

- [ ] **Step 10.2: Rodar app e fazer o fluxo completo manualmente**

```powershell
& "C:\Users\Pedro Casaroti\AppData\Local\Programs\Python\Python313\python.exe" -m streamlit run app.py
```

Checklist:
- [ ] Aba Ocultar funciona.
- [ ] Aba Extrair recupera o texto idêntico.
- [ ] Aba Integridade mostra ✅ para mensagem e indica imagens estruturalmente equivalentes.
- [ ] README abre e renderiza as capturas.

- [ ] **Step 10.3: Verificar estrutura final**

```powershell
Get-ChildItem "C:\Users\Pedro Casaroti\projeto_esteganografia" -Recurse -File | Select-Object FullName
```

Confirmar presença de:
- `app.py`, `stego.py`, `tests/test_stego.py`
- `requirements.txt`, `.gitignore`, `.streamlit/config.toml`
- `Imagem.png`, `mensagem.txt`, `Imagem_com_mensagem.png`, `mensagem_extraida.txt`
- `capturas/01-aba-ocultar.png` ... `04-aba-integridade.png`
- `README.md`
- `docs/superpowers/specs/2026-05-21-esteganografia-lsb-design.md`
- `docs/superpowers/plans/2026-05-21-esteganografia-lsb.md`

- [ ] **Step 10.4: Log git final**

```powershell
git log --oneline
```

Expected: ~9 commits limpos representando cada task.

---

## Plano B — se stepic não funcionar em Python 3.13

Se `import stepic` falhar no Step 2.4, substituir o `stego.py` pela implementação LSB manual abaixo (continua atendendo o enunciado, pois "Python com bibliotecas" inclui Pillow):

```python
"""Implementação LSB manual usando apenas Pillow (fallback se stepic falhar)."""
import hashlib
from PIL import Image

DELIMITADOR = "###FIM###"


def _texto_para_bits(texto: str) -> str:
    return "".join(f"{b:08b}" for b in texto.encode("utf-8"))


def _bits_para_texto(bits: str) -> str:
    bytes_lista = bytearray()
    for i in range(0, len(bits) - 7, 8):
        bytes_lista.append(int(bits[i : i + 8], 2))
    return bytes_lista.decode("utf-8", errors="ignore")


def ocultar(imagem_path: str, mensagem: str, saida_path: str) -> str:
    img = Image.open(imagem_path).convert("RGB")
    pixels = list(img.getdata())
    bits = _texto_para_bits(mensagem + DELIMITADOR)
    if len(bits) > len(pixels) * 3:
        raise ValueError("Imagem pequena demais para a mensagem.")
    novos = []
    idx = 0
    for r, g, b in pixels:
        canais = [r, g, b]
        for c in range(3):
            if idx < len(bits):
                canais[c] = (canais[c] & ~1) | int(bits[idx])
                idx += 1
        novos.append(tuple(canais))
    img.putdata(novos)
    img.save(saida_path, "PNG")
    return saida_path


def extrair(imagem_path: str) -> str:
    img = Image.open(imagem_path).convert("RGB")
    bits = []
    for r, g, b in img.getdata():
        bits.extend([r & 1, g & 1, b & 1])
    texto = _bits_para_texto("".join(map(str, bits)))
    if DELIMITADOR not in texto:
        raise ValueError("Delimitador não encontrado — não há mensagem oculta.")
    return texto.split(DELIMITADOR)[0]


def _sha256_de_arquivo(caminho: str) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def verificar_integridade(arquivo_original: str, arquivo_comparado: str) -> dict:
    hash_a = _sha256_de_arquivo(arquivo_original)
    hash_b = _sha256_de_arquivo(arquivo_comparado)
    return {"hash_original": hash_a, "hash_comparado": hash_b, "iguais": hash_a == hash_b}
```

Os testes existentes (Task 3 e 4) continuam válidos para essa implementação — a API é idêntica. No README, ajustar a seção "Ferramentas utilizadas" para refletir Pillow puro em vez de stepic.
