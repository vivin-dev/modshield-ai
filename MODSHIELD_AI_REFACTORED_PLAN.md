# ModShield AI - Refactored Build Plan
## Prototype → Production Handoff (Claude + Base 44 Split)

**Version:** 2.0  
**Date:** July 16, 2026  
**Founder:** Vivin (14 y/o) + Uncle  
**Goal:** Prove the concept works, get buy-in, then scale.

---

## Phase Overview

| Phase | Owner | Timeline | Goal |
|-------|-------|----------|------|
| **Phase 1: Concept Validation** | Claude | 1 week | Interactive prototype + uncle approval |
| **Phase 2: Local Prototype Bot** | Claude | 2 weeks | Working Discord bot with live toxicity scoring |
| **Phase 3: Production Readiness** | Base 44 | 2 weeks | Containerization, CI/CD, monitoring, security |
| **Phase 4: Scaling & SaaS** | Vivin + Uncle | Ongoing | Customer onboarding, billing, growth |

---

# PHASE 1: Concept Validation (COMPLETE ✅)

**Owner:** Claude  
**Status:** DONE — Interactive prototype dashboard in Claude artifact

## Deliverables
- ✅ Interactive message simulator (type a message, see AI toxicity score)
- ✅ Live dashboard with metrics (messages analyzed, actions taken, burnout score)
- ✅ External threat detection simulation (Reddit/Discord keywords)
- ✅ Admin override panel mockup
- **Artifact Link:** Share with uncle for feedback

**Handoff to Phase 2:** Uncle approves concept → proceed with real bot

---

# PHASE 2: Local Prototype Bot (CLAUDE'S WORK)

## Overview
Build a **fully functional Discord bot** running on your Mac that:
- Listens to real Discord messages
- Batches them (3-second window)
- Scores toxicity via Groq API
- Executes moderation actions (warn/mute/ban/shadow-ban)
- Logs everything to PostgreSQL
- Generates real-time metrics

**This phase is NOT production-ready.** It's for:
- Proving the concept works with real Discord data
- Testing AI context awareness (gaming slang vs. toxicity)
- Validating the database schema
- Gathering feedback from a test server

---

## Step 1: Local Environment Setup (30 min)

### 1.1 Install Core Dependencies

**Python 3.11+**
```bash
# Check version
python3 --version

# If not installed, download from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH" during install
```

**Node.js + npm**
```bash
# Check version
node --version && npm --version

# If not installed, download from https://nodejs.org/ (LTS recommended)
```

**Git** (Already on Mac)
```bash
git --version
```

### 1.2 Create Project Folder Structure

```bash
mkdir ~/projects/modshield-ai
cd ~/projects/modshield-ai

# Initialize git
git init
git config user.name "Your Name"
git config user.email "vivin.dhanasekaran@gmail.com"

# Create subdirectories
mkdir bot dashboard prisma

# Create .gitignore
cat > .gitignore << 'EOF'
.env
.env.local
node_modules/
__pycache__/
*.pyc
.vscode/
.DS_Store
dist/
build/
EOF

git add .gitignore && git commit -m "init: project structure"
```

### 1.3 Set Up Environment Variables

Create `/modshield-ai/.env`:
```bash
# Discord Bot
DISCORD_TOKEN=your_bot_token_here

# AI Engine
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3-8b-instant

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/modshield_db

# Reddit API (Optional for Phase 2, needed Phase 3)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_BOT_USERNAME=your_reddit_username

# Environment
NODE_ENV=development
PYTHON_ENV=development
```

Create `.env.example` (commit this, NOT `.env`):
```bash
DISCORD_TOKEN=
GROQ_API_KEY=
GROQ_MODEL=llama-3-8b-instant
DATABASE_URL=postgresql://user:password@localhost:5432/modshield_db
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_BOT_USERNAME=
NODE_ENV=development
PYTHON_ENV=development
```

### 1.4 Get Required API Keys

