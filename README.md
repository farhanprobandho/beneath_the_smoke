# Beneath the Smoke — GitHub-first Windows setup

This is a beginner-friendly overlay for a **one-day NASA Space Apps** web project about the 2026 fires in West Kalimantan, using NISAR and complementary satellite data.

> **Scientific status:** The starter shows only a general Ketapang basemap and an explicit unverified-data message. No NISAR scene, compatible pre/post pair, or burned-area raster has been verified by this starter. Never present placeholders as observations.

## 0. Install prerequisites

Install Git for Windows, Visual Studio Code, Node.js (recent LTS), Python 3.11/3.12, and GitHub Copilot if you want the included VS Code custom agents. In PowerShell, verify:

```powershell
git --version
node --version
npm.cmd --version
py --version
```

## 1. Create the GitHub repository FIRST

Go to https://github.com/new and create a repository named `beneath-the-smoke`. Leave **Add a README**, **.gitignore**, and **license** all unset, so that it begins empty. Public visibility is suitable for open-source submissions. Do not copy real credentials into it.

## 2. Clone the empty repository

In PowerShell, change to your usual projects directory (create it if needed) and replace `YOUR_USERNAME` below:

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\Projects" | Out-Null
cd "$HOME\Projects"
git clone https://github.com/YOUR_USERNAME/beneath-the-smoke.git
cd beneath-the-smoke
code .
```

A `You appear to have cloned an empty repository` warning is expected. The `.git` directory is already configured; **do not run `git init` or `git remote add`**.

## 3. Create a Python virtual environment BEFORE frontend setup

From the cloned repo root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe --version
```

Optional activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation is blocked by a PowerShell execution policy, you can simply use `.\.venv\Scripts\python.exe` in every Python command. You do not need to change machine-wide PowerShell policies.

## 4. Scaffold React + TypeScript INSIDE the cloned repo

From the `beneath-the-smoke` directory:

```powershell
npm.cmd create vite@latest . -- --template react-ts
```

**Important:** Vite sees `.venv` and `.git` and may prompt that the directory is not empty. Choose **Ignore files and continue**. **Never select Remove existing files and continue**, because that can delete `.venv` and other existing files. Do not use `--overwrite`.

Then install frontend dependencies:

```powershell
npm.cmd install
npm.cmd install maplibre-gl
```

Vite guidance: https://vite.dev/guide/

## 5. Add the contents of the starter ZIP

Download `beneath_the_smoke_starter_github_first.zip` and move or locate it in Downloads. From the cloned repo root:

```powershell
Expand-Archive -Path "$HOME\Downloads\beneath_the_smoke_starter_github_first.zip" -DestinationPath . -Force
```

If it has a different download name or location, change the path. The ZIP contains **contents for the repo root**, not a containing project folder. It replaces the default Vite `src/App.tsx`, styles, and `.gitignore`, and adds `.github/agents/`, docs, scripts, and the data manifest. **Do not copy over your `.venv` or `.git` folder.**

## 6. Check the Python discovery environment

```powershell
.\.venv\Scripts\python.exe -m pip install -r scripts/requirements-discovery.txt
.\.venv\Scripts\python.exe scripts/check_data.py
```

The script requires Internet. If it works, it saves results under `results/` (ignored by Git). It searches for possible NISAR scenes but does not establish scientific validity by itself. Full geospatial dependencies can be installed later via `scripts/requirements-geospatial.txt`.

## 7. Run the React map

```powershell
npm.cmd run dev
```

Open the local address Vite prints (normally `http://localhost:5173/`). You should see a Ketapang basemap and an explicit **Data verification in progress** message.

In a separate terminal, verify the build:

```powershell
npm.cmd run build
```

## 8. Check VS Code custom agents

Open the repository root in VS Code and sign in to Copilot. In Chat choose the Copilot harness if multiple are available. Press `Ctrl+Shift+P` and run **Chat: Open Customizations**, then open **Agents**. You should see Planner, Data Scientist, Frontend Engineer, and Reviewer from `.github/agents/*.agent.md`.

For a first task, select **Data Scientist** and ask it to read `AGENTS.md`, `docs/STATUS.md`, `docs/SCIENCE_CHECKLIST.md`, and the checker outputs; verify live NISAR granule footprints, metadata and fire observations, and document what remains unverified. Use the prompt in `docs/AGENT_PROMPTS.md` if desired.

Use only one agent at a time for the first iteration; review its diffs and commands.

## 9. Commit and push

Do this after verifying the `.gitignore`, checking for secrets, and reviewing changed files:

```powershell
git status
git add .
git commit -m "Initialize Beneath the Smoke starter and agents"
git push -u origin main
```

Your clone already has a Git remote named `origin`. Do **not** use `git init` or `git remote add origin` again.

## Useful sources

- NISAR user guide: https://nisar-docs.asf.alaska.edu/
- ASF Vertex: https://search.asf.alaska.edu/
- VS Code custom agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
- MapLibre docs: https://maplibre.org/maplibre-gl-js/docs/
