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

    integridade_img = stego.verificar_integridade(str(imagem_real), str(saida_imagem))
    assert not integridade_img["iguais"], "imagem com mensagem é idêntica à original — algo deu errado"
