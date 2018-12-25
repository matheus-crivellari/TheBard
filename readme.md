# TheBard
TheBard is a text-based roleplaying game engine. It's intended for building interactive story-telling contents that can be played as an table-top rpg campaign.

## How does it work?
TheBard is a command line application able to read a specific-formatted JSON file and tell a story to the user which he/her can interact with. The player can take decisions and change the flow of the story. 

A content-maker structures a json file using easy commands and his/her screenplay habilities to tell an interactive story. It's possible to define variables and check them in order to make non-linear storylines.

## Testing
This game engine only works in console/terminal so far.

### Requirements
- The only requirement is [Python 3.7](https://www.python.org/downloads/release/python-372/) installed

- Optional requirement is [`pipenv`](https://pipenv.readthedocs.io/en/latest/).

### How to test
1. Clone this repository

        git clone https://github.com/matheus-crivellari/TheBard.git thebard

2. Run the project 

        cd thebard
        python run.py

## Roadmap
### Done
- Player command `look <ambient>|<object>`;
- Player command `pick <object>`;
- Player command `quit`;
### TO-DO
- Player command `use <object> <object>`;
- Player command `wear <wearable>`;
- Player command `attack <object>`;
- Player command `open <door>|<object>`;
- Turn-based combat game logic;
- Leveling system;
- Multiplayer gameplay;
- Equipment and buff enhancement system;
- Consumable item consuming system.