**Discord Bot Token:**
1. Go to https://discord.com/developers/applications
2. Click "New Application" → name it "ModShield AI"
3. Go to "Bot" → "Add Bot"
4. Under TOKEN, click "Copy" → paste into `.env`
5. Enable these intents:
   - Message Content Intent ✅
   - Guild Messages ✅
   - Direct Messages ✅

**Groq API Key:**
1. Go to https://console.groq.com/keys
2. Create new API key
3. Copy → paste into `.env` as `GROQ_API_KEY`

**PostgreSQL Database:**
- **Option A (Recommended for prototype):** Free Supabase account
  - Go to https://supabase.com → sign up
  - Create new project
  - Copy `postgresql://...` connection string → paste into `.env` as `DATABASE_URL`
- **Option B:** Local PostgreSQL (needs Docker or native install)

---

## Step 2: Python Bot Backend Setup (CLAUDE BUILDS THIS)

### 2.1 Install Python Dependencies

```bash
cd ~/projects/modshield-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**File: `/bot/requirements.txt`**
```
discord.py==2.4.0
python-dotenv==1.0.0
prisma==0.14.0
groq==0.9.0
aiohttp==3.9.0
pydantic==2.5.0
pydantic-settings==2.1.0
```

### 2.2 Initialize Prisma

```bash
cd ~/projects/modshield-ai

# Install Prisma CLI globally
npm install -g prisma

# Initialize Prisma (creates prisma/ folder & schema.prisma)
prisma init

# Copy our schema.prisma into prisma/schema.prisma
# (Claude will provide this)
```

### 2.3 Create PostgreSQL Database

```bash
# If using Supabase, the DB is already created

# If using local PostgreSQL, run:
psql -U postgres -c "CREATE DATABASE modshield_db;"
```

### 2.4 Run Prisma Migrations

```bash
# Generate Prisma client
prisma generate

# Create tables in database
prisma migrate dev --name init

# Verify tables were created
prisma studio  # Opens a GUI to browse your database
```

---

## Step 3: Bot Core Logic (CLAUDE BUILDS THIS)

### Files to Create:

1. `/bot/main.py` — Bot initialization + message queue listener
2. `/bot/ai_engine.py` — Groq API client + toxicity scoring
3. `/bot/moderation.py` — Warn/mute/ban/shadow-ban handlers
4. `/bot/database.py` — Prisma client initialization
5. `/bot/config.py` — Constants & configuration

**Claude will provide complete, production-ready code for all of these.**

### Key Behaviors:

- **Message Batching:** Collect messages for 3 seconds, then send batch to Groq (saves 95% API cost)
- **Toxicity Scoring:** AI returns JSON with score (0.0–1.0) + reasoning
- **Context Awareness:** Distinguishes gaming slang ("nuke their base") from actual toxicity
- **Moderation Actions:** Auto-warn/mute/ban based on score thresholds
- **Shadow-Ban Sandbox:** Trolls' messages deleted publicly but reposted to hidden channel
- **Audit Logging:** Every action logged to PostgreSQL with original message context

---

## Step 4: Database Schema (CLAUDE PROVIDES THIS)

**File: `/prisma/schema.prisma`**

Complete Prisma schema with:
- `Guild` — Server config
- `User` — Tracked users (flags, mutes, bans)
- `ChatMessage` — Message cache + AI scores
- `AiAction` — Audit log (all moderation actions)
- `ExternalThreat` — Threat intelligence
- `ModMetric` — Daily metrics (toxicity rate, burnout score)

**Claude already provided this in the earlier message.**

---

## Step 5: Run the Bot Locally

```bash
cd ~/projects/modshield-ai

# Activate Python virtual environment
source venv/bin/activate

# Start the bot
python bot/main.py
```

**Expected output:**
```
✓ Discord bot connected
✓ Listening to messages
✓ AI engine ready (Groq API)
✓ Database connected
```

### Test It:

1. Create a test Discord server (or use an existing one)
2. Invite the bot to the server (invite link in Discord Dev Portal)
3. Send test messages in a channel the bot can see
4. Bot should log them, score toxicity, and take actions

---

## Step 6: Next.js Dashboard (CLAUDE BUILDS THIS)

**Local dashboard to visualize metrics in real-time.**

### Setup

```bash
cd ~/projects/modshield-ai/dashboard

