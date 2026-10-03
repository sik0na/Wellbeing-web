# deploy.py - uploads the website to a Hugging Face Space, which builds the Dockerfile
# and puts the site online.
#
# Once:     python -c "from huggingface_hub import login; login()"     (paste your HF token)
# Deploy:   python deploy.py YOUR-HF-USERNAME/wellbeing-checkin
#
# Run it again after every change to update the website.

import sys
from huggingface_hub import HfApi

if len(sys.argv) != 2:
    print("Usage: python deploy.py YOUR-HF-USERNAME/SPACE-NAME")
    sys.exit(1)

space = sys.argv[1]

HfApi().upload_folder(
    folder_path=".",
    repo_id=space,
    repo_type="space",
    # Never upload these: private data, big folders, and files the server doesn't need
    ignore_patterns=[
        "venv/*", "wellbeing.db", "**/__pycache__/*", ".git/*",
        "frontend/node_modules/*", "frontend/dist/*",
        "data/*", "tests/*", "try_*.py", "emotion_model.joblib",
    ],
)

name = space.replace("/", "-").lower()
print("Uploaded! Hugging Face is now building your site (about 5-10 minutes).")
print("Your website will be at: https://" + name + ".hf.space")
