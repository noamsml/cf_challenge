from storage.adapter import Transacter

class ProductionTransacter(Transacter):
    def __init__(self):
        super().__init__('mysql://root@localhost/urlshortener')


class TestTransacter(Transacter):
    def __init__(self):
        super().__init__('mysql://root@localhost/urlshortener_test')
