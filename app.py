from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "biblioteca.db"


def conectar_banco():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    return conexao


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/cadastro")
def cadastro():
    conexao = conectar_banco()

    autores = conexao.execute(
        "SELECT * FROM autores ORDER BY nome"
    ).fetchall()

    categorias = conexao.execute(
        "SELECT * FROM categorias ORDER BY nome"
    ).fetchall()

    conexao.close()

    return render_template(
        "cadastro.html",
        autores=autores,
        categorias=categorias
    )


@app.route("/cadastrar", methods=["POST"])
def cadastrar_livro():
    titulo = request.form["titulo"]
    ano_publicacao = request.form["ano_publicacao"]
    id_autor = request.form["id_autor"]
    id_categoria = request.form["id_categoria"]

    conexao = conectar_banco()

    conexao.execute(
        """
        INSERT INTO livros
        (titulo, ano_publicacao, id_autor, id_categoria)
        VALUES (?, ?, ?, ?)
        """,
        (titulo, ano_publicacao, id_autor, id_categoria)
    )

    conexao.commit()
    conexao.close()

    return redirect(url_for("acervo"))


@app.route("/acervo")
def acervo():
    conexao = conectar_banco()

    livros = conexao.execute(
        """
        SELECT
            livros.id,
            livros.titulo,
            livros.ano_publicacao,
            livros.id_autor,
            livros.id_categoria,
            autores.nome AS autor,
            categorias.nome AS categoria
        FROM livros
        JOIN autores
            ON livros.id_autor = autores.id
        JOIN categorias
            ON livros.id_categoria = categorias.id
        ORDER BY livros.titulo
        """
    ).fetchall()

    conexao.close()

    return render_template("acervo.html", livros=livros)


@app.route("/editar/<int:id>")
def editar_livro(id):
    conexao = conectar_banco()

    livro = conexao.execute(
        "SELECT * FROM livros WHERE id = ?",
        (id,)
    ).fetchone()

    autores = conexao.execute(
        "SELECT * FROM autores ORDER BY nome"
    ).fetchall()

    categorias = conexao.execute(
        "SELECT * FROM categorias ORDER BY nome"
    ).fetchall()

    conexao.close()

    return render_template(
        "editar.html",
        livro=livro,
        autores=autores,
        categorias=categorias
    )


@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar_livro(id):
    titulo = request.form["titulo"]
    ano_publicacao = request.form["ano_publicacao"]
    id_autor = request.form["id_autor"]
    id_categoria = request.form["id_categoria"]

    conexao = conectar_banco()

    conexao.execute(
        """
        UPDATE livros
        SET titulo = ?,
            ano_publicacao = ?,
            id_autor = ?,
            id_categoria = ?
        WHERE id = ?
        """,
        (
            titulo,
            ano_publicacao,
            id_autor,
            id_categoria,
            id
        )
    )

    conexao.commit()
    conexao.close()

    return redirect(url_for("acervo"))


@app.route("/excluir/<int:id>")
def excluir_livro(id):
    conexao = conectar_banco()

    conexao.execute(
        "DELETE FROM livros WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect(url_for("acervo"))


if __name__ == "__main__":
    app.run(debug=True)
