# AGENTS.md

Guidance for AI agents working in this repository.

## Repository overview

This repository (`mattty1/mattty1`) is **documentation-only**. It does not contain application source code, package manifests, Docker Compose, or automated tests.

| Branch | Contents |
|--------|----------|
| `main` | `README.md` only |
| `cursor/test-abcd-modelowanie-3d-0ec8` | `README.md` + `test_ABCD_Modelowanie_3D.md` (75-question ABCD quiz on 3D modeling / 3D printing, Polish) |

There is nothing to `npm install`, `pip install`, build, or lint in the default tree.

## Cursor Cloud specific instructions

- **No runtime services are required.** There is no API, database, or frontend dev server defined in this repo.
- **Dependency refresh:** The VM update script is a no-op (`true`) because there are no language or package dependencies to install on startup.
- **Working with quiz content:** Check out `origin/cursor/test-abcd-modelowanie-3d-0ec8` (or a branch based on it) when you need `test_ABCD_Modelowanie_3D.md`. `main` does not include that file.
- **Optional local preview:** To browse the Markdown in a browser, from the repo root run `python3 -m http.server 8765` and open `http://127.0.0.1:8765/test_ABCD_Modelowanie_3D.md`. Stop the server when finished.
- **Lint / test / build:** Not applicable until application code is added. Validating the quiz document (75 numbered questions, answer key table) can be done with shell checks against `test_ABCD_Modelowanie_3D.md`.
- **Git:** Use normal `git fetch` / `git checkout` / `git pull` against `origin` (`https://github.com/mattty1/mattty1`). Pre-commit hooks in `.git/hooks` are sample files only; the agent hooks path is configured in `.git/config` for Cursor Cloud.
