import unittest 
from cripto import get_hesh, is_hesh_equal

class CryptoTest(unittest.TestCase):
    # Проверка Коректного создани Хеша
    def test_get_hesh(self):
        self.assertEqual(get_hesh('привет'), 'e58f1e8c55fa105bdd3f40e5037eb0b039b5998d52c05e6cd98878dd2da5cab2')
        self.assertEqual(get_hesh('Ты Валет, понял !!!'), 'cd0faadfd46dc6808d5984e4c7299defc7dab69cd25a9c29aa72566618b33230')
        self.assertEqual(get_hesh('Ничего не Вечно, так что пака, 12:45'), '47ab81959fe343c67c4cd8041a48ce4aec58971a36066c215d08db2f8d2f9e58')
    
    # Проверка двух Хешей на равность
    def test_is_hesh_equal(self):
        self.assertEqual(is_hesh_equal('e58f1e8c55fa105bdd3f40e5037eb0b039b5998d52c05e6cd98878dd2da5cab2', 
                                       'e58f1e8c55fa105bdd3f40e5037eb0b039b5998d52c05e6cd98878dd2da5cab2'), True)
        self.assertEqual(is_hesh_equal('e58f1e8c55fa105bdd3f40e5037eb0b039b5998d52c05e6cd98878dd2da5cab2', 
                                       'W58f1e8c55fa105bdd3f40e5037eb0b039b5998d52c05e6cd98878dd2da5cab2'), False)



if __name__ == '__main__':
    unittest.main()  