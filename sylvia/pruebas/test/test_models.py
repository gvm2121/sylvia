from django.test import SimpleTestCase

# Create your tests here.
class Testeo(SimpleTestCase):
    
    def test_prueba(self):
        print('Dentro de testeo')
        assert 1==1