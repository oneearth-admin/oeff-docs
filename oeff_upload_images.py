#!/usr/bin/env python3
"""Upload film poster images to Eventbrite events as logo/banner images."""

import json
import os
import sys
import urllib.request
import urllib.error
import mimetypes
import uuid

TOKEN = os.environ.get("EVENTBRITE_TOKEN", "")
API = "https://www.eventbriteapi.com/v3"
STATE_FILE = os.path.join(os.path.dirname(__file__), "eventbrite-state.json")
POSTER_DIR = os.path.join(os.path.dirname(__file__), "film-posters")

# Map row -> image filename
IMAGE_MAP = {
    "row_2": "reasons-for-hope.jpg",
    "row_3": "beyond-zero.jpg",
    "row_4": "plastic-people.jpg",
    # row_5: TBD film, no image
    "row_6": "drowned-land.jpg",
    "row_8": "how-to-power-a-city.jpg",
    "row_9": "rooted.jpg",
    "row_10": "how-to-power-a-city.jpg",  # same film
    "row_11": None,  # Young Filmmakers - no poster
    "row_12": "40-acres.jpg",
    "row_13": "40-acres.jpg",  # same film
    "row_14": "rails-to-trails.jpg",
    "row_17": None,  # Young Filmmakers - no poster
    "row_18": "rails-to-trails.jpg",  # same film
}

# Image source URLs for the spreadsheet
IMAGE_SOURCES = {
    "reasons-for-hope.jpg": "https://reasonsforhope-movie.com/",
    "beyond-zero.jpg": "https://rocofilms.com/films/beyond-zero/",
    "plastic-people.jpg": "https://plasticpeopledoc.com/",
    "drowned-land.jpg": "https://drownedland.com",
    "how-to-power-a-city.jpg": "https://www.powercityfilm.com/",
    "rooted.jpg": "https://rootedstories.com/rooted-film/",
    "40-acres.jpg": "https://www.magnoliapictures.com/40-acres-press-kit",
    "rails-to-trails.jpg": "https://www.pbs.org/show/from-rails-to-trails/",
}


def api_get(path):
    req = urllib.request.Request(f"{API}{path}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  GET ERROR {e.code}: {e.read().decode()[:200]}")
        return None


def api_post(path, data=None):
    url = f"{API}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  POST ERROR {e.code}: {e.read().decode()[:200]}")
        return None


def multipart_upload(upload_url, upload_data, file_path, file_param):
    """Upload a file using multipart/form-data."""
    boundary = uuid.uuid4().hex
    lines = []

    # Add form fields from upload_data
    for key, val in upload_data.items():
        if val:  # skip empty fields
            lines.append(f"--{boundary}")
            lines.append(f'Content-Disposition: form-data; name="{key}"')
            lines.append("")
            lines.append(str(val))

    # Add file
    filename = os.path.basename(file_path)
    content_type = mimetypes.guess_type(file_path)[0] or "image/jpeg"
    lines.append(f"--{boundary}")
    lines.append(f'Content-Disposition: form-data; name="{file_param}"; filename="{filename}"')
    lines.append(f"Content-Type: {content_type}")
    lines.append("")

    # Build body
    header_bytes = "\r\n".join(lines).encode("utf-8") + b"\r\n"
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    footer_bytes = f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = header_bytes + file_bytes + footer_bytes

    req = urllib.request.Request(upload_url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        print(f"  UPLOAD ERROR {e.code}: {e.read().decode()[:200]}")
        return None


def upload_image(file_path):
    """Upload an image to Eventbrite and return the logo_id."""
    # Step 1: Get upload instructions
    instructions = api_get("/media/upload/?type=image-event-logo")
    if not instructions:
        return None

    upload_url = instructions["upload_url"]
    upload_token = instructions["upload_token"]
    upload_data = instructions["upload_data"]
    file_param = instructions["file_parameter_name"]

    # Step 2: Upload the file
    print(f"    Uploading to {upload_url}...")
    status = multipart_upload(upload_url, upload_data, file_path, file_param)
    if not status:
        return None

    # Step 3: Notify Eventbrite the upload is complete
    result = api_post("/media/upload/", {
        "upload_token": upload_token,
        "crop_mask": {
            "top_left": {"x": 0, "y": 0},
            "width": 1920,
            "height": 1080
        }
    })
    if result and "id" in result:
        return result["id"]
    # Try without crop mask
    result = api_post("/media/upload/", {"upload_token": upload_token})
    if result and "id" in result:
        return result["id"]
    return None


def set_event_logo(event_id, logo_id):
    """Set the logo/banner image on an event."""
    return api_post(f"/events/{event_id}/", {"event": {"logo_id": str(logo_id)}})


def main():
    if not TOKEN:
        print("Set EVENTBRITE_TOKEN env var.")
        sys.exit(1)

    with open(STATE_FILE) as f:
        state = json.load(f)

    # Cache: filename -> logo_id (reuse uploads for same film at multiple venues)
    upload_cache = {}
    results = {}  # row -> {logo_id, source_url}

    for row_key, ev in sorted(state["events"].items()):
        event_id = ev["event_id"]
        event_name = ev["event_name"]
        image_file = IMAGE_MAP.get(row_key)

        print(f"\n[{row_key}] {event_name}")

        if image_file is None:
            print("  SKIP — no poster image available")
            results[row_key] = {"status": "NO_IMAGE"}
            continue

        file_path = os.path.join(POSTER_DIR, image_file)
        if not os.path.exists(file_path):
            print(f"  SKIP — file not found: {image_file}")
            results[row_key] = {"status": "FILE_MISSING"}
            continue

        # Check cache
        if image_file in upload_cache:
            logo_id = upload_cache[image_file]
            print(f"  Reusing cached upload: logo_id={logo_id}")
        else:
            print(f"  Uploading {image_file}...")
            logo_id = upload_image(file_path)
            if logo_id:
                upload_cache[image_file] = logo_id
                print(f"  Uploaded: logo_id={logo_id}")
            else:
                print("  FAILED to upload")
                results[row_key] = {"status": "UPLOAD_FAILED"}
                continue

        # Set on event
        print(f"  Setting logo on event {event_id}...")
        if set_event_logo(event_id, logo_id):
            print("  OK")
            source = IMAGE_SOURCES.get(image_file, "")
            results[row_key] = {"status": "OK", "logo_id": logo_id, "source": source}
            # Save logo_id to state
            ev["logo_id"] = str(logo_id)
        else:
            print("  FAILED to set logo")
            results[row_key] = {"status": "SET_FAILED", "logo_id": logo_id}

    # Save state
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    # Summary
    print(f"\n{'='*60}")
    ok = sum(1 for r in results.values() if r.get("status") == "OK")
    skip = sum(1 for r in results.values() if r.get("status") in ("NO_IMAGE", "FILE_MISSING"))
    fail = sum(1 for r in results.values() if "FAILED" in r.get("status", ""))
    print(f"Done: {ok} images set, {skip} skipped, {fail} failed")

    # Output for spreadsheet
    print(f"\n{'='*60}")
    print("Image source URLs for spreadsheet (column N):")
    for row_key in sorted(results.keys()):
        r = results[row_key]
        if r.get("source"):
            print(f"  {row_key}: {r['source']}")
        else:
            print(f"  {row_key}: (none)")


if __name__ == "__main__":
    main()
