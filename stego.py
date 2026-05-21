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
    if isinstance(bytes_msg, str):
        # stepic 0.5.0 retorna str onde cada codepoint é um byte (latin-1),
        # então recuperamos os bytes originais e decodificamos como UTF-8.
        bytes_msg = bytes_msg.encode("latin-1")
    return bytes_msg.decode("utf-8")


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
