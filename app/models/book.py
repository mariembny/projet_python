from app.database import get_db

def get_all_books():
    conn = get_db()
    books = conn.execute('SELECT * FROM livres ORDER BY id_livre').fetchall()
    conn.close()
    return [dict(b) for b in books]

def get_book_by_id(book_id):
    conn = get_db()
    book = conn.execute('SELECT * FROM livres WHERE id_livre = ?', (book_id,)).fetchone()
    conn.close()
    return dict(book) if book else None

def search_books(query):
    conn = get_db()
    q = f'%{query}%'
    books = conn.execute(
        'SELECT * FROM livres WHERE titre LIKE ? OR auteur LIKE ? OR CAST(id_livre AS TEXT) = ?',
        (q, q, query)
    ).fetchall()
    conn.close()
    return [dict(b) for b in books]

def add_book(titre, auteur, categorie, annee_publication, quantite_disponible, statut, date_retour=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO livres (titre, auteur, categorie, annee_publication, quantite_disponible, statut, date_retour)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (titre, auteur, categorie, annee_publication, quantite_disponible, statut, date_retour))
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return book_id

def update_book(book_id, titre, auteur, categorie, annee_publication, quantite_disponible, statut, date_retour=None):
    conn = get_db()
    conn.execute('''
        UPDATE livres SET titre=?, auteur=?, categorie=?, annee_publication=?,
        quantite_disponible=?, statut=?, date_retour=?
        WHERE id_livre=?
    ''', (titre, auteur, categorie, annee_publication, quantite_disponible, statut, date_retour, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = get_db()
    conn.execute('DELETE FROM livres WHERE id_livre = ?', (book_id,))
    conn.commit()
    conn.close()

def get_library_context():
    """Returns all books formatted as context for AI chatbot."""
    books = get_all_books()
    if not books:
        return "La bibliothèque est vide."
    
    lines = ["=== CATALOGUE DE LA BIBLIOTHÈQUE ===\n"]
    for b in books:
        date_info = f", retour prévu le {b['date_retour']}" if b['date_retour'] else ""
        lines.append(
            f"ID: {b['id_livre']} | Titre: {b['titre']} | Auteur: {b['auteur']} | "
            f"Catégorie: {b['categorie']} | Année: {b['annee_publication']} | "
            f"Quantité: {b['quantite_disponible']} | Statut: {b['statut']}{date_info}"
        )
    return "\n".join(lines)
