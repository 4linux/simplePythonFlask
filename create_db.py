from sqlalchemy_utils.functions import database_exists, create_database
from project import create_app, db
from project.models import Courses

# Cursos, cargas horarias e capas retirados de https://4linux.com.br/cursos/
DEFAULT_COURSES = [
    ('Linux Fundamentals', 20, 'curso-701-linux-fundamentals.jpg'),
    ('Linux System Administrator', 40, 'curso-703-linux-system-administrator.jpg'),
    ('Docker: Administração de Containers – DCA', 40, 'curso-540-docker.jpg'),
    ('Kubernetes: Orquestração de Ambientes Escaláveis CKAD/CKA', 52, 'curso-541-kubernetes.jpg'),
    ('CI/CD: Integração e Entrega Contínua', 40, 'curso-524-cicd.jpg'),
    ('Especialista em Automação com Ansible', 40, 'curso-535-ansible.jpg'),
    ('Python Fundamentals', 40, 'curso-520-python-fundamentals.jpg'),
    ('IA no Universo Kubernetes', 20, 'curso-547-ia-kubernetes.jpg'),
]

app = create_app()

with app.app_context():
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    db.create_all()

    # Carga inicial: somente quando a tabela de cursos esta vazia
    if Courses.query.count() == 0:
        for name, duration, image in DEFAULT_COURSES:
            db.session.add(Courses(name, duration, image))

    db.session.commit()
    print('Banco de dados pronto: %d cursos cadastrados' % Courses.query.count())
