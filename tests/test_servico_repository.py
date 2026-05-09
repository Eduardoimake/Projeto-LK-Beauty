from repository import ServicoRepository
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

def test_criar_servico(session):
    repo = ServicoRepository(session)
    servico = repo.criar("Maquiagem", 80, 150.0)
    assert servico.id is not None
    assert servico.nome == "Maquiagem"

def test_buscar_por_id(session):
    repo = ServicoRepository(session)
    servico_criado = repo.criar("Maquiagem", 80, 150.0)
    servico = repo.buscar_por_id(servico_criado.id)
    assert servico.id == servico_criado.id

def test_listar_todos(session):
    repo = ServicoRepository(session)
    repo.criar("Maquiagem", 80, 150.0)
    repo.criar("penteado", 60, 80.0)
    resultado = repo.listar_todos()
    assert len(resultado) == 2

def test_atualizar(session):
    repo = ServicoRepository(session)
    servico = repo.criar("Maquiagem", 80, 150.0)
    servico.nome = "penteado"
    repo.atualizar(servico)
    assert servico.nome == "penteado"

def test_deletar(session):
    repo = ServicoRepository(session)
    servico_criado = repo.criar("Maquiagem", 80, 150.0)
    repo.deletar(servico_criado)
    resultado = repo.listar_todos()
    assert len(resultado) == 0

def test_buscar_cliente_inexistente(session):
    repo = ServicoRepository(session)
    resultado = repo.buscar_por_id(999)
    assert resultado is None