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
        #db.session.delete(user)
        #assert db.session.query(User).count() == 0
        #assert db.session.query(Song).count() == 0

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
    """This will test the login function"""
    assert db.session.query(User).count() == 0

    # create a new user in the database
    user = User("newuser@test.test", "Test1234!")
    db.session.add(user)
    db.session.commit()
    assert db.session.query(User).count() == 1
    assert user.is_authenticated() is True
    user = User.query.filter_by(email='newuser@test.test').first()
    assert user.email == 'newuser@test.test'

    data = {
        'email': user.email,
        'password': user.password
    }
    response = client.post('/login', data=data)
    assert response.status_code == 302

    # verify new user is active
    assert user.active is True

#logout test
def logout(client):
    return client.get('/logout', follow_redirects=True)

#Deny Access Test
def test_deny_access(client):
    response = client.get("/browse_songs")
    assert response.status_code == 404

#Deny Upload Test
def test_deny_upload(client):
    response = client.get("/songs/upload", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

#Test login page
def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200

#Test registration page
def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200






