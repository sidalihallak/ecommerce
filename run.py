#!/usr/bin/env python
import os
from app import create_app, graph
from app.models import User

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_CONFIG', 'development'))
    with app.app_context():
        if graph.users.get_all().next is None:
            u = User(username='sidali')
            u.set_password('malika')
            u.save()
    app.run()
