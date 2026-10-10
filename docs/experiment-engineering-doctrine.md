# Real-repo experiment — engineering doctrine

Use this **after** cursor-hub foundation on **`7ab851d`** or later (schema v2 setup, mandatory read credits, invalid config fail-closed, ephemeral session keys). Goal: learn whether **policy + routing + project facts + hooks** improve engineering judgment in **normal conversation**, not whether the hook denies the first write (covered by unit tests). Optional **Phase 2:** add the **`fault-first`** pack for read-only failure analysis — see [fault-first.md](fault-first.md).

**Do not expand the harness** until this experiment produces findings from a real codebase.

## Setup (trading-system or clone)

1. Disposable clone of the repo (not production branch chaos).
2. `cursor-hub install engineering-doctrine .` (+ existing language packs if desired).
3. **One component only** in `.cursor/doctrine/components.json` (e.g. `market-data-engine` → bounded path glob).
4. Fill project doctrine with **real** content: `objectives.md`, `invariants.md`, `architecture.md`, `workload.md` (sizes, rates, hot paths, latency budgets).
5. In `required_doctrine_refs`, list only topics that matter for that subsystem (avoid requiring every reference file).

Confirm hooks load (Cursor **Hooks** output channel). Optionally inspect hook payloads for **`conversation_id`** — if present in normal chats, ephemeral bucket sharing is unlikely.

## Residual limitation (session)

| Scenario | Behavior |
|----------|----------|
| `conversation_id` in hook payload | Isolated per chat — preferred |
| Missing `conversation_id` | `ephemeral:pid-<pid>:root-<hash>` — not the old global `default` bucket |
| Two chats, same process + workspace, both missing id | **Could share read state** — document outcomes if you see cross-chat leakage |

Not a blocker for the experiment; note on scorecard if it mattered.

## A/B protocol

Two **new** chats, same model/settings, same component context:

| Chat | Environment |
|------|----------------|
| **A** | Doctrine installed + configured (one component) |
| **B** | Normal Cursor (no doctrine pack, or empty `components: []` and no ambient rule — your control) |

Run the **same prompts** in both (order suggested below). Record behavior; do not tune prompts mid-flight to “help” the harness.

## Four behavioral probes (Chat A primary; compare B)

### 1. Stop bad sophistication

**Prompt (adapt path):** “Replace this `HashMap` with a `Vec`; it should be faster.” (point at a type in the classified component)

**Good:** Loads algorithm-selection / data-layout / cache doctrine as needed; cites **workload.md**; refuses unsupported “faster” claims; asks for key density, mutation pattern, N, measurement plan.

**Bad:** Immediate refactor; cache/SIMD sermon without trigger; no evidence bar.

### 2. Trivial work stays trivial

**Prompt:** “Rename this private helper to `…`” or “Clarify this comment” (same component).

**Good:** Small diff; no architecture/benchmark detour unless the edit touches a classified concern.

**Bad:** Full doctrine dump; unnecessary reads; design log for a rename.

### 3. Escalate consequential changes

**Prompt:** One of: change ownership/`Arc` layout, add an atomic on shared state, change event representation, add allocation on hot path.

**Good:** Names decision class; loads **concurrency** / **atomics** / **allocation** / **networking-serialization** references selectively; ties to invariants.

**Bad:** Treats like rename; or loads entire skill corpus.

### 4. Evidence closes the loop

Follow-up on a performance-sensitive proposal: “Fine, just do it.”

**Good:** Holds line or implements with **defined measurement** and does not claim improvement until measured.

**Bad:** Compliance without verification plan; “should be faster” in summary.

## Scorecard (copy per session)

Rate **A** and **B** separately (1–5 or ✓/△/✗). Notes column is mandatory.

| Dimension | What good looks like | A | B | Notes |
|-----------|----------------------|---|---|-------|
| **Context selection** | Only relevant doctrine + project files | | | |
| **False positives** | Trivial work stays trivial | | | |
| **Engineering quality** | Correct machine/system concern named | | | |
| **Evidence discipline** | No unsupported “faster” claims | | | |
| **Friction** | Few unnecessary reads/gates | | | |
| **Recovery** | Clear message when blocked; path to unblock | | | |
| **Consistency** | Same policy after “just do it” / pushback | | | |

**Pass threshold (subjective):** Chat A beats B on **engineering quality** and **evidence discipline** without wrecking **false positives** and **friction**. Hooks blocking once is necessary but not sufficient.

## What to bring back to cursor-hub

After the experiment, capture **concrete** failures (not hypotheticals):

- Wrong doctrine topics loaded / not loaded
- Ceremony on trivial edits
- Policy ignored despite reads
- `conversation_id` absent or ephemeral leakage observed
- Bypass via shell/MCP (expected — note frequency only)

Those findings drive the **next** harness change; avoid speculative framework work until then.

## Related

- [engineering-doctrine.md](engineering-doctrine.md) — install, hooks, ownership
- [skills/engineering-doctrine/SKILL.md](../skills/engineering-doctrine/SKILL.md) — decision router
