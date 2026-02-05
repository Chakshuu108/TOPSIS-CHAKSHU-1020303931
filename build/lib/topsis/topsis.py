import sys
import pandas as pd
import numpy as np


def main():
    if len(sys.argv) != 5:
        print("Usage: topsis <inputfile> <weights> <impacts> <outputfile>")
        sys.exit(1)

    input_file, weights, impacts, output_file = sys.argv[1:]

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print("Error: File not found")
        sys.exit(1)

    if df.shape[1] < 3:
        print("Error: File must have 3 or more columns")
        sys.exit(1)

    data = df.iloc[:, 1:]

    try:
        data = data.astype(float)
    except:
        print("Error: Columns must be numeric")
        sys.exit(1)

    weights = list(map(float, weights.split(',')))
    impacts = impacts.split(',')

    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        print("Error: Weights, impacts and columns mismatch")
        sys.exit(1)

    for i in impacts:
        if i not in ['+', '-']:
            print("Error: Impacts must be + or -")
            sys.exit(1)

    norm = data / np.sqrt((data ** 2).sum())
    weighted = norm * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    d_pos = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = d_neg / (d_pos + d_neg)

    df['Topsis Score'] = score
    df['Rank'] = score.rank(ascending=False).astype(int)

    df.to_csv(output_file, index=False)
    print("TOPSIS completed successfully")
