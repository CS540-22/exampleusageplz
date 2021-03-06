import re
from unittest import TestCase
from app import create_app
import json
from datetime import datetime

class TestWelcome(TestCase):
    
    def setUp(self):
        self.app = create_app()#.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        # set app db to use sqlite in memory
        self.app = self.app.test_client()
        self.app.testing = True

    def test_create(self):
        """
        Tests creation of a post
        """
        # create a sample post
        data = {
            'title': 'Test Post',
            'content': 'This is a test post',
            # 'user_id': 1,
            'id': 1, #TODO: use UUID?
            'call_id': 1,
            #'created_at': '2018-01-01T00:00:00Z',
            #'updated_at': '2018-01-01T00:00:00Z',
            # optional
            'scope': None
        }
        self.app.delete('api/posts/1')
        
        #rv = self.app.post('/api/posts', data=json.dumps(data), content_type='application/json')
        rv = self.app.post('/api/posts', data=json.dumps(data), content_type='application/json')
        result = json.loads(rv.data)
        self.assertEqual(rv.status_code, 201)

        # check that the post was created with the right data
        self.assertEqual(result['title'], data['title'])
        self.assertEqual(result['content'], data['content'])
        self.assertEqual(result['scope'], data['scope'])
        self.assertEqual(result['id'], data['id'])
        #self.assertEqual(result['user_id'], data['user_id'])

        self.assertEqual(datetime.strptime(result['created_at'],'%a, %d %b %Y %H:%M:%S GMT').date(), datetime.utcnow().date())
        self.assertEqual(datetime.strptime(result['updated_at'],'%a, %d %b %Y %H:%M:%S GMT').date(), datetime.utcnow().date())

        self.app.delete('api/posts/1')

    def test_update(self):
        # create a sample post
        data = {
            'title': 'Test Post',
            'content': 'This is a test post',
            # 'user_id': 1,
            'id': 1, #TODO: use UUID?
            'call_id': 1,
            #'created_at': '2018-01-01T00:00:00Z',
            #'updated_at': '2018-01-01T00:00:00Z',
            # optional
            'scope': None
        }
        self.app.delete('api/posts/1')
        
        #rv = self.app.post('/api/posts', data=json.dumps(data), content_type='application/json')
        rv = self.app.post('/api/posts', data=json.dumps(data), content_type='application/json')

        # data to update with
        data = {
            'title': 'Updated Test Post',
            'content': 'This is an updated test post',
            # 'user_id': 1,
            'id': 1, #TODO: use UUID?
            'call_id': 1,
            #'created_at': '2018-01-01T00:00:00Z',
            #'updated_at': '2018-01-01T00:00:00Z',
            # optional
            'scope': None
        }
        self.app.put('/api/posts/1', data=json.dumps(data), content_type='application/json')
        rv = self.app.get('/api/posts/1')
        result = json.loads(rv.data)
        self.assertEqual(rv.status_code, 200)

        # check that the post was updated with the right data
        self.assertEqual(result['title'], data['title'])
        self.assertEqual(result['content'], data['content'])
        self.assertEqual(result['scope'], data['scope'])
        self.assertEqual(result['id'], data['id'])
        #self.assertEqual(result['user_id'], data['user_id'])

        self.assertEqual(datetime.strptime(result['created_at'],'%a, %d %b %Y %H:%M:%S GMT').date(), datetime.utcnow().date())
        self.assertEqual(datetime.strptime(result['updated_at'],'%a, %d %b %Y %H:%M:%S GMT').date(), datetime.utcnow().date())

        self.app.delete('api/posts/1')

    def test_delete(self):
        # create a sample post
        data = {
            'title': 'Test Post',
            'content': 'This is a test post',
            # 'user_id': 1,
            'id': 1, #TODO: use UUID?
            'call_id': 1,
            #'created_at': '2018-01-01T00:00:00Z',
            #'updated_at': '2018-01-01T00:00:00Z',
            # optional
            'scope': None
        }
        
        
        #rv = self.app.post('/api/posts', data=json.dumps(data), content_type='application/json')
        rv = self.app.post('/api/posts', data=json.dumps(data), content_type='application/json')

        rv = self.app.delete('api/posts/1')
        self.assertEqual(rv.status_code, 200)
        result = json.loads(rv.data)


        self.assertEqual(result['title'], data['title'])
        self.assertEqual(result['content'], data['content'])
        self.assertEqual(result['scope'], data['scope'])
        self.assertEqual(result['id'], data['id'])
        

        # make sure it's deleted
        rv = self.app.get('/api/posts/1')
        self.assertEqual(rv.status_code, 404)
        
    def test_get_single(self):
        # create a sample post
        data = {
            'title': 'Test Post',
            'content': 'This is a test post',
            # 'user_id': 1,
            'id': 1, #TODO: use UUID?
            'call_id': 1,
            #'created_at': '2018-01-01T00:00:00Z',
            #'updated_at': '2018-01-01T00:00:00Z',
            # optional
            'scope': None
        }
        rv = self.app.post('/api/posts', data=json.dumps(data), content_type='application/json')

        
        rv = self.app.get('/api/posts/1')
        self.assertNotEqual(rv.status_code, 404)
        
        result = json.loads(rv.data)
        self.assertEqual(result['title'], data['title'])
        self.assertEqual(result['content'], data['content'])
        self.assertEqual(result['scope'], data['scope'])
        self.assertEqual(result['id'], data['id'])
        
        rv = self.app.delete('api/posts/1')
        self.assertEqual(rv.status_code, 200)

        # make sure it's deleted
        rv = self.app.get('/api/posts/1')
        self.assertEqual(rv.status_code, 404)

    
    # Test post search functionality
    def test_search(self):

        # create api
        data = dict(id = int(1), name='test1', lang='js', semantic_version='1.0.0')
        rv = self.app.post('/api/apis', data=json.dumps(data), content_type='application/json')

        # create the calls
        data1 = dict(id = int(1), api_id=int(1), full_name='pop')
        data2 = dict(id = int(2), api_id=int(1), full_name='push')

        rv = self.app.post('/api/calls', data=json.dumps(data1), content_type='application/json')
        rv = self.app.post('/api/calls', data=json.dumps(data2), content_type='application/json')

        rv = self.app.get('/api/calls')
        self.assertEqual(rv.status_code, 200)

        # make sure it returned the right data
        result = json.loads(rv.data)
        self.assertEqual(result[0]['id'], data1['id'])
        self.assertEqual(result[0]['api_id'], data1['api_id'])
        self.assertEqual(result[0]['full_name'], data1['full_name'])

        self.assertEqual(result[1]['id'], data2['id'])
        self.assertEqual(result[1]['api_id'], data2['api_id'])
        self.assertEqual(result[1]['full_name'], data2['full_name'])


        for i in range (0,15):
            data = {
                'title': 'Test Post #' + str(i),
                'content': 'This is a test post #' + str(i),
                # 'user_id': 1,
                'id': i, #TODO: use UUID?
                'call_id': 1,
                #'created_at': '2018-01-01T00:00:00Z',
                #'updated_at': '2018-01-01T00:00:00Z',
                # optional
                'scope': None
            }
            self.app.post('/api/posts', data=json.dumps(data), content_type='application/json')
        
        
        rv = self.app.get('/api/posts/search', query_string=dict(lang = 'js', call_id = '1', api='1'), content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        result = json.loads(rv.data)

        #import sys
        # print to stderr
        #print(result, file=sys.stderr)

        for i in range(0, len(result),5 ):
            for j in range(i,i+5):
                #self.assertEqual(result[i][j]['api'], 1)

                self.assertEqual(result[i][j]['title'], 'Test Post #' + str(j))
                self.assertEqual(result[i][j]['content'], 'This is a test post #' + str(j))
                self.assertEqual(result[i][j]['id'], j)
                self.assertEqual(result[i][j]['call_id'], 1)



        for i in range (0,15):
            self.app.delete('api/posts/' + str(i))
        #import sys
        #print("DEBUG: sucess on search posts", file=sys.stderr)

        