# Install Next.js
npx create-next-app@latest . --typescript --tailwind --no-eslint

# Install Shadcn components
npx shadcn-ui@latest init

# Install Prisma client for dashboard
npm install @prisma/client
```

### Key Pages:

- `/dashboard/` — Main metrics (toxicity rate, actions taken, burnout)
- `/dashboard/messages` — Live message stream
- `/dashboard/threats` — External threat log
- `/dashboard/admin` — Override AI decisions

**Claude will provide complete Next.js code.**

---

## Step 7: Testing & Validation

### Manual Testing

1. Send normal messages → should not trigger actions ✅
2. Send toxic messages → should warn/mute ✅
3. Send gaming slang → should NOT flag as toxic ✅
4. Verify database logs everything ✅
5. Check dashboard updates in real-time ✅

### Test Cases (Provided by Claude)

```python
# bot/tests/test_ai_engine.py
def test_gaming_slang_not_toxic():
    score = ai_engine.score_message("let's nuke their base")
    assert score < 0.3  # Should be low toxicity

def test_actual_toxicity_high_score():
    score = ai_engine.score_message("you're trash, uninstall")
    assert score > 0.7  # Should be high toxicity
```

---

# PHASE 3: Production Readiness (BASE 44'S WORK)

## Overview

Once the local prototype works and uncle approves, **Base 44 takes over** to make it production-ready.

---

## Step 1: Containerization (Docker)

### 1.1 Create Bot Dockerfile

**File: `/bot/Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### 1.2 Create Dashboard Dockerfile

**File: `/dashboard/Dockerfile`**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

CMD ["npm", "start"]
```

### 1.3 Docker Compose (Local Testing)

**File: `/docker-compose.yml`**
```yaml
version: '3.9'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: modshield_db
      POSTGRES_PASSWORD: secure_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  bot:
    build: ./bot
    environment:
      DATABASE_URL: postgresql://postgres:secure_password@postgres:5432/modshield_db
      DISCORD_TOKEN: ${DISCORD_TOKEN}
      GROQ_API_KEY: ${GROQ_API_KEY}
    depends_on:
      - postgres
    restart: unless-stopped

  dashboard:
    build: ./dashboard
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://postgres:secure_password@postgres:5432/modshield_db
    depends_on:
      - postgres
    restart: unless-stopped

volumes:
  postgres_data:
