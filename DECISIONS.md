## ADR-007

Use a component-based React architecture with lifted state.

Reason:

Keep UI components focused on presentation while allowing HomePage to own the shared application state. This follows React best practices, improves component reusability, and simplifies future features such as gameplay history, AI statistics, and prediction confidence.

## ADR-008

Title:
Separate Raw Gameplay History from Training Data

Decision:

Store raw gameplay events independently and generate machine learning datasets through a preprocessing pipeline.

Reason:

Raw event logs should never be modified directly. Feature engineering should be reproducible and allow multiple dataset versions to be generated from the same history.

---

## ADR-009

Title:
Use Sliding Window Feature Engineering

Decision:

Generate supervised learning samples using a sliding window of the player's previous three moves.

Reason:

Sequential gameplay cannot be used directly for supervised learning. The sliding window transforms sequential history into fixed-length feature vectors suitable for classification algorithms.

---

## ADR-010

Title:
Keep Machine Learning in a Separate Python Module

Decision:

Implement preprocessing, model training, and prediction inside the dedicated `ml/` project.

Reason:

Python provides the best ecosystem for machine learning while allowing the Java backend to remain focused on application orchestration. This separation mirrors common production architectures.


## ADR-011: chronological evaluation and bundled preprocessing
Keep the last 20% as a chronological holdout with a three-window gap. Fit the encoder and model together on training rows only. Serialize their pipeline and metadata atomically. Keep Java at the documented Java 21 baseline.


## ADR-012: independent local prediction service
Serve inference through FastAPI on loopback port 8001. Require exactly three completed moves and forbid extra fields. Missing models return 503 so the game can use random play. Model artifacts are loaded locally rather than accepted over HTTP.


## ADR-013: backend-owned session history and bounded fallback
Use server history rather than client-provided history. Resolve inference before persisting the current move. Limit inference to 600 ms and use random fallback. Serialize play operations to preserve round ordering and keep local live history separate from checked-in samples. Session state is ephemeral and limited to 1000 entries.


## ADR-014: reveal only after animation and inference
Start the request and a cancellable 1.35-second reveal timer together. Publish the response only after both finish; keep controls locked while either is pending. Render first-person hands with SVG so no raster assets are required, and honor reduced-motion settings.


## ADR-015: snapshot retraining and last-valid-model reload
Freeze history for reproducibility, validate a candidate before promotion, archive the old artifact, and atomically replace the model. A file lock prevents overlapping CLI operations. Serve the last validated predictor if a replacement cannot load. Training and rollback remain local operations.


## ADR-016: select models within training data
Use three expanding chronological folds with a three-window gap inside the training 80%. Fix the selected model before evaluating the final holdout. Compare two baselines and five classifiers, with deterministic ties favoring simpler earlier candidates. Comparison alone writes a report; promotion requires the retraining workflow.
