"""
Utilitários diversos para a aplicação, como manipulação
de arquivos e outras funções auxiliares.
"""

import os


def list_files(path: str) -> list[str]:
    """
    Lista os arquivos em um diretório específico.

    Args:
        path (str): O caminho para o diretório.

    Returns:
        list[str]: Uma lista de caminhos para os arquivos encontrados.
    """

    files = []

    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            files.append(full_path)

    return files
