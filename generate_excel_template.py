import openpyxl

def generate_template():
    """
    This script generates an Excel template file for importing articles.
    The template will have the required headers.
    """
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Artigos"

    headers = ["titulo", "conteudo", "categoria_nome", "autor_username"]
    sheet.append(headers)

    # Add some example data
    example_data = [
        ("Artigo de Exemplo 1", "Este é o conteúdo do primeiro artigo.", "Geral", "admin"),
        ("Outro Artigo", "Conteúdo de exemplo para o segundo artigo.", "Notícias", "admin"),
    ]

    for row in example_data:
        sheet.append(row)

    file_name = "template_importacao_artigos.xlsx"
    workbook.save(file_name)
    print(f"Template \"{file_name}\" gerado com sucesso.")

if __name__ == "__main__":
    generate_template()
