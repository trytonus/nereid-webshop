# -*- coding: utf-8 -*-
import unittest
from trytond.tests.test_tryton import POOL, USER, DB_NAME, CONTEXT
from trytond.transaction import Transaction
from test_base import BaseTestCase


class TestDownloadInvoice(BaseTestCase):

    def test_0010_download_invoice(self):
        """
        Test to download invoice from a sale
        """
        Address = POOL.get('party.address')
        SalePayment = POOL.get('sale.payment')
        PaymentGateway = POOL.get('payment_gateway.gateway')
        Journal = POOL.get('account.journal')
        Invoice = POOL.get('account.invoice')
        SaleConfig = POOL.get('sale.configuration')

        with Transaction().start(DB_NAME, USER, CONTEXT):
            self.setup_defaults()
            app = self.get_app()

            self.create_test_products()

            template1, = self.Product.search([], limit=1)
            product1, = template1.products

            party2, = self.Party.create([{
                'name': 'Registered User',
            }])

            self.registered_user, = self.NereidUser.create([{
                'party': party2.id,
                'display_name': 'Registered User',
                'email': 'example@example.com',
                'password': 'password',
                'company': self.company.id,
            }])

            uom, = self.Uom.search([], limit=1)
            # Create sale
            address, = Address.create([{
                'party': party2.id,
                'name': 'Name',
                'street': 'Street',
                'streetbis': 'StreetBis',
                'zip': 'zip',
                'city': 'City',
                'country': self.available_countries[0].id,
                'subdivision':
                    self.available_countries[0].subdivisions[0].id,
            }])

            sale_config = SaleConfig(1)
            sale_config.payment_authorize_on = 'manual'
            sale_config.payment_capture_on = 'sale_process'
            sale_config.gift_card_method = 'order'
            sale_config.save()

            sale, = self.Sale.create([{
                'party': party2,
                'company': self.company.id,
                'invoice_address': address.id,
                'shipment_address': address.id,
                'currency': self.usd.id,
                'lines': [
                    ('create', [{
                        'product': product1.id,
                        'quantity': 1,
                        'unit': template1.sale_uom.id,
                        'unit_price': template1.list_price,
                        'description': 'description',
                    }])]
            }])
            self.Sale.quote([sale])

            cash_journal, = Journal.search([
                ('name', '=', 'Cash')
            ])

            gateway = PaymentGateway(
                name='Manual',
                journal=cash_journal,
                provider='self',
                method='manual',
            )
            gateway.save()

            # Create a sale payment
            SalePayment.create([{
                'sale': sale.id,
                'amount': sale.total_amount,
                'gateway': gateway,
                'credit_account': party2.account_receivable.id,
            }])
            self.Sale.confirm([sale])
            with Transaction().set_context(company=self.company.id):
                self.Sale.process([sale])
                Invoice.post(sale.invoices)
            with app.test_client() as c:
                # Loged in user tries to download invoice
                self.login(c, 'example@example.com', 'password')
                response = c.get(
                    '/orders/invoice/%s/download' % (sale.invoices[0].id, )
                )
                self.assertEqual(response.status_code, 200)


def suite():
    "Test suite"
    test_suite = unittest.TestSuite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestDownloadInvoice)
    )
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
