# Unit 1: Linux Scavenger Hunt

Linux is the system inside your Codespace. The terminal lets you give it short text commands.

## Goal

Use a few commands to follow autonomous-driving themed clues.

Commands for today:

- `pwd`: show where you are.
- `ls`: list files.
- `cd`: move into a folder.
- `mkdir`: make a folder.
- `cat`: show a text file.

## Start The Hunt

Run:

```bash
pwd
```

Expected output may look like:

```text
/workspaces/ada-prelearning
```

List the files:

```bash
ls
```

Expected output includes:

```text
README.md  docs  scripts
```

Move to the clue folder:

```bash
cd scripts/scavenger_clues
```

Read the first clue:

```bash
cat start.txt
```

Expected output:

```text
Start here, driver! Your first clue is in the camera folder.
Use: cd camera
Then use: cat clue.txt
```

## Follow The Clues

Run these commands one at a time:

```bash
cd camera
cat clue.txt
cd ../lane
cat clue.txt
cd ../stop_sign
cat clue.txt
cd ../sensor
cat clue.txt
cd ../route
cat final_clue.txt
```

Expected final output:

```text
Route complete! You used the terminal like an ADA navigator.
```

## Make Your Own Garage Folder

Go back to the project root:

```bash
cd ../../..
```

Make a practice folder:

```bash
mkdir my_garage
```

Check that it exists:

```bash
ls
```

Expected output includes:

```text
my_garage
```

## Tiny Modification

Open `scripts/scavenger_clues/route/final_clue.txt`.

Add one friendly sentence, like:

```text
Nice driving, future ADA engineer!
```

Then read it again:

```bash
cat scripts/scavenger_clues/route/final_clue.txt
```

## Reflection

Which terminal command felt most useful: `pwd`, `ls`, `cd`, `mkdir`, or `cat`?
