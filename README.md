# DeepAnomaly — Self-Supervised Anomaly Detection in Time Series

B.Tech Final Year Project | 7th Sem AI | Ankur Saini (23EBKAI009)

Autoencoder trained only on normal data; anomalies detected via
reconstruction error. Dataset: ECG5000.


## Results

Two architectures were trained and compared on the same held-out test set:

| Model | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|
| Dense Autoencoder | *(fill)* | *(fill)* | *(fill)* | *(fill)* |
| LSTM Autoencoder | *(fill)* | *(fill)* | *(fill)* | *(fill)* |

**Why compare these two:** the dense autoencoder treats each timestep as an
independent input feature, with no explicit notion of sequence order. The
LSTM autoencoder encodes the sequence through recurrence, which should, in
principle, capture temporal structure the dense model cannot. The gap (or
lack of one) between them is itself a useful result — ECG beats are short
and strongly periodic, which may make the ordering advantage smaller than
expected.

## Using the Dashboard

- **Model selector:** run inference with the dense or LSTM autoencoder.
- **Compare both:** run both models on the same file and see how many
  sequences each flags and how often they agree.
- **Chart:** click any row to plot the original sequence against each
  model's reconstruction. Large gaps mark the regions the model could not
  explain, which is where the anomaly is.

Sample data with a known mix of normal and anomalous beats:
`docs/sample_data/demo_sequences.csv` (ground truth in `demo_labels.csv`).


## Deployment (Railway)

Both services are deployed as separate Railway services from this monorepo.

**Backend**
1. New Railway service → connect this repo → set Root Directory to `backend`
2. Railway auto-detects the Dockerfile
3. Set environment variable: `CORS_ORIGINS=<frontend-railway-url>`
4. Deploy — note the generated public URL (e.g. `https://deepanomaly-backend.up.railway.app`)

**Frontend**
1. New Railway service → same repo → set Root Directory to `frontend`
2. Set build argument: `VITE_API_URL=<backend-url>/api`
3. Deploy

**Live demo:** https://appealing-success-production-8f9e.up.railway.app

**Backend API:** https://deepanomaly-timeseries-production.up.railway.app/docs


## Try It Now

No setup needed — the app is live:

1. Visit the [live demo](https://appealing-success-production-8f9e.up.railway.app)
2. Upload `docs/sample_data/demo_sequences.csv` (included in this repo)
3. View detected anomalies and the reconstruction chart