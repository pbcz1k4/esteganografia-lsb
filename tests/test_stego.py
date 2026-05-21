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
