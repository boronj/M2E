import argparse, feat, sys
from pathlib import Path
from tqdm import tqdm
import pandas as pd

def find_videos(path: Path):
	return [
    	item for item in path.rglob('*')
    	if item.is_file() and item.suffix.lower() in {'.mp4', '.avi', '.mov'}
	]

def summarize_video(per_frame_df):
	'''
	Returns probabilities of emotions + the top emotion.
	per_frame_def: pd.DataFrame (has probabilities for top emotions)
	'''
	out = {"video": list(set(per_frame_df['input']))[0]}
	emo_cols = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise', 'neutral']
	if set(emo_cols).issubset(per_frame_df.columns):
		emo_means = per_frame_df[emo_cols].mean(skipna=True)
		out.update({f"emo_{c}_mean": float(emo_means[c]) for c in emo_cols})
		top = emo_means.idxmax()
		out["top_emotion"] = top
		out["top_emotion_mean_prob"] = float(emo_means[top])
	return pd.Series(out)


# ----- main pipeline -----


def main():
	parser = argparse.ArgumentParser(description="Analyze videos with Py-Feat and export AU/emotion tables.")
	parser.add_argument("--input", type=str, default="videos_input", help="Folder with videos")
	parser.add_argument("--out", type=str, default="outputs", help="Output folder")
	parser.add_argument("--overwrite", action="store_true", help="Overwrite existing per-frame CSVs")
	args = parser.parse_args()


	in_dir = Path(args.input)
	out_root = Path(args.out)
	per_frame_dir = out_root / "per_frame_csv"
	per_frame_dir.mkdir(parents=True, exist_ok=True)


	# Initialize detector once
	detector = feat.Detector()


	summaries = []


	videos = list(find_videos(in_dir))
	if not videos:
		print(f"No videos found in {in_dir.resolve()}. Add .mp4/.mov/etc. files first.", file=sys.stderr)
		sys.exit(1)


	for vid in tqdm(videos, desc="Analyzing videos"):
		stem = vid.stem
		per_frame_csv = per_frame_dir / f"{stem}.csv"


		if per_frame_csv.exists() and not args.overwrite:
			df = pd.read_csv(per_frame_csv)
		else:
			try:
				fex = detector.detect_video(str(vid), skip_frames = 10)
			except Exception as e:
				print(f"[WARN] Skipping {vid.name}: {e}", file=sys.stderr)
				continue

			df = pd.DataFrame(fex)
			
			df.to_csv(per_frame_csv, index=False)


			summary_row = summarize_video(df)
			summaries.append(summary_row)


	out_summary = out_root / "summaries.csv"
	summary_df = pd.DataFrame(summaries)
	summary_df.sort_values("video").to_csv(out_summary, index=False)


	print(f"\nDone.\nPer-frame CSVs: {per_frame_dir.resolve()}\nSummary table: {out_summary.resolve()}")


if __name__ == "__main__":
	main()
