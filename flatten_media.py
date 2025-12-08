
import os
import shutil

media_path = os.path.join(os.getcwd(), 'media')

print(f"Movendo arquivos para a raiz de {media_path}...")

moved_count = 0

# Percorre todas as subpastas da pasta media
for root, dirs, files in os.walk(media_path):
    if root == media_path:
        continue # Ignora a própria pasta raiz

    for file in files:
        source_path = os.path.join(root, file)
        dest_path = os.path.join(media_path, file)
        
        # Move o arquivo para a pasta media raiz
        if not os.path.exists(dest_path):
            shutil.move(source_path, dest_path)
            moved_count += 1

print(f"{moved_count} arquivos de imagem movidos para a pasta raiz /media/.")

# Apaga as pastas agora vazias
print("Limpando subpastas vazias...")
for root, dirs, files in os.walk(media_path, topdown=False):
    if root != media_path:
        try:
            os.rmdir(root)
            print(f"  - Removida pasta vazia: {root}")
        except OSError:
            # A pasta não está vazia, o que é inesperado, mas não faremos nada
            pass

print("\n--- Reorganização de Imagens Finalizada ---")
