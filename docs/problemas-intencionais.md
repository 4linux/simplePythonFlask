# Problemas intencionais

Este documento é para o **instrutor**. A aplicação funciona e seus testes passam, mas o código mantém de propósito os problemas abaixo, para que apareçam na análise do SonarQube e sirvam de exemplo em aula.

Nenhum deles altera o comportamento da aplicação.

> A coluna "O que a análise aponta" é o resultado esperado pelas regras padrão do SonarQube. Rode a análise na versão do SonarQube usada no laboratório e ajuste esta lista com o que de fato aparecer.

## Mantidos de propósito

|Problema|Onde|O que a análise aponta|
|---|---|---|
|`if` aninhados que poderiam ser um só|`project/users/views.py`, funções `login` e `register`|Code smell: "Merge this if statement with the enclosing one". É o exemplo usado na aula de SonarQube|
|Código comentado|`project/__init__.py`, `project/models.py`, `project/users/views.py`|Code smell: "Remove this commented out code"|
|Função duplicada|`login_required` em `project/users/views.py` e `project/courses/views.py`|Duplicação de código|
|`print` de depuração|`project/users/views.py`, função `register`|Code smell de log/depuração em código de produção|
|Imports sem uso|`datetime` em `project/models.py`; `request` em `project/courses/views.py`|Code smell: import não utilizado|
|Chave padrão fixa no código|`SECRET_KEY` e `DB_PASSWORD` em `project/_config.py`|Security hotspot: credencial no código|
|Imagens sem texto alternativo|logo em `project/templates/login.html` e `register.html`|Apontamento de acessibilidade em HTML|
|Trechos sem cobertura de teste|`/ready` e `/logout`|Cobertura abaixo de 100%|

## Sugestão de uso em aula

1. Rodar a análise e mostrar os itens acima no painel do SonarQube.
2. Criar um Quality Gate que reprove pela quantidade de code smells, para ver o pipeline falhar.
3. Corrigir os `if` aninhados ao vivo e ver a contagem cair na análise seguinte:

```python
if request.method == 'POST' and form.validate_on_submit():
```

## O que **não** é intencional

Se algum teste falhar, a imagem não construir ou a aplicação não subir com `docker compose up`, é defeito de verdade e deve ser corrigido.
