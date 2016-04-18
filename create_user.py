from getpass import getpass
import sys

from app import app
from app import db
from app.models import User
import bcrypt


def main():
    with app.app_context():
        users = User.query.all()
        if users:
            print 'The following users already exist:'
            for user in users:
                print '    %s' % user.username
            print
            create = raw_input('Create another user (y/n)? ')
            if create.lower() == 'n':
                return

        username = raw_input('Enter username: ')
        password = getpass().encode('utf-8')
        assert password == getpass('Password (again): ').encode('utf-8')

        user = User(username=username,
                    encpwd=bcrypt.hashpw(password, bcrypt.gensalt()))
        db.session.add(user)
        db.session.commit()
        print 'User added.'


if __name__ == '__main__':
    sys.exit(main())
