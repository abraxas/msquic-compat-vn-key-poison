# Lab notes

Replay: `cd lab && ./run.sh` (or the root wrapper `msquic-compat-vn-key-poison-Abraxas-Labs.py`). Compose project `msquic-compat-vn`. Loopback only: proxy `127.0.0.1:18150`, server `127.0.0.1:18151`.

Victim is patched `quicsample` on MsQuic v2.6.1 (`a01333cf`). Oracle is handshake `Connected`, not a payload.

| Phase | Inject | Client `Connected` |
|---|---|---|
| CONTROL | none | yes |
| INJECT | truncated QUIC v2 Handshake `f06b3343cf0000` first | no |
| NEGATIVE | truncated `f0112233440000` first | yes |

Witness: `SUCCESS MSQUIC-COMPAT-VN-KEY-POISON-WITNESS`

Do not ship `poc-last-run.txt`. The sample prints a resumption ticket on the control/negative paths.
