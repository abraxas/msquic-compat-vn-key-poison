#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  ID: msquic-compat-vn-key-poison (High: 7.5)
#  Vendor: Microsoft MsQuic
#  Versions: v2.6.1 (a01333cf)
#  Impact: Unauth handshake DoS (compatible-VN key poison)
#  Requires: UDP inject from the server 4-tuple, loopback lab
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
#  The in-container oracle is lab/poc.py. This file runs lab/run.sh.
#
######################################################################################

from __future__ import annotations

import os
import stat
import subprocess
import sys

BANNER = r"""
        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
 d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"

                     ABRAXAS LABS
  https://abraxaslabs.tech  github.com/abraxas  @abraxas_null
  abraxas.null@proton.me
"""


def main() -> int:
    print(BANNER, file=sys.stderr, flush=True)
    print(
        "Authorized lab only. Loopback. Witness MSQUIC-COMPAT-VN-KEY-POISON-WITNESS.",
        file=sys.stderr,
        flush=True,
    )
    here = os.path.dirname(os.path.abspath(__file__))
    lab = os.path.join(here, "lab")
    run = os.path.join(lab, "run.sh")
    if not os.path.isfile(run):
        print("FAIL MSQUIC-COMPAT-VN-KEY-POISON lab/run.sh missing", file=sys.stderr)
        return 1
    mode = os.stat(run).st_mode
    if not mode & stat.S_IXUSR:
        os.chmod(run, mode | stat.S_IXUSR)
    raise SystemExit(subprocess.call(["/bin/bash", run], cwd=lab))


if __name__ == "__main__":
    raise SystemExit(main())
