import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bibliotheque.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livres (
            id_livre INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            categorie TEXT NOT NULL,
            annee_publication INTEGER,
            quantite_disponible INTEGER DEFAULT 1,
            statut TEXT DEFAULT 'disponible',
            date_retour TEXT
        )
    ''')
    
    # Insert sample data if table is empty
    cursor.execute('SELECT COUNT(*) FROM livres')
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_books = [
            ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Roman', 1943, 3, 'disponible', None),
            ('Les Misérables', 'Victor Hugo', 'Roman', 1862, 0, 'emprunté', '15/03/2026'),
            ('Notre-Dame de Paris', 'Victor Hugo', 'Roman', 1831, 2, 'disponible', None),
            ('Les Contemplations', 'Victor Hugo', 'Poésie', 1856, 1, 'disponible', None),
            ('Orgueil et Préjugés', 'Jane Austen', 'Roman', 1813, 2, 'disponible', None),
            ('Jane Eyre', 'Charlotte Brontë', 'Roman', 1847, 1, 'disponible', None),
            ('Le Rouge et le Noir', 'Stendhal', 'Roman', 1830, 0, 'emprunté', '20/04/2026'),
            ('L\'Étranger', 'Albert Camus', 'Roman', 1942, 2, 'disponible', None),
            ('Madame Bovary', 'Gustave Flaubert', 'Roman', 1857, 1, 'disponible', None),
            ('Germinal', 'Émile Zola', 'Roman', 1885, 3, 'disponible', None),
            ('Le Comte de Monte-Cristo', 'Alexandre Dumas', 'Roman', 1844, 2, 'disponible', None),
            ('Vingt mille lieues sous les mers', 'Jules Verne', 'Science-Fiction', 1870, 1, 'réservé', None),
            ('Le Tour du monde en 80 jours', 'Jules Verne', 'Aventure', 1872, 2, 'disponible', None),
            ('Voyage au centre de la Terre', 'Jules Verne', 'Science-Fiction', 1864, 1, 'disponible', None),
            ('Harry Potter à l\'école des sorciers', 'J.K. Rowling', 'Fantasy', 1997, 4, 'disponible', None),
            ('Introduction à l\'algorithmique', 'Thomas Cormen', 'Informatique', 2009, 2, 'disponible', None),
            ('Python pour les nuls', 'Mark Lutz', 'Informatique', 2013, 3, 'disponible', None),
            ('Sapiens', 'Yuval Noah Harari', 'Histoire', 2011, 2, 'disponible', None),
            ('Une brève histoire du temps', 'Stephen Hawking', 'Science', 1988, 1, 'emprunté', '10/04/2026'),
            ('Les Fleurs du mal', 'Charles Baudelaire', 'Poésie', 1857, 2, 'disponible', None),
        ]
        cursor.executemany('''
            INSERT INTO livres (titre, auteur, categorie, annee_publication, quantite_disponible, statut, date_retour)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_books)
    
    conn.commit()
    conn.close()
