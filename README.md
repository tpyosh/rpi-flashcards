# rpi-flashcards

`rpi-flashcards` is a terminal-first English flashcard project that will later run on Raspberry Pi Zero 2 W with a 2.13-inch SPI e-paper display. The repository is intentionally small at this stage: it focuses on a runnable command-line proof of concept, a reproducible dictionary pipeline, and a display abstraction that can be extended without rewriting core study logic.

## Project Purpose

- Validate the flashcard learning flow on macOS before touching Raspberry Pi hardware.
- Separate `core`, `data`, `ui_terminal`, `display`, and `platform` so hardware work stays isolated.
- Build a reproducible data pipeline that can regenerate small or large study decks from free dictionary sources later.

## Current Status

Phase 1 is implemented:

- terminal demo with reveal / next / rate / quit
- tiny bundled seed dictionary for local development
- normalized entry schema and deck generation config
- PNG preview renderer for display-layer validation
- tests for core session behavior, data validation, deck generation, and rendering prep

## Staged Roadmap

1. macOS terminal PoC with a tiny sample deck
2. normalized dictionary format and deterministic deck generation
3. Raspberry Pi terminal parity
4. PNG-based frame rendering for display validation
5. isolated e-paper adapter integration
6. future extensions: buttons, quiz mode, lightweight review logic, boot-to-app flow

See [docs/roadmap.md](docs/roadmap.md) for phase-level done conditions.

## Local Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

## Terminal PoC

Run the current demo:

```bash
make run-demo
```

Commands inside the demo:

- `r` reveal definition and example
- `n` move to the next card
- `1` rate as `again`
- `2` rate as `hard`
- `3` rate as `good`
- `4` rate as `easy`
- `q` quit

Progress events are written to `state/demo-progress.json`.

## Data Pipeline Overview

The repository separates data into four stages:

- `data/raw/`: source-shaped input records
- `data/normalized/`: clean normalized dictionary entries
- `data/decks/`: generated study decks
- `state/`: runtime review and progress data

Current pipeline commands:

```bash
make normalize-data
make build-deck
```

The current seed data is intentionally tiny and deterministic. It is meant to validate schema, filtering, and regeneration behavior before pulling in a larger free source such as Open English WordNet plus frequency metadata.

## Rendering Preview

Generate a local PNG preview of the first flashcard:

```bash
make preview-render
```

The generated PNG acts as a hardware-free validation layer for future e-paper rendering.

## Raspberry Pi Migration Plan

1. keep using the same deck files and core session logic
2. run the existing terminal UI on Raspberry Pi Zero 2 W unchanged
3. add Raspberry Pi-specific glue only inside `src/rpi_flashcards/platform`
4. wire display adapters through `src/rpi_flashcards/display` without changing `core`

## E-paper Integration Plan

- keep app logic independent from GPIO and vendor drivers
- build image/frame preparation first
- preview rendered output as PNG on macOS
- add a panel adapter behind a display abstraction later
- retain terminal fallback after hardware support exists

Because 2.13-inch SPI kits may ship with different controller revisions, this repository treats panel support as an adapter problem, not a core application concern.

## Future Extensions

- next / previous physical buttons
- quiz mode
- lightweight review state logic
- offline packaging for Raspberry Pi deployment
- auto-start on boot

## Repository Layout

```text
src/rpi_flashcards/core        domain and session logic
src/rpi_flashcards/data        ingestion, normalization, deck generation
src/rpi_flashcards/ui_terminal terminal UX
src/rpi_flashcards/display     frame preparation and preview rendering
src/rpi_flashcards/platform    Raspberry Pi-specific glue
data/                          raw, normalized, generated deck assets
state/                         persisted review state
docs/                          architecture, hardware, data source, roadmap
tests/                         focused automated tests
```

## Hardware Uncertainty and Adapter Strategy

Different 2.13-inch SPI e-paper kits can map to different controllers and Python drivers. The repository assumes:

- the study workflow must not depend on a specific Waveshare module name
- rendering output should be prepared before device-specific transmission
- a future adapter can map a prepared frame to one concrete panel driver

See [docs/hardware.md](docs/hardware.md) for the current hardware strategy.

