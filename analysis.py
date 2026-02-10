import glob, argparse, os
import pandas as pd
from tqdm import tqdm
from colorama import Fore, Style
from m2e.error_handling import throw_error

#Take GEMAPS table for each file and add it to its respective AU summaries row 
def combineTables(gemaps_directory, au_tables_path, output_path):
  try:
    au_dataset = pd.read_csv(au_tables_path)
  except Exception as e:
    throw_error("dataset failed to load", e)
  else:
    #Create columns in au_dataset to support GEMAPS columns
    gemaps_column_names = list(pd.read_csv(gemaps_directory[0]).columns)
    for column in tqdm(gemaps_column_names, desc = "Adding GEMAPS columns: ", total = len(gemaps_column_names)):
      au_dataset[column] = [0]*len(au_dataset)

    #Merge values into au_dataset 
    for i in tqdm(au_dataset.index, desc = "Combining datasets: ", total = len(au_dataset.index)):
      #Check in gemaps_directory for an equivalent file
      video_file = str(au_dataset.at[i, "video"]) #.../.../.../xxx.csv
      
      if video_file.replace(".csv",".mp4") in gemaps_directory:
        #If it is in au_dataset, access the values from that file
        gemaps_dataset = pd.read_csv(video_file)
        assert len(list(gemaps_dataset.columns)) == len(gemaps_column_names), "Amount of columns in GEMAPS dataset doesn't align" #Idk if this will actually go through or not and I don't want to check manually
        #Load them one-by-one into au_dataset
        for column in tqdm(list(gemaps_dataset.columns), desc = "Combining columns: ", total = len(list(gemaps_dataset.columns))):
          au_dataset.at[i, column] = gemaps_dataset[0][column]

    #Return the new AU dataset, and also export it into a new thing
    au_dataset.to_csv(output_path, index = False)
    return au_dataset

#Run regression(?) analysis
def PLSRegression():
  pass


#main() sets up directory to point to
def main():
  parser = argparse.ArgumentParser(description="Analyzing CSV data.")
  parser.add_argument("--au_tables", type=str, description="Directory path linking to Action Unit tables.")
  parser.add_argument("--gemaps_tables", type=str, description="Directory path linking to GEMAPS tables.")
  parser.add_argument("--output_path", type=str, description="Absolute path to output combined AU/GEMAPS tables to.")
  args = parser.parse_args()

  #Find all existing GEMAPS tables, combine them into AU summaries table
  gemaps_tables = glob.glob(f"{args.gemaps_tables}/*.csv")
  if len(gemaps_tables) == 0:
    raise RuntimeError(f"no GEMAPS tables found in directory '{args.gemaps_tables}'")
  if os.path.exists(f"{args.au_tables}/summaries.csv"):
    combineTables(gemaps_tables, f"{args.au_tables}/summaries.csv")
  else:
    raise RuntimeError(f"AU summary table doesn't exist at '{args.au_tables}/summaries.csv'")

  #Run PLS regression on a specifed column/acoustic cue
  PLSRegression()
  

if __name__ == "__main__":
  main()
