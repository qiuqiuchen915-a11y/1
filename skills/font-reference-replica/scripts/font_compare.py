#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageChops

def load_rgba(path):
    return Image.open(path).convert("RGBA")

def arr_rgb(im):
    return np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0

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

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("reference")
    ap.add_argument("candidate")
    ap.add_argument("--diff", default="font_diff.png")
    args=ap.parse_args()

    r=load_rgba(args.reference)
    c=load_rgba(args.candidate)
    if r.size != c.size:
        raise SystemExit(f"Size mismatch: {r.size} vs {c.size}")

    ra=arr_rgb(r); ca=arr_rgb(c)
    rg=grayscale(ra); cg=grayscale(ca)
    mae=float(np.mean(np.abs(ra-ca)))
    edgef=f1(edge(rg),edge(cg))

    ralpha=np.asarray(r)[...,3]/255.0
    calpha=np.asarray(c)[...,3]/255.0
    iou=mask_iou(ralpha,calpha)

    ssim=None
    try:
        from skimage.metrics import structural_similarity
        ssim=float(structural_similarity(rg,cg,data_range=1.0))
    except Exception:
        pass

    ImageChops.difference(r,c).save(args.diff)

    print(f"MAE: {mae:.6f}")
    print(f"Edge F1: {edgef:.6f}")
    print(f"Alpha IoU: {iou:.6f}")
    print("SSIM:", f"{ssim:.6f}" if ssim is not None else "N/A")
    print("Diff:", Path(args.diff).resolve())

if __name__=="__main__":
    main()
