#!/usr/bin/env python3
"""Compare a reconstructed typography crop against a reference crop."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageChops

def edge_map(gray: np.ndarray, threshold: float = 0.12) -> np.ndarray:
    gx = np.abs(np.diff(gray, axis=1, prepend=gray[:, :1]))
    gy = np.abs(np.diff(gray, axis=0, prepend=gray[:1, :]))
    return np.hypot(gx, gy) >= threshold

def edge_f1(a: np.ndarray, b: np.ndarray) -> float:
    ea, eb = edge_map(a), edge_map(b)
    tp = np.logical_and(ea, eb).sum()
    fp = np.logical_and(~ea, eb).sum()
    fn = np.logical_and(ea, ~eb).sum()
    p = tp / (tp + fp + 1e-9)
    r = tp / (tp + fn + 1e-9)
    return float(2 * p * r / (p + r + 1e-9))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reference")
    ap.add_argument("candidate")
    ap.add_argument("--out", default="font_diff.png")
    args = ap.parse_args()
    ref = Image.open(args.reference).convert("RGB")
    cand = Image.open(args.candidate).convert("RGB")
    if ref.size != cand.size:
        raise SystemExit(f"Size mismatch: reference={ref.size}, candidate={cand.size}")
    a = np.asarray(ref).astype(np.float32) / 255.0
    b = np.asarray(cand).astype(np.float32) / 255.0
    mae = float(np.mean(np.abs(a - b)))
    ga, gb = a.mean(axis=2), b.mean(axis=2)
    ef1 = edge_f1(ga, gb)
    ssim = None
    try:
        from skimage.metrics import structural_similarity
        ssim = float(structural_similarity(ga, gb, data_range=1.0))
    except Exception:
        pass
    ImageChops.difference(ref, cand).save(args.out)
    print(f"MAE: {mae:.6f}")
    print(f"Edge F1: {ef1:.6f}")
    print("SSIM:", f"{ssim:.6f}" if ssim is not None else "N/A (install scikit-image)")
    print(f"Diff saved to: {Path(args.out).resolve()}")

if __name__ == "__main__":
    main()
