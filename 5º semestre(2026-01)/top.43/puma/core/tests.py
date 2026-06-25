from django.test import TestCase

class PumaViewsTestCase(TestCase):
    
    def test_home_view_status_code(self):
        """
        Teste para verificar se a página inicial (index) 
        está a carregar corretamente e a devolver o código HTTP 200 (OK).
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)