# yt-wl-cli

Command line utility to prune your YouTube Watch Later playlist using the YouTube Data API.

## Prerequisites

1. Install the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install).
2. Authenticate with YouTube permissions:

   ```sh
   gcloud auth application-default login --scopes=https://www.googleapis.com/auth/youtube
   ```

   This stores credentials locally so the script can call the API.
3. Optionally create a `.env` file alongside the script for any environment variables, such as
   `GOOGLE_APPLICATION_CREDENTIALS` if your credentials are in a non-default location.
4. Install dependencies:

   ```sh
   make install
   ```

## Usage

Preview the oldest five videos that would be removed:

```sh
make run ARGS="--count 5 --dry-run"
```

Remove the oldest ten videos:

```sh
make run ARGS="--count 10"
```

Filter by a specific date:

```sh
make run ARGS="--before 2023-01-01 --dry-run"
```

Run `make help` for a summary of available commands.

