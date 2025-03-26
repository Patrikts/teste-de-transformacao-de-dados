import requests
import pandas as pd
import PyPDF2
import zipfile
import os

# 1. Fazer o download do arquivo PDF
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
response = requests.get(url)

# Salvar o PDF localmente
pdf_file_path = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
with open(pdf_file_path, 'wb') as f:
    f.write(response.content)

# 2.1. Extrair dados da tabela Rol de Procedimentos e Eventos em Saúde
def extract_table_from_pdf(pdf_path):
    data = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    # Ajuste conforme necessário para capturar os dados da tabela corretamente
                    data.append(line.split())  
    return data

# Extraindo os dados
table_data = extract_table_from_pdf(pdf_file_path)

# 2.2. Salvar os dados em uma tabela estruturada, em formato CSV
df = pd.DataFrame(table_data)

# Substituir as abreviações OD e AMB pelas descrições completas
df.replace({'OD': 'Descrição Completa OD', 'AMB': 'Descrição Completa AMB'}, inplace=True)

# Salvar o DataFrame em um arquivo CSV
csv_file_path = "Rol_de_Procedimentos.csv"
df.to_csv(csv_file_path, index=False)

# 2.3. Compactar o CSV em um arquivo ZIP
zip_file_path = "Teste_Patrik.zip"
with zipfile.ZipFile(zip_file_path, 'w') as zipf:
    zipf.write(csv_file_path)

# Remover o arquivo CSV após a compactação
os.remove(csv_file_path)

print("Download, processamento e limpeza concluídos com sucesso!")
