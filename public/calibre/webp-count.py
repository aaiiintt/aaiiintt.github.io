import os

directory = 'images'
webp_files = [f for f in os.listdir(directory) if f.endswith('.webp')]

filenames = ', '.join(f'"{file}"' for file in webp_files)

with open('URLS.txt', 'w') as file:
    file.write(filenames)