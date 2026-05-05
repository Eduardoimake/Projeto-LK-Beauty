from dotenv import load_dotenv
import os

load_dotenv()

STUDIO_NOME = os.environ.get("STUDIO_NOME")
STUDIO_TELEFONE = os.environ.get("STUDIO_TELEFONE")
MODO_DEBUG = os.environ.get("MODO_DEBUG")