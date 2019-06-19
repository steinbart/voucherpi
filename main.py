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
        code = voucher['code']
        filename = "data/" + code + ".pdf"
        s = f.read().replace("%code%", code)
        # Insert voucher into document
        print("+ Printing voucher " + code)
        # Convert to PDF
        pdfkit.from_string(s, filename, {'page-size': 'A4', 'margin-top': '5cm', 'margin-left': '4cm', 'margin-right': '4cm', 'margin-bottom': '5cm'})
        # Attempt to print PDF
        c.printFile(settings.CUPS_PRINTER, filename, code, {})
        os.remove(filename)


if __name__ == '__main__':
    # Check if data dir exists/create
    os.rmdir("data")
    os.mkdir("data")
    global api
    api = Unifi(settings.UNIFI_USERNAME, settings.UNIFI_PASSWORD, settings.UNIFI_URL, site=settings.UNIFI_SITE)
    print("+ Initialized Unifi API")
    cups.setServer(settings.CUPS_SERVER)
    global c
    c = cups.Connection()
    print("+ Initialized CUPS")

    b = Button(settings.BUTTON_PIN)
    b.when_released = print_voucher
    while True:
        pass
