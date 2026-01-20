import pandas as pd
import os




    

class DatabaseManager:
    def __init__(self, csv_path="data/solutions.csv"):
        self.csv_path = csv_path
        self.df = None
        self.load_database()

    def load_database(self):
        """Charge le CSV de manière robuste."""
        if os.path.exists(self.csv_path):
            try:
                # Tentative 1 : Virgule (Standard)
                self.df = pd.read_csv(self.csv_path, sep=',', on_bad_lines='skip')
                
                # Si Pandas n'a trouvé qu'une seule colonne, c'est probablement un point-virgule
                if self.df.shape[1] <= 1:
                    self.df = pd.read_csv(self.csv_path, sep=';', on_bad_lines='skip')
                
                self.df = self.df.fillna("Non renseigné")
                print(f"✅ Base chargée : {len(self.df)} solutions (certaines lignes corrompues ont été sautées).")
            except Exception as e:
                print(f"❌ Erreur critique lors de la lecture du CSV : {e}")
        else:
            print(f"❌ Erreur : Le fichier {self.csv_path} est introuvable.")

    def get_solution_context(self, index):
        """Prépare un texte complet pour que Gemini analyse une solution précise."""
        row = self.df.iloc[index]
        # On utilise des doubles guillemets "" pour les clés contenant des apostrophes
        context = f"""
        Solution: {row["Dénomination actuelle"]}
        Résumé: {row["Résumé"]}
        Cas d'usage: {row["Cas d'usage"]}
        Innovation: {row["Type d'innovation"]}
        Sport ciblé: {row["Sport ciblé"]}
        Proposition de valeur: {row["Caractéristiques clés / proposition de valeur"]}
        Modèle économique: {row["Modèle économique"]}
        """
        return context


    def get_unique_categories(self):
        if self.df is not None and 'Catégorisation' in self.df.columns:
            cats = self.df['Catégorisation'].dropna().unique().tolist()
            return sorted([str(c) for c in cats if str(c).strip() != "" and str(c) != "Non renseigné"])
        return []


    def search_by_keyword(self, keyword):
        """Recherche simple par mot-clé dans les colonnes principales."""
        mask = self.df.apply(lambda row: keyword.lower() in str(row).lower(), axis=1)
        return self.df[mask]
