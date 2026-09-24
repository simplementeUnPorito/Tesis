# Autonomous Experimental Campaign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, verify, and launch a time-aware, append-only experimental campaign that gathers thesis evidence overnight and remains safely interruptible and resumable during the day.

**Architecture:** A small `lab/campaign` package separates append-only persistence, scheduling, experiment selection, hardware access, execution, analysis, and supervision. `lab/campana_experimental.py` is the only user-facing command and the acquisition process is the only owner of COM8; analysis reads complete JSONL records without opening the port.

**Tech Stack:** Python 3.14 standard library (`argparse`, `dataclasses`, `datetime`, `json`, `signal`, `statistics`, `unittest`, `zoneinfo`), existing `pyserial`, existing `lab/barrido_total.py` hardware primitives.

**Spec:** `lab/specs/2026-09-23-campana-experimental-autonoma-design.md`

## Global Constraints

- Do not change GPIO19, GPIO26, or GPIO27 or any hardware pin assignment.
- The only PSoC reset is the existing ESP32 `psocreset` command through GPIO19.
- Do not flash firmware during a campaign.
- Use `America/Asuncion`; save both local offset-aware and UTC timestamps.
- Before 07:00 long tests are allowed; from 07:00 only bounded, checkpointed work may start.
- Every received sample is appended before advancing campaign state.
- Never rewrite or delete historical campaign results.
- Default storage budget is 3 GiB; warn at 90% and stop new acquisition at 95%.
- A user stop is normal and must not consume supervisor restart attempts.
- Keep the current `barrido_reaprendizaje_20260923` process running until the new implementation passes its hardware smoke test.
- Use only Python standard-library additions; do not add a database or scheduler dependency.

## Review Focus

- A stop arriving between journal append and checkpoint update must resume without duplicating the completed event; Task 1 tests event-ID deduplication and Task 5 tests crash recovery.
- A local-time transition through 07:00 or a UTC-offset change must never start long work; Task 2 tests offset-aware boundary times and conservative scheduling.
- Invalid-but-fresh analog taps must remain evidence rather than being mistaken for a dead acquisition path; Task 4 tests the distinction.
- A reset failure or absent COM8 must back off and preserve the active visit instead of producing a false FALLA; Tasks 4 and 7 test both paths.
- Analysis during a partial final JSONL write must ignore only the incomplete tail and must never open COM8; Tasks 1 and 6 test truncation and port isolation.

---

## File Structure

- `lab/campaign/__init__.py`: package version and public types.
- `lab/campaign/model.py`: immutable identifiers, campaign/event/visit/work-item dataclasses and serialization.
- `lab/campaign/journal.py`: append-only JSONL, atomic state, storage budget, snapshots, recovery.
- `lab/campaign/schedule.py`: timezone-aware night/day policy and safe-start decisions.
- `lab/campaign/catalog.py`: ordered N0-N4/D0-D3 work generation and representative-pair selection.
- `lab/campaign/hardware.py`: allowlisted adapter around `barrido_total` serial primitives and locked pin manifest.
- `lab/campaign/runner.py`: cancelable sampling, visit closure, reset blocks and campaign state machine.
- `lab/campaign/analysis.py`: deterministic aggregate metrics and report/CSV generation.
- `lab/campaign/legacy.py`: idempotent import of existing `resultados.jsonl`.
- `lab/campaign/supervisor.py`: child lifecycle, backoff, compact health and actionable alerts.
- `lab/campana_experimental.py`: `run`, `resume`, `status`, `stop`, `analyze`, and `import-legacy` CLI.
- `lab/README.md`: copy/paste operating instructions for Windows and Linux.
- `lab/test_campaign_*.py`: unit and integration tests using `unittest` and fake hardware.

### Task 1: Append-only domain model and journal

**Files:**
- Create: `lab/campaign/__init__.py`
- Create: `lab/campaign/model.py`
- Create: `lab/campaign/journal.py`
- Create: `lab/test_campaign_journal.py`

**Interfaces:**
- Produces: `CampaignConfig`, `Event`, `Visit`, `WorkItem`, `Journal.append_event()`, `Journal.close_visit()`, `Journal.load_events(kind: str | None = None)`, `Journal.load_visits()`, `Journal.write_state()`, `Journal.read_state()`, `Journal.snapshot()`, and `Journal.storage_status()`.
- Consumes: filesystem paths and JSON-serializable dictionaries only.

- [ ] **Step 1: Write failing serialization, truncation, deduplication, and budget tests**

