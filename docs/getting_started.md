# Getting Started

Welcome! This short setup gets you coding in the browser.

## Goal

By the end, you will:

- Open the project in GitHub Codespaces.
- Open a terminal.
- Run your first ADA Python script.

## Open Codespaces

If your instructor has published this repo on GitHub:

1. Sign in to GitHub.
2. Open the `ada-prelearning` repo page.
3. Click `Code`.
4. Click `Codespaces`.
5. Click `Create codespace on main`.
6. Wait for the browser coding space to open.

Quick link format:

```text
https://codespaces.new/OWNER/ada-prelearning
```

Because this repo is public, anyone can view it on GitHub. You may still need to sign in to create a Codespace.

## Open A Terminal

In Codespaces, click:

```text
Terminal -> New Terminal
```

Now run:

```bash
pwd
```

Expected output will look something like:

```text
/workspaces/ada-prelearning
```

## Run Your First Script

Run:

```bash
python scripts/hello_ada.py
```

Expected output:

```text
Welcome to ADA Prelearning!
Your browser coding space is ready.
Today we will practice Python, Linux, and simple driving logic.
Action: MOVE
```

If `python` does not work, try:

```bash
python3 scripts/hello_ada.py
```

## Tiny Modification

Open `scripts/hello_ada.py`.

Change this line:

```python
print("Action: MOVE")
```

to:

```python
print("Action: SLOW")
```

Run the script again:

```bash
python scripts/hello_ada.py
```

## Reflection

What felt new today: the browser coding space, the terminal, or Python?

