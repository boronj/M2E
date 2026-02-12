import glob, argparse, os, pprint
import pandas as pd
import numpy as np
from tqdm import tqdm
from colorama import Fore, Style
from m2e.error_handling import throw_error
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

MEASURED_METRIC = "loudness_sma3_amean"

#Take GEMAPS table for each file and add it to its respective AU summaries row 
def combine_tables(gemaps_directory, gemaps_tables_path, au_tables_path, output_path):
  try:
    au_dataset = pd.read_csv(au_tables_path)
  except Exception as e:
    throw_error("dataset failed to load", e)
  else:
    #Create columns in au_dataset to support GEMAPS columns
    gemaps_column_names = list(pd.read_csv(gemaps_directory[0]).columns)
    for column in tqdm(gemaps_column_names, desc = "Adding GEMAPS columns: ", total = len(gemaps_column_names)):
      au_dataset[column] = [0]*len(au_dataset)

    print(gemaps_directory)
      
    #Merge values into au_dataset 
    for i in tqdm(au_dataset.index, desc = "Combining datasets: ", total = len(au_dataset.index)):
      #Check in gemaps_directory for an equivalent file
      video_file = str(au_dataset.at[i, "video"]).split("/") #.../.../.../xxx.mp4
      video_file = video_file[len(video_file)-1].replace(".mp4", ".csv")
      video_path = gemaps_tables_path+"/"+video_file
      if video_path in gemaps_directory:
        #If it is in au_dataset, access the values from that file
        gemaps_dataset = pd.read_csv(video_path)
        assert len(list(gemaps_dataset.columns)) == len(gemaps_column_names), "Amount of columns in GEMAPS dataset doesn't align" #Idk if this will actually go through or not and I don't want to check manually
        #Load them one-by-one into au_dataset
        for column in tqdm(list(gemaps_dataset.columns), desc = "Combining columns: ", total = len(list(gemaps_dataset.columns))):
          au_dataset.at[i, column] = gemaps_dataset[column][0]

    #Return the new AU dataset, and also export it into a new thing
    au_dataset.to_csv(output_path, index = False)
    return au_dataset

#Run PLS regression model + analysis

#TO_DO: Check through dataframe (n_components is apparently set to a max 1 row, this shouldn't be the case so smth's off)
        #Figure out if *all* AU data instead of means should be put in (this isn't that hard of a change but does require another 2.5 hours of time)
        #Check if using linear regression would work better than PLS
        #Everything also runs to 0 for some reason so check for that as well

def pls_regression(x_axis, y_axis):
  x_train, x_test, y_train, y_test = train_test_split(x_axis, y_axis, test_size = 0.2, random_state=42)
  pls_model = PLSRegression(n_components=1, scale=True)
  pls_model.fit(x_train, y_train)
  y_predicted = pls_model.predict(x_test)
  mse = mean_squared_error(y_test, y_predicted)
  coefficients = pls_model.coef_
  r2 = r2_score(y_test, y_predicted)
  return (mse, coefficients, r2)

#main() sets up directory to point to
def main():
  parser = argparse.ArgumentParser(description="Analyzing CSV data.")
  parser.add_argument("--au_tables", type=str, help="Directory path linking to Action Unit tables.")
  parser.add_argument("--gemaps_tables", type=str, help="Directory path linking to GEMAPS tables.")
  parser.add_argument("--output_path", type=str, help="Absolute path to output combined AU/GEMAPS tables to.")
  args = parser.parse_args()

  #Find all existing GEMAPS tables, combine them into AU summaries table
  gemaps_tables = glob.glob(f"{args.gemaps_tables}/*.csv")
  if len(gemaps_tables) == 0:
    raise RuntimeError(f"no GEMAPS tables found in directory '{args.gemaps_tables}'")
  if os.path.exists(f"{args.au_tables}/summaries.csv"):
    dataset = combine_tables(gemaps_tables, args.gemaps_tables, f"{args.au_tables}/summaries.csv", args.output_path)
  else:
    raise RuntimeError(f"AU summary table doesn't exist at '{args.au_tables}/summaries.csv'")
    
  au_cols = [x for x in dataset.columns if "AU" in x]
  au_results = {}
  #Run PLS regression on a specifed column/acoustic cue
  for au in tqdm(au_cols, desc = "Running PLS regression: ", total = len(au_cols)):
    regression_model_results = pls_regression(dataset[MEASURED_METRIC].to_frame(MEASURED_METRIC), dataset[au].to_frame(au))
    au_results[au.split("_")[0]] = {
        "MSE": regression_model_results[0],
        "Coefficients": regression_model_results[1],
        "R^2": regression_model_results[2]
    }
      
  #Display results
  print(f"{'AU':<6} {'MSE':<6} {'Coeffs':<20} {'R^2':<10}")
  print('-'*42)
  for col in au_results:
       print(f"{col:<6} {au_results[col]['MSE']:<6.2f} {au_results[col]['MSE']:<6.2f} {au_results[col]['R^2']:<6.2f}")


if __name__ == "__main__":
  main()
