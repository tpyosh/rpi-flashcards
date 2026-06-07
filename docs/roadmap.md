# Roadmap

## Phase 1: macOS Terminal PoC

Done condition:

- terminal deck can reveal, advance, quit, and record lightweight ratings
- sample data and generated deck are committed
- tests cover core session and deck logic

## Phase 2: Data Pipeline Stabilization

Done condition:

- raw, normalized, deck, and state layers are clearly separated
- deck regeneration is reproducible from config
- larger free dictionary source ingestion is documented

## Phase 3: Raspberry Pi Terminal Parity

Done condition:

- the same terminal UX runs on Raspberry Pi Zero 2 W
- packaging and state paths work on-device
- no GPIO dependency is required yet

## Phase 4: Rendering and Preview

Done condition:

- frame preparation is independent of terminal UI
- card previews can be rendered to PNG on macOS
- rendering prep has tests that do not require hardware

## Phase 5: E-paper Adapter

Done condition:

- one concrete adapter can display prepared frames on a confirmed panel
- terminal mode remains available as fallback
- refresh policy is controlled in the adapter layer

## Phase 6: Future Extensions

Candidates:

- physical buttons for next / previous
- quiz mode
- lightweight spaced review logic
- power optimization
- boot-to-app startup flow

