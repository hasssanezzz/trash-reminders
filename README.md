# Trash reminders

A simple python reminder script.

## How it works

It takes input from the specified json file, and every X minutes it display a message box with two options "Retry" and "Cancel", If you clicked retry the reminder will continue to work, if you clicked cancel the reminder will be canceled and won't run, and it runs the specefied sound file.

## Make it work

`$ main.exe -i <YOUR_JSON_FILE_PATH> -s <SOUND_FILE_PATH>`

## The JSON input file

The input file is simply an array of object that have three propertiers as described below:

```JSON
[
  {
    "name": "Water", // reminder title
    "message": "drink water", // reminder text
    "every": 5 // remind you every five minutes
  }
]

```

## Example JSON file

```JSON
[
  {
    "name": "Water",
    "message": "drink water",
    "every": 5
  },
  {
    "name": "Push ups",
    "message": "5 push ups",
    "every": 10
  },
  {
    "name": "Stretches",
    "message": "Neck and back stretches",
    "every": 20
  }
]
```
I am telling the script to remind me:
- Every 5 minutes to drink water,
- Every 10 minutes to do 5 push ups
- Every 20 minutes to stretch my neck and back.
