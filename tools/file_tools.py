import base64
import os
import requests


def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Помилка під час завантаження зображення: {e}")
    except Exception as e:
        print(f"Помилка: {e}")
        
        
def save_image(content, save_path):
    if content is None:
        print(f"Немає даних для збереження")
        return
    if os.path.exists(save_path):
        print(f"Файл '{save_path}' вже існує.")
        return
    with open(save_path, 'wb') as image_file:
        image_file.write(content)
        print(f"Файл '{save_path}' збережено.")
        

def get_base64_image(content):
    return base64.b64encode(content).decode('utf-8') if content else None
    
