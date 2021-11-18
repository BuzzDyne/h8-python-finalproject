import app
import unittest

class MyTestCase(unittest.TestCase):
    dir_payload  = {
        "department": "Test Deparment",
        "gender": 0,
        "name": "Test User",
        "uid": 0
    }

    mov_payload = {
        "budget": 90000,
        "director_id": 2,
        "original_title": "Test Movie",
        "overview": "Test Overview.",
        "popularity": 60,
        "release_date": "2021-05-27",
        "revenue": 2787965087,
        "tagline": "Enter the World of Pandora.",
        "title": "Avatar 2",
        "uid": 19975,
        "vote_average": 7.2,
        "vote_count": 11800
    }

    test_dir_id = 1
    test_mov_id = 1
    

    def setUp(self):
        app.connex_app.app.testing = True
        self.app = app.connex_app.app.test_client()

    def test_a_get_all_director(self):
        result = self.app.get('/api/director')
        self.assertEqual(result.status_code, 200)

    def test_b_post_director(self):
        result = self.app.post('/api/director', json=self.dir_payload)

        result_data = result.get_json()

        for key in self.dir_payload:
            self.assertEqual(
                self.dir_payload[key], 
                result_data[key], 
                f'Received response differs from sent payload at ({key}) key (Sent: {self.dir_payload[key]} | Received: {result_data[key]})'
            )
    
    def test_c_get_single_director(self):
        result = self.app.get(f'/api/director/id/{self.test_dir_id}')
        
        result_data = result.get_json()

        self.assertEqual(
            result_data['id'], 
            self.test_dir_id,
            f"Received id ({result_data['id']}) differs from requested id ({self.test_dir_id})"
        )

    def test_d_get_all_movie(self):
        result = self.app.get('/api/movies')
        # Make your assertions
        self.assertEqual(result.status_code, 200)

    def test_e_post_movie(self):
        result = self.app.post('/api/movies', json=self.mov_payload)

        result_data = result.get_json()


        for key in self.mov_payload:
            x = self.mov_payload[key]
            y = result_data[key]
            self.assertEqual(x, y, 
                f"Received response differs from sent payload at ({key}) key (Sent: {x} | Received: {y})"
            )

    def test_f_get_single_movie(self):
        result = self.app.get(f'/api/movie/id/{self.test_mov_id}')
        
        result_data = result.get_json()

        self.assertEqual(
            result_data['id'], 
            self.test_mov_id,
            f"Received id ({result_data['id']}) differs from requested id ({self.test_mov_id})"
        )


if __name__ == '__main__':
    unittest.main()