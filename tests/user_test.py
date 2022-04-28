import logging

from app import db
from app.db.models import User, Song
from faker import Faker

def test_adding_user(application):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0
        #showing how to add a record
        #create a record
        user = User('keith@webizly.com', 'testtest')
        #add it to get ready to be committed
        db.session.add(user)
        #call the commit
        db.session.commit()
        #assert that we now have a new user
        assert db.session.query(User).count() == 1
        #finding one user record by email
        user = User.query.filter_by(email='keith@webizly.com').first()
        log.info(user)
        #asserting that the user retrieved is correct
        assert user.email == 'keith@webizly.com'
        #this is how you get a related record ready for insert
        user.songs= [Song("test","smap","rock","1999"),Song("test2","te","pop","2020")]
        #commit is what saves the songs
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='test').first()
        assert song1.title == "test"
        #changing the title of the song
        song1.title = "SuperSongTitle"
        #saving the new title of the song
        db.session.commit()
        song2 = Song.query.filter_by(title='SuperSongTitle').first()
        assert song2.title == "SuperSongTitle"
        #checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0

def test_register(client):
    """ POST to /register """
    new_email = 'newuser@test.test'
    new_password = 'Test1234!'
    data = {
        'email' : new_email,
        'password' : new_password,
        'confirm' : new_password
    }
    resp = client.post('register', data=data)

    assert resp.status_code == 302

    # verify new user is in database
    new_user = User.query.filter_by(email=new_email).first()
    assert new_user.email == new_email

    db.session.delete(new_user) # pylint: disable=no-member

def test_login(client):
    """ POST to login """
    data = {
        'email' : 'testuser@test.com',
        'password' : 'testtest'
    }
    resp = client.post('login', data=data)

    assert resp.status_code == 302

#def test_loggedIn_dash(client):






