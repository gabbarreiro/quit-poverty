"""
Tratamento de dados do BTG.
"""

import io
import os

import pandas as pd
import msoffcrypto as msoff

from ..misc import adjust_description, list_files


def remove_password(path: str, password: str) -> pd.DataFrame:
    """
    Lê um arquivo Excel protegido por senha e retorna um DataFrame.

    Args:
        path (str): O caminho para o arquivo Excel.
        password (str): A senha para acessar o arquivo.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados do arquivo Excel.
    """

    file = msoff.OfficeFile(open(path, "rb"))

    file.load_key(password=password)

    decrypted = io.BytesIO()
    file.decrypt(decrypted)

    return decrypted


def parse_btg_account(path: str) -> pd.DataFrame:
    """
    Lê e padroniza os dados de extratos bancários do BTG Pactual.

    Args:
        path (str):
            O caminho para o diretório contendo os arquivos de extrato.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados padronizados.
    """

    rename_columns = {
        "Data e hora": "date_ref",
        "Categoria": "category",
        "Transação": "transaction",
        "Descrição": "original_description",
        "Valor": "amount",
    }

    raw_data = pd.DataFrame()

    for file in list_files(path):
        df = pd.read_excel(file, header=10)
        df = df.rename(columns=rename_columns)
        df = df[rename_columns.values()]

        raw_data = pd.concat([raw_data, df], ignore_index=True)

    raw_data = raw_data.dropna()
    raw_data = raw_data.reset_index(drop=True)

    raw_data["description"] = raw_data.apply(
        axis=1, func=lambda row: f"{row["transaction"]} - {row["original_description"]}"
    )

    raw_data["description"] = raw_data["description"].apply(adjust_description)

    raw_data = raw_data.drop(
        columns=["transaction", "original_description", "category"]
    )

    raw_data["date_ref"] = pd.to_datetime(
        raw_data["date_ref"].str.split(" ").str[0], dayfirst=True
    )

    raw_data["source"] = "conta_btg"

    return raw_data


def parse_btg_credit_card(path: str) -> pd.DataFrame:
    """
    Lê e padroniza os dados de faturas de cartão de crédito do BTG Pactual.

    Args:
        path (str): O caminho para o diretório contendo os arquivos de fatura.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados padronizados.
    """

    # Achou que eu ia deixar meu CPF no código?
    # Não sou vibe coder, tchê!
    password = os.environ.get("meu_cpf")

    rename_columns = {
        "Data": "date_ref",
        "Descrição": "description",
        "Valor": "amount",
    }

    raw_data = pd.DataFrame()

    for file in list_files(path):
        df = pd.read_excel(remove_password(file, password), header=19)

        df = df.rename(columns=rename_columns)
        df = df[rename_columns.values()]

        raw_data = pd.concat([raw_data, df], ignore_index=True)

    raw_data = raw_data.dropna(subset=["description"])
    raw_data["description"] = raw_data["description"].apply(adjust_description)

    raw_data = raw_data[raw_data["date_ref"] != "Data"]

    raw_data["date_ref"] = pd.to_datetime(
        raw_data["date_ref"].astype(str).str.split(" ").str[0], yearfirst=True
    )
    raw_data["amount"] = raw_data["amount"].astype(float) * -1

    raw_data["source"] = "cartao_btg"

    return raw_data
