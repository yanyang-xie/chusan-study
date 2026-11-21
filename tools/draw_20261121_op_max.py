#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""20261121 圆最值题配图（OP 最大值 = √3+1）
   图1：OP 取最大值时的构型
   图2：P 点的轨迹 = 以 AC 为直径的圆
   坐标：O(0,0) 半径2，A(0,2)、B(0,-2)、F(0,-1)、C(-√3,-1)、D(√3,-1)
"""
import math
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

plt.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "questions", "数学", "images", "2026-11")
os.makedirs(OUT, exist_ok=True)

r3 = math.sqrt(3.0)
O = np.array([0.0, 0.0])
A = np.array([0.0, 2.0])
B = np.array([0.0, -2.0])
F = np.array([0.0, -1.0])
C = np.array([-r3, -1.0])
D = np.array([r3, -1.0])
Q = (A + C) / 2                                  # AC 中点，P 轨迹圆心，OQ = 1
# OP 取最大值时的 P 与对应的 E（解析解，下面用 assert 逐项校验）
Pm = np.array([-(3.0 + r3) / 2.0, (1.0 + r3) / 2.0])
Em = np.array([-1.0, r3])
assert abs(np.linalg.norm(Q - O) - 1.0) < 1e-9              # OQ = 1
assert abs(np.linalg.norm(Pm - Q) - r3) < 1e-9              # QP = 半径 √3
assert abs(np.linalg.norm(Pm - O) - (r3 + 1.0)) < 1e-9      # OP = √3 + 1
assert abs(np.linalg.norm(Em - O) - 2.0) < 1e-9             # E 在 ⊙O 上
assert abs(float(np.cross(Em - A, Pm - A))) < 1e-9          # A、E、P 共线
assert abs(float(np.dot(Em - A, Pm - C))) < 1e-9            # CP ⊥ AE
assert abs(float(np.cross(Q - O, Pm - O))) < 1e-9           # O、Q、P 共线


def right_angle(ax, vertex, p1, p2, size=0.12, color="#777777"):
    v = np.array(vertex, dtype=float)
    u1 = np.array(p1, dtype=float) - v
    u1 = u1 / np.linalg.norm(u1)
    u2 = np.array(p2, dtype=float) - v
    u2 = u2 / np.linalg.norm(u2)
    pts = [v + size * u1, v + size * (u1 + u2), v + size * u2]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=1.2, zorder=6)


def base_frame(ax):
    ax.add_patch(Circle(O, 2.0, fill=False, lw=2.0, color="#222222"))
    ax.plot([A[0], B[0]], [A[1], B[1]], color="#222222", lw=1.4)
    ax.plot([C[0], D[0]], [C[1], D[1]], color="#222222", lw=1.4)
    right_angle(ax, F, A, D, size=0.14)
    for pt, name, dx, dy in [(O, "O", -0.30, -0.02), (A, "A", -0.26, 0.12),
                             (B, "B", -0.10, -0.30), (C, "C", -0.30, -0.06),
                             (D, "D", 0.14, -0.06), (F, "F", 0.13, -0.24)]:
        ax.plot(pt[0], pt[1], "o", ms=4.5, color="#222222", zorder=6)
        ax.text(pt[0] + dx, pt[1] + dy, name, fontsize=15, zorder=7)


def finish(ax, title, extra):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-3.2, 2.5)
    ax.set_ylim(-2.6, 2.55)
    ax.text(-3.15, 2.35, title, fontsize=13.5, color="#333333")
    ax.text(-3.15, -2.42, extra, fontsize=13, color="#7b3fa0")


# ---------------- 图1：OP 取最大值 ----------------
fig, ax = plt.subplots(figsize=(8.4, 6.9))
base_frame(ax)
ax.add_patch(Circle(Q, r3, fill=False, lw=1.7, ls=(0, (5, 4)), color="#1f77b4"))
ax.plot([A[0], C[0]], [A[1], C[1]], lw=1.3, ls=(0, (6, 3)), color="#1f77b4")
ax.plot([A[0], Em[0]], [A[1], Em[1]], lw=1.5, color="#2ca02c")
ax.plot([C[0], Pm[0]], [C[1], Pm[1]], lw=1.5, color="#d62728")
ax.plot([Pm[0], O[0], Q[0]], [Pm[1], O[1], Q[1]], lw=2.4, color="#7b3fa0")
right_angle(ax, Pm, C, A, size=0.13)
for pt, name, dx, dy, col in [(Q, "Q", -0.06, 0.20, "#1f77b4"),
                              (Pm, "P", -0.34, 0.22, "#d62728"),
                              (Em, "E", 0.10, 0.20, "#2ca02c")]:
    ax.plot(pt[0], pt[1], "o", ms=5, color=col, zorder=6)
    ax.text(pt[0] + dx, pt[1] + dy, name, fontsize=15, color=col, zorder=7)


def side_label(ax, p, q, text_, offset, col, fs=13):
    """把标注文字放在线段 p-q 的中点，再沿法向平移 offset"""
    v = np.array(q, dtype=float) - np.array(p, dtype=float)
    n = np.array([-v[1], v[0]])
    n = n / np.linalg.norm(n)
    m = (np.array(p, dtype=float) + np.array(q, dtype=float)) / 2 + offset * n
    ax.text(m[0], m[1], text_, fontsize=fs, color=col,
            ha="center", va="center", zorder=8,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=.85))


side_label(ax, O, Q, "OQ = 1", -0.30, "#7b3fa0")
side_label(ax, Q, Pm, "QP = √3（半径）", -0.34, "#1f77b4", fs=12.5)
side_label(ax, O, Pm, "OP = 1 + √3", 0.36, "#7b3fa0")
finish(ax, "OP 最大时：O、Q、P 三点共线，Q 在 O 和 P 中间",
       "P 跑到 ⊙O 外面了，但它到 Q 的距离永远是 √3")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "20261121-01.png"), dpi=200)
fig.savefig(os.path.join(OUT, "20261121-01.svg"))
plt.close(fig)

# ---------------- 图2：P 的轨迹 ----------------
fig, ax = plt.subplots(figsize=(8.4, 6.9))
base_frame(ax)
ax.add_patch(Circle(Q, r3, fill=False, lw=2.0, color="#1f77b4"))
ax.plot([A[0], C[0]], [A[1], C[1]], lw=1.6, color="#1f77b4")
ax.plot(Q[0], Q[1], "o", ms=5, color="#1f77b4", zorder=6)
ax.text(Q[0] - 0.10, Q[1] + 0.18, "Q", fontsize=15, color="#1f77b4")
for i, ang in enumerate([0.9, 1.9, 2.9]):
    E = np.array([2 * math.cos(ang), 2 * math.sin(ang)])
    d = (E - A) / np.linalg.norm(E - A)
    P = A + float(np.dot(C - A, d)) * d
    ax.plot([A[0], E[0]], [A[1], E[1]], lw=1.2, color="#2ca02c", alpha=.8)
    ax.plot([C[0], P[0]], [C[1], P[1]], lw=1.2, color="#d62728", alpha=.8)
    ax.plot(E[0], E[1], "o", ms=4.5, color="#2ca02c")
    ax.plot(P[0], P[1], "o", ms=5, color="#d62728")
    # E 的标注沿"圆心向外"方向放，P 的标注沿"轨迹圆心 Q 向外"方向放，避免压线
    re_ = E / np.linalg.norm(E)
    rp_ = (P - Q) / np.linalg.norm(P - Q)
    ax.text(E[0] + 0.30 * re_[0], E[1] + 0.30 * re_[1], f"E{i+1}", fontsize=12.5,
            color="#2ca02c", ha="center", va="center")
    ax.text(P[0] + 0.34 * rp_[0], P[1] + 0.34 * rp_[1], f"P{i+1}", fontsize=12.5,
            color="#d62728", ha="center", va="center")
    right_angle(ax, P, C, A, size=0.11)
ax.plot([Pm[0], O[0], Q[0]], [Pm[1], O[1], Q[1]], lw=2.0, color="#7b3fa0")
ax.plot(Pm[0], Pm[1], "o", ms=5.5, color="#7b3fa0", zorder=6)
ax.annotate("紫色这条线拉到最头的 P，就是 OP 最大的时刻（见图1）",
            xy=(Pm[0], Pm[1]), xytext=(-3.05, -1.35),
            fontsize=12, color="#7b3fa0",
            arrowprops=dict(arrowstyle="->", color="#7b3fa0", lw=1.2,
                            connectionstyle="arc3,rad=-0.2"))
finish(ax, "∠APC 永远是 90° ⇒ P 只能落在以 AC 为直径的蓝色虚线圆上",
       "O 到这个蓝圆最远的点 = OQ + 半径 = 1 + √3")
ax.set_ylim(-2.75, 2.55)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "20261121-02.png"), dpi=200)
fig.savefig(os.path.join(OUT, "20261121-02.svg"))
plt.close(fig)

print("saved")
for f in sorted(os.listdir(OUT)):
    print(" ", f)
