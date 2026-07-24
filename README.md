# SOC Triage — Codespaces build-along demo

A tiny, self-contained example to show what an interactive "build alongside us"
demo feels like in GitHub Codespaces. Someone opens this repo, a full dev
environment appears in their browser with **zero setup**, they edit one function,
re-run it, and watch a security alert get triaged into structured output.

Nothing here touches a real system, needs an API key, or makes a network call.
That's deliberate — it's the safe skeleton you drop the real logic into later.

## The 90-second demo

1. **Open in Codespaces.** Click the green **`< > Code`** button on the repo →
   the **Codespaces** tab → **Create codespace on main**. Wait ~30–60s while
   VS Code loads in the browser. (No install. That's the headline.)
2. **Run it.** In the terminal at the bottom, type:
   ```bash
   python triage.py
   ```
   You get a triage card plus the structured JSON that would feed Sentinel or
   ServiceNow downstream.
3. **Build alongside.** Open `triage.py`, find the big commented block, make a
   live edit (see below), and re-run. It changes instantly. *That's the
   build-along.*

## Live edit to do in front of your boss

Add a confidence score. Inside the build-along block in `triage.py`, add:

```python
    confidence = "Low" if alert["mfa_satisfied"] else "High"
```

Then add `confidence: str` to the `Triage` dataclass near the top, pass
`confidence=confidence` into the `return Triage(...)` call, and add one line to
`print_card`. Re-run — the new field appears in both the card and the JSON.

(Or just change the MITRE technique string, or the recommended action — any edit
works. The point is: edit → run → see it change, in an isolated browser
environment, with no setup.)

## Running the dry run yourself (two screens)

- **Screen 1 — "attendee":** your personal GitHub in an incognito window.
- **Screen 2 — "presenter":** your ISA GitHub.
- Both open **this same repo** in Codespaces. Each gets its own isolated
  container on its own account — editing on one screen never affects the other.
  That isolation is exactly what keeps a real room of attendees safe.

**Tip:** make this repo **public** for the demo. It's only mock data and a toy
function, so there's nothing sensitive — and public means any account (your
boss's brand-new one, or your incognito personal one) can open it in Codespaces
on its own free quota with no invites or permissions to fuss with.

## When you build the real workshop

Everything stays the same except the "brain." Instead of the rules in
`triage_alert`, that one function calls Claude — through a broker your team runs,
so no attendee ever holds a key:

```python
resp = requests.post(f"{BROKER_URL}/triage",
    headers={"Authorization": f"Bearer {WORKSHOP_TOKEN}"},
    json={"alert": alert}, timeout=30)
# the broker holds the real Anthropic key and calls claude-sonnet-5
```

The devcontainer, the repo layout, the edit-and-run loop, the per-attendee
isolation — all identical. You're just swapping deterministic rules for a
brokered model call when you're ready.
