from argparse import ArgumentParser
import os
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

import cups
import pdfkit
from gpiozero import Button
from unifipy import Unifi

import settings


def print_voucher():
    # Read file
    f = open('templates/voucher.html', 'r')
    vouchers = api.generate_voucher(expire=settings.EXPIRE, usages=settings.USAGES)
    for voucher in vouchers:
        code = voucher['code']
        filename = NamedTemporaryFile("data/" + code + ".pdf")
        s = f.read().replace("%code%", code)
        # Insert voucher into document
        print("+ Printing voucher " + code)
        # Convert to PDF
        pdfkit.from_string(s, filename,
                           {'page-size': 'A4', 'margin-top': '4cm', 'margin-left': '2.5cm', 'margin-right': '2.5cm',
                            'margin-bottom': '2cm'})
        # Attempt to print PDF
        c.printFile(settings.CUPS_PRINTER, filename, code, {})
        os.remove(filename)


if __name__ == '__main__':
    parser = ArgumentParser(description="VoucherPI CLI")
    parser.add_argument("--local", default=False, help="Enable local mode (don't use GPIO, trigger instantly)",
                        action="store_true")
    args = parser.parse_args()
    api = Unifi(settings.UNIFI_USERNAME, settings.UNIFI_PASSWORD, settings.UNIFI_URL, site=settings.UNIFI_SITE)
    print("+ Initialized Unifi API")
    cups.setServer(settings.CUPS_SERVER)
    c = cups.Connection()
    print("+ Initialized CUPS")
    if args.local:
        print("+ Using local mode, triggering input")
        print_voucher()
    else:
        print("+ Listening for input on pin " + str(settings.BUTTON_PIN))
        b = Button(settings.BUTTON_PIN, bounce_time=settings.BUTTON_DEBOUNCE_TIME)
        b.when_released = print_voucher
        while True:
            pass
