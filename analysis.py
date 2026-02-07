import glob, argparse, os
import pandas as pd

#Take GEMAPS table for each file and add it to its respective AU summaries row 
def combineTables(gemaps_directory):
  pass

#Run regression(?) analysis
def PLSRegression():
  pass


#main() sets up directory to point to
def main():
  parser = argparse.ArgumentParser(description="Analyzing CSV data.")
  parser.add_argument("--au_tables", type=str, description="Directory path linking to Action Unit tables.")
  parser.add_argument("--gemaps_tables", type=str, description="Directory path linking to GEMAPS tables.")
  parser.add_argument("--output_path", type=str, description="Directory path to output combined AU/GEMAPS tables to.")
  args = parser.parse_args()

  #Find all existing GEMAPS tables, combine them into AU summaries table
  gemaps_tables = glob.glob(f"{args.gemaps_tables}/*.csv")
  if len(gemaps_tables) == 0:
    raise RuntimeError(f"no GEMAPS tables found in directory '{args.gemaps_tables}'")
  if os.path.exists(f"{args.au_tables}/summaries.csv"):
    combineTables(gemaps_tables)
  else:
    raise RuntimeError(f"AU summary table doesn't exist at '{args.au_tables}/summaries.csv'")

  #Run PLS regression on a specifed column/acoustic cue
  PLSRegression()
  

if __name__ == "__main__":
  main()
