import streamlit as st
from utils.file_manager import FileManager

st.set_page_config(
    page_title="Gestionnaire de fichiers",
    page_icon="📁",
    layout="wide"
)

def main():
    st.title("📁 Gestionnaire de fichiers")
    st.write("Uploadez et gérez vos fichiers en toute simplicité !")
    
    # Initialisation du gestionnaire de fichiers
    file_manager = FileManager()
    
    # Interface d'upload
    with st.container():
        st.subheader("Upload de fichier")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choisissez un fichier à uploader",
                type=None,
                help="Sélectionnez le fichier que vous souhaitez uploader"
            )
            
        with col2:
            # Sélection du répertoire de destination
            structure = file_manager.get_file_structure()
            directories = [''] + [d for d in structure.keys() if d]
            destination = st.selectbox(
                "Répertoire de destination",
                directories,
                format_func=lambda x: "Racine" if x == '' else x
            )
        
        if uploaded_file:
            st.info(f"Fichier sélectionné : {uploaded_file.name}")
            st.write(f"Taille : {uploaded_file.size} bytes")
            
            if st.button("📤 Uploader", type="primary"):
                with st.spinner("Upload en cours..."):
                    saved_path = file_manager.save_file(uploaded_file, destination)
                    if saved_path:
                        st.success("✅ Fichier uploadé avec succès!")
                        st.write(f"Sauvegardé sous : {saved_path}")
                    else:
                        st.error("❌ Erreur lors de l'upload du fichier")

if __name__ == "__main__":
    main()