```python
class JournalTests(unittest.TestCase):
    def test_incomplete_tail_is_ignored_and_event_id_is_idempotent(self):
        journal = Journal(self.root, budget_bytes=100_000)
        event = Event.make("c1", "e1", "b1", "v1", "sample", {"lp_uv": 12})
        self.assertTrue(journal.append_event(event))
        self.assertFalse(journal.append_event(event))
        with journal.events_path.open("ab") as fh:
            fh.write(b'{"event_id":"cut')
        self.assertEqual([event.event_id], [e.event_id for e in journal.load_events()])

    def test_storage_thresholds_are_exact(self):
        journal = Journal(self.root, budget_bytes=100)
        self.assertEqual("ok", journal.storage_status(89))
        self.assertEqual("warning", journal.storage_status(90))
        self.assertEqual("stop", journal.storage_status(95))

    def test_state_is_rebuilt_from_complete_records(self):
        journal = Journal(self.root)
        journal.append_event(Event.make("c1", "e1", "b1", "v1", "sample", {}))
        journal.close_visit(Visit.interrupted("c1", "e1", "b1", "v1", "operator"))
        self.assertEqual("v1", journal.rebuild_state()["last_visit_id"])
```

- [ ] **Step 2: Run the tests and verify the expected import failure**

Run: `python -m unittest -v lab.test_campaign_journal`

Expected: FAIL because `lab.campaign.journal` does not exist.

- [ ] **Step 3: Implement immutable records and canonical JSON serialization**

```python
@dataclass(frozen=True)
class Event:
    event_id: str
    campaign_id: str
    experiment_id: str
    block_id: str
    visit_id: str
    kind: str
    local_time: str
    utc_time: str
    monotonic_s: float
    payload: dict[str, Any]

    @classmethod
    def make(cls, campaign_id, experiment_id, block_id, visit_id, kind, payload):
        now = datetime.now(UTC)
        key = f"{campaign_id}|{experiment_id}|{block_id}|{visit_id}|{kind}|{time.monotonic_ns()}"
        return cls(hashlib.sha256(key.encode()).hexdigest()[:24], campaign_id,
                   experiment_id, block_id, visit_id, kind,
                   now.astimezone(ZoneInfo("America/Asuncion")).isoformat(),
                   now.isoformat(), time.monotonic(), payload)
```

Define `Visit.status` as one of `COMPLETE`, `INTERRUPTED`, `INVALID`, or `ERROR`. Define `WorkItem` with `kind`, `pair`, `max_duration_s`, `reset_policy`, `interruptible`, `order_index`, and `metadata`.

- [ ] **Step 4: Implement append with flush/fsync, complete-line loading, atomic state, snapshot, and budget checks**

```python
def _append_json(path: Path, payload: dict[str, Any]) -> None:
    encoded = (json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n").encode()
    with path.open("ab", buffering=0) as fh:
        fh.write(encoded)
        os.fsync(fh.fileno())

def _load_complete_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        raw = raw[:raw.rfind(b"\n") + 1]
    return [json.loads(line) for line in raw.splitlines() if line.strip()]
```

Use a set of loaded IDs to make `append_event()` and `close_visit()` idempotent. Write state to `state.json.tmp`, `fsync`, then `os.replace`.

- [ ] **Step 5: Run tests and syntax checks**

Run: `python -m unittest -v lab.test_campaign_journal && python -m py_compile lab/campaign/model.py lab/campaign/journal.py`

Expected: all tests PASS and compilation exits 0.

- [ ] **Step 6: Commit Task 1**

```powershell
git add -- lab/campaign/__init__.py lab/campaign/model.py lab/campaign/journal.py lab/test_campaign_journal.py
git commit -m "feat(lab): add append-only campaign journal"
```

### Task 2: Time-aware scheduler and stop policy

**Files:**
- Create: `lab/campaign/schedule.py`
- Create: `lab/test_campaign_schedule.py`

**Interfaces:**
- Consumes: `datetime`, `WorkItem`, `margin_s`.
- Produces: `SchedulePolicy.phase_at(now) -> Literal["night", "day"]`, `seconds_until_day(now) -> float`, `may_start(item, now) -> bool`, and `StopToken`.

- [ ] **Step 1: Write failing boundary, offset-aware, and stop-token tests**

```python
class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.tz = ZoneInfo("America/Asuncion")
        self.policy = SchedulePolicy(day_starts=time(7, 0), margin_s=600)

    def test_065959_is_night_and_070000_is_day(self):
        self.assertEqual("night", self.policy.phase_at(datetime(2026, 9, 23, 6, 59, 59, tzinfo=self.tz)))
        self.assertEqual("day", self.policy.phase_at(datetime(2026, 9, 23, 7, 0, 0, tzinfo=self.tz)))

    def test_long_item_is_rejected_when_it_does_not_fit(self):
        item = WorkItem.example(max_duration_s=1200, interruptible=False)
        now = datetime(2026, 9, 23, 6, 45, tzinfo=self.tz)
        self.assertFalse(self.policy.may_start(item, now))

    def test_stop_file_and_signal_share_one_token(self):
        token = StopToken(self.root / ".run" / "STOP")
        token.path.parent.mkdir(parents=True)
        token.path.write_text("stop\n", encoding="ascii")
        self.assertTrue(token.requested())
        self.assertEqual("stop_file", token.reason)
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest -v lab.test_campaign_schedule`

