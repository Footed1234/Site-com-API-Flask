from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Filme(Base):
    __tablename__ = 'Filmes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    anoLancamento = Column(Integer, nullable=False)
    autor = Column(String(100), nullable=False)
    genero = Column(String(100), nullable=False)
    bilheteria = Column(Integer, nullable=False)
    imagem = Column(String(300), nullable=True)

class Lancamento(Base):
    __tablename__ = 'Lancamentos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idFilme = Column(Integer, ForeignKey('Filmes.id'))

class Usuarios(Base):
    __tablename__ = "Usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    senha = Column(String(100), nullable=False)


class Avaliacao(Base):
    __tablename__ = 'Avaliacoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    idUsuario = Column(Integer, ForeignKey('Usuarios.id'), nullable=False)
    idFilme = Column(Integer, ForeignKey('Filmes.id'), nullable=False)
    nota = Column(Integer, nullable=False)  # Nota de 0 a 10
    data_avaliacao = Column(DateTime, default=datetime.now)

    # Relacionamentos (opcional, mas útil para queries)
    usuario = relationship("Usuarios", backref="avaliacoes")
    filme = relationship("Filme", backref="avaliacoes")