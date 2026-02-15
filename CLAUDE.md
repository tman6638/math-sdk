# CLAUDE.md — Stake Engine Math SDK

## Project Overview

This is the **Stake Engine Math SDK**, a Python-based engine for defining game rules, simulating outcomes, and optimizing win distributions for slot/casino games. It generates backend configuration files, lookup tables, and simulation results for game development.

- **Primary URL:** https://engine.stake.com/
- **Documentation:** https://stakeengine.github.io/math-sdk/
- **Python version:** >= 3.12

## Repository Structure

```
math-sdk/
├── src/                        # Core SDK source code
│   ├── calculations/           # Game math (board, lines, ways, scatter, cluster, tumble)
│   ├── config/                 # Configuration management (Config, BetMode, constants)
│   ├── events/                 # Event system (reveal, freespin, tumble, wincap)
│   ├── executables/            # Reusable game actions
│   ├── state/                  # Game state machines and simulation orchestration
│   ├── wins/                   # Win management and multiplier strategies
│   └── write_data/             # Output generation (lookup tables, configs, JSON)
├── games/                      # Example games and templates (11 game directories)
│   └── template/               # Starting point for new game development
├── tests/                      # pytest unit tests
│   └── win_calculations/       # Tests for line, ways, scatter, cluster calculations
├── utils/                      # Utility scripts (analytics, RGS verification, compression)
├── optimization_program/       # Rust-based win distribution optimizer
├── docs/                       # MkDocs documentation site source
├── Makefile                    # Build automation
├── setup.py                    # Package configuration
└── requirements.txt            # Python dependencies
```

## Build & Development Commands

All commands use `make` from the project root:

```bash
make setup              # Create virtualenv, install dependencies, install package
make run GAME=<name>    # Run a specific game (e.g., make run GAME=0_0_lines)
make test               # Run all pytest unit tests
make test_run           # Run sample game simulations (integration tests)
make clean              # Remove virtualenv and __pycache__
```

The virtual environment is created at `env/` in the project root. Activate it with `source env/bin/activate` if running Python directly.

## Testing

- **Framework:** pytest 8.3.5
- **Test location:** `tests/win_calculations/`
- **Run tests:** `make test` (or `pytest tests/` with venv active)
- **Test files:** `test_linespay.py`, `test_wayspay.py`, `test_scatterpay.py`, `test_clusterpay.py`
- **Test config:** `game_test_config.py` provides `GamestateTest` base class and helpers

RGS verification (`utils/rgs_verification.py`) validates win distributions, RTPs, hit rates, and probability distributions before upload.

## Code Conventions

### Naming
- **Classes:** PascalCase — `GeneralGameState`, `WinManager`, `BetMode`
- **Functions/methods:** snake_case — `create_books`, `get_win_level`
- **Constants:** UPPER_SNAKE_CASE — `ANTEMAPPING`, `ISBUYBONUSMAPPING`
- **Private members:** underscore prefix — `_name`, `_cost`

### Formatting & Linting
- **Formatter:** Black (configured via VSCode)
- **Linter:** pylint (configured via VSCode)
- No pre-commit hooks or CI pipelines are configured

### Design Patterns
- **Inheritance:** Base classes in `src/` are extended by game-specific implementations (e.g., `Config` → `GameConfig`, `GeneralGameState` → game state)
- **Abstract base classes:** `GeneralGameState` uses `ABC` with `@abstractmethod`
- **Singleton:** `GameConfig` uses `_instance` singleton pattern
- **Manager classes:** `WinManager`, `SymbolStorage` manage collections of game objects
- Type hints used selectively (e.g., `get_lines(...) -> dict`, `board: list[list[Symbol]]`)

## Key Abstractions

### Game State Machine
`GeneralGameState` (abstract) is extended for each game. It tracks the board, wins, events, symbols, and multipliers. Supports basegame and freegame modes.

### Symbol System
Symbols have configurable attributes (wild, scatter, multiplier, blank) checked via `check_attribute()`. Special functions can be registered on symbols dynamically.

### Event Recording
All game actions are recorded in a `Book` (event log). Events include reveal, win info, freespin trigger, tumble, and wincap. Serialized to JSON/JSONL for frontend consumption.

### Win Calculation Pipeline
Board generation → Win detection (lines/ways/scatter/cluster) → Multiplier application → Output

## Game Development Workflow

Each game directory follows a standard structure:

| File | Purpose |
|------|---------|
| `run.py` | Main entry point |
| `game_config.py` | Game-specific configuration (extends `Config`) |
| `gamestate.py` | Game-specific state (extends `GeneralGameState`) |
| `game_calculations.py` | Game-specific math logic |
| `game_executables.py` | Game-specific actions |
| `game_override.py` | Custom symbol behaviors |
| `game_optimization.py` | Optimization settings |
| `reels/` | Reel strip definitions |

**Typical execution flow in `run.py`:**
1. Create `GameConfig` (singleton, extends `Config`)
2. Create `GameState` (extends `GeneralGameState`)
3. Run `create_books()` — multi-threaded simulation
4. Run `generate_configs()` — output configuration files
5. Run `OptimizationExecution` — Rust-based optimization
6. Run `create_stat_sheet()` — statistical analysis
7. Run `execute_all_tests()` — RGS verification

## Optimization System

The optimization program is written in Rust (`optimization_program/src/`) and orchestrated by Python (`optimization_program/run_script.py`):

1. Python creates `setup.toml` with optimization parameters
2. Python invokes Rust binary via `cargo run --release`
3. Rust performs win distribution optimization
4. Results returned to Python for further processing

Requires Rust/Cargo to be installed (provided by the devcontainer).

## Key Dependencies

| Package | Purpose |
|---------|---------|
| numpy | Numerical computing, array operations |
| boto3 | AWS S3 integration for file uploads |
| pytest | Unit testing |
| xlsxwriter | Excel report generation |
| zstandard | Fast compression for game data |
| matplotlib | Data visualization for analytics |
| python-dotenv | Environment variable management |
| toml | Configuration file parsing |

## Development Environment

The project includes a devcontainer configuration (`.devcontainer/devcontainer.json`) with:
- Python 3.12 base image
- Git, GitHub CLI, and Rust toolchain
- Post-create hook runs `make setup` automatically

## Important Notes for AI Assistants

- Always run `make setup` before running tests or games if the virtual environment doesn't exist
- Game-specific code lives in `games/<game_name>/`; core SDK code lives in `src/`
- Do not modify example game files unless specifically asked — they serve as reference implementations
- The `template/` game directory is the canonical starting point for new games
- When modifying core SDK code in `src/`, run `make test` to verify nothing breaks
- Output files (lookup tables, configs) are generated into game directories and are git-ignored
- The Rust optimization program must be compiled with `cargo build --release` before use
