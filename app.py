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