Expected: FAIL because `SchedulePolicy` and `StopToken` are undefined.

- [ ] **Step 3: Implement conservative local scheduling**

```python
def may_start(self, item: WorkItem, now: datetime) -> bool:
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    if self.phase_at(now) == "day":
        return item.interruptible and item.max_duration_s <= self.day_unit_limit_s
    return item.max_duration_s + self.margin_s <= self.seconds_until_day(now)
```

Calculate the next 07:00 in `America/Asuncion`, never by adding a fixed number of UTC seconds. `StopToken.request()` sets an in-memory event; `requested()` checks both the event and the exact stop-file path.

- [ ] **Step 4: Run tests and compile**

Run: `python -m unittest -v lab.test_campaign_schedule && python -m py_compile lab/campaign/schedule.py`

Expected: PASS.

- [ ] **Step 5: Commit Task 2**

```powershell
git add -- lab/campaign/schedule.py lab/test_campaign_schedule.py
git commit -m "feat(lab): schedule night and interruptible day work"
```

### Task 3: Ordered experiment catalog and representative selection

**Files:**
- Create: `lab/campaign/catalog.py`
- Create: `lab/test_campaign_catalog.py`

**Interfaces:**
- Consumes: completed `Visit` records, phase, deterministic seed.
- Produces: `select_representative_pairs(visits)`, `Catalog.next_items(phase, visits, seed)`, ordered experiment IDs `N0` through `N4` and `D0` through `D3`.

- [ ] **Step 1: Write failing ordering and selection tests**

```python
class CatalogTests(unittest.TestCase):
    def test_representatives_include_control_top_stable_and_boundary(self):
        visits = fixture_visits()
        pairs = select_representative_pairs(visits, stable_count=5, boundary_count=2)
        self.assertEqual((1, 1), pairs[0])
        self.assertEqual(8, len(pairs))
        self.assertEqual(pairs, select_representative_pairs(visits, 5, 2))

    def test_night_order_is_fixed(self):
        ids = [item.experiment_id for item in Catalog().next_items("night", fixture_visits(), 19)]
        self.assertEqual(["N0", "N1", "N2", "N3", "N4"], list(dict.fromkeys(ids)))

    def test_day_never_contains_reset_or_unbounded_work(self):
        items = Catalog().next_items("day", fixture_visits(), 19)
        self.assertTrue(all(i.reset_policy == "never" and i.interruptible for i in items))
        self.assertEqual(["D0", "D1", "D2", "D3"], list(dict.fromkeys(i.experiment_id for i in items)))
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest -v lab.test_campaign_catalog`

Expected: FAIL because the catalog is absent.

- [ ] **Step 3: Implement scoring without outcome leakage**

```python
def pair_score(rows: list[Visit]) -> tuple[float, float, float]:
    complete = [r for r in rows if r.status == "COMPLETE"]
    pass_rate = sum(r.verdict == "PASA" for r in complete) / max(1, len(complete))
    gain = rows[0].pga * rows[0].pgaout
    spread = statistics.pstdev([r.lp_final_mv for r in complete if r.lp_final_mv is not None]) if len(complete) > 1 else float("inf")
    return pass_rate, gain, -spread
```

Freeze selected pairs in each generated block's metadata. Generate ascendant, descendant, and serpentine N2 sequences from the frozen set. N3 always starts with `(1, 1)`, records `before_reset` and `after_reset`, and uses only the existing reset policy. Day D0 prioritizes missing/discordant pairs; D1 is one bounded full round; D2 inserts `(1, 1)` controls; D3 emits an analysis work item that does not require hardware.

- [ ] **Step 4: Run tests and compile**

Run: `python -m unittest -v lab.test_campaign_catalog && python -m py_compile lab/campaign/catalog.py`

Expected: PASS.

- [ ] **Step 5: Commit Task 3**

```powershell
git add -- lab/campaign/catalog.py lab/test_campaign_catalog.py
git commit -m "feat(lab): define ordered thesis experiment catalog"
```

### Task 4: Locked and allowlisted hardware adapter

**Files:**
- Create: `lab/campaign/hardware.py`
- Create: `lab/test_campaign_hardware.py`
- Modify: `lab/barrido_total.py` only if a public wrapper is required; do not change pin constants or command semantics.

