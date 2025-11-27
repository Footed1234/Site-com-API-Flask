from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Modelo import Filme, Lancamento, Usuarios, Avaliacao
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL") # Pegando a string de conexão

# Setup do Flask
app = Flask(__name__)
CORS(app) # Permite chamadas de fora (como de um HTML/JS)

# Conexão com o banco de dados
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@app.route("/afilmes", methods=["POST"])
def add_filme():
    session = Session()
    try:
        dados = request.get_json()

        print("📥 Dados recebidos:", dados)

        # Validação dos campos obrigatórios
        campos_obrigatorios = ["nome", "anoLancamento", "autor", "genero", "bilheteria"]
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                return jsonify({"erro": f"Campo '{campo}' é obrigatório"}), 400

        # Criar filme (SEM campos de avaliação)
        novo_filme = Filme(
            nome=dados["nome"],
            anoLancamento=int(dados["anoLancamento"]),
            autor=dados["autor"],
            genero=dados["genero"],
            bilheteria=int(dados["bilheteria"]),
            imagem=dados.get("imagem")
        )

        session.add(novo_filme)
        session.commit()
        print("✅ Filme criado com ID:", novo_filme.id)

        # Se for 2024/2025, adicionar em Lançamentos
        ano = int(dados["anoLancamento"])
        if ano in [2024, 2025]:
            novo_lanc = Lancamento(idFilme=novo_filme.id)
            session.add(novo_lanc)
            session.commit()
            print("✅ Também adicionado em Lançamentos")

        return jsonify({"status": "Filme cadastrado", "id": novo_filme.id})

    except Exception as e:
        session.rollback()
        print("❌ Erro ao cadastrar filme:", str(e))
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500
    finally:
        session.close()

@app.route("/afilmes", methods=["GET"])
def listar_filmes():
    session = Session()
    try:
        filmes = session.query(Filme).all()
        resultado = []
        for f in filmes:
            resultado.append({
                "id": f.id,
                "nome": f.nome,
                "anoLancamento": f.anoLancamento,
                "autor": f.autor,
                "genero": f.genero,
                "bilheteria": f.bilheteria,
                "imagem": f.imagem
                # REMOVIDOS: avaliacao_media e total_avaliacoes
            })
        return jsonify(resultado)
    finally:
        session.close()

@app.route("/afilmes/<int:id>", methods=["PUT"])
def atualizar_filme(id):
    session = Session()
    dados = request.json or {}

    filme = session.query(Filme).get(id)
    if not filme:
        session.close()
        return jsonify({"erro": "Filme não encontrado"}), 404

    # Atualizar apenas campos existentes (SEM avaliação)
    filme.nome = dados.get("nome", filme.nome)
    filme.anoLancamento = dados.get("anoLancamento", filme.anoLancamento)
    filme.autor = dados.get("autor", filme.autor)
    filme.genero = dados.get("genero", filme.genero)
    filme.bilheteria = dados.get("bilheteria", filme.bilheteria)
    filme.imagem = dados.get("imagem", filme.imagem)
    # REMOVIDO: filme.avaliacao

    try:
        session.commit()
        return jsonify({"status": "Filme atualizado com sucesso!"})
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

@app.route("/afilmes/<int:id>", methods=["DELETE"])
def deletar_filme(id):
    session = Session()
    filme = session.query(Filme).get(id)

    if not filme:
        session.close()
        return jsonify({"erro": "Filme não encontrado"}), 404

    # Deleta de Lancamentos se o ano for 2024 ou 2025
    if filme.anoLancamento in [2024, 2025]:
        lancamento = session.query(Lancamento).filter_by(
            nome=filme.nome,
            anoLancamento=filme.anoLancamento,
            autor=filme.autor,
            genero=filme.genero
        ).first()
        if lancamento:
            session.delete(lancamento)

    session.delete(filme)
    session.commit()
    session.close()

    return jsonify({"status": "Filme removido com sucesso!"})

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    session = Session()
    usuarios = session.query(Usuarios).all()

    resultado = []
    for u in usuarios:
        resultado.append({
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "idade": u.idade,
            "senha": u.senha
        })
    session.close()
    return jsonify(resultado)


