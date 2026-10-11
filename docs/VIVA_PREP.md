# Viva Preparation

## One-line pitch
An autoencoder trained only on normal data flags anything it cannot reconstruct well, so no anomaly labels are needed.

## Likely questions

**Why train only on normal data?**
Anomalies are rare and unlabelled in practice. If anomalies leak into training, the model learns to reconstruct them too, the two error distributions overlap, and detection fails.

**Why does reconstruction error detect anomalies?**
The bottleneck (16 dims from 140) forces the model to learn the structure of normal data. Inputs that deviate from that structure cannot be compressed and rebuilt faithfully, so their error is high.

**How did you choose the threshold?**
The 95th percentile of reconstruction error on a normal-only validation set. It never touches test data, which would be leakage. A side effect: about 5% of normal data is flagged by construction.

**Why not report accuracy?**
The test set is ~78% anomalous. Predicting "anomaly" for everything gives ~78% accuracy. I report precision, recall, F1, ROC-AUC and PR-AUC.

**Why compare dense and LSTM?**
The dense model ignores timestep order; the LSTM models it explicitly. [State your measured result here and explain it. ECG beats are short and periodic, so the gap may be small.]

**What is data leakage and where did you prevent it?**
Information from test data influencing training. The scaler is fit on training data only, the threshold comes from validation data, and test values are not clipped.

**Why MinMax scaling?**
The decoder ends in a sigmoid with range [0, 1], so targets in the same range keep the loss well-conditioned.

**Why FastAPI and React?**
FastAPI gives typed request validation (Pydantic) and automatic docs; Python keeps inference in the same language as training. React with a separate API shows a proper client/server split.

**How is it deployed?**
Two Docker services on Railway. CORS origins and the API URL come from environment variables. The model is loaded once at startup, not per request.

**Why are model weights in git?**
A shortcut for a student project. In production they belong in a model registry or object storage, not version control.

## Honest limitations (say these before they ask)
- One dataset, and an easy one.
- 5% false-positive rate is built into the threshold choice.
- Detects abnormality, not its type.
- Univariate input only.

## If asked "what would you do next?"
Test on multivariate data (NASA Turbofan), add per-timestep anomaly localisation, try a variational or transformer-based model, and tune the threshold against a real false-alarm cost.