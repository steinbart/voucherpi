from argparse import ArgumentParser
import os
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

import cups
import pdfkit
from gpiozero import Button, LED
from unifipy import Unifi

import settings


def print_voucher():
    # Read file
    print("+ Attempting to print voucher")
    with open('templates/voucher.html', 'r') as f:
        vouchers = api.generate_voucher(expire=settings.EXPIRE, usages=settings.USAGES)
        for voucher in vouchers:
            code = voucher['code']
            with NamedTemporaryFile() as x:
                # Insert voucher into document
                s = f.read().replace("%code%", code)
                print("+ Printing voucher " + code)
                # Convert to PDF
                pdfkit.from_string(s, x.name,
                                   {'page-size': 'A4', 'margin-top': '4cm', 'margin-left': '2.5cm',
                                    'margin-right': '2.5cm',
                                    'margin-bottom': '2cm'})
                # Attempt to print PDF
                c.printFile(settings.CUPS_PRINTER, x.name, code, {})


if __name__ == '__main__':
    LED(settings.LED_PIN).on()
    api = Unifi(settings.UNIFI_USERNAME, settings.UNIFI_PASSWORD, settings.UNIFI_URL, site=settings.UNIFI_SITE)
    print("+ Initialized Unifi API")
    cups.setServer(settings.CUPS_SERVER)
    c = cups.Connection()
    print("+ Initialized CUPS")
    print("+ Listening for input on pin " + str(settings.BUTTON_PIN))
    b = Button(settings.BUTTON_PIN, bounce_time=settings.BUTTON_DEBOUNCE_TIME)
    b.when_released = print_voucher
    while True:
        pass
