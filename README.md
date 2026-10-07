# DeepAnomaly — Self-Supervised Anomaly Detection in Time Series

B.Tech Final Year Project | 7th Sem AI | Ankur Saini (23EBKAI009)

Autoencoder trained only on normal data; anomalies detected via
reconstruction error. Dataset: ECG5000.

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