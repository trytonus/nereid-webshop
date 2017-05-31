# -*- coding: utf-8 -*-
import unittest

import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class TestViewsDepends(ModuleTestCase):
    '''
    Test views and depends
    '''
    module = "nereid_webshop"


def suite():
    """
    Define suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestViewsDepends)
    )
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
