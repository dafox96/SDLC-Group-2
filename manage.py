from flask import Flask


def deploy():
    """Run deployment tasks."""
    from app import create_app, db
    from flask_migrate import upgrade, migrate, init, stamp

    app: Flask = create_app()
    app.app_context().push()
    db.create_all()

    # migrate database to latest revision
    init()
    stamp()
    migrate()
    upgrade()


deploy()
