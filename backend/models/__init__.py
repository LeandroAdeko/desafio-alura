from sqlalchemy import Column, Integer, Float, Boolean, String, Date, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from db.database import Base

class BaseClass:
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != '_sa_instance_state'}

class Album(Base):
    __tablename__ = "albuns"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    lancamento = Column(Date, nullable=False)
    artista_id = Column(Integer, ForeignKey("artistas.id"))

    artista = relationship("Artista", back_populates="albuns")
    comentarios = relationship("Comentario", back_populates="album")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != '_sa_instance_state'}

class Artista(Base):
    __tablename__ = "artistas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)

    albuns = relationship("Album", back_populates="artista")
    clipes = relationship("Clipe", back_populates="artista")
    shows = relationship("Show", back_populates="artista")
    comentarios = relationship("Comentario", back_populates="artista")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != '_sa_instance_state'}

class AvaliacaoModelo(Base):
    __tablename__ = "avaliacoes_modelo"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, default=datetime.now)
    recall_spam = Column(Float)
    f1_macro = Column(Float)
    acuracia_total = Column(Float)
    passou_threshold = Column(Boolean)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != '_sa_instance_state'}

class Clipe(Base):
    __tablename__ = "clipes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    artista_id = Column(Integer, ForeignKey("artistas.id"))

    artista = relationship("Artista", back_populates="clipes")
    comentarios = relationship("Comentario", back_populates="clipe")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != '_sa_instance_state'}

class ComentarioTag(Base):
    __tablename__ = "comentario_tags"

    comentario_id = Column(UUID(as_uuid=True), ForeignKey("comentarios.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    comentario = relationship("Comentario", back_populates="comentario_tags")
    tag = relationship("Tag", back_populates="comentario_tags")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != '_sa_instance_state'}

class CategoriaComentario(enum.Enum):
    ELOGIO = "ELOGIO"
    CRITICA = "CRITICA"
    SUGESTAO = "SUGESTAO"
    DUVIDA = "DUVIDA"
    SPAM = "SPAM"


class Comentario(Base):
    __tablename__ = "comentarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    texto = Column(String, nullable=False)
    categoria = Column(Enum(CategoriaComentario), nullable=False)
    confianca = Column(Float)
    origem = Column(String)
    criado_em = Column(DateTime, default=datetime.now)
    artista_id = Column(Integer, ForeignKey("artistas.id"))
    album_id = Column(Integer, ForeignKey("albuns.id"))
    clipe_id = Column(Integer, ForeignKey("clipes.id"))
    show_id = Column(Integer, ForeignKey("shows.id"))

    artista = relationship("Artista", back_populates="comentarios")
    album = relationship("Album", back_populates="comentarios")
    clipe = relationship("Clipe", back_populates="comentarios")
    show = relationship("Show", back_populates="comentarios")
    comentario_tags = relationship("ComentarioTag", back_populates="comentario")

    def to_dict(self):
        res = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != '_sa_instance_state'}
        res['categoria'] = res['categoria'].name
        return res
    
class ResumoSemanal(Base):
    __tablename__ = "resumos_semanais"

    id = Column(Integer, primary_key=True, index=True)
    semana_ref = Column(Date, nullable=False)
    texto_resumo = Column(String, nullable=False)
    enviado_em = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != '_sa_instance_state'}

class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    local = Column(String, nullable=False)
    data = Column(Date, nullable=False)
    artista_id = Column(Integer, ForeignKey("artistas.id"))

    artista = relationship("Artista", back_populates="shows")
    comentarios = relationship("Comentario", back_populates="show")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != '_sa_instance_state'}

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    descricao = Column(String)

    comentario_tags = relationship("ComentarioTag", back_populates="tag")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != '_sa_instance_state'}

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != '_sa_instance_state'}