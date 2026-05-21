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