**Interfaces:**
- Consumes: port name and existing `barrido_total` functions.
- Produces: `Hardware.open()`, `close()`, `ensure_acquisition()`, `set_gain()`, `snapshot()`, `reset_psoc()`, `wait_ready()`, and `PIN_LOCK`.

- [ ] **Step 1: Write failing command allowlist, pin-lock, fresh-invalid and reset tests**

```python
class HardwareTests(unittest.TestCase):
    def test_pin_manifest_is_immutable(self):
        self.assertEqual({"psoc_reset": 19, "psoc_uart": 26, "psoc_sync": 27}, dict(PIN_LOCK))
        with self.assertRaises(TypeError):
            PIN_LOCK["psoc_reset"] = 18

    def test_unknown_command_is_rejected_before_serial_write(self):
        backend = FakeBackend()
        hw = Hardware("COM8", backend=backend)
        with self.assertRaises(UnsafeCommand):
            hw.command("gpio 19 low")
        self.assertEqual([], backend.writes)

    def test_fresh_out_of_range_taps_prove_acquisition_is_alive(self):
        hw = Hardware("COM8", backend=FakeBackend(snapshot=fresh_snapshot(valid=False)))
        self.assertTrue(hw.ensure_acquisition())

    def test_reset_sequence_uses_only_psocreset(self):
        backend = FakeBackend(snapshot=fresh_snapshot(valid=True))
        Hardware("COM8", backend=backend).reset_psoc()
        self.assertEqual(["psocreset"], backend.writes)
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest -v lab.test_campaign_hardware`

Expected: FAIL because the adapter is absent.

- [ ] **Step 3: Implement the adapter and explicit allowlist**

```python
PIN_LOCK = MappingProxyType({"psoc_reset": 19, "psoc_uart": 26, "psoc_sync": 27})
EXACT_COMMANDS = frozenset({"clear", "startwait 5", "ctl report", "psocreset"})
PATTERN_COMMANDS = (re.compile(r"pga [0-8]$"), re.compile(r"pgaout [0-8]$"), re.compile(r"ctl get (?:0|1)$"))

def _allowed(command: str) -> bool:
    return command in EXACT_COMMANDS or any(p.fullmatch(command) for p in PATTERN_COMMANDS)
```

The real backend initializes and closes the existing `barrido_total` reader exactly once. It treats recent tap values with `valid=0` as live acquisition data and leaves validity for later verdict analysis. `reset_psoc()` sends only `psocreset`, clears stale telemetry, waits up to the configured readiness deadline, then checks acquisition.

- [ ] **Step 4: Run the adapter and existing sweep regression tests**

Run: `python -m unittest -v lab.test_campaign_hardware lab.test_barrido_total && python -m py_compile lab/campaign/hardware.py lab/barrido_total.py`

Expected: PASS with no pin changes in `git diff`.

- [ ] **Step 5: Commit Task 4**

```powershell
git add -- lab/campaign/hardware.py lab/test_campaign_hardware.py lab/barrido_total.py
git commit -m "feat(lab): add locked ESP32 PSoC hardware adapter"
```

### Task 5: Cancelable runner, checkpoints, and crash-safe resume

**Files:**
- Create: `lab/campaign/runner.py`
- Create: `lab/test_campaign_runner.py`

**Interfaces:**
- Consumes: `Journal`, `SchedulePolicy`, `Catalog`, `Hardware`, `StopToken`.
- Produces: `CampaignRunner.run()`, `run_item()`, `run_gain_visit()`, `run_drift_block()`, `run_reset_block()`, and compact health updates.

- [ ] **Step 1: Write failing stop, interruption, crash, no-reset and reset tests**

```python
class RunnerTests(unittest.TestCase):
    def test_stop_after_sample_closes_interrupted_visit(self):
        stop = StopAfterChecks(2)
        runner = make_runner(stop=stop, hardware=FakeHardware([sample(1), sample(2)]))
        runner.run_item(gain_item((8, 16), duration_s=60))
        visit = runner.journal.load_visits()[-1]
        self.assertEqual("INTERRUPTED", visit.status)
        self.assertEqual(2, len(runner.journal.load_events(kind="sample")))

    def test_resume_does_not_duplicate_completed_event(self):
        runner = make_runner(crash_after_append=True)
        with self.assertRaises(SimulatedCrash):
            runner.run_item(gain_item((1, 1), duration_s=2))
        resumed = make_runner(root=runner.root)
        resumed.run_item(gain_item((1, 1), duration_s=2))
        ids = [e.event_id for e in resumed.journal.load_events()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_warm_drift_never_resets(self):
        hardware = FakeHardware(repeating_sample=sample(0))
        make_runner(hardware=hardware).run_item(drift_item((1, 1), duration_s=6))
        self.assertEqual(0, hardware.reset_count)

    def test_reset_block_records_paired_measurements(self):
        hardware = FakeHardware(repeating_sample=sample(0))
        runner = make_runner(hardware=hardware)
        runner.run_item(reset_item((1, 1)))
        kinds = [e.kind for e in runner.journal.load_events()]
        self.assertEqual(1, hardware.reset_count)
        self.assertIn("before_reset", kinds)
        self.assertIn("after_reset", kinds)
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest -v lab.test_campaign_runner`

