# VoucherPI

[![Maintainability](https://api.codeclimate.com/v1/badges/c86f5a901bdc349b7ab5/maintainability)](https://codeclimate.com/github/steinbart/voucherpi/maintainability)

VoucherPI is a simple, hacky script that prints out a freshly generated voucher using the Unifi API.

The implementation is hacky and needs to be worked on. Error handling is non-existant. It can and will crash.

## Configuration

See `settings.py`.

## Installation

This repository provides `voucherpi.service`, an expample systemd service file for this project.

Adjust neccesary parameters and copy to `/etc/systemd/user/voucherpi.service`. You can also create a link. You can also create a link.

1. `systemctl --user enable voucherpi`
2. `systemctl --user start  voucherpi`


## Maintainers

- Daniel Malik <daniel.malik@steinbart.xyz>
