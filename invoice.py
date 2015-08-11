# -*- coding: utf-8 -*-
import tempfile
from trytond.pool import PoolMeta, Pool
from nereid import route, login_required, abort, \
    current_user
from nereid.helpers import send_file

__all__ = ['Invoice']
__metaclass__ = PoolMeta


class Invoice:

    __name__ = 'account.invoice'

    @route('/orders/invoice/<int:active_id>/download')
    @login_required
    def download_invoice(self):
        """
        Allow user to download invoice.
        """
        Report = Pool().get('account.invoice', type='report')

        if self.party != current_user.party:
            abort(403)

        vals = Report.execute([self.id], {})
        with tempfile.NamedTemporaryFile(delete=False) as file:
            file.write(vals[1])
        return send_file(
            file.name,
            as_attachment=True,
            attachment_filename=vals[3],
        )