Expected: FAIL because `CampaignRunner` is undefined.

- [ ] **Step 3: Implement sample-first persistence and terminal visit closure**

```python
while elapsed < item.max_duration_s:
    if self.stop.requested():
        return self._close_interrupted(ctx, self.stop.reason)
    snap = self.hardware.snapshot()
    event = self._sample_event(ctx, snap)
    self.journal.append_event(event)
    self.journal.write_state(self._state_after(event))
    if self.stop.requested():
        return self._close_interrupted(ctx, self.stop.reason)
    if self._criterion_met(item, ctx.samples):
        return self._close_complete(ctx)
    self.clock.sleep(self.sample_period_s)
```

Generate deterministic event IDs from campaign, visit, sample index, and payload hash so replay after a crash is idempotent. Record invalid readings as samples. Classify a visit only at closure. `INTERRUPTED` and `ERROR` never become `FALLA`.

- [ ] **Step 4: Implement ordered run loop and storage/07:00 transitions**

Before every item: check storage, current phase, `may_start`, and stop. At 90% append `STORAGE_WARNING`; at 95% run analysis work only and set `needs_operator`. If 07:00 arrives during an interruptible item, close it at the next sample. A non-interruptible night item can only exist if it passed the conservative fit check.

- [ ] **Step 5: Run runner tests plus all campaign tests**

Run: `python -m unittest -v lab.test_campaign_journal lab.test_campaign_schedule lab.test_campaign_catalog lab.test_campaign_hardware lab.test_campaign_runner`

Expected: PASS.

- [ ] **Step 6: Commit Task 5**

```powershell
git add -- lab/campaign/runner.py lab/test_campaign_runner.py
git commit -m "feat(lab): run checkpointed and cancelable experiments"
```

### Task 6: Deterministic cumulative analysis

**Files:**
- Create: `lab/campaign/analysis.py`
- Create: `lab/test_campaign_analysis.py`

**Interfaces:**
- Consumes: snapshot paths from `Journal.snapshot()`.
- Produces: `analyze(snapshot) -> Analysis`, `write_csv()`, and `write_report()`; never imports `serial` or `hardware`.

- [ ] **Step 1: Write failing aggregation, censoring, reset-pair and no-serial tests**

```python
class AnalysisTests(unittest.TestCase):
    def test_interrupted_is_reported_but_not_counted_as_failure(self):
        result = analyze(snapshot_with("PASA", "FALLA", "INTERRUPTED"))
        self.assertEqual(1, result.counts["PASA"])
        self.assertEqual(1, result.counts["FALLA"])
        self.assertEqual(1, result.counts["INTERRUPTED"])
        self.assertEqual(2, result.verdict_denominator)

    def test_reset_delta_is_paired_by_block_and_pair(self):
        result = analyze(snapshot_with_reset_pair(before_mv=12.0, after_mv=20.0))
        self.assertEqual(8.0, result.reset_deltas_mv[("b1", 1, 1)])

    def test_analysis_does_not_import_serial_stack(self):
        with mock.patch.dict(sys.modules, {"serial": None}):
            importlib.reload(analysis_module)
            analysis_module.analyze(self.snapshot)
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest -v lab.test_campaign_analysis`

Expected: FAIL because analysis is absent.

- [ ] **Step 3: Implement robust summaries**

Calculate per pair and condition: complete observations, verdict denominator, PASS rate, median and p90 stabilization time, worst complete stabilization time, LP median/range/p10/p90, linear drift in mV/h with sample count and duration, IDAC ranges, tap saturation rate, before/after reset deltas, and order-specific medians. Require at least three complete visits before labeling a result repeatable; otherwise label it exploratory.

Use simple least squares implemented locally:

```python
def slope_per_hour(points: list[tuple[float, float]]) -> float | None:
    if len(points) < 2 or points[-1][0] == points[0][0]:
        return None
    mx = statistics.fmean(x for x, _ in points)
    my = statistics.fmean(y for _, y in points)
    den = sum((x - mx) ** 2 for x, _ in points)
    return 3600.0 * sum((x - mx) * (y - my) for x, y in points) / den
```

- [ ] **Step 4: Write atomic CSV and Markdown outputs with visit traceability**

