import argparse

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
        description="Download Objaverse-XL objects based on annotations"
    )
    parser.add_argument(
        "--output",
        default="~/.objaverse",
        help="Directory to store downloaded objects",
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
    parser.add_argument(
        "--processes",
        type=int,
        default=None,
        help="Number of parallel processes to use for downloads",
    )
    args = parser.parse_args()

    for src in args.sources:
        downloader = DOWNLOADERS[src]
        annotations = downloader.get_annotations(
            download_dir=args.output,
            refresh=args.refresh,
        )
        downloader.download_objects(
            objects=annotations,
            download_dir=args.output,
            processes=args.processes,
        )


if __name__ == "__main__":
    main()
