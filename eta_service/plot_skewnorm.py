from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skewnorm


def plot_skewnorm_distribution(mean=0.7, stdev=0.1, skewness=-5):
    # The default params are params for a sample distribution
    # mu=mean, nu=median, sigma=stdev, gamma=skewness
    # Negative values are left skewed, positive values are right skewed

    distribution = skewnorm(a=skewness, loc=mean, scale=stdev)
    skewnorm_mean = round(distribution.mean(), 4)
    skewnorm_median = round(distribution.median(), 4)
    skewnorm_stdev = round(distribution.std(), 4)
    minus1_skewnorm_stdev = round(distribution.mean() - distribution.std(), 4)
    plus1_skewnorm_stdev = round(distribution.mean() + distribution.std(), 4)
    minus2_skewnorm_stdev = round(distribution.mean() - 2 * distribution.std(), 4)
    plus2_skewnorm_stdev = round(distribution.mean() + 2 * distribution.std(), 4)

    text = rf"""
    $\mu$ = {mean}
    $\sigma$ = {stdev}
    $\gamma$ = {skewness}

    Skewed $\mu$ = {skewnorm_mean}
    Skewed $\nu$ = {skewnorm_median}
    Skewed $\sigma$ = {skewnorm_stdev}

    Skewed +/- $\sigma$ = [{minus1_skewnorm_stdev}, {plus1_skewnorm_stdev}]
    Skewed +/- 2$\sigma$ = [{minus2_skewnorm_stdev}, {plus2_skewnorm_stdev}]
    """

    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    sample_pts = np.linspace(0, 1, 10000)
    ax.plot(sample_pts, distribution.pdf(sample_pts))

    # Mean
    ax.axvline(x=skewnorm_mean, color="red", ls="--", lw=0.75)
    ax.text(
        skewnorm_mean,
        0.99,
        s=rf"$\mu$, {skewnorm_mean}",
        fontsize=8,
        horizontalalignment="right",
        verticalalignment="top",
        rotation=90,
        transform=ax.transAxes,
    )
    # 1 stdev
    ax.axvline(x=minus1_skewnorm_stdev, color="salmon", ls="--", lw=0.75)
    ax.axvline(x=plus1_skewnorm_stdev, color="salmon", ls="--", lw=0.75)
    ax.text(
        minus1_skewnorm_stdev,
        0.99,
        s=rf"-$\sigma$, {minus1_skewnorm_stdev}",
        fontsize=8,
        horizontalalignment="right",
        verticalalignment="top",
        rotation=90,
        transform=ax.transAxes,
    )
    ax.text(
        plus1_skewnorm_stdev,
        0.99,
        s=rf"+$\sigma$, {plus1_skewnorm_stdev}",
        fontsize=8,
        horizontalalignment="right",
        verticalalignment="top",
        rotation=90,
        transform=ax.transAxes,
    )
    # 2 stdev
    ax.axvline(x=minus2_skewnorm_stdev, color="pink", ls="--", lw=0.75)
    ax.axvline(x=plus2_skewnorm_stdev, color="pink", ls="--", lw=0.75)
    ax.text(
        minus2_skewnorm_stdev,
        0.99,
        s=rf"-2$\sigma$, {minus2_skewnorm_stdev}",
        fontsize=8,
        horizontalalignment="right",
        verticalalignment="top",
        rotation=90,
        transform=ax.transAxes,
    )
    ax.text(
        plus2_skewnorm_stdev,
        0.99,
        s=rf"+2$\sigma$, {plus2_skewnorm_stdev}",
        fontsize=8,
        horizontalalignment="right",
        verticalalignment="top",
        rotation=90,
        transform=ax.transAxes,
    )
    # Info
    ax.text(
        0.05, 0.9, s=text, fontsize=11, verticalalignment="top", transform=ax.transAxes
    )

    # Axis and labels
    ax.set_xlim(0, 1)
    ax.set_xticks(np.linspace(0, 1, 11), minor=False)
    ax.set_ylim(ymin=0)
    ax.set_xlabel("Percentage")
    ax.set_ylabel("Density")
    ax.set_title(
        rf"Probability Density Function ($\mu$={mean}, $\sigma$={stdev}, $\gamma$={skewness})"
    )

    # Save image
    Path("./sample_distributions").mkdir(parents=True, exist_ok=True)
    fig.savefig(
        f"./sample_distributions/PDF_mean{mean}_stdev{stdev}_skewness{skewness}.png"
    )


if __name__ == "__main__":
    plot_skewnorm_distribution(mean=0.7, stdev=0.1, skewness=-5)
