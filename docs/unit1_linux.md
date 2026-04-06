# Unit 1: Linux Scavenger Hunt

Linux is the system inside your Codespace. The terminal lets you give it short text commands.

This unit owns the terminal basics. You will not write Python yet; you will use `pwd`, `ls`, `cd`, `mkdir`, and `cat` to move through a small autonomous-driving architecture scavenger hunt.

## Goal

Use a few commands to follow autonomous-driving architecture printouts.

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
LICENSE  README.md  docs  scripts  web_sim
```

Move to the clue folder:

```bash
cd scripts/scavenger_clues
```

Read the first printout:

```bash
cat start.txt
```

Expected output:

```text
Start here, autonomy engineer!
This scavenger hunt follows a modern autonomous-driving architecture:
sensing -> perception -> localization -> planning -> control -> end-to-end AV agent

Your first printout is in the 01_sensing folder.
Use: cd 01_sensing
Then use: cat printout.txt
```

## Follow The Clues

Run these commands one at a time:

```bash
cd 01_sensing
cat printout.txt
cd ../02_perception
cat printout.txt
cd ../03_localization
cat printout.txt
cd ../04_planning
cat printout.txt
cd ../05_control
cat printout.txt
cd ../06_end_to_end_av_agent
cat final_printout.txt
```

Expected final output:

```text
Route complete! You used the terminal like an ADA autonomy engineer.
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

Open `scripts/scavenger_clues/06_end_to_end_av_agent/final_printout.txt`.

Add one friendly sentence, like:

```text
Nice driving, future ADA engineer!
```

Then read it again:

```bash
cat scripts/scavenger_clues/06_end_to_end_av_agent/final_printout.txt
```

## Reflection

Which terminal command felt most useful: `pwd`, `ls`, `cd`, `mkdir`, or `cat`?

Next, Unit 2 uses the same terminal to run your first small Python vehicle assistant.
