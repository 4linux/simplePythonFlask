from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

#Base = declarative_base()
#engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile('_config.py')
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from project.users.views import users_blueprint
    from project.courses.views import courses_blueprint
    from project.health.views import health_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(courses_blueprint)
    app.register_blueprint(health_blueprint)

    return app
