import os
from datetime import datetime
import pathlib
from typing import Union, List, Dict
import shutil
import base64

class FileManager:
    """
    Classe gérant les opérations sur les fichiers et répertoires
    """
    def __init__(self, base_path: str = "uploads"):
        """
        Initialise le gestionnaire de fichiers
        
        Args:
            base_path (str): Chemin de base pour les fichiers
        """
        self.base_path = base_path
        self._create_base_directory()
        
    def _create_base_directory(self) -> None:
        """Crée le répertoire de base s'il n'existe pas"""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
            
    def save_file(self, uploaded_file, directory: str = "") -> Union[str, None]:
        """
        Sauvegarde un fichier uploadé dans le répertoire spécifié
        
        Args:
            uploaded_file: Fichier uploadé via st.file_uploader
            directory (str): Sous-répertoire où sauvegarder le fichier
            
        Returns:
            str: Chemin du fichier sauvegardé ou None si erreur
        """
        if uploaded_file is None:
            return None
            
        # Création du chemin complet
        save_dir = os.path.join(self.base_path, directory)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        # Création d'un nom de fichier unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        secure_filename = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(save_dir, secure_filename)
        
        try:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return file_path
        except Exception as e:
            return None
            
    def get_file_structure(self) -> Dict:
        """
        Retourne la structure complète des fichiers et répertoires
        
        Returns:
            Dict: Structure des fichiers et répertoires
        """
        structure = {}
        
        for root, dirs, files in os.walk(self.base_path):
            # Chemin relatif par rapport au répertoire de base
            relative_path = os.path.relpath(root, self.base_path)
            if relative_path == '.':
                relative_path = ''
                
            # Ajout des informations des fichiers
            path_info = {
                'files': [
                    {
                        'name': f,
                        'size': os.path.getsize(os.path.join(root, f)),
                        'modified': datetime.fromtimestamp(
                            os.path.getmtime(os.path.join(root, f))
                        ).strftime('%Y-%m-%d %H:%M:%S')
                    } for f in files
                ],
                'directories': dirs
            }
            structure[relative_path] = path_info
            
        return structure
        
    def create_directory(self, directory_name: str) -> bool:
        """
        Crée un nouveau répertoire
        
        Args:
            directory_name (str): Nom du répertoire à créer
            
        Returns:
            bool: True si création réussie, False sinon
        """
        try:
            path = os.path.join(self.base_path, directory_name)
            if not os.path.exists(path):
                os.makedirs(path)
                return True
            return False
        except Exception:
            return False
            
    def move_file(self, file_path: str, destination: str) -> bool:
        """
        Déplace un fichier vers un nouveau répertoire
        
        Args:
            file_path (str): Chemin relatif du fichier
            destination (str): Chemin relatif du répertoire de destination
            
        Returns:
            bool: True si déplacement réussi, False sinon
        """
        try:
            src = os.path.join(self.base_path, file_path)
            dst = os.path.join(self.base_path, destination)
            
            if not os.path.exists(dst):
                os.makedirs(dst)
                
            shutil.move(src, os.path.join(dst, os.path.basename(file_path)))
            return True
        except Exception:
            return False
            
    def delete_item(self, path: str) -> bool:
        """
        Supprime un fichier ou un répertoire
        
        Args:
            path (str): Chemin relatif de l'élément à supprimer
            
        Returns:
            bool: True si suppression réussie, False sinon
        """
        try:
            full_path = os.path.join(self.base_path, path)
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
            return True
        except Exception:
            return False
            
    def get_file_download_link(self, file_path: str) -> Union[str, None]:
        """
        Génère un lien de téléchargement pour un fichier
        
        Args:
            file_path (str): Chemin relatif du fichier
            
        Returns:
            str: Données encodées en base64 du fichier ou None si erreur
        """
        try:
            full_path = os.path.join(self.base_path, file_path)
            with open(full_path, 'rb') as f:
                bytes_data = f.read()
            b64 = base64.b64encode(bytes_data).decode()
            return b64
        except Exception:
            return None
