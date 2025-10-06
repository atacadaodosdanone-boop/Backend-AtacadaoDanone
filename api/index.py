import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import app as application

# O Vercel espera uma variável 'application' ou 'app' para o WSGI
# Já renomeamos para 'application' no import acima

