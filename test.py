import unittest
from information import*
app=Flask(__name__)
class FlaskTestcase(unittest.TestCase):
    def test_availability_create_user(self):
        tester = app.test_client( self )
        response = tester.post('/user',data=dict(rollno='rollno'))
        self.assertTrue('Roll no already exist!!!', response.data)

    def test_create_user(self):
        tester = app.test_client(self)
        response = tester.post('/user',content_type = 'application/json')
        self.assertTrue(response.status_code,201)

        response = tester.post ( '/user', data=dict (name='name', rollno='rollno',address='address',branch='branch') )
        self.assertTrue("Data stored successfully!!!", response.data )

        response = tester.post('/user', content_type='application/xml')
        self.assertTrue ( response.status_code, 201 )
    def test_get_user(self):
        tester = app.test_client(self)
        response = tester.get('/user', content_type='application/json')
        self.assertTrue(response.status_code, 200)
        response = tester.get('/user', content_type='application/xml')
        self.assertTrue ( response.status_code, 200)

    def test_get_one_user(self):
        tester = app.test_client ( self )
        response = tester.get( '/user/rollno', content_type='application/json' )
        self.assertTrue(response.status_code, 200 )
        response = tester.get( '/user/rollno', content_type='application/xml' )
        self.assertTrue( response.status_code, 200 )
    def test_modify_user(self):
        tester = app.test_client(self)
        response = tester.put('/user/rollno', content_type='application/json' )
        self.assertTrue ( response.status_code, 201 )
        response = tester.put('/user/rollno', content_type='application/xml' )
        self.assertTrue ( response.status_code, 201 )
    def test_delete_user(self):
        tester = app.test_client(self)
        response = tester.delete('/user/rollno', data=dict(rollno='rollno'))
        self.assertTrue ( response.status_code, 200)

if __name__=='__main__':
    unittest.main ( )