Write temporary files followed by `os.replace`. Every aggregate row includes source `visit_id` values or a deterministic group identifier. Include a `BLOQUEADO_POR_HARDWARE` section for ADC synchronization, low-frequency excitation, additional nodes, and simultaneous MASW.

- [ ] **Step 5: Run analysis tests and compile**

Run: `python -m unittest -v lab.test_campaign_analysis && python -m py_compile lab/campaign/analysis.py`

Expected: PASS.

- [ ] **Step 6: Commit Task 6**

```powershell
git add -- lab/campaign/analysis.py lab/test_campaign_analysis.py
git commit -m "feat(lab): analyze cumulative experiment evidence"
```

### Task 7: CLI, supervisor, status, and normal operator stop

**Files:**
- Create: `lab/campaign/supervisor.py`
- Create: `lab/campana_experimental.py`
- Create: `lab/test_campaign_cli.py`
- Create: `lab/test_campaign_supervisor.py`

**Interfaces:**
- Consumes: package components from Tasks 1-6.
- Produces: commands `run`, `resume`, `status`, `stop`, `analyze`, `import-legacy`; supervisor health states `starting`, `running`, `recovering`, `waiting_for_device`, `stopped_by_operator`, `complete`, `needs_operator`.

- [ ] **Step 1: Write failing parser and stop/status tests**

```python
class CliTests(unittest.TestCase):
    def test_defaults_lock_timezone_budget_and_port(self):
        ns = parse_args(["run", "--output", "run1"])
        self.assertEqual("COM8", ns.port)
        self.assertEqual("America/Asuncion", ns.timezone)
        self.assertEqual(3 * 1024 ** 3, ns.budget_bytes)

    def test_stop_creates_exact_stop_file(self):
        rc = main(["stop", "--output", str(self.root)])
        self.assertEqual(0, rc)
        self.assertEqual("stop\n", (self.root / ".run" / "STOP").read_text())

    def test_status_reads_health_without_opening_hardware(self):
        write_health(self.root, status="running")
        with mock.patch("lab.campaign.hardware.Hardware.open") as opened:
            self.assertEqual(0, main(["status", "--output", str(self.root)]))
            opened.assert_not_called()
```

- [ ] **Step 2: Write failing supervisor planned-stop and backoff tests**

```python
class SupervisorTests(unittest.TestCase):
    def test_operator_stop_is_not_a_failure(self):
        sup = Supervisor(FakeChild(returncode=0, health="stopped_by_operator"))
        self.assertEqual(0, sup.run())
        self.assertEqual(0, sup.failure_count)

    def test_missing_device_waits_without_spending_restarts(self):
        sup = Supervisor(FakePortDetector([None, None, "COM8"]), FakeChild(0))
        sup.run(max_cycles=3)
        self.assertEqual(0, sup.failure_count)
```

- [ ] **Step 3: Run tests and verify failure**

Run: `python -m unittest -v lab.test_campaign_cli lab.test_campaign_supervisor`

Expected: FAIL because CLI and supervisor are absent.

- [ ] **Step 4: Implement CLI and process ownership**

`run` creates `campaign.json` if absent, refuses to run if a live PID owns the output, removes only a stale STOP file after recording `RESUME_REQUESTED`, and invokes the supervisor. `resume` requires an existing campaign. `status`, `stop`, and `analyze` never instantiate hardware. `stop` writes `.run/STOP` atomically rather than killing the child.

- [ ] **Step 5: Implement supervisor backoff and compact alerts**

Reuse the proven backoff sequence `[15, 30, 60, 120, 300, 600]`. Treat `stopped_by_operator` and `complete` as successful terminal states. Treat missing hardware as `waiting_for_device` without incrementing failures. After eight actual process failures, write `alert.json` with `requires_codex: true` and the last 30 output lines.

- [ ] **Step 6: Run CLI, supervisor, and complete campaign test suite**

Run: `python -m unittest -v lab.test_campaign_journal lab.test_campaign_schedule lab.test_campaign_catalog lab.test_campaign_hardware lab.test_campaign_runner lab.test_campaign_analysis lab.test_campaign_cli lab.test_campaign_supervisor`

Expected: PASS.

- [ ] **Step 7: Commit Task 7**

```powershell
git add -- lab/campaign/supervisor.py lab/campana_experimental.py lab/test_campaign_cli.py lab/test_campaign_supervisor.py
git commit -m "feat(lab): add autonomous campaign CLI and supervisor"
```

### Task 8: Idempotent legacy import and historical parity

**Files:**
- Create: `lab/campaign/legacy.py`
- Create: `lab/test_campaign_legacy.py`

**Interfaces:**
- Consumes: current `resultados.jsonl` and target `Journal`.
- Produces: `import_barrido(path, journal) -> ImportSummary` with deterministic IDs and unchanged source files.

