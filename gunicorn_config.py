"""Configuração do Gunicorn para produção"""

import os

# Bind para aceitar conexões de qualquer origem
bind = "0.0.0.0:" + str(os.environ.get("PORT", "5000"))

# Número de workers (processos)
workers = 2

# Tipo de worker
worker_class = "sync"

# Timeout
timeout = 120

# Logs
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Configurações de segurança
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

