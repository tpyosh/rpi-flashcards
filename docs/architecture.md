# Architecture

## Goals

- keep the terminal PoC runnable at every phase
- make Raspberry Pi migration a packaging problem, not a rewrite
- isolate display-driver uncertainty behind a stable rendering interface

## Layering

```text
core <- ui_terminal
core <- display
display <- platform
data is independent from ui_terminal
```

## Packages

### `src/rpi_flashcards/core`

Contains the study deck model, review history, and session mechanics such as reveal, next, and rating.

### `src/rpi_flashcards/data`

Contains raw-file ingestion, normalized entry validation, deterministic deck generation, and JSON-based state persistence.

### `src/rpi_flashcards/ui_terminal`

Contains the current terminal interaction loop. It depends on `core` and `data`, but it knows nothing about GPIO or SPI.

### `src/rpi_flashcards/display`

Contains frame preparation and PNG preview rendering. The current rendering path validates layout decisions before any hardware adapter is added.

### `src/rpi_flashcards/platform`

Reserved for Raspberry Pi-specific glue such as panel-driver selection, SPI setup, and later GPIO button wiring.

## Current Runtime Flow

1. load a generated deck from `data/decks/`
2. create a `FlashcardSession`
3. run terminal commands for reveal / next / rating
4. persist review events to `state/`
5. optionally render a prepared card frame to PNG

## Why This Shape

- `core` remains reusable for both terminal and e-paper modes
- `data` can evolve into a larger pipeline without changing runtime UI
- `display` can target PNG preview now and e-paper hardware later
- `platform` stays thin and avoids contaminating the application model