- [ ] **Step 1: Write failing import idempotence and parity tests**

```python
class LegacyImportTests(unittest.TestCase):
    def test_import_twice_keeps_one_visit_per_source_row(self):
        source = write_legacy_rows(self.root, [legacy_row(1, 1, 1), legacy_row(8, 50, 1)])
        journal = Journal(self.root / "new")
        first = import_barrido(source, journal)
        second = import_barrido(source, journal)
        self.assertEqual(2, first.imported)
        self.assertEqual(0, second.imported)
        self.assertEqual(2, len(journal.load_visits()))

    def test_import_preserves_verdict_counts_and_source_bytes(self):
        before = self.source.read_bytes()
        summary = import_barrido(self.source, self.journal)
        self.assertEqual({"PASA": 38, "FALLA": 25, "APRENDIENDO": 18}, summary.verdicts)
        self.assertEqual(before, self.source.read_bytes())
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m unittest -v lab.test_campaign_legacy`

Expected: FAIL because importer is absent.

- [ ] **Step 3: Implement deterministic import**

Derive `visit_id` as SHA-256 of the normalized absolute source path, source line number, legacy `vuelta`, `pga_cod`, `pgaout_cod`, and `marca`. Map legacy `APRENDIENDO` to a completed observation whose `verdict` remains `APRENDIENDO`; do not map it to `INTERRUPTED`. Store source path, line, and row hash in metadata.

- [ ] **Step 4: Run importer tests against a snapshot of the real campaign**

Run:

```powershell
python -m unittest -v lab.test_campaign_legacy
python lab/campana_experimental.py import-legacy --source lab/barrido_reaprendizaje_20260923/resultados.jsonl --output lab/_import_validation
python lab/campana_experimental.py analyze --output lab/_import_validation
```

Expected: imported row count equals the complete-line count in the source; verdict counts in the generated report equal the source counts. Remove only the exact temporary `lab/_import_validation` directory after inspecting its resolved path is inside `C:\Github\Tesis\lab`.

- [ ] **Step 5: Commit Task 8**

```powershell
git add -- lab/campaign/legacy.py lab/test_campaign_legacy.py lab/campana_experimental.py
git commit -m "feat(lab): import legacy sweep evidence idempotently"
```

### Task 9: Operator documentation and full simulated acceptance

**Files:**
- Modify: `lab/README.md`
- Create: `lab/test_campaign_acceptance.py`

**Interfaces:**
- Consumes: public CLI from Task 7.
- Produces: copy/paste runbook and one end-to-end simulated campaign.

- [ ] **Step 1: Write a failing end-to-end simulation**

```python
class AcceptanceTests(unittest.TestCase):
    def test_night_to_day_stop_resume_and_analysis(self):
        clock = ScriptedClock([night_time(), day_time()])
        app = simulated_app(self.root, clock=clock)
        app.run(max_items=3)
        app.stop()
        app.resume(max_items=2)
        report = app.analyze()
        self.assertGreater(len(app.journal.load_events()), 0)
        self.assertTrue(any(v.status == "INTERRUPTED" for v in app.journal.load_visits()))
        self.assertIn("N1", report.experiments)
        self.assertIn("D0", report.experiments)
        self.assertFalse(app.hardware.concurrent_open_detected)
```

- [ ] **Step 2: Run acceptance test and verify failure**

Run: `python -m unittest -v lab.test_campaign_acceptance`

Expected: FAIL until all simulation seams are connected.

- [ ] **Step 3: Connect injectable clock/hardware seams and make acceptance pass**

Do not introduce a separate simulation implementation. Inject `Clock` and `Hardware` protocols into the same runner used by production. Ensure the test traverses journal, scheduler, catalog, runner, stop/resume, and analysis.

- [ ] **Step 4: Document exact operating commands**

Add the following verified workflow to `lab/README.md`, with PowerShell and Linux path examples:

```text
python lab/campana_experimental.py run --port COM8 --output lab/campanas/campana_YYYYMMDD
python lab/campana_experimental.py status --output lab/campanas/campana_YYYYMMDD
python lab/campana_experimental.py stop --output lab/campanas/campana_YYYYMMDD
python lab/campana_experimental.py resume --port COM8 --output lab/campanas/campana_YYYYMMDD
python lab/campana_experimental.py analyze --output lab/campanas/campana_YYYYMMDD
```

Explain that `stop` is safe, `resume` appends, analysis does not use COM8, the laptop must remain powered while it owns USB, and Linux uses the detected `/dev/serial/by-id/...` path.

- [ ] **Step 5: Run every campaign test and static compilation**

Run:

