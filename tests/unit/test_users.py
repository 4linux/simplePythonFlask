import unittest
from project import create_app, db
from project.models import Users, Courses


class AllTests(unittest.TestCase):

    def setUp(self):
        self.flask_app = create_app({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        })
        self.context = self.flask_app.app_context()
        self.context.push()
        self.app = self.flask_app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def login(self, name, password):
        return self.app.post('/',data=dict(
            name=name,password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout',follow_redirects=True)

    def register(self,name,email,password,confirm):
        return self.app.post('/register',data=dict(
            name=name,email=email,password=password,confirm=confirm),
            follow_redirects=True)

    def test_user_can_register(self):
        new_user = Users('devops','devops@example.com','qwe123qwe')
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(Users).all()
        for row in test:
            assert row.name == 'devops'

    def test_user_can_loging(self):
        self.register('devops','devops@example.com','qwe123qwe','qwe123qwe')
        response = self.login('devops','qwe123qwe')
        self.assertIn(b'Bem vindo ao Painel de Cursos!!!', response.data)

    def test_user_cannot_login_with_wrong_password(self):
        self.register('devops','devops@example.com','qwe123qwe','qwe123qwe')
        response = self.login('devops','senhaerrada')
        self.assertIn('Usuário ou senha errada!!!'.encode(), response.data)

    def test_registered_user_has_default_role_and_hashed_password(self):
        self.register('devops','devops@example.com','qwe123qwe','qwe123qwe')
        user = Users.query.filter_by(name='devops').first()
        self.assertEqual(user.role, 'user')
        self.assertNotEqual(user.password, 'qwe123qwe')

    def test_user_cannot_register_twice(self):
        self.register('devops','devops@example.com','qwe123qwe','qwe123qwe')
        response = self.register('devops','devops@example.com','qwe123qwe','qwe123qwe')
        self.assertIn('Esse usuário ou email já foram registrados'.encode(), response.data)

    def test_courses_requires_login(self):
        response = self.app.get('/courses', follow_redirects=True)
        self.assertIn('Necessário o login!!!'.encode(), response.data)

    def test_logged_user_can_list_courses(self):
        db.session.add(Courses('Linux Fundamentals', 40, 'curso-701-linux-fundamentals.jpg'))
        db.session.commit()
        self.register('devops','devops@example.com','qwe123qwe','qwe123qwe')
        response = self.login('devops','qwe123qwe')
        self.assertIn(b'Linux Fundamentals', response.data)

    def test_health(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'ok')


if __name__ == '__main__':
    unittest.main()
