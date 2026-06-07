# rpi-flashcards

`rpi-flashcards` is a terminal-first Raspberry Pi dictionary display project. The target
experience is simple: show one English word and its Japanese translation at a time, advance on a
timer, and later render the same view on a 2.13-inch SPI e-paper display.

The project is intentionally staged. macOS terminal checks come first, then Raspberry Pi terminal
parity over SSH, then e-paper bring-up.

## Project Purpose

- Validate the passive dictionary display experience before hardware work.
- Use a sample English/Japanese word dictionary to settle the UI and data format.
- Keep `core`, `data`, `ui_terminal`, `display`, and `platform` separated so Raspberry Pi and
  e-paper work stay isolated.
- Avoid quiz, rating, reveal, and progress-tracking features until the dictionary display works.

## Current Status

The repository currently contains an initial terminal flashcard proof of concept. That PoC is being
reshaped into a timer-based dictionary display.

Current durable pieces:

- small bundled seed data for local development
- normalized data and generated deck pipeline scaffolding
- terminal entrypoint through `make run-demo`
- PNG preview rendering scaffold for later display validation
- tests for existing core, data, and display behavior

Planned immediate change:

- replace the interactive reveal/rating terminal flow with random English/Japanese word display
- use a 5-second interval for development mode
- keep the runtime offline and hardware-free

## Roadmap

1. sample dictionary UI check
2. sample dictionary format finalization
3. real dictionary formation
4. Raspberry Pi port and SSH check from Mac
5. e-paper operation test
6. dictionary display on e-paper

See [docs/roadmap.md](docs/roadmap.md) for phase-level done conditions.

## Local Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

## Target Terminal Demo

The planned Phase 1 terminal demo should run with:

```bash
make run-demo
```

Expected development-mode behavior:

- load a sample dictionary of English/Japanese word pairs
- display one word and one Japanese translation at a time
- select entries randomly
- advance automatically every 5 seconds
- quit with `q` or Ctrl-C
- do not ask quiz questions
- do not record ratings or progress state

Example target output:

```text
rpi-flashcards dictionary display
interval: 5s
quit: q or Ctrl-C

careful
注意深い

next in 5s
```

## Data Pipeline Overview

The target dictionary data flow separates four concerns:

- `data/raw/`: source-shaped dictionary or generated asset input
- `data/normalized/`: validated English/Japanese word-pair records
- `data/decks/` or future display assets: generated runtime dictionary snapshots
- `state/`: reserved for later runtime state, not required for Phase 1

The first stable dictionary format should represent at least:

- `entry_id`
- `word`
- `japanese`

Optional fields can include `part_of_speech`, `tags`, and `source`.

For the real dictionary phase, the first planned source candidate is EJDict-hand. The project should
download and inspect the raw source before finalizing parser and filtering rules. See
[docs/data-sources.md](docs/data-sources.md) for the candidate list and download-and-inspect spike.

## Raspberry Pi Migration Plan

1. keep using the same dictionary assets and core random-selection logic
2. run the terminal display on Raspberry Pi over SSH from a Mac
3. keep e-paper, GPIO, and SPI out of the app until terminal behavior is confirmed on-device
4. add Raspberry Pi-specific setup only inside `src/rpi_flashcards/platform` or docs

## E-paper Integration Plan

- confirm the exact 2.13-inch panel and Python driver first
- run a minimal e-paper hardware test before wiring app logic
- keep frame preparation in `src/rpi_flashcards/display`
- map prepared dictionary frames to one concrete panel adapter later
- retain terminal mode as the fallback during hardware debugging

## Later Extensions

- physical buttons for pause, next, or shutdown
- boot-to-app startup flow
- display history or duplicate avoidance
- quiz mode
- lightweight learning or review state

## Repository Layout

```text
src/rpi_flashcards/core        dictionary display state and selection logic
src/rpi_flashcards/data        ingestion, normalization, dictionary asset generation
src/rpi_flashcards/ui_terminal terminal display UX
src/rpi_flashcards/display     frame preparation and preview rendering
src/rpi_flashcards/platform    Raspberry Pi-specific glue
data/                          raw, normalized, generated dictionary assets
state/                         reserved for future persisted runtime state
docs/                          architecture, hardware, data source, roadmap
tests/                         focused automated tests
```

## Hardware Uncertainty and Adapter Strategy

Different 2.13-inch SPI e-paper kits can map to different controllers and Python drivers. The
repository assumes:

- dictionary data and random-selection logic must not depend on a specific panel
- rendering output should be prepared before device-specific transmission
- a future adapter can map a prepared frame to one concrete panel driver

See [docs/hardware.md](docs/hardware.md) for the current hardware strategy.