```powershell
python -m unittest -v lab.test_barrido_total lab.test_campaign_journal lab.test_campaign_schedule lab.test_campaign_catalog lab.test_campaign_hardware lab.test_campaign_runner lab.test_campaign_analysis lab.test_campaign_cli lab.test_campaign_supervisor lab.test_campaign_legacy lab.test_campaign_acceptance
python -m compileall -q lab/campaign lab/campana_experimental.py
git diff --check
```

Expected: all tests PASS, compilation exits 0, and `git diff --check` is silent.

- [ ] **Step 6: Commit Task 9**

```powershell
git add -- lab/README.md lab/test_campaign_acceptance.py lab/campaign lab/campana_experimental.py
git commit -m "docs(lab): add autonomous campaign operating runbook"
```

### Task 10: Hardware smoke test, migration, launch, and monitoring

**Files:**
- Runtime output only: `lab/campanas/campana_<timestamp>/`
- Modify only if the smoke test exposes a verified defect: the owning production file and its regression test.

**Interfaces:**
- Consumes: validated CLI, current COM8 hardware, legacy results, current supervisor PID/health.
- Produces: live autonomous campaign, imported evidence, compact health, and active 40-minute heartbeat.

- [ ] **Step 1: Record the current campaign checkpoint without opening COM8**

Run:

```powershell
Get-Content -Raw -LiteralPath lab\barrido_reaprendizaje_20260923\.run\health.json
(Get-Content -LiteralPath lab\barrido_reaprendizaje_20260923\resultados.jsonl).Count
Get-Content -LiteralPath lab\barrido_reaprendizaje_20260923\.run\supervisor.log -Tail 20
```

Expected: `status` is `running` or a diagnosed recoverable state; record the complete-row count.

- [ ] **Step 2: Request a safe boundary and stop only the verified old supervisor tree**

Wait until `resultados.jsonl` gains a complete line or the active visit reaches its documented maximum. Resolve the exact supervisor PID from its PID file and child PID from health. Verify both command lines contain the expected scripts, then stop child and supervisor. Recount JSONL and confirm every line parses. Preserve all old `.run` logs under timestamped names.

- [ ] **Step 3: Run isolated hardware smoke test**

Run:

```powershell
python lab/campana_experimental.py run --port COM8 --output lab/campanas/smoke_20260923 --max-items 1 --day-unit-limit-s 30
python lab/campana_experimental.py status --output lab/campanas/smoke_20260923
python lab/campana_experimental.py stop --output lab/campanas/smoke_20260923
python lab/campana_experimental.py resume --port COM8 --output lab/campanas/smoke_20260923 --max-items 1
python lab/campana_experimental.py analyze --output lab/campanas/smoke_20260923
```

Expected: one bounded `x1/x1` visit, a normal stop, COM8 released, resume appends without duplicate IDs, and analysis completes without hardware access.

- [ ] **Step 4: Import the historical campaign into a new production directory**

Create one timestamped production directory and run:

```powershell
python lab/campana_experimental.py import-legacy --source lab/barrido_reaprendizaje_20260923/resultados.jsonl --output lab/campanas/campana_20260923
python lab/campana_experimental.py analyze --output lab/campanas/campana_20260923
```

Compare imported row count and verdict counts with the original using a read-only script. Do not alter the legacy directory.

- [ ] **Step 5: Launch production campaign hidden under its supervisor**

Run `python lab/campana_experimental.py run --port COM8 --output lab/campanas/campana_20260923` through `Start-Process -WindowStyle Hidden`, redirecting stdout/stderr into its `.run` directory. Verify `health.json` reports `running`, no `alert.json` exists, the PID command line is correct, and at least one new event line is appended.

- [ ] **Step 6: Update the 40-minute heartbeat**

Point the existing heartbeat to the new production directory. It reads only `health.json` and actionable `alert.json`, stays silent during healthy work, never opens COM8, diagnoses only deterministic safe recoveries, and notifies on physical intervention, exhausted recovery, storage threshold, or explicit completion.

- [ ] **Step 7: Run fresh final verification and push**

Run:

```powershell
python -m unittest -v lab.test_barrido_total lab.test_campaign_journal lab.test_campaign_schedule lab.test_campaign_catalog lab.test_campaign_hardware lab.test_campaign_runner lab.test_campaign_analysis lab.test_campaign_cli lab.test_campaign_supervisor lab.test_campaign_legacy lab.test_campaign_acceptance
python -m compileall -q lab/campaign lab/campana_experimental.py
git diff --check
git status --short
```

Expected: tests PASS, compilation exits 0, no whitespace errors, only runtime campaign data remains untracked, and no unrelated user changes are staged.

Commit only implementation and documentation files, then `git push origin main`. Report the production output directory, active health state, imported/new event counts, the five operator commands, and the fact that GPIO assignments were unchanged.
