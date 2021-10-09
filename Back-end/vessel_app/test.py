try:
    from run import app
    import unittest
    from global_api import routes

except Exception as e:
    print("Some Models are Missing {}".format(e))


#Contiunous Intergrations 
# Unit test for the entire application

class FlaskTest(unittest.TestCase):

    #check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check if content return is application/json
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type, "application/json")

    # check for Data returned 
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue(b'Message' in response.data)

class TestGlobalApi(unittest.TestCase):

    def test_create_token(self):
        result = routes.create_token()

if __name__ == "main":
    unittest.main()