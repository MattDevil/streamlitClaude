import streamlit as st
import os
from datetime import datetime
import pathlib
from typing import Union
import shutil

class FileUploader:
    """
    Classe gérant l'upload de fichiers via Streamlit
    """
    def __init__(self, upload_path: str = "uploads"):
        """
        Initialise le gestionnaire d'upload de fichiers
        
        Args:
            upload_path (str): Chemin où les fichiers seront sauvegardés
        """
        self.upload_path = upload_path
        self._create_upload_directory()
        
    def _create_upload_directory(self) -> None:
        """Crée le dossier d'upload s'il n'existe pas"""
        if not os.path.exists(self.upload_path):
            os.makedirs(self.upload_path)
            
    def save_file(self, uploaded_file) -> Union[str, None]:
        """
        Sauvegarde le fichier uploadé avec un horodatage
        
        Args:
            uploaded_file: Fichier uploadé via st.file_uploader
            
        Returns:
            str: Chemin du fichier sauvegardé ou None si erreur
        """
        if uploaded_file is None:
            return None
        
        # Création d'un nom de fichier unique avec horodatage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = pathlib.Path(uploaded_file.name).suffix
        secure_filename = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(self.upload_path, secure_filename)
        
        try:
            # Sauvegarde du fichier
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return file_path
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde du fichier: {str(e)}")
            return None
    
    def get_uploaded_files(self) -> list:
        """
        Retourne la liste des fichiers déjà uploadés
        
        Returns:
            list: Liste des fichiers dans le dossier d'upload
        """
        if not os.path.exists(self.upload_path):
            return []
        return os.listdir(self.upload_path)
    
    def delete_file(self, filename: str) -> bool:
        """
        Supprime un fichier du dossier d'upload
        
        Args:
            filename (str): Nom du fichier à supprimer
            
        Returns:
            bool: True si suppression réussie, False sinon
        """
        file_path = os.path.join(self.upload_path, filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

def main():
    st.title("📁 Gestionnaire de fichiers")
    st.write("Uploadez vos fichiers en toute simplicité !")
    
    # Initialisation du gestionnaire de fichiers
    uploader = FileUploader()
    
    # Interface d'upload
    with st.container():
        st.subheader("Upload de fichier")
        uploaded_file = st.file_uploader(
            "Choisissez un fichier à uploader",
            type=None,  # Accepte tous les types de fichiers
            help="Sélectionnez le fichier que vous souhaitez uploader"
        )
        
        if uploaded_file:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"Fichier sélectionné : {uploaded_file.name}")
                st.write(f"Taille : {uploaded_file.size} bytes")
            
            with col2:
                if st.button("📤 Uploader", type="primary"):
                    with st.spinner("Upload en cours..."):
                        saved_path = uploader.save_file(uploaded_file)
                        if saved_path:
                            st.success("✅ Fichier uploadé avec succès!")
                            st.write(f"Sauvegardé sous : {saved_path}")
    
    # Affichage des fichiers existants
    with st.container():
        st.subheader("Fichiers uploadés")
        files = uploader.get_uploaded_files()
        
        if not files:
            st.info("Aucun fichier uploadé pour le moment.")
        else:
            for file in files:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"📄 {file}")
                with col2:
                    if st.button("🗑️", key=f"delete_{file}"):
                        if uploader.delete_file(file):
                            st.rerun()

if __name__ == "__main__":
    main()
