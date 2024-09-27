import os
import boto3  # type: ignore
from botocore.exceptions import NoCredentialsError  # type: ignore

# Função para listar as imagens da pasta local
def listar_imagens(caminho_pasta):
    # Criar uma lista para armazenar as imagens encontradas
    imagens = []
    
    # Percorrer todos os arquivos na pasta
    for arquivo in os.listdir(caminho_pasta):
        # Verificar se o arquivo é uma imagem (extensões comuns)
        if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):  # Considerar extensão em minúsculas
            imagens.append(os.path.join(caminho_pasta, arquivo))

    return imagens

# Função para fazer upload de um arquivo para o Amazon S3
def fazer_upload_s3(arquivo, bucket, nome_s3):
    # Criar um cliente S3 (substituir pelas suas credenciais)
    s3 = boto3.client('s3', aws_access_key_id='SEU_ACCESS_KEY',
                      aws_secret_access_key='SEU_SECRET_KEY')

    try:
        # Enviar o arquivo para o bucket S3
        s3.upload_file(arquivo, bucket, nome_s3)
        print(f'Sucesso no upload: {nome_s3}')
        return True
    except FileNotFoundError:
        print('Arquivo não encontrado.')
        return False
    except NoCredentialsError:
        print('Credenciais inválidas.')
        return False
    except Exception as e:
        print(f'Ocorreu um erro ao enviar {nome_s3}: {e}')
        return False

# Função principal do projeto
def backup_imagens_para_nuvem():
    # Especificar o caminho da pasta onde estão as imagens
    caminho_pasta = './imagens_hamburgueria'  # Substitua pelo caminho correto
    # Nome do bucket S3 onde as imagens serão armazenadas
    bucket_name = 'nome-do-seu-bucket-s3'  # Substitua pelo nome do seu bucket

    # 1. Listar todas as imagens na pasta local
    imagens = listar_imagens(caminho_pasta)
    
    # Verificar se existem imagens
    if not imagens:
        print("Nenhuma imagem foi encontrada na pasta.")
        return

    # 2. Fazer upload de cada imagem para o Amazon S3
    for imagem in imagens:
        nome_imagem_s3 = os.path.basename(imagem)  # Nome do arquivo para o S3
        sucesso = fazer_upload_s3(imagem, bucket_name, nome_imagem_s3)

        if sucesso:
            print(f"Imagem {nome_imagem_s3} enviada com sucesso.")
        else:
            print(f"Falha no upload da imagem {nome_imagem_s3}.")

# Executar o backup das imagens
if __name__ == '__main__':
    backup_imagens_para_nuvem()