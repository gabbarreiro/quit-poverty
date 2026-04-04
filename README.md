# Quit-Poverty

Software pessoal feito para tratar e carregar dados de movimentações financeiras **pessoais** para banco de dados.
Sâo lidos arquivos em formato _xlsx_ e _csv_ referentes a:

- Fatura de cartão de crédito
- Extrato de conta corrente
- Movimentações de investimentos

Assim, uma vez tratos os dados são enviados para o banco de dados para alimentar dashboards externos pessoais
do autor da aplicação. Os dashboards estão em uma instância [Metabase](https://www.metabase.com/) pessoal
do autor.

# Etapas

O processo feito por essa aplicação segue o seguinte passo a passo:

1. Tratamento e consolidação dos dados
2. Classificação automática
3. Classificação manual pelo usuário (por planilha)
4. Carregamento dos lançamentos contábeis em banco de dados

# Licença

A licença para o projeto é [MIT License](https://opensource.org/license/mit), disponível no arquivo [LICENSE](LICENSE).

