# Design decisions

## Completed history belongs to the backend

Clients choose their own move but cannot supply inference history. Prediction happens before the
current round is stored. This preserves ordering and prevents current-move leakage. Sessions are
bounded and ephemeral; CSV persists events for training and analysis.

## Keep inference separate from game orchestration

FastAPI loads a local scikit-learn artifact and accepts exactly three moves. Java applies game
rules and counters predictions. A 600 ms inference bound and random fallback keep rounds playable
when the predictor is unavailable. There is no HTTP model-upload or retraining endpoint.

## Evaluate chronologically

Training fits preprocessing and classifiers together. A three-window gap separates the training
80% from holdout. Three expanding folds within training choose among two baselines and five
classifiers. Holdout results are reported after selection, not used to choose the model.

## Promote only validated artifacts

Retraining uses a frozen history snapshot, validates a candidate, archives the previous model and
atomically promotes the replacement under a local lock. Failed reloads retain the last good model.
Rollback uses a validated archive. Joblib artifacts remain trusted local inputs.

## Record repetition rules separately

An offline model can repeat the same wrong prediction forever for an unchanged three-move window.
When inference is available and all previous moves match, predict that repeated move and counter it.
Record ADAPTIVE instead of ML, with separate counts and no fabricated classifier confidence.
This assumes the streak continues and can be beaten by changing moves.

## Gate results on both animation and API completion

The 1.35-second chant and API request run together. Publish outcomes/scores only after both finish;
keep controls locked and cancel pending work on unmount. SVG hands avoid external asset dependencies.

## Ship a complete Docker stack and a distinct browser demo

The full application needs Java/Python, so Docker packages all three services behind Nginx. Private
networking and named volumes provide a repeatable local deployment. GitHub Pages hosts a frontend
demo that makes no API calls and labels its simpler rules clearly. No hosted backend is required.
