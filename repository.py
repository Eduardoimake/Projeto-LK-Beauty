from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Cliente, Servico, Agendamento
from datetime import datetime


class ClienteRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def criar(
            self, 
            nome: str, 
            telefone: str, 
            email: str | None = None
            ) -> Cliente:
        cliente = Cliente(nome=nome, telefone=telefone, email=email)
        self._session.add(cliente)
        self._session.commit()
        self._session.refresh(cliente)
        return cliente
    
    def buscar_por_id(self, id: int) -> Cliente | None:
        cliente = self._session.get(Cliente, id)
        return cliente
    
    def listar_todos(self) -> list[Cliente]:
        stmt = select(Cliente)
        return self._session.execute(stmt).scalars().all()
    
    def atualizar(self, cliente: Cliente) -> None:
        self._session.commit()

    def deletar(self, cliente: Cliente) -> None:
        self._session.delete(cliente)
        self._session.commit()

class ServicoRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def criar(
            self, 
            nome: str, 
            duracao_min: int, 
            preco: float
            ) -> Servico:
        servico = Servico(nome=nome, duracao_min=duracao_min, preco=preco)
        self._session.add(servico)
        self._session.commit()
        self._session.refresh(servico)
        return servico
    
    def buscar_por_id(self, id: int) -> Servico | None:
        servico = self._session.get(Servico, id)
        return servico
    
    def listar_todos(self) -> list[Servico]:
        stmt = select(Servico)
        return self._session.execute(stmt).scalars().all()
    
    def atualizar(self, servico: Servico) -> None:
        self._session.commit()

    def deletar(self, servico: Servico) -> None:
        self._session.delete(servico)
        self._session.commit()

class AgendamentoRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def criar(
            self, 
            cliente_id: int, 
            servico_id: int, 
            data_hora: datetime,
            status: str
            ) -> Agendamento:
        agendamento = Agendamento(cliente_id=cliente_id, servico_id=servico_id, data_hora=data_hora, status=status)
        self._session.add(agendamento)
        self._session.commit()
        self._session.refresh(agendamento)
        return agendamento
    
    def buscar_por_id(self, id: int) -> Agendamento | None:
        agendamento = self._session.get(Agendamento, id)
        return agendamento
    
    def listar_todos(self) -> list[Agendamento]:
        stmt = select(Agendamento)
        return self._session.execute(stmt).scalars().all()
    
    def atualizar(self, agendamento: Agendamento) -> None:
        self._session.commit()

    def deletar(self, agendamento: Agendamento) -> None:
        self._session.delete(agendamento)
        self._session.commit()