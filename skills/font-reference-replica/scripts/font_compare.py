#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageChops

def load_rgba(path):
    return Image.open(path).convert("RGBA")

def arr_rgb(im):
    # Composite before discarding alpha: invisible RGB must not affect QA.
    white = Image.new("RGBA", im.size, "white")
    return np.asarray(Image.alpha_composite(white, im).convert("RGB"),
                      dtype=np.float32) / 255.0

def grayscale(a):
    return a[...,0]*0.299 + a[...,1]*0.587 + a[...,2]*0.114

def edge(gray):
    gx = np.abs(np.diff(gray, axis=1, prepend=gray[:, :1]))
    gy = np.abs(np.diff(gray, axis=0, prepend=gray[:1, :]))
    return np.hypot(gx, gy) > 0.10

def f1(a,b):
    tp = np.logical_and(a,b).sum()
    fp = np.logical_and(~a,b).sum()
    fn = np.logical_and(a,~b).sum()
    p = tp/(tp+fp+1e-9)
    r = tp/(tp+fn+1e-9)
    return float(2*p*r/(p+r+1e-9))

def mask_iou(a,b,thr=0.5):
    aa=a>thr; bb=b>thr
    inter=np.logical_and(aa,bb).sum()
    union=np.logical_or(aa,bb).sum()
    return float(inter/(union+1e-9))

def glyph_mask(im, mask_path=None, tolerance=16):
    """Return (binary glyph mask, source); auto RGB assumes a plain border."""
    if mask_path:
        with Image.open(mask_path) as mask:
            if mask.size != im.size:
                raise ValueError("Mask size mismatch")
            return np.asarray(mask.convert("L")) > 127, "explicit"
    rgba = np.asarray(im)
    alpha = rgba[..., 3]
    # Only alpha with transparent background pixels can describe a silhouette.
    if np.any(alpha <= 127):
        return alpha > 127, "alpha"
    rgb = rgba[..., :3].astype(np.float32)
    border = np.concatenate((rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]))
    background = np.median(border, axis=0)
    if np.any(np.max(np.abs(border - background), axis=1) > tolerance):
        raise ValueError("Non-uniform border: supply an explicit glyph mask")
    return np.max(np.abs(rgb - background), axis=2) > tolerance, "border-rgb"


def component_count(mask):
    """Count 8-connected foreground components without optional dependencies."""
    pending = set(zip(*np.nonzero(mask)))
    count = 0
    while pending:
        stack = [pending.pop()]
        count += 1
        while stack:
            y, x = stack.pop()
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    neighbor = (y + dy, x + dx)
                    if neighbor in pending:
                        pending.remove(neighbor)
                        stack.append(neighbor)
    return count


def region_metrics(reference, candidate, box):
    x0, y0, x1, y1 = box
    h, w = reference.shape
    if candidate.shape != reference.shape:
        raise ValueError("Mask size mismatch")
    if not (0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h):
        raise ValueError("ROI must be non-empty and inside the image")
    a, b = reference[y0:y1, x0:x1], candidate[y0:y1, x0:x1]
    iou = mask_iou(a, b) if np.logical_or(a, b).any() else None
    return iou, f1(edge(a.astype(float)), edge(b.astype(float))), component_count(a), component_count(b)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("reference")
    ap.add_argument("candidate")
    ap.add_argument("--diff", default="font_diff.png")
    ap.add_argument("--reference-mask", help="white glyph / black background mask")
    ap.add_argument("--candidate-mask", help="white glyph / black background mask")
    ap.add_argument("--background-tolerance", type=int, default=16,
                    help="RGB distance from plain border background (0..254)")
    ap.add_argument("--roi", type=int, nargs=4, action="append", default=[],
                    metavar=("X0", "Y0", "X1", "Y1"),
                    help="repeat for aligned junction crops; end coordinates exclusive")
    args=ap.parse_args()
    if not 0 <= args.background_tolerance <= 254:
        ap.error("--background-tolerance must be between 0 and 254")

    r=load_rgba(args.reference)
    c=load_rgba(args.candidate)
    if r.size != c.size:
        raise SystemExit(f"Size mismatch: {r.size} vs {c.size}")

    ra=arr_rgb(r); ca=arr_rgb(c)
    rg=grayscale(ra); cg=grayscale(ca)
    mae=float(np.mean(np.abs(ra-ca)))
    edgef=f1(edge(rg),edge(cg))

    try:
        rm, rs = glyph_mask(r, args.reference_mask, args.background_tolerance)
        cm, cs = glyph_mask(c, args.candidate_mask, args.background_tolerance)
    except ValueError as exc:
        ap.error(str(exc))
    iou = mask_iou(rm, cm) if np.logical_or(rm, cm).any() else None

    try:
        regions = [(box, region_metrics(rm, cm, box)) for box in args.roi]
    except ValueError as exc:
        ap.error(str(exc))

    ssim=None
    try:
        from skimage.metrics import structural_similarity
        ssim=float(structural_similarity(rg,cg,data_range=1.0))
    except ImportError:
        pass
    except ValueError as exc:
        print("SSIM unavailable:", exc)

    # RGB diff is visible even when the two alpha channels are identical.
    ImageChops.difference(
        Image.fromarray(np.rint(ra * 255).astype(np.uint8)),
        Image.fromarray(np.rint(ca * 255).astype(np.uint8))).save(args.diff)

    print(f"MAE: {mae:.6f}")
    print(f"Edge F1: {edgef:.6f}")
    print("Glyph mask IoU:", f"{iou:.6f}" if iou is not None else "N/A (empty masks)")
    print(f"Mask sources: {rs} / {cs}")
    print(f"Mask Edge F1: {f1(edge(rm.astype(float)), edge(cm.astype(float))):.6f}")
    print("Note: aligned glyph crops required; MAE/Edge F1/SSIM include background and effects.")
    print("SSIM:", f"{ssim:.6f}" if ssim is not None else "N/A")
    for box, (local_iou, local_edge, rc, cc) in regions:
        score = f"{local_iou:.6f}" if local_iou is not None else "N/A (empty masks)"
        print(f"ROI {tuple(box)}: IoU={score}; Mask Edge F1={local_edge:.6f}; components(8)={rc}/{cc}")
        if rc != cc:
            print("Warning: ROI connectivity differs; inspect bridges, gaps and segmentation.")
    print("Diff:", Path(args.diff).resolve())

if __name__=="__main__":
    main()
