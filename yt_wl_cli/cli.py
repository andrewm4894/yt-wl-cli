import argparse
import datetime
from typing import List

from dotenv import load_dotenv
import google.auth
from googleapiclient.discovery import build

YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
PLAYLIST_ID = "WL"


def get_service():
    """Build an authenticated YouTube service using application default credentials."""
    credentials, _ = google.auth.default(scopes=[YOUTUBE_SCOPE])
    return build("youtube", "v3", credentials=credentials)


def fetch_playlist_items(service) -> List[dict]:
    """Return all items from the Watch Later playlist sorted by date added."""
    items = []
    request = service.playlistItems().list(
        playlistId=PLAYLIST_ID,
        part="id,snippet",
        maxResults=50,
    )
    while request is not None:
        response = request.execute()
        items.extend(response.get("items", []))
        request = service.playlistItems().list_next(request, response)
    items.sort(key=lambda i: i["snippet"]["publishedAt"])
    return items


def remove_items(service, items: List[dict], dry_run: bool = False) -> None:
    for item in items:
        title = item["snippet"]["title"]
        video_id = item["snippet"]["resourceId"]["videoId"]
        if dry_run:
            print(f"Would remove {title} ({video_id})")
        else:
            service.playlistItems().delete(id=item["id"]).execute()
            print(f"Removed {title} ({video_id})")


def parse_before(value: str) -> datetime.datetime:
    dt = datetime.datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt


def main(argv: List[str] | None = None) -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Remove old videos from your YouTube Watch Later playlist"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of oldest videos to remove",
    )
    parser.add_argument(
        "--before",
        type=parse_before,
        help="Remove videos added before this ISO timestamp (e.g. 2023-01-01)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List videos without removing them",
    )

    args = parser.parse_args(argv)

    try:
        service = get_service()
    except Exception as exc:  # pragma: no cover - network configuration
        raise SystemExit(f"Failed to authenticate: {exc}") from exc

    items = fetch_playlist_items(service)

    if args.before:
        items = [
            i
            for i in items
            if datetime.datetime.fromisoformat(
                i["snippet"]["publishedAt"].replace("Z", "+00:00")
            )
            < args.before
        ]

    to_remove = items[: args.count]
    if not to_remove:
        print("No videos match criteria.")
        return

    remove_items(service, to_remove, dry_run=args.dry_run)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
