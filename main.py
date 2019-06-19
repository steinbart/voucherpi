import cups

from unifi import Unifi
import settings
import pdfkit
from gpiozero import Button
import os


def print_voucher():
    # Read file
    f = open('templates/voucher.html', 'r')
    vouchers = api.generate_voucher(expire=settings.EXPIRE, usages=settings.USAGES)
    for voucher in vouchers:
        s = f.read().replace("%code%", voucher['code'])
        # Insert voucher into document
        print(f"+ Printing voucher {voucher['code']}")
        # Convert to PDF
        pdfkit.from_string(s, f"data/{voucher['code']}.pdf", {'page-size': 'A4', 'margin-top': '5cm', 'margin-left': '4cm', 'margin-right': '4cm', 'margin-bottom': '5cm'})
        # Attempt to print PDF
        c.printFile(settings.CUPS_PRINTER, f"data/{voucher['code']}.pdf", voucher['code'], {})
        os.remove(f"data/{voucher['code']}.pdf")


if __name__ == '__main__':
    global api
    api = Unifi(settings.UNIFI_USERNAME, settings.UNIFI_PASSWORD, settings.UNIFI_URL, site=settings.UNIFI_SITE)
    cups.setServer(settings.CUPS_SERVER)
    global c
    c = cups.Connection()

    b = Button(1)
    b.when_released = print_voucher
