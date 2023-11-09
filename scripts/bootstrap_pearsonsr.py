"""This script analyses results files produced by singuularity containers and
calculates the bootstrapped Pearson's R between predicted and true pK values.
"""

from scipy import stats
import numpy as np
import pandas as pd
from glob import glob


def bootstrap_pearsonr_calculate(y_true, y_pred, n_samples=10000, seed=42):
    """Estimates a two-sided 95% confidence interval for the Pearson
    correlation coefficient using the bootstrap method."""
    assert len(y_true) == len(y_pred)
    indices = np.arange(len(y_true))
    coefficients = []
    r = stats.pearsonr(y_true, y_pred)[0]
    rng = np.random.default_rng(seed)
    for i in range(n_samples):
        sample_indices = rng.choice(indices, size=len(indices), replace=True)
        y_true_sample = y_true[sample_indices]
        y_pred_sample = y_pred[sample_indices]
        r_boot = stats.pearsonr(y_true_sample, y_pred_sample)[0]
        coefficients.append(r_boot)
    quantiles = np.quantile(coefficients, q=[0.025, 0.975])
    return r, quantiles


def wrapped_boostrap_pearsonr(filename):
    df = pd.read_csv(filename)
    pred = df["pred"]
    true = df["pk"]
    return bootstrap_pearsonr_calculate(true, pred)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate Pearson's R using the bootstrap method."
    )
    parser.add_argument(
        "--filename",
        type=str,
        help="Path to the file containing the predicted and true pK values or \
            regex expression for multiple files wrapped in quotes.",
    )
    args = parser.parse_args()
    if "*" in args.filename:
        filenames = glob(args.filename)
        for filename in filenames:
            r, quantiles = wrapped_boostrap_pearsonr(filename)
            print(f"{filename}: {r} ({quantiles[0]}, {quantiles[1]})")
    else:
        r, quantiles = wrapped_boostrap_pearsonr(args.filename)
        print(f"{args.filename}: {r} ({quantiles[0]}, {quantiles[1]})")