@app.route("/usuarios", methods=["POST"])
def adicionar_usuario():
    session = Session()
    dados = request.json

    novo = Usuarios(
        nome=dados["nome"],
        email=dados["email"],
        idade=dados["idade"],
        senha=dados["senha"]
    )

    session.add(novo)
    session.commit()

    return jsonify({"status":"Usuário cadastrado", "id": novo.id})


@app.route("/usuarios/<int:id>", methods=["PUT"])
def editar_usuario(id):
    session = Session()
    dados = request.json
    usuario = session.query(Usuarios).get(id)

    if usuario is None:
        return jsonify({"erro":"Usuário não encontrado"})

    usuario.nome = dados["nome"]
    usuario.email = dados["email"]
    usuario.idade = dados["idade"]
    usuario.senha = dados["senha"]

    session.commit()
    return jsonify({"status":"Usuário atualizado"})


@app.route("/usuarios/<int:id>", methods=["DELETE"])
def deletar_usuario(id):
    session = Session()
    usuario = session.query(Usuarios).get(id)

    if usuario is None:
        return jsonify({"erro":"Usuário não encontrado"})

    session.delete(usuario)
    session.commit()

    return jsonify({"status":"Usuário deletado"})

@app.route("/lancamentos", methods=["POST"])
def add_lancamento():
    session = Session()
    dados = request.json
    novo = Lancamento(**dados)
    session.add(novo)
    session.commit()
    return jsonify({"status": "Lançamento cadastrado", "id": novo.id})


@app.route("/avaliar", methods=["POST"])
def avaliar_filme():
    session = Session()
    try:
        dados = request.get_json()

        # Verificar se usuário já avaliou este filme
        avaliacao_existente = session.query(Avaliacao).filter_by(
            idUsuario=dados["idUsuario"],
            idFilme=dados["idFilme"]
        ).first()

        if avaliacao_existente:
            # Atualizar avaliação existente
            avaliacao_existente.nota = dados["nota"]
            mensagem = "Avaliação atualizada"
        else:
            # Criar nova avaliação
            nova_avaliacao = Avaliacao(
                idUsuario=dados["idUsuario"],
                idFilme=dados["idFilme"],
                nota=dados["nota"]
            )
            session.add(nova_avaliacao)
            mensagem = "Avaliação registrada"

        session.commit()
        return jsonify({"status": mensagem})

    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()


@app.route("/lancamentos", methods=["GET"])
def get_lancamentos():
    session = Session()

    # Buscar lançamentos com dados do filme via relacionamento
    lancamentos = session.query(Lancamento).join(Filme).all()

    resultado = []
    for lanc in lancamentos:
        filme = lanc.filme
        resultado.append({
            "id": filme.id,
            "nome": filme.nome,
            "anoLancamento": filme.anoLancamento,
            "autor": filme.autor,
            "genero": filme.genero,
            "bilheteria": filme.bilheteria,
            "avaliacao_media": filme.avaliacao_media,
            "total_avaliacoes": filme.total_avaliacoes,
            "imagem": filme.imagem
        })

    session.close()
    return jsonify(resultado)


@app.route("/minha-avaliacao/<int:idUsuario>/<int:idFilme>", methods=["GET"])
def get_minha_avaliacao(idUsuario, idFilme):
    session = Session()
    try:
        # Buscar avaliação específica do usuário para este filme
        avaliacao = session.query(Avaliacao).filter_by(
            idUsuario=idUsuario,
            idFilme=idFilme
        ).first()

        if avaliacao:
            return jsonify({
                "avaliacao": {
                    "id": avaliacao.id,
                    "nota": avaliacao.nota,
                    "data_avaliacao": avaliacao.data_avaliacao.isoformat()
                }
            })
        else:
            return jsonify({"avaliacao": None})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
