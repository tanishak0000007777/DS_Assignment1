# Import required libraries
import sys              # To read command-line arguments
import pandas as pd     # To handle CSV files and data frames
import numpy as np      # For mathematical operations
import os               # To check file existence


# Function to print error message and stop execution
def error(msg):
    print(f"Error: {msg}")
    sys.exit(1)


def main():

    # -------------------------------
    # STEP 1: CHECK COMMAND LINE INPUT
    # -------------------------------

    # The program must receive exactly 4 arguments
    # python code.py input.csv weights impacts output.csv
    if len(sys.argv) != 5:
        error("Incorrect number of parameters.\nUsage: python code.py <InputFile> <Weights> <Impacts> <OutputFile>")

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]


    # -------------------------------
    # STEP 2: CHECK INPUT FILE EXISTS
    # -------------------------------

    if not os.path.isfile(input_file):
        error("Input file not found")


    # -------------------------------
    # STEP 3: READ CSV FILE
    # -------------------------------

    try:
        df = pd.read_csv(input_file)
    except:
        error("Unable to read the input file")


    # -------------------------------
    # STEP 4: BASIC DATA VALIDATION
    # -------------------------------

    # Minimum 3 columns required
    if df.shape[1] < 3:
        error("Input file must contain three or more columns")

    # Exclude first column (identifier column)
    data = df.iloc[:, 1:]

    # Check if all values are numeric
    if not np.all(data.map(lambda x: isinstance(x, (int, float)))):
        error("From 2nd to last columns must contain numeric values only")


    # -------------------------------
    # STEP 5: PROCESS WEIGHTS & IMPACTS
    # -------------------------------

    # Convert weights string to list of floats
    try:
        weights = list(map(float, weights.split(",")))
    except:
        error("Weights must be numeric and comma separated")

    # Convert impacts string to list
    impacts = impacts.split(",")

    # Check matching lengths
    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        error("Number of weights, impacts and columns must be the same")

    # Validate impacts
    for i in impacts:
        if i not in ['+', '-']:
            error("Impacts must be either + or -")


    # -------------------------------
    # STEP 6: TOPSIS CALCULATION
    # -------------------------------

    # Step 6.1: Normalize the decision matrix
    norm_data = data / np.sqrt((data ** 2).sum())

    # Step 6.2: Apply weights
    weighted_data = norm_data * weights

    # Step 6.3: Determine ideal best and worst
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

    # Step 6.4: Calculate distance from ideal best & worst
    dist_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # Step 6.5: Calculate TOPSIS score
    topsis_score = dist_worst / (dist_best + dist_worst)


    # -------------------------------
    # STEP 7: RANKING & OUTPUT
    # -------------------------------

    df["Topsis Score"] = topsis_score
    df["Rank"] = topsis_score.rank(ascending=False).astype(int)

    # Save results to output file
    df.to_csv(output_file, index=False)

    print("TOPSIS analysis completed successfully.")


# Run the program
if __name__ == "__main__":
    main()
