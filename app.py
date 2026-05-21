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
