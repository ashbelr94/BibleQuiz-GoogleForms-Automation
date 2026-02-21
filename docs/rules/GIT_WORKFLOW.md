# Git Wrap-up & Push Workflow

This document defines the automated workflow for finalizing a task and pushing changes to the repository. Whenever the user requests a "wrap-up" or references this file for a commit, the agent MUST follow these steps:

## 1. Discovery & Inspection
- Run `git status` to identify all modified and untracked files.
- Run `git diff HEAD` to review the actual code changes.
- Identify the core "Value" of the changes (e.g., a new feature, a bug fix, documentation update).

## 2. Staging
- Automatically stage all relevant changes using `git add .` (unless specific files are requested to be excluded).
- Run `git status` again to verify the staging area.

## 3. Semantic Commit Message Generation
Propose a commit message following the **Conventional Commits** format:
- `feat:` for new features (e.g., the Gradio UI).
- `fix:` for bug fixes.
- `docs:` for documentation-only changes.
- `refactor:` for code changes that neither fix a bug nor add a feature.
- `chore:` for updating build tasks, package manager configs, etc.

The message should include:
- A clear summary line.
- A bulleted list of specific changes.

## 4. Execution
- Perform the commit: `git commit -m "<message>"`
- Push the changes: `git push origin main` (or the current active branch).

## 5. Confirmation
- Confirm the success of the push with a final `git status`.
- Provide a brief summary of the finalized task to the user.
