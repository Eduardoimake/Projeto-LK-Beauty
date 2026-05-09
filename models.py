from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from sqlalchemy import String
from sqlalchemy import ForeignKey
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(unique=True)
    instagram: Mapped[str | None] = mapped_column(String(100))
    agendamentos: Mapped[List["Agendamento"]] = relationship(back_populates="cliente")

    def __repr__(self) -> str:
        return f"Cliente(id={self.id!r}, nome={self.nome!r})"

class Servico(Base):
    __tablename__ = "servicos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    duracao_min: Mapped[int] = mapped_column()
    preco: Mapped[float] = mapped_column()
    agendamentos: Mapped[List["Agendamento"]] = relationship(back_populates="servico")

    def __repr__(self) -> str:
        return f"Servico(id={self.id!r}, nome={self.nome!r}), duracao_min={self.duracao_min!r}, preco={self.preco!r})"

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))
    servico_id: Mapped[int] = mapped_column(ForeignKey("servicos.id"))
    data_hora: Mapped[datetime] = mapped_column()
    status: Mapped[str] = mapped_column(String(20))
    cliente: Mapped["Cliente"] = relationship(back_populates="agendamentos")
    servico: Mapped["Servico"] = relationship(back_populates="agendamentos")
    
    def __repr__(self) -> str:
        return f"Agendamento(id={self.id!r}, cliente_id={self.cliente_id!r}, servico_id={self.servico_id!r}, data_hora={self.data_hora!r}, status={self.status!r})"