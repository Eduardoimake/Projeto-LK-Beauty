from repository import ClienteRepository
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base

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

def test_criar_cliente(session):
    repo = ClienteRepository(session)
    cliente = repo.criar(nome="Ana Lima", telefone="21999990001")
    assert cliente.id is not None
    assert cliente.nome == "Ana Lima"

def test_buscar_por_id(session):
    repo = ClienteRepository(session)
    cliente_criado = repo.criar(nome="Ana Lima", telefone="21999990001")
    cliente = repo.buscar_por_id(cliente_criado.id)
    assert cliente.id == cliente_criado.id

def test_listar_todos(session):
    repo = ClienteRepository(session)
    clientes = [
        repo.criar(nome="Ana Lima", telefone="21999990001"), 
        repo.criar(nome="Julia Maria", telefone="21999990002")
        ]
    resultado = repo.listar_todos()
    assert len(resultado) == 2

def test_atualizar(session):
    repo = ClienteRepository(session)
    cliente = repo.criar(nome="Ana Lima", telefone="21999990001")
    cliente.telefone = "21999990002"
    repo.atualizar(cliente)
    assert cliente.telefone == "21999990002"

def test_deletar(session):
    repo = ClienteRepository(session)
    cliente_criado = repo.criar(nome="Ana Lima", telefone="21999990001")
    repo.deletar(cliente_criado)
    resultado = repo.listar_todos()
    assert len(resultado) == 0

def test_buscar_cliente_inexistente(session):
    repo = ClienteRepository(session)
    resultado = repo.buscar_por_id(999)
    assert resultado is None