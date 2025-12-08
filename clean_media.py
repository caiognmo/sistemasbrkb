
import os
import glob

source_base_path = os.path.join(os.getcwd(), 'Base Definitiva')
dest_path = os.path.join(os.getcwd(), 'media')
image_extensions = ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'bmp']

deleted_count = 0

print(f"Limpando imagens da pasta {dest_path}...")

for ext in image_extensions:
    search_pattern = os.path.join(source_base_path, '**', f'*.{ext}')
    for file_path in glob.glob(search_pattern, recursive=True):
        file_name = os.path.basename(file_path)
        media_file_path = os.path.join(dest_path, file_name)
        if os.path.exists(media_file_path):
            try:
                os.remove(media_file_path)
                deleted_count += 1
            except Exception as e:
                print(f"  - Erro ao deletar {media_file_path}: {e}")

print(f"\nLimpeza finalizada. {deleted_count} imagens de backup removidas da pasta /media/.")
