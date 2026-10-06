"""Neuron Zoo: five firing personalities from the Izhikevich (2003) model.

Run:  python zoo.py   ->  assets/neuron_zoo.png
"""
import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, PANEL, INK, MUTE = "#0d1117", "#161b22", "#e6edf3", "#8b949e"
PINK, LAV, MINT, PEACH, SKY = "#ff7eb6", "#b794f6", "#7ee8c7", "#ffb86b", "#79c0ff"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": PANEL, "savefig.facecolor": BG,
    "text.color": INK, "axes.labelcolor": MUTE, "xtick.color": MUTE,
    "ytick.color": MUTE, "axes.edgecolor": "#30363d", "font.size": 10,
})

# name, tagline, (a, b, c, d), input current, colour
ZOO = [
    ("Regular spiking", "the chill cortical workhorse", (0.02, 0.2, -65, 8), 14, PINK),
    ("Intrinsically bursting", "opens with a flurry, then settles", (0.02, 0.2, -55, 4), 10, LAV),
    ("Chattering", "rapid-fire mini bursts", (0.02, 0.2, -50, 2), 10, MINT),
    ("Fast spiking", "the inhibitory speed demon", (0.1, 0.2, -65, 2), 10, PEACH),
    ("Low-threshold spiking", "slow to start, steady beat", (0.02, 0.25, -65, 2), 10, SKY),
]


def simulate(params, current, T=200.0, dt=0.25, t_on=20.0):
    """Euler-integrate the Izhikevich neuron. Returns (time_ms, voltage_mV)."""
    a, b, c, d = params
    n = int(T / dt)
    v, u = -65.0, b * -65.0
    vs = np.empty(n)
    for k in range(n):
        i_in = current if k * dt >= t_on else 0.0
        v += dt * (0.04 * v * v + 5 * v + 140 - u + i_in)
        u += dt * a * (b * v - u)
        if v >= 30:
            vs[k] = 30
            v, u = c, u + d
        else:
            vs[k] = v
    return np.arange(n) * dt, vs


def glow(ax, x, y, color):
    for lw, alpha in ((7, 0.06), (4, 0.12), (2.2, 0.25), (1.2, 1.0)):
        ax.plot(x, y, color=color, lw=lw, alpha=alpha, solid_capstyle="round")


def main():
    os.makedirs("assets", exist_ok=True)
    fig, axes = plt.subplots(3, 2, figsize=(13, 8.5))
    axes = axes.ravel()
    for ax, (name, tag, params, current, color) in zip(axes, ZOO):
        t, v = simulate(params, current)
        glow(ax, t, v, color)
        ax.set_ylim(-85, 58)
        ax.set_title(name, loc="left", color=color, fontweight="bold", fontsize=12)
        ax.text(0.99, 0.92, tag, transform=ax.transAxes, ha="right", color=MUTE, fontsize=9, style="italic")
        ax.set_ylabel("mV")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[3].set_xlabel("time (ms)")
    axes[4].set_xlabel("time (ms)")

    info = axes[5]
    info.axis("off")
    info.text(0.0, 0.95, "Neuron Zoo", fontsize=22, fontweight="bold", color=PINK, va="top")
    info.text(0.0, 0.70, "Same equation, five personalities.\nTweak four numbers (a, b, c, d)\nand a neuron changes how it spikes.", fontsize=10.5, color=INK, va="top", linespacing=1.3)
    info.text(0.0, 0.30, "v' = 0.04v\u00b2 + 5v + 140 - u + I\nu' = a(bv - u)\nif v \u2265 30 mV:  v \u2190 c,  u \u2190 u + d", fontsize=10, color=LAV, family="monospace", va="top", linespacing=1.3)

    fig.tight_layout(pad=2)
    fig.savefig("assets/neuron_zoo.png", dpi=130)
    print("saved assets/neuron_zoo.png")


if __name__ == "__main__":
    main()
