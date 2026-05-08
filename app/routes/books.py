from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models.book import (
    get_all_books, get_book_by_id, add_book,
    update_book, delete_book, search_books
)

books_bp = Blueprint('books', __name__)

@books_bp.route('/')
def index():
    books = get_all_books()
    stats = {
        'total': len(books),
        'disponible': sum(1 for b in books if b['statut'] == 'disponible'),
        'emprunte': sum(1 for b in books if b['statut'] == 'emprunté'),
        'reserve': sum(1 for b in books if b['statut'] == 'réservé'),
    }
    return render_template('index.html', books=books, stats=stats)

@books_bp.route('/books')
def list_books():
    query = request.args.get('q', '')
    if query:
        books = search_books(query)
    else:
        books = get_all_books()
    return render_template('books/list.html', books=books, query=query)

@books_bp.route('/books/add', methods=['GET', 'POST'])
def add_book_route():
    if request.method == 'POST':
        titre = request.form['titre'].strip()
        auteur = request.form['auteur'].strip()
        categorie = request.form['categorie'].strip()
        annee = request.form.get('annee_publication', '')
        quantite = request.form.get('quantite_disponible', 1)
        statut = request.form.get('statut', 'disponible')
        date_retour = request.form.get('date_retour', '').strip() or None

        if not titre or not auteur or not categorie:
            flash('Veuillez remplir tous les champs obligatoires.', 'error')
            return render_template('books/form.html', book=request.form, action='add')

        try:
            annee = int(annee) if annee else None
            quantite = int(quantite)
        except ValueError:
            flash('Année et quantité doivent être des nombres valides.', 'error')
            return render_template('books/form.html', book=request.form, action='add')

        add_book(titre, auteur, categorie, annee, quantite, statut, date_retour)
        flash(f'✅ Le livre "{titre}" a été ajouté avec succès!', 'success')
        return redirect(url_for('books.list_books'))

    return render_template('books/form.html', book=None, action='add')

@books_bp.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
def edit_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        flash('Livre introuvable.', 'error')
        return redirect(url_for('books.list_books'))

    if request.method == 'POST':
        titre = request.form['titre'].strip()
        auteur = request.form['auteur'].strip()
        categorie = request.form['categorie'].strip()
        annee = request.form.get('annee_publication', '')
        quantite = request.form.get('quantite_disponible', 1)
        statut = request.form.get('statut', 'disponible')
        date_retour = request.form.get('date_retour', '').strip() or None

        try:
            annee = int(annee) if annee else None
            quantite = int(quantite)
        except ValueError:
            flash('Année et quantité doivent être des nombres valides.', 'error')
            return render_template('books/form.html', book=book, action='edit')

        update_book(book_id, titre, auteur, categorie, annee, quantite, statut, date_retour)
        flash(f'✅ Le livre "{titre}" a été modifié avec succès!', 'success')
        return redirect(url_for('books.list_books'))

    return render_template('books/form.html', book=book, action='edit')

@books_bp.route('/books/<int:book_id>/delete', methods=['POST'])
def delete_book_route(book_id):
    book = get_book_by_id(book_id)
    if book:
        delete_book(book_id)
        flash(f'🗑️ Le livre "{book["titre"]}" a été supprimé.', 'success')
    return redirect(url_for('books.list_books'))

@books_bp.route('/books/<int:book_id>')
def view_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        flash('Livre introuvable.', 'error')
        return redirect(url_for('books.list_books'))
    return render_template('books/detail.html', book=book)

@books_bp.route('/api/books')
def api_books():
    books = get_all_books()
    return jsonify(books)
