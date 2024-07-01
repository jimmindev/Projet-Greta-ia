import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def download_images(search_terms, num_pages=3):
    for search_term in search_terms:
        output_folder = 'image_folder_no_logo'
        os.makedirs(output_folder, exist_ok=True)

        for page in range(1, num_pages + 1):
            start_index = (page - 1) * 100  # 100 images per page on Google Images
            url = rf'https://www.google.fr/search?sca_esv=601398990&hl=fr&sxsrf=ACQVn0-9hdMGVh-PZ6CVtN4ZY-zDT9oWPQ:1706189726510&q={search_term}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwiSscWE1PiDAxWqQ6QEHcMWC90Q0pQJegQIEhAB&biw=1920&bih=919&dpr=1&start={start_index}'

            page_content = requests.get(url).text
            soup = BeautifulSoup(page_content, 'html.parser')

            thumbnails = []

            for raw_img in soup.find_all('img'):
                link = raw_img.get('src')
                if link and link.startswith("https://"):
                    thumbnails.append(link)

            existing_images = [file for file in os.listdir(output_folder) if file.endswith('.png')]
            latest_index = max([int(file.split('_')[1].split('.')[0]) for file in existing_images], default=-1) + 1

            for i, thumbnail in enumerate(thumbnails):
                img_url = urljoin(url, thumbnail)
                img_data = requests.get(img_url).content
                nom = search_term.split()[-1]
                img_path = os.path.join(output_folder, f'image_{latest_index + i}_{nom}_page{page}.png')

                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)

            print(f"{len(thumbnails)} images appended in the '{output_folder}' folder for search term: '{search_term}' from page {page} with .png extension.")

search_terms = ['photo cosplay', 'photographie nature', 'photographie ville', 'photographie dehors',
    'photo portrait',
    'photographie coucher de soleil',
    'photographie architecture',
    'photographie de voyage',
    'photographie macro',
    'photo animaux sauvages',
    'photo noir et blanc',
    'photographie urbaine',
    'photo art abstrait',
    'photo montagne',
    'photo plage',
    'photographie aérienne',
    'photographie de nuit',
    'photo macro flore',
    'photo mode',
    'photographie street art',
    'photo sportive',
    'photographie sous-marine',
    'photo en noir et blanc',
    'photographie vintage'
]
download_images(search_terms, num_pages=3)