```

**Run with:**
```bash
docker-compose up --build
```

---

## Step 2: CI/CD Pipeline (GitHub Actions)

**File: `/.github/workflows/deploy.yml`**

Automatic testing & deployment on every push:
1. Run Python tests (pytest)
2. Run JavaScript tests (Jest)
3. Check code quality (Black, ESLint)
4. Build Docker images
5. Deploy to Render or Railway

---

## Step 3: Monitoring & Error Tracking

**Sentry Integration** — Auto-capture bot crashes, errors, performance issues

```python
# bot/main.py
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("PYTHON_ENV"),
)
```

---

## Step 4: Rate Limiting & Scaling

- Add Redis for rate limiting (prevent Groq API abuse)
- Implement exponential backoff for API retries
- Monitor Groq token usage

---

## Step 5: Security Hardening

- Rotate Discord bot token regularly
- Audit log access control
- Encrypt sensitive fields in database
- Add request signing for webhook verification

---

## Step 6: Deployment to Production

**Option A: Railway.app** (Recommended for beginners)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

**Option B: Render**
```bash
# Connect GitHub repo → auto-deploys on push
```

**Option C: AWS EC2 + ECS**
```bash
# More complex, full infrastructure control
```

---

## Step 7: Metrics & Analytics

- Track DAU (Daily Active Users)
- Monitor bot performance (message processing time)
- Track moderation action volume
- Calculate per-server costs (Groq API usage)

---

# PHASE 4: SaaS Launch (VIVIN + UNCLE)

## Overview

Now that the bot is production-ready, **you and your uncle** handle:

1. **Customer Onboarding** — Server owners install the bot from marketplace
2. **Billing Integration** — Stripe payments (free tier + premium)
3. **Customer Support** — Discord support server
4. **Growth & Marketing** — Reach gaming communities

---

## Step 1: Discord Bot Marketplace Listing

- List ModShield AI in Discord's official app directory
- Write compelling description
- Add screenshots from the dashboard

---

## Step 2: Stripe Billing

**Pricing Model:**
- **Free:** 100 messages/day, no advanced features
- **Pro:** $9.99/month, unlimited, advanced threat detection
- **Enterprise:** Custom pricing, white-label

---

## Step 3: Customer Success

- Landing page (Vercel)
- Documentation site (Docs.rs or GitBook)
- Discord support server
- Email support template

---

## Step 4: Growth Metrics

- Servers using ModShield
- Moderation actions prevented
- Customer lifetime value (LTV)
- Monthly recurring revenue (MRR)

---

# File Checklist (What Claude Provides)

## Phase 2 Code Files (Complete & Production-Ready)

- [ ] `bot/main.py` — Bot init + message queue
- [ ] `bot/ai_engine.py` — Groq/OpenAI client
- [ ] `bot/moderation.py` — Warn/mute/ban/shadow-ban handlers
- [ ] `bot/database.py` — Prisma client
- [ ] `bot/config.py` — Constants
- [ ] `bot/scraper_compliant.py` — Reddit API + external threats
- [ ] `bot/requirements.txt` — Python dependencies
- [ ] `bot/tests/test_ai_engine.py` — Unit tests
- [ ] `prisma/schema.prisma` — Database schema
- [ ] `dashboard/app/page.tsx` — Main dashboard
- [ ] `dashboard/app/api/metrics/route.ts` — Metrics API
- [ ] `dashboard/package.json` — Next.js dependencies
- [ ] `.env.example` — Environment template
- [ ] `.gitignore` — Git ignore rules
- [ ] `README.md` — Setup & run instructions

---

# Handoff Checklist (Phase 2 → Phase 3)

Before handing off to Base 44:

- [ ] Local bot runs without errors
- [ ] Database schema matches production needs
- [ ] All AI logic tested with real Discord data
- [ ] Dashboard displays real metrics
- [ ] Uncle approves feature set
- [ ] Code is clean & documented
- [ ] `.env.example` is complete
- [ ] README has clear setup instructions
- [ ] No hardcoded secrets in repo

---

# Timeline & Milestones

| Milestone | Owner | Date | Status |
|-----------|-------|------|--------|
| Phase 1: Prototype validation | Claude | Now | ✅ DONE |
| Phase 2: Local bot working | Claude | +2 weeks | 🟡 IN PROGRESS |
| Phase 2: Uncle approves | You + Uncle | +2 weeks | ⏳ PENDING |
| Phase 3: Docker & CI/CD | Base 44 | +2 weeks | ⏳ PENDING |
| Phase 3: Deployed to production | Base 44 | +3 weeks | ⏳ PENDING |
| Phase 4: Beta customers | You + Uncle | +4 weeks | ⏳ PENDING |
| Phase 4: Paid tier launch | You + Uncle | +6 weeks | ⏳ PENDING |

---

# Questions for Your Uncle

Before moving to Phase 2, ask:

1. **"Does the prototype dashboard prove the concept works?"**
2. **"Would you pay for this if it was fully built?"**
3. **"What Discord server should we test it on?"**
4. **"Should we add any features before going production?"**
5. **"Who should handle deployment/hosting when it's done?"**

If he says "yes" to all → proceed to Phase 2 immediately.

---

# Next Steps (Right Now)

1. ✅ Show uncle the interactive prototype (artifact link)
2. ⏳ Get his feedback & approval
3. ⏳ Set up local environment (Step 1 of Phase 2)
4. ⏳ Start building the real bot (Claude does this)

**Ready to move to Phase 2?**
