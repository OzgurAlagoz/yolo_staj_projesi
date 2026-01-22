# Task: Robustness and Failure Case Analysis

- [ ] **Instrumentation**
    - [ ] Modify `src/tracker_bytetrack.py` to log Unique ID counts.
    - [ ] Modify `src/tracker_deepsort.py` to log Unique ID counts.
- [ ] **Tuning Setup**
    - [ ] Modify `configs/custom_bytetrack.yaml` temporarily for tuning tests.
- [ ] **Execution & Analysis**
    - [ ] Run ByteTrack on `store-aisle` (Baseline).
    - [ ] Run ByteTrack on `store-aisle` (Tuned).
    - [ ] Run DeepSORT on `classroom` (Occlusion test).
- [ ] **Reporting**
    - [ ] Create `reports/failure_analysis.md` with:
        - [ ] Metrics (FPS, ID Counts).
        - [ ] Failure Case Examples (Occlusion, Crowd).
        - [ ] Tuning Results (Improvement analysis).
