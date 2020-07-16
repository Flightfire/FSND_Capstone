import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import app, db

from database.models import setup_db, Actor, Movie

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.db = db
        self.client = self.app.test_client

        # All endpoints are tested with executive producer credentials
        # as RBAC testing is handled by the Postman testing suite. 
        self.executive_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImowT1oxaHVZN0duXzU2Q0NITDU5biJ9.eyJpc3MiOiJodHRwczovL3Rlc3R5dGVzdGVyeXNvbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwYzlmNTRhMTViN2IwMDEzNjIxYTg4IiwiYXVkIjoiQ2FzdGluZyBBZ2VuY3kiLCJpYXQiOjE1OTQ4NjAyMjMsImV4cCI6MTU5NDg2NzQyMywiYXpwIjoiNnNoR0lXWWNpV2dkZVNMaTlhQzRLMVhmSDBLdVN6S2IiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.UB_UV9gMo8dF72okj54feKcjFfSZ_vqMGhdP6oCqRWRU7wCI0lj8NBjry6nfEH000q-Co12-rcg6e38CDQUS5TemB0LzIyCCfb12k5_aDyCzYiA6k1Od0tyR5-k-ZnJwQdKTJ8P1jEpVgXbLXLkLer4LYzt5WihHNCUFtzTxFRQs8SmDAnrh3lQyvF8aEIZ4wA1xlw1fkBnM_b_VmlbPo93Ru3GsvB8WRMwbmaYHfCVZwER3iwlH9cBb71fc_R15Yhv5fJqgjGwRcQeNEERPuViM4D3lk9UlA5SBAZ5i3h8aMxRqIanFHPGsQo8n-PJP3z2nyGSfsNYVvDEiVLDLbA'
        self.auth_header = {'Authorization' : 'Bearer '+self.executive_director_token}
        self.db.create_all()
    
    def tearDownClass():
        """Executed after each test"""
        db.drop_all()
        pass

    def assert_200(self, res, data):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def assert_404(self, res, data):
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def assert_422(self, res, data):
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def assert_500(self, res, data):
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Server Error')
    
    # Actors

    def test_a_post_actors(self):
        res = self.client().post('/actors',
                headers = self.auth_header,
                json= {
                 'name' : 'Tommy Lee Jones', 
                 'age' : 78, 
                 'gender' : 'Male'  
                })
        data = json.loads(res.data)
        self.assert_200(res, data)
        self.assertTrue(data['actors'])
    
    def test_b_get_actors(self):
        res = self.client().get('/actors', 
                headers = self.auth_header)
        data = json.loads(res.data)
        self.assert_200(res, data)
        self.assertTrue(data['actors'])

    def test_c_invalid_post_age(self):
        res = self.client().post('/actors',
                headers = self.auth_header,
                json= {
                 'name' : 'Tommy Lee Jones', 
                 'age' : "Eighty Nine", 
                 'gender' : 'Male'  
                })
        data = json.loads(res.data)
        self.assert_422(res, data)

    def test_d_patch_actors(self):
        res = self.client().patch('/actors/1',
                headers = self.auth_header,
                json= {
                 'name' : 'Tommy Lee Jones', 
                 'age' : 87, 
                 'gender' : 'Male'  
                })
        data = json.loads(res.data)
        self.assert_200(res, data)
        self.assertTrue(data['actors'])
    
    def test_e_invalid_patch_age(self):
        res = self.client().patch('/actors/1',
                headers = self.auth_header,
                json= {
                 'name' : 'Tommy Lee Jones', 
                 'age' : "Eighty Nine", 
                 'gender' : 'Male'  
                })
        data = json.loads(res.data)
        self.assert_422(res, data)
    
    def test_f_delete_actor(self):
        res = self.client().delete('/actors/1', 
                headers = self.auth_header)
        data = json.loads(res.data)
        self.assert_200(res, data)
        self.assertTrue(data['delete'])

    def test_g_invalid_delete_actor(self):
        res = self.client().delete('/actors/1000', 
                headers = self.auth_header)
        data = json.loads(res.data)
        self.assert_404(res, data)

    
    # Movies

    def test_h_post_movie(self):
        res = self.client().post('/movies',
                headers = self.auth_header,
                json= {
                 'title' : 'The Smoking Gun', 
                 'release_date' : '2007-06-08 12:35:29.123'  
                })
        data = json.loads(res.data)
        self.assert_200(res, data)
        self.assertTrue(data['movie'])
    
    def test_i_get_movies(self):
        res = self.client().get('/movies', 
                headers = self.auth_header)
        data = json.loads(res.data)
        self.assert_200(res, data)
        self.assertTrue(data['movies'])

    def test_j_invalid_release_date(self):
        res = self.client().post('/movies',
                headers = self.auth_header,
                json= {
                 'title' : 'The Smoking Gun', 
                 'release_date' : 'XTYS'  
                })
        data = json.loads(res.data)
        self.assert_422(res, data)

    def test_k_invalid_title(self):
        res = self.client().post('/movies',
                headers = self.auth_header,
                json= {
                 'title' : 27.6, 
                 'release_date' : '2007-06-08 12:35:29.123'  
                })
        data = json.loads(res.data)
        self.assert_422(res, data)

    def test_l_patch_movies(self):
        res = self.client().patch('/movies/1',
                headers = self.auth_header,
                json= {
                 'title' : 'Top Gun', 
                 'release_date' : '2007-06-08 12:35:29.123'  
                })
        data = json.loads(res.data)
        self.assert_200(res, data)
        self.assertTrue(data['movies'])
    
    def test_m_invalid_patch_title(self):
        res = self.client().patch('/movies/1',
                headers = self.auth_header,
                json= {
                 'title' : 4556.68745, 
                 'release_date' : '2007-06-08 12:35:29.123'  
                })
        data = json.loads(res.data)
        self.assert_422(res, data)
    
    def test_n_invalid_patch_date(self):
        res = self.client().patch('/movies/1',
                headers = self.auth_header,
                json= {
                 'title' : 'Top Gun', 
                 'release_date' : 'THYFW'  
                })
        data = json.loads(res.data)
        self.assert_422(res, data)


    def test_o_delete_movie(self):
        res = self.client().delete('/movies/1', 
                headers = self.auth_header)
        data = json.loads(res.data)
        self.assert_200(res, data)
        self.assertTrue(data['delete'])

    def test_p_invalid_delete_movie(self):
        res = self.client().delete('/movies/1000', 
                headers = self.auth_header)
        data = json.loads(res.data)
        self.assert_404(res, data)













    # def test_get_movies(self):
    #     res = self.client().get('/movies', 
    #             headers = {'Authorization' : 'Bearer '+self.executive_director_token})
    #     data = json.loads(res.data)

    #     self.assert_200(res, data)
    #     self.assertTrue(data['movies'])

    # def test_delete_question(self):
    #     res = self.client().delete('/questions/10')
    #     data = json.loads(res.data)
    #     self.assert_200(res, data)
    #     self.assertEqual(data['question_id'], 10)

    # def test_404_invalid_delete_request(self):
    #     res = self.client().delete('/questions/1000')
    #     data = json.loads(res.data)
    #     self.assert_404(res, data)

    # def test_create_question(self):
    #     res = self.client().post(
    #         '/question', 
    #          json= {
    #              'question' : 'data1', 
    #              'answer' : 'data2', 
    #              'difficulty' : '3',
    #              'category' : 1
    #          })

    #     data = json.loads(res.data)

    #     self.assert_200(res, data)
    #     self.assertTrue(data['question_id'])
                
    # def test_422_invalid_difficulty(self):
    #     res = self.client().post(
    #         '/question', 
    #          json= {
    #              'question' : 'data1', 
    #              'answer' : 'data2', 
    #              'difficulty' : '17',
    #              'category' : 1
    #          })

    #     data = json.loads(res.data)

    #     self.assert_422(res, data)

    # def test_422_invalid_category(self):
    #     res = self.client().post(
    #         '/question', 
    #          json= {
    #              'question' : 'data1', 
    #              'answer' : 'data2', 
    #              'difficulty' : '1',
    #              'category' : 1000
    #          }
    #     )

    #     data = json.loads(res.data)

    #     self.assert_422(res, data)

    # def test_search_questions(self):
    #     res = self.client().post(
    #        '/questions', 
    #        json= {
    #            'searchTerm' : 'Testing'
    #        } 
    #     )

    #     data = json.loads(res.data)
    #     self.assert_200(res, data)

    # def test_select_questions_by_category(self):
    #     res = self.client().get('/categories/3/questions')

    #     data = json.loads(res.data)
    #     self.assert_200(res, data)

    # def test_422_invalid_category_for_questions_by_category(self):
    #     res = self.client().get('/categories/1000/questions')

    #     data = json.loads(res.data)
    #     self.assert_422(res, data)
    
    # def test_start_quiz(self):
    #     res = self.client().post(
    #         '/quizzes', 
    #          json= {
    #              'previous_questions' : [1,2,3], 
    #              'quiz_category' : {
    #                 'id' : '1',
    #                 'type' : '2'
    #              } 
    #          }
    #     )

    #     data = json.loads(res.data)
    #     self.assert_200(res, data)

    # def test_select_all_categories_quiz(self):
    #     res = self.client().post(
    #         '/quizzes', 
    #          json= {
    #              'previous_questions' : [1,2,3], 
    #              'quiz_category' : {
    #                 'id' : '1',
    #                 'type' : 'click'
    #              } 
    #          }
    #     )

    #     data = json.loads(res.data)
    #     self.assert_200(res, data)
    
    # def test_422_invalid_category_id(self):
    #     res = self.client().post(
    #         '/quizzes', 
    #          json= {
    #              'previous_questions' : [1,2,3], 
    #              'quiz_category' : {
    #                 'id' : '1000',
    #                 'type' : '2'
    #              } 
    #          }
    #     )

    #     data = json.loads(res.data)
    #     self.assert_422(res, data)
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()