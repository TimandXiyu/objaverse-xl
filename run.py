import argparse
import pandas as pd

from objaverse.xl.github import GitHubDownloader
from objaverse.xl.sketchfab import SketchfabDownloader
from objaverse.xl.smithsonian import SmithsonianDownloader


DOWNLOADERS = {
    "github": GitHubDownloader(),
    "sketchfab": SketchfabDownloader(),
    "smithsonian": SmithsonianDownloader(),
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download Objaverse-XL annotations"
    )
    parser.add_argument(
        "--output",
        default="~/.objaverse",
        help="Directory to store annotation parquet files",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force redownload of annotations",
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        choices=list(DOWNLOADERS.keys()),
        default=list(DOWNLOADERS.keys()),
        help="Data sources to download",
    )
    args = parser.parse_args()

    frames = []
    for src in args.sources:
        df = DOWNLOADERS[src].get_annotations(
            download_dir=args.output,
            refresh=args.refresh,
        )
        frames.append(df)

    annotations = pd.concat(frames, ignore_index=True)
    dest = f"{args.output.rstrip('/')}/annotations.parquet"
    annotations.to_parquet(dest)
    print(f"Saved {len(annotations)} annotations to {dest}")


if __name__ == "__main__":
    main()
