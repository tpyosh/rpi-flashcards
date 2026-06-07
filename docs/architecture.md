# Architecture

## Goals

- keep the terminal dictionary display runnable at every phase
- make Raspberry Pi migration a packaging and environment problem, not a rewrite
- isolate e-paper driver uncertainty behind a stable display interface
- keep quiz, rating, reveal, and progress-tracking behavior out of the first display path

## Layering

```text
core <- ui_terminal
core <- display
display <- platform
data is independent from ui_terminal
```

## Packages

### `src/rpi_flashcards/core`

Owns display-session logic that does not depend on terminal or hardware details. For the first
target flow, this should mean choosing the next English/Japanese word pair from a dictionary asset,
with deterministic random behavior available for tests.

### `src/rpi_flashcards/data`

Owns raw-file ingestion, normalized English/Japanese dictionary validation, and generation of
runtime dictionary assets. It should not know whether the target renderer is terminal or e-paper.

### `src/rpi_flashcards/ui_terminal`

Owns the terminal timer display. It should load the dictionary through `data`, ask `core` for the
next item, print one English word and one Japanese translation, wait for the configured interval,
and repeat until the user quits.

### `src/rpi_flashcards/display`

Owns frame preparation and PNG preview rendering. The first e-paper-facing work should happen here
without changing dictionary data or random-selection logic.

### `src/rpi_flashcards/platform`

Reserved for Raspberry Pi-specific glue such as setup notes, panel-driver selection, SPI setup,
and later GPIO button wiring.

## Target Runtime Flow

1. load a generated dictionary asset from `data/`
2. create a display session with a random source
3. terminal UI requests and prints the next English/Japanese pair
4. wait for the configured timer interval
5. repeat until `q` or Ctrl-C
6. later, render the same pair through `display` for e-paper output

## Current Implementation Note

The repository still contains an initial flashcard-style session with reveal, next, rating, and
progress concepts. The next implementation pass should replace the active terminal path with the
timer-based dictionary display described here.

## Why This Shape

- `core` remains reusable for terminal and e-paper display modes
- `data` can evolve from sample entries to a real dictionary without changing UI code
- `display` can validate layout with PNG output before using a physical panel
- `platform` stays thin and avoids contaminating the application model
