# tic-tac-toe
<!-- hobby project -->
# Tic Tac Toe — Streamlit single-file app

This repository contains a single-file Streamlit Tic Tac Toe app (`app.py`) and `requirements.txt`.  
You can run locally or deploy to Streamlit Community Cloud.

## Files
- `app.py` — main app (single file)
- `requirements.txt` — dependencies

## Run locally
1. Clone repo:
   ```bash
   git clone https://github.com/<divyamsingh4444>/tic-tac-toe.git
   cd tic-tac-toe
2. (recommended) Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the app locally:

```bash
streamlit run app.py
```

## Deploying to Streamlit Community Cloud (streamlit.io/cloud)

1. Push this repo to GitHub (if not already). Make sure `requirements.txt` is present — it includes `streamlit`.
2. Go to https://share.streamlit.io/ and sign in with your GitHub account.
3. Click "New app", pick the repository and branch (`main`) and set the file path to `app.py`.
4. Click "Deploy" — Streamlit will use `requirements.txt` to install dependencies and run `app.py`.

## Clean repository notes

If you have a committed virtual environment (e.g. `venv/`) it is best to stop tracking it so you don't push many files to the repo. To untrack a committed venv without deleting your local copy run:

```bash
git rm -r --cached venv
git commit -m "Remove committed virtualenv from repo and add to .gitignore"
git push
```

After that, `venv/` will remain locally but won't be in the Git repository anymore.
