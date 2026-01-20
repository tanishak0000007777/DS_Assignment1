import sys
import pandas as pd
import numpy as np
import os

def error(msg):
    print(f"Error: {msg}")
    sys.exit(1)

def main():
    # 1. Check number of arguments
    if len(sys.argv) != 5:
        error("Incorrect number of parameters.\nUsage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    # 2. Check if input file exists
    if not os.path.isfile(input_file):
        error("Input file not found")

    # 3. Read CSV
    try:
        df = pd.read_csv(input_file)
    except:
        error("Unable to read input file")

    # 4. Check minimum columns
    if df.shape[1] < 3:
        error("Input file must contain three or more columns")

    data = df.iloc[:, 1:]

    # 5. Check numeric values
    if not np.all(data.applymap(lambda x: isinstance(x, (int, float)))):
        error("From 2nd to last columns must contain numeric values only")

    # 6. Parse weights & impacts
    try:
        weights = list(map(float, weights.split(",")))
    except:
        error("Weights must be numeric and comma separated")

    impacts = impacts.split(",")

    # 7. Validate weights & impacts length
    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        error("Number of weights, impacts and columns must be the same")

    # 8. Validate impacts
    for i in impacts:
        if i not in ['+', '-']:
            error("Impacts must be either + or -")

    # ---------------- TOPSIS CALCULATION ---------------- #

    # Step 1: Normalize
    norm_data = data / np.sqrt((data ** 2).sum())

    # Step 2: Apply weights
    weighted_data = norm_data * weights

    # Step 3: Ideal best & worst
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted_data.iloc[:, i].max())
            ideal_worst.append(weighted_data.iloc[:, i].min())
        else:
            ideal_best.append(weighted_data.iloc[:, i].min())
            ideal_worst.append(weighted_data.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Step 4: Distance calculation
    dist_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # Step 5: TOPSIS score
    score = dist_worst / (dist_best + dist_worst)

    # Step 6: Ranking
    df["Topsis Score"] = score
    df["Rank"] = score.rank(ascending=False).astype(int)

    # 9. Save output
    df.to_csv(output_file, index=False)
    print("TOPSIS analysis completed successfully.")

if __name__ == "__main__":
    main()
