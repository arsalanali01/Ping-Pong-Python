# Ping Pong (Python + Pygame)

Classic Pong built with Python/Pygame. Clean architecture, tested game logic, CI, and ready for extension (AI opponent, power-ups, etc.).

![demo](docs/demo.gif)

## Features
- Smooth paddle/ball physics
- Modular logic separated from rendering (easy to test)
- Basic AI opponent option (WIP)
- Headless CI with tests

## Quick Start
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pong.game
