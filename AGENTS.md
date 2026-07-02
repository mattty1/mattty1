# AGENTS.md

Guidance for AI agents working in this repository.

## Repository overview

`mattty1/mattty1` is a personal repository whose `main` branch contains only a
placeholder `README.md`. The actual projects live on separate feature branches and
are almost all small, self-contained **Python / Streamlit** apps (plus one
presentation-generator and some Markdown quiz content).

| Branch | Contents |
|--------|----------|
| `main` | `README.md` only (empty scaffold) |
| `cursor/streamlit-pc-builder-513b` | Streamlit "Kreator zestawu komputerowego" PC-parts configurator with a CSV catalog in `data/` |
| `cursor/pc-builder-streamlit-app-0246` | Alternative Streamlit PC builder (`app.py` + `data/components.csv`) |
| `cursor/pc-konfigurator-59f2` | Streamlit PC configurator (`pc_konfigurator.py`) |
| `cursor/prezentacja-iphone-samsung-c422` | `build_presentation.py` (python-pptx) generating an iPhone vs Samsung deck |
| `cursor/test-abcd-modelowanie-3d-0ec8` | Markdown ABCD quiz on 3D modeling/printing (Polish) |

Because the projects are branch-scoped, `main` has no `requirements.txt`, tests,
Dockerfile, or lint config. Check out (or branch from) the relevant feature branch
to work on a given app.

## Cursor Cloud specific instructions

- **Stack:** Python 3.12 + pip. The recurring app framework is **Streamlit** (with
  `pandas` and `matplotlib`). No database, backend API, or Node toolchain is involved.
- **Dependency refresh:** The VM update script installs a branch's `requirements.txt`
  when present, otherwise it installs the common `streamlit` / `pandas` / `matplotlib`
  stack. It is guarded so it works even on the empty `main` branch.
- **`streamlit` is not on `PATH`:** pip installs the console script to
  `~/.local/bin`, which is not on `PATH`. Always launch apps with
  `python3 -m streamlit run <app.py>` rather than the bare `streamlit` command.
- **Running a Streamlit app:** from the branch's app directory run
  `python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true`.
  It serves on port `8501`; verify with `curl -s -o /dev/null -w '%{http_code}' http://localhost:8501`
  (expect `200`). The PC-builder apps require their `data/*.csv` catalog to sit next
  to the app file, so run them from within the checked-out branch directory.
- **Working across branches:** `main` does not contain the app code. Use
  `git worktree add <dir> origin/<branch>` (or check out the branch) to get an app's
  files without disturbing your current branch.
- **Lint / test / build:** No lint config or automated tests exist. "Build/run" for
  these apps just means launching the Streamlit server as above; the presentation
  branch is "built" by running `python3 build_presentation.py`.
