#!/usr/bin/env python3
"""
Create the OEFF 2026 Film Supplemental Form via Google Forms REST API.

Uses the token from google-auth.py (stdlib, no pip).
Translates the spec from apps-script/FilmSupplemental.js into API calls.

Usage:
    python3 create-supplemental-form.py
"""

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TOKEN_FILE = Path.home() / "tools" / ".google-token.json"
FORMS_API = "https://forms.googleapis.com/v1/forms"


def get_access_token():
    """Refresh and return a valid access token."""
    with open(TOKEN_FILE) as f:
        data = json.load(f)

    body = urllib.parse.urlencode({
        "client_id": data["client_id"],
        "client_secret": data["client_secret"],
        "refresh_token": data["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()

    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["access_token"]


def api_call(method, url, token, body=None):
    """Make an authenticated Google API call."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"API error {e.code}: {err[:1000]}", file=sys.stderr)
        raise


# ── Film list (matches Film Intake Survey) ──
FILMS_2026 = [
    "F26-001 | Jane Goodall: Reasons for Hope",
    "F26-002 | Plastic People",
    "F26-003 | Beyond Zero",
    "F26-004 | Drowned Land",
    "F26-005 | Rooted",
    "F26-006 | How to Power a City",
    "F26-007 | The Last Ranger / Planetwalker",
    "F26-008 | 40 Acres",
    "F26-010 | Whose Water?",
    "F26-011 | Rails to Trails",
    "F26-012 | In Our Nature",
]


def build_form_items():
    """Build the batchUpdate requests to add all form items."""
    requests = []
    idx = 0

    def add_item(item_dict):
        nonlocal idx
        requests.append({
            "createItem": {
                "item": item_dict,
                "location": {"index": idx},
            }
        })
        idx += 1

    # ── Section 1: Your Film ──
    add_item({
        "title": "Your Film",
        "description": (
            "One Earth Film Festival 2026\n"
            "Festival Week: April 22 – 28, 2026\n\n"
            "Thanks for submitting the Film Intake Survey! This short follow-up "
            "helps us coordinate promotion, schedule any post-screening conversation, "
            "and connect audiences with your work.\n\n"
            "Should take about 5 minutes."
        ),
        "pageBreakItem": {},
    })

    add_item({
        "title": "Film Title",
        "description": "Select your film from the dropdown.",
        "questionItem": {
            "question": {
                "required": True,
                "choiceQuestion": {
                    "type": "DROP_DOWN",
                    "options": [{"value": f} for f in FILMS_2026],
                },
            }
        },
    })

    add_item({
        "title": "Your Name",
        "questionItem": {
            "question": {
                "required": True,
                "textQuestion": {"paragraph": False},
            }
        },
    })

    add_item({
        "title": "Your Email",
        "questionItem": {
            "question": {
                "required": True,
                "textQuestion": {"paragraph": False},
            }
        },
    })

    # ── Section 2: Post-Screening Conversation ──
    add_item({
        "title": "Post-Screening Conversation",
        "description": (
            "We love connecting audiences with filmmakers after screenings. "
            "This can be a brief Q&A, a moderated conversation, or a virtual check-in.\n\n"
            "OEFF offers a $100 stipend for virtual appearances and up to $300 for in-person."
        ),
        "pageBreakItem": {},
    })

    add_item({
        "title": "Would you or a representative be available for a post-screening conversation?",
        "questionItem": {
            "question": {
                "required": True,
                "choiceQuestion": {
                    "type": "RADIO",
                    "options": [
                        {"value": "Yes — in person"},
                        {"value": "Yes — virtually"},
                        {"value": "Maybe — let's discuss"},
                        {"value": "No"},
                    ],
                },
            }
        },
    })

    add_item({
        "title": "If yes: name and role of the person who would participate",
        "description": 'e.g., "Jane Smith, Director" or "Same as above"',
        "questionItem": {
            "question": {
                "required": False,
                "textQuestion": {"paragraph": False},
            }
        },
    })

    add_item({
        "title": "If yes: their email (if different from yours)",
        "questionItem": {
            "question": {
                "required": False,
                "textQuestion": {"paragraph": False},
            }
        },
    })

    add_item({
        "title": "Preferred format?",
        "questionItem": {
            "question": {
                "required": False,
                "choiceQuestion": {
                    "type": "RADIO",
                    "options": [
                        {"value": "Brief Q&A (10-15 min)"},
                        {"value": "Moderated conversation (20-30 min)"},
                        {"value": "Panel with other filmmakers"},
                        {"value": "Open to any format"},
                    ],
                },
            }
        },
    })

    # ── Section 3: Promotion ──
    add_item({
        "title": "Promotion",
        "description": (
            "Help us amplify your screening. We'll tag you in our posts "
            "and share any materials you provide."
        ),
        "pageBreakItem": {},
    })

    add_item({
        "title": "Social media handles",
        "description": "Film and/or filmmaker accounts — Instagram, X, Facebook, TikTok, Letterboxd, etc.",
        "questionItem": {
            "question": {
                "required": False,
                "textQuestion": {"paragraph": True},
            }
        },
    })

    add_item({
        "title": "Premiere status for this screening",
        "questionItem": {
            "question": {
                "required": False,
                "choiceQuestion": {
                    "type": "RADIO",
                    "options": [
                        {"value": "Chicago-area premiere"},
                        {"value": "Midwest premiere"},
                        {"value": "US premiere"},
                        {"value": "Not a premiere"},
                        {"value": "Not sure"},
                    ],
                },
            }
        },
    })

    add_item({
        "title": "Any updates about the film since you submitted?",
        "description": "Awards, press, new trailer, upcoming releases — anything we should know for promo.",
        "questionItem": {
            "question": {
                "required": False,
                "textQuestion": {"paragraph": True},
            }
        },
    })

    add_item({
        "title": "Do you have a trailer or clip we can use for promotion?",
        "questionItem": {
            "question": {
                "required": False,
                "choiceQuestion": {
                    "type": "RADIO",
                    "options": [
                        {"value": "Yes — I'll send the link"},
                        {"value": "Yes — it's on our website"},
                        {"value": "No"},
                        {"value": "Not sure"},
                    ],
                },
            }
        },
    })

    add_item({
        "title": "Trailer/clip link (if available)",
        "questionItem": {
            "question": {
                "required": False,
                "textQuestion": {"paragraph": False},
            }
        },
    })

    add_item({
        "title": "Where can audiences watch or buy your film after the festival?",
        "questionItem": {
            "question": {
                "required": False,
                "choiceQuestion": {
                    "type": "RADIO",
                    "options": [
                        {"value": "Available on a streaming platform"},
                        {"value": "Available for purchase/rental online"},
                        {"value": "Not yet available — festival circuit only"},
                        {"value": "Other — I'll explain below"},
                    ],
                },
            }
        },
    })

    add_item({
        "title": "Platform or purchase link (if applicable)",
        "questionItem": {
            "question": {
                "required": False,
                "textQuestion": {"paragraph": False},
            }
        },
    })

    return requests


def main():
    print("Refreshing access token...")
    token = get_access_token()
    print("  Token refreshed.")

    # Step 1: Create the form (title only)
    print("\nCreating form...")
    form = api_call("POST", FORMS_API, token, {
        "info": {
            "title": "OEFF 2026 — Filmmaker Follow-Up",
        }
    })
    form_id = form["formId"]
    print(f"  Form created: {form_id}")

    # Step 2: Update description and settings
    print("Updating form info...")
    api_call("POST", f"{FORMS_API}/{form_id}:batchUpdate", token, {
        "requests": [{
            "updateFormInfo": {
                "info": {
                    "description": (
                        "One Earth Film Festival 2026\n"
                        "Festival Week: April 22 – 28, 2026\n\n"
                        "Thanks for submitting the Film Intake Survey! This short follow-up "
                        "helps us coordinate promotion, schedule any post-screening conversation, "
                        "and connect audiences with your work.\n\n"
                        "Should take about 5 minutes."
                    ),
                },
                "updateMask": "description",
            }
        }],
    })

    # Step 3: Add all items
    print("Adding form items...")
    items = build_form_items()
    api_call("POST", f"{FORMS_API}/{form_id}:batchUpdate", token, {
        "requests": items,
    })
    print(f"  Added {len(items)} items.")

    # Step 4: Get the final form to confirm
    final = api_call("GET", f"{FORMS_API}/{form_id}", token)
    responder_url = final.get("responderUri", "?")
    edit_url = f"https://docs.google.com/forms/d/{form_id}/edit"

    print("\n" + "=" * 55)
    print("FORM CREATED SUCCESSFULLY")
    print("=" * 55)
    print(f"Edit URL:     {edit_url}")
    print(f"Live URL:     {responder_url}")
    print(f"Form ID:      {form_id}")
    print("=" * 55)
    print()
    print("NEXT STEPS:")
    print("1. Open the edit URL and preview it")
    print("2. Link a response spreadsheet (Form → Settings → Responses → Spreadsheet)")
    print("3. Include the live URL in the Monday filmmaker email")


if __name__ == "__main__":
    main()
