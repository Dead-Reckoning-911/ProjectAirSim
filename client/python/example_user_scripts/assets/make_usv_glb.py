#!/usr/bin/env python3
"""Write assets/usv.glb — small surface craft for the maritime intercept scene."""
from __future__ import annotations

import json
import struct
from pathlib import Path

import numpy as np


def _box(cx, cy, cz, sx, sy, sz):
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    v = np.array(
        [
            [cx - hx, cy - hy, cz - hz],
            [cx + hx, cy - hy, cz - hz],
            [cx + hx, cy + hy, cz - hz],
            [cx - hx, cy + hy, cz - hz],
            [cx - hx, cy - hy, cz + hz],
            [cx + hx, cy - hy, cz + hz],
            [cx + hx, cy + hy, cz + hz],
            [cx - hx, cy + hy, cz + hz],
        ],
        dtype=np.float32,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [4, 6, 5],
            [4, 7, 6],
            [0, 4, 5],
            [0, 5, 1],
            [1, 5, 6],
            [1, 6, 2],
            [2, 6, 7],
            [2, 7, 3],
            [3, 7, 4],
            [3, 4, 0],
        ],
        dtype=np.uint16,
    )
    return v, faces


def _part(cx, cy, cz, sx, sy, sz, rgb):
    v, f = _box(cx, cy, cz, sx, sy, sz)
    n = np.zeros_like(v)
    for a, b, c in f:
        e1, e2 = v[b] - v[a], v[c] - v[a]
        nn = np.cross(e1, e2)
        ln = np.linalg.norm(nn) or 1.0
        nn = nn / ln
        n[a] += nn
        n[b] += nn
        n[c] += nn
    n /= np.clip(np.linalg.norm(n, axis=1, keepdims=True), 1e-6, None)
    col = np.tile(np.array(rgb + (1.0,), dtype=np.float32), (len(v), 1))
    return v, n, col, f


def build() -> bytes:
    # Metres. Bow +X. Dark hull, light deck, white cabin — USV-ish from nadir.
    parts = [
        _part(0.0, 0.0, 0.45, 12.0, 3.4, 0.9, (0.12, 0.16, 0.20)),
        _part(0.4, 0.0, 0.95, 10.5, 3.0, 0.18, (0.78, 0.80, 0.82)),
        _part(-1.6, 0.0, 1.55, 3.4, 2.4, 1.1, (0.92, 0.93, 0.94)),
        _part(3.4, 0.0, 1.15, 1.6, 1.4, 0.45, (0.18, 0.22, 0.28)),
    ]
    vs, ns, cs, fs = [], [], [], []
    base = 0
    for v, n, c, f in parts:
        vs.append(v)
        ns.append(n)
        cs.append(c)
        fs.append(f + base)
        base += len(v)
    v = np.concatenate(vs)
    n = np.concatenate(ns)
    c = np.concatenate(cs)
    f = np.concatenate(fs)
    vbin = v.tobytes()
    nbin = n.tobytes()
    cbin = c.tobytes()
    fbin = f.tobytes()
    blob = vbin + nbin + cbin + fbin
    vo, no, co, fo = 0, len(vbin), len(vbin) + len(nbin), len(vbin) + len(nbin) + len(cbin)
    gltf = {
        "asset": {"version": "2.0", "generator": "DeadReckoning-USV"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "USV"}],
        "meshes": [
            {
                "primitives": [
                    {
                        "attributes": {"POSITION": 0, "NORMAL": 1, "COLOR_0": 2},
                        "indices": 3,
                        "mode": 4,
                    }
                ]
            }
        ],
        "accessors": [
            {
                "bufferView": 0,
                "componentType": 5126,
                "count": len(v),
                "type": "VEC3",
                "min": v.min(0).tolist(),
                "max": v.max(0).tolist(),
            },
            {"bufferView": 1, "componentType": 5126, "count": len(n), "type": "VEC3"},
            {"bufferView": 2, "componentType": 5126, "count": len(c), "type": "VEC4"},
            {"bufferView": 3, "componentType": 5123, "count": int(f.size), "type": "SCALAR"},
        ],
        "bufferViews": [
            {"buffer": 0, "byteOffset": vo, "byteLength": len(vbin), "target": 34962},
            {"buffer": 0, "byteOffset": no, "byteLength": len(nbin), "target": 34962},
            {"buffer": 0, "byteOffset": co, "byteLength": len(cbin), "target": 34962},
            {"buffer": 0, "byteOffset": fo, "byteLength": len(fbin), "target": 34963},
        ],
        "buffers": [{"byteLength": len(blob)}],
    }
    js = json.dumps(gltf, separators=(",", ":")).encode() + b"   "
    js = js[: len(js) - (len(js) % 4)]
    blob += b"\x00" * ((4 - (len(blob) % 4)) % 4)
    json_chunk = struct.pack("<I", len(js)) + b"JSON" + js
    bin_chunk = struct.pack("<I", len(blob)) + b"BIN\x00" + blob
    total = 12 + len(json_chunk) + len(bin_chunk)
    header = struct.pack("<III", 0x46546C67, 2, total)
    return header + json_chunk + bin_chunk


def main():
    out = Path(__file__).with_name("usv.glb")
    out.write_bytes(build())
    print(f"wrote {out} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
