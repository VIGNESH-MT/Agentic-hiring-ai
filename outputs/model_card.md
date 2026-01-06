# Model Card — Resume Screening Prediction Model

## Objective
The objective of this model is to predict recruiter hiring decisions (Hire vs Reject)
based on resume-derived features in order to support automated resume screening.

## Prediction Task
Binary classification:
- 1 → Hire
- 0 → Reject

Classification was chosen because the dataset does not contain a stable AI Score
column across versions and because binary hiring outcomes are directly actionable
in recruitment workflows.

## Data
Source:
AI-Powered Resume Screening Dataset (Kaggle, 2025).

Features used:
- Textual features: normalized resume skills aggregated into `skills_text`
- Structured features: years of experience, number of projects, salary expectation

Target variable:
- `recruiter_decision`

## Models

### Baseline Model
- TF-IDF vectorization on `skills_text`
- Logistic Regression classifier

Artifacts:
- `models/baseline.pkl`
- `outputs/metrics_baseline.json`

### Final Model
- TF-IDF on `skills_text`
- Structured numeric features passed through
- Logistic Regression with class balancing and regularization

Artifacts:
- `models/final.pkl`
- `outputs/metrics_final.json`

## Evaluation Metrics
Primary metrics:
- Accuracy
- ROC-AUC
- Precision, Recall, F1-score (per class)

Detailed metrics are stored in the corresponding JSON files.

## Improvements Over Baseline
The final model improves robustness by incorporating structured resume features,
reducing variance caused by sparse skill text and improving decision stability
under class imbalance.

## Limitations
- The model learns historical recruiter decisions and may inherit existing biases.
- Skills not explicitly mentioned in resumes cannot be inferred.
- Model performance may degrade for non-technical or uncommon roles.

## Bias and Fairness Considerations
This model may reflect biases present in historical hiring data.
It should be used only as a decision-support tool and not as a fully automated
hiring system.

## Intended Use
Decision-support system for recruiters.
Not intended for autonomous hiring decisions without human oversight.
