# Problemas intencionais

Este documento é para o **instrutor**. A aplicação funciona e seus testes passam, mas o código mantém de propósito os problemas abaixo, para que apareçam na análise do SonarQube e sirvam de exemplo em aula.

Nenhum deles altera o comportamento da aplicação.

> Resultado conferido em 06/10/2026 com o **SonarQube Community Build 26.9**, perfil **Sonar way**, analisando `project` como código e `tests` como testes. Os números podem mudar em outras versões.

## Resultado da análise

|Medida|Valor|
|---|---|
|Quality Gate (Sonar way)|Passed|
|Security|3 issues, nota D|
|Reliability|2 issues, nota B|
|Maintainability|13 issues, nota A|
|Cobertura|89,1%|
|Testes unitários|8|
|Duplicação|0%|

A interface do SonarQube agrupa os 18 apontamentos por qualidade de software, como na tabela acima. Pela classificação antiga, ainda disponível na API, eles são 15 code smells e 3 vulnerabilidades.

## O que o SonarQube aponta

|Problema|Onde|Apontamento|
|---|---|---|
|`if` aninhados que poderiam ser um só|`project/users/views.py`, linhas 36 e 68 (funções `login` e `register`)|Code smell: "Merge this if statement with the enclosing one". É o exemplo usado na aula|
|Código comentado|`project/__init__.py`, `project/models.py`, `project/users/views.py` (4 ocorrências) e `project/templates/login.html` (2 ocorrências)|Code smell: "Remove this commented out code"|
|Texto repetido|`project/users/views.py`, linha 26|Code smell: "Define a constant instead of duplicating this literal 'users.login' 3 times"|
|Imagens sem texto alternativo|`project/templates/login.html` e `register.html`|Code smell: "Provide alternative text for this element"|
|Seletor CSS duplicado|`project/static/css/main.css`, linha 137|Code smell: "Duplicate selector"|
|Método de teste que não é teste|`tests/unit/test_users.py`, linha 28 (`logout`)|Code smell: "Rename this method so that it starts with test"|
|Senha padrão no código|`project/_config.py`, linha 12|Vulnerabilidade: credencial potencialmente fixa no código|
|CSRF desabilitável|`project/__init__.py`, linha 13|Vulnerabilidade: "Make sure disabling CSRF protection is safe here"|
|Recurso externo sem verificação de integridade|`project/templates/_base.html`, linha 7|Vulnerabilidade: falta `integrity` em um recurso de CDN|
|Trechos sem cobertura de teste|`/ready` e `/logout`|Cobertura abaixo de 100%|

## Mantidos de propósito, mas não apontados

Estes problemas existem no código, mas o perfil **Sonar way** não os aponta:

|Problema|Onde|
|---|---|
|Função duplicada|`login_required` em `project/users/views.py` e `project/courses/views.py`. O trecho é curto demais para a detecção de duplicação|
|`print` de depuração|`project/users/views.py`, função `register`|
|Imports sem uso|`datetime` em `project/models.py`; `request` em `project/courses/views.py`|

Servem para discutir em aula que uma ferramenta de análise não encontra tudo, e que as regras ativas dependem do Quality Profile.

## Sugestão de uso em aula

1. Rodar a análise e mostrar os itens acima no painel do SonarQube.
2. Criar um Quality Gate que reprove com mais de 10 code smells em todo o código (o projeto tem 15), para ver a análise e depois o pipeline falharem.
3. Corrigir os `if` aninhados ao vivo e ver a contagem cair na análise seguinte:

```python
if request.method == 'POST' and form.validate_on_submit():
```

## O que **não** é intencional

Se algum teste falhar, a imagem não construir ou a aplicação não subir com `docker compose up`, é defeito de verdade e deve ser corrigido.
