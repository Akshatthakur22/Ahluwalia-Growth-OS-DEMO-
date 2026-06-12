# Deployment Guide — Ahluwalia Growth OS (Demo)

Deploy **frontend** on Vercel and **backend** on Render, with **Neon PostgreSQL** as the database.

---

## Prerequisites

- GitHub repo pushed with latest code
- [Neon](https://neon.tech) PostgreSQL database (already seeded for demo)
- [Render](https://render.com) account
- [Vercel](https://vercel.com) account

---

## 1. Database (Neon)

Your Neon `DATABASE_URL` is used by the Render backend.

**One-time setup** (if using a fresh database):

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # paste Neon DATABASE_URL

python scripts/seed_db.py
python scripts/enrich_demo_data.py   # optional rich demo data
python scripts/migrate_pdf_fields.py
python scripts/migrate_field_intelligence.py
python scripts/migrate_meeting_pdf.py
python scripts/add_perf_indexes.py
python scripts/update_demo_users.py
```

---

## 2. Backend — Render

### Option A: Blueprint (`render.yaml`)

1. Render Dashboard → **New** → **Blueprint**
2. Connect this GitHub repo
3. Set secrets when prompted:
   - `DATABASE_URL` — Neon connection string
   - `CORS_ORIGINS` — your Vercel URL (e.g. `https://ahluwalia-growth-os.vercel.app`)

### Option B: Manual Web Service

| Setting | Value |
|---------|-------|
| Root Directory | `backend` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/health` |

### Environment Variables (Render)

```env
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=<generate-a-long-random-string>
DEBUG=False
ENVIRONMENT=production
CORS_ORIGINS=https://YOUR-APP.vercel.app
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=5
DATABASE_POOL_RECYCLE=300
```

**Verify:** `https://YOUR-API.onrender.com/health` → `{"status":"healthy"}`

**Note:** Render free tier sleeps after ~15 min idle. Wake the API 2 minutes before a client demo.

---

## 3. Frontend — Vercel

1. Vercel → **Add New Project** → import GitHub repo
2. **Root Directory:** `frontend`
3. Framework: Next.js (auto-detected)

### Environment Variable (Vercel)

```env
NEXT_PUBLIC_API_URL=https://YOUR-API.onrender.com
```

No trailing slash. Redeploy after setting.

**Verify:** Open Vercel URL → login with `9876543210` / `password123`

---

## 4. CORS (critical)

After Vercel deploy, update Render `CORS_ORIGINS`:

```
https://your-app.vercel.app
```

For preview deployments, comma-separate multiple origins:

```
https://your-app.vercel.app,https://your-app-git-main-user.vercel.app
```

---

## 5. Demo Logins

| Role | Name | Mobile | Password |
|------|------|--------|----------|
| Field Executive | Rohit Sain | 9876543210 | password123 |
| Marketing Associate | Namita Kaushal | 9876543211 | password123 |
| Showroom Sales | Rakesh Pandey | 9876543212 | password123 |
| Manager | Vikram Patel | 9876543213 | password123 |
| CEO | Pritpal Singh | 9876543214 | password123 |

---

## 6. Pre-Demo Checklist

- [ ] Push latest code to `main`
- [ ] Render service is **Live** (not sleeping)
- [ ] `/health` returns healthy
- [ ] Vercel `NEXT_PUBLIC_API_URL` points to Render
- [ ] `CORS_ORIGINS` includes Vercel URL
- [ ] Login works for CEO + Field roles
- [ ] Search `9812345678` returns Green Valley data
- [ ] Open app 2 min before client call (cold start)

---

## 7. Known Demo Limitations

- **Photo uploads** stored on Render disk — lost on redeploy (use URL demo photos)
- **Architect Growth Engine, Builder Command Center, LMS** — Phase 2 (not in demo)
- **Demo passwords** are shared — not for production users

---

## 8. Troubleshooting

| Issue | Fix |
|-------|-----|
| Login fails / CORS error | Match `CORS_ORIGINS` to exact Vercel URL (https, no trailing slash) |
| Slow first load | Render/Neon cold start — wait 30–60s or upgrade Render |
| 502 on API | Check Render logs; verify `DATABASE_URL` |
| Images 404 | `NEXT_PUBLIC_API_URL` must be Render base URL (not `/api/v1`) |

---

## 9. Optional: Keep API Warm

Use [UptimeRobot](https://uptimerobot.com) or similar to ping `https://YOUR-API.onrender.com/health` every 10 minutes during demo week.
