from repository import AgendamentoRepository, ClienteRepository, ServicoRepository
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base
from datetime import datetime

@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session

def test_criar_agendamento(session):
    cliente_repo = ClienteRepository(session)
    servico_repo = ServicoRepository(session)
    agendamento_repo = AgendamentoRepository(session)
    cliente = cliente_repo.criar("Ana", "21999999999")
    servico = servico_repo.criar("Maquiagem", 80, 150.0)

    agendamento = agendamento_repo.criar(
        cliente_id=cliente.id,
        servico_id=servico.id,
        data_hora=datetime(2025, 6, 15, 10, 0),
        status="agendado"
    )
    assert agendamento.id is not None
    assert agendamento.cliente_id == cliente.id

def test_buscar_por_id(session):
    cliente_repo = ClienteRepository(session)
    servico_repo = ServicoRepository(session)
    agendamento_repo = AgendamentoRepository(session)
    cliente = cliente_repo.criar("Ana", "21999999999")
    servico = servico_repo.criar("Maquiagem", 80, 150.0)

    agendamento_criado = agendamento_repo.criar(
        cliente_id=cliente.id,
        servico_id=servico.id,
        data_hora=datetime(2025, 6, 15, 10, 0),
        status="agendado"
    )
    agendamento = agendamento_repo.buscar_por_id(agendamento_criado.id)
    assert agendamento.id == agendamento_criado.id

def test_listar_todos(session):
    cliente_repo = ClienteRepository(session)
    servico_repo = ServicoRepository(session)
    agendamento_repo = AgendamentoRepository(session)
    cliente = cliente_repo.criar("Ana", "21999999999")
    servico = servico_repo.criar("Maquiagem", 80, 150.0)
    
    agendamento_repo.criar(
        cliente_id=cliente.id,
        servico_id=servico.id,
        data_hora=datetime(2025, 6, 15, 10, 0),
        status="agendado"
    )
    resultado = agendamento_repo.listar_todos()
    assert len(resultado) == 1

def test_atualizar(session):
    cliente_repo = ClienteRepository(session)
    servico_repo = ServicoRepository(session)
    agendamento_repo = AgendamentoRepository(session)
    cliente = cliente_repo.criar("Ana", "21999999999")
    servico = servico_repo.criar("Maquiagem", 80, 150.0)

    agendamento = agendamento_repo.criar(
        cliente_id=cliente.id,
        servico_id=servico.id,
        data_hora=datetime(2025, 6, 15, 10, 0),
        status="agendado"
    )
    agendamento.status = "cancelado"
    agendamento_repo.atualizar(agendamento)
    assert agendamento.status == "cancelado"

def test_deletar(session):
    cliente_repo = ClienteRepository(session)
    servico_repo = ServicoRepository(session)
    agendamento_repo = AgendamentoRepository(session)
    cliente = cliente_repo.criar("Ana", "21999999999")
    servico = servico_repo.criar("Maquiagem", 80, 150.0)
    
    agendamento = agendamento_repo.criar(
        cliente_id=cliente.id,
        servico_id=servico.id,
        data_hora=datetime(2025, 6, 15, 10, 0),
        status="agendado"
    )
    agendamento_repo.deletar(agendamento)
    resultado = agendamento_repo.listar_todos()
    assert len(resultado) == 0

def test_buscar_agendamento_inexistente(session):
    agendamento_repo = AgendamentoRepository(session)
    resultado = agendamento_repo.buscar_por_id(999)
    assert resultado is None