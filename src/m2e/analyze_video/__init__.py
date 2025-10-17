import argparse
out[f"{col}__rate"] = float(per_frame_df[col].mean(skipna=True))


# Emotions: mean probability across frames + top emotion
if emo_cols:
	emo_means = per_frame_df[emo_cols].mean(skipna=True)
	out.update({f"emo_{c}__mean": float(emo_means[c]) for c in emo_cols})
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
	detector = Detector()


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
				fex = detector.detect_video(str(vid))
			except Exception as e:
				print(f"[WARN] Skipping {vid.name}: {e}", file=sys.stderr)
				continue

			df = pd.DataFrame(fex)
			df.to_csv(per_frame_csv, index=False)


			summary_row = summarize_video(df, vid.name)
			summaries.append(summary_row)


			out_summary = out_root / "summaries.csv"
			summary_df = pd.DataFrame(summaries)
			summary_df.sort_values("video").to_csv(out_summary, index=False)


	print(f"\nDone.\nPer-frame CSVs: {per_frame_dir.resolve()}\nSummary table: {out_summary.resolve()}")


if __name__ == "__main__":
	main()