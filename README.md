# Monitora
Estudo Python/Django


# instalaçãos necessarias
- Python v3.10.5 + Django v.4.0.6.

# Libs
-django4-background-tasks


# Configuração E-mail
-Necessario adicionar informações de e-mail para que possa ocorrer o envio.

- Em settings.py, altere <br />
-- EMAIL_HOST_USER = 'Seu-email' <br />
-- EMAIL_HOST_PASSWORD = 'Sua-senha' <br />
-- EMAIL_FROM_ADDRESS = 'Seu-email' <br />
-- DEFAULT_FROM_EMAIL = 'Seu-email' <br />

# Aplicação
-Para rodar a validação de ativos, será necessario realizar a execução em um segundo prompt o comando de ``python manage.py process_tasks``
