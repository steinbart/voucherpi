import sys
import time
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
    led.blink(0.25, 0.25)
    print("+ Attempting to print voucher")
    with open('templates/voucher.html', 'r') as f:
        try:
            vouchers = api.generate_voucher(expire=settings.EXPIRE, usages=settings.USAGES)
        except Exception:
            print("+ Failed to generate voucher")
            kill()
        for voucher in vouchers:
            code = voucher['code']
            with NamedTemporaryFile() as x:
                # Insert voucher into document
                s = f.read().replace("%code%", code)
                print("+ Printing voucher " + code)
                # Convert to PDF
                pdfkit.from_string(s, x.name,
                                   {'page-size': 'A4', 'margin-top': '4cm'})
                # Attempt to print PDF
                c.printFile(settings.CUPS_PRINTER, x.name, code, {})
                time.sleep(1)
                led.off()
                led.on()


def kill():
    led.off()
    time.sleep(3)
    sys.exit(1)


if __name__ == '__main__':
    led = LED(settings.LED_PIN)
    try:
        api = Unifi(settings.UNIFI_USERNAME, settings.UNIFI_PASSWORD, settings.UNIFI_URL, site=settings.UNIFI_SITE)
    except Exception:
        print("+ Could not connect to Unifi API")
        kill()
    led.on()
    print("+ Initialized Unifi API")
    cups.setServer(settings.CUPS_SERVER)
    c = cups.Connection()
    print("+ Initialized CUPS")
    print("+ Listening for input on pin " + str(settings.BUTTON_PIN))
    b = Button(settings.BUTTON_PIN, bounce_time=settings.BUTTON_DEBOUNCE_TIME)
    b.when_released = print_voucher
    while True:
        pass
