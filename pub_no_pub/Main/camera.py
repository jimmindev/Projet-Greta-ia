import requests
from requests.auth import HTTPDigestAuth
import time

def capture_images(ip_address, username, password, num_images=10, interval=2):
    # URL de l'API pour capturer une image sur une caméra FOSCAM
    capture_url = f"http://{ip_address}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={username}&pwd={password}"

    for i in range(num_images):
        try:
            # Effectuer la requête pour capturer l'image
            response = requests.get(capture_url, stream=True, timeout=5)

            # Vérifier si la requête a réussi
            if response.status_code == 200:
                # Enregistrement de l'image dans un fichier (vous pouvez personnaliser le nom du fichier si nécessaire)
                with open(f"image_{i + 1}.jpg", 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)

                print(f"Image {i + 1} capturée avec succès.")
            else:
                print(f"Échec de la capture de l'image {i + 1}. Code d'état : {response.status_code}")

            # Attendre le temps spécifié entre chaque capture
            time.sleep(interval)

        except requests.RequestException as e:
            print(f"Erreur lors de la capture de l'image {i + 1}: {e}")

if __name__ == "__main__":
    # Informations de la caméra
    camera_ip = "192.168.20.37:88"
    camera_username = "dev_IA_P3"
    camera_password = "dev_IA_P3"

    # Nombre d'images à capturer
    images_to_capture = 2

    # Interval entre chaque capture (en secondes)
    capture_interval = 2

    # Appel de la fonction pour capturer les images
    capture_images(camera_ip, camera_username, camera_password, images_to_capture, capture_interval)
