# Deployment Options - No Terminal Needed!

## 🎯 Three Ways to Run 24/7

### Option 1: Web Dashboard (Recommended)
**Best for**: Monitoring multiple repos with visual interface

```bash
# Start the dashboard
cd autonomous_reviewer
export GITHUB_TOKEN='your_token'
python dashboard.py
```

Then open: **http://localhost:5000**

**Features:**
- ✅ Web UI to start/stop monitoring
- ✅ Real-time statistics
- ✅ Visual status indicators
- ✅ Monitor multiple repos
- ✅ No terminal needed after starting

**Screenshot:**
```
┌─────────────────────────────────────┐
│ 🤖 Autonomous PR Review Dashboard  │
├─────────────────────────────────────┤
│ Status: 🟢 Active                   │
│ Monitoring: org/repo1, org/repo2    │
│                                     │
│ PRs Reviewed: 42                    │
│ Critical Issues: 7                  │
│ Reviews Posted: 42                  │
│                                     │
│ [▶️ Start] [⏹️ Stop]                │
└─────────────────────────────────────┘
```

---

### Option 2: GitHub Action (Zero Infrastructure!)
**Best for**: Automatic reviews on every PR, no server needed

**Setup:**
1. The workflow file is already in `.github/workflows/pr-review.yml`
2. Add API key to repo secrets:
   - Go to repo Settings → Secrets → Actions
   - Add `ANTHROPIC_API_KEY` (or use GITHUB_TOKEN for free Ollama alternative)
3. Done! Every new PR gets reviewed automatically

**How it works:**
- PR opened → GitHub Action triggers → AI reviews → Posts comment
- Runs on GitHub's servers (FREE!)
- No terminal, no server, fully automatic

**To use Ollama instead of Claude:**
Edit `.github/workflows/pr-review.yml` and remove the Anthropic key requirement.

---

### Option 3: Docker Container (Deploy Anywhere)
**Best for**: Running on a server 24/7

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

**Access dashboard:** http://your-server:5000

**Deploy to cloud:**
```bash
# AWS, DigitalOcean, etc
scp -r ai-pr-review user@server:/home/user/
ssh user@server
cd ai-pr-review
export GITHUB_TOKEN='your_token'
docker-compose up -d
```

---

## 🚀 Quick Comparison

| Method | Server Needed | Terminal Needed | Cost | Best For |
|--------|--------------|-----------------|------|----------|
| Web Dashboard | Yes (local/server) | Only to start | Free | Visual monitoring |
| GitHub Action | No | No | Free* | Automatic reviews |
| Docker | Yes (server) | Only to start | Server cost | Production 24/7 |

*Free tier: 2,000 minutes/month

---

## 📱 Web Dashboard Usage

### Starting Monitoring

1. **Open dashboard:** http://localhost:5000
2. **Enter repos:**
   ```
   yourusername/repo1
   company/repo2
   org/repo3
   ```
3. **Set interval:** 60 seconds (or longer)
4. **Click "Start Monitoring"**
5. **Dashboard runs 24/7** - just keep browser tab open or run on server

### Features

- **Real-time stats:** See PRs reviewed, issues found
- **Status monitoring:** Visual indicators
- **Start/stop controls:** No terminal commands needed
- **Recent reviews:** See what was reviewed
- **Auto-refresh:** Updates every 5 seconds

---

## 🎬 GitHub Action Setup (Detailed)

### Step 1: Enable GitHub Actions

File is already in: `.github/workflows/pr-review.yml`

### Step 2: Add Secrets (if using Claude)

1. Go to your repo on GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `ANTHROPIC_API_KEY`
5. Value: Your Claude API key
6. Click "Add secret"

### Step 3: Test It

1. Create a new PR
2. Go to "Actions" tab
3. See "Autonomous PR Review" workflow running
4. Check PR comments for the review

### Using Free Ollama Instead

Edit `.github/workflows/pr-review.yml`:

```yaml
# Remove this line:
ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

# The agent will use Ollama by default (free!)
```

**Note:** GitHub Actions runners don't have Ollama installed, so you'll need to modify the agent to use Claude/GPT or add Ollama installation step.

---

## 🐳 Docker Deployment

### Local Docker

```bash
# Build
docker build -t pr-review .

# Run dashboard
docker run -d \
  -p 5000:5000 \
  -e GITHUB_TOKEN='your_token' \
  --name pr-review \
  pr-review

# View logs
docker logs -f pr-review

# Stop
docker stop pr-review
```

### Docker Compose (Recommended)

```bash
# Create .env file
echo "GITHUB_TOKEN=your_token" > .env

# Start
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

### Deploy to Cloud

**DigitalOcean:**
```bash
# Create droplet with Docker
# SSH in
git clone git@github.com:youcefjd/ai-pr-review.git
cd ai-pr-review
echo "GITHUB_TOKEN=your_token" > .env
docker-compose up -d

# Access: http://your-droplet-ip:5000
```

**AWS EC2:**
```bash
# Launch EC2 instance
# Install Docker
# Same as above
```

**Fly.io (Free tier):**
```bash
fly launch
fly secrets set GITHUB_TOKEN=your_token
fly deploy
```

---

## 🔒 Security Notes

### Dashboard Security

**For production, add authentication:**

```python
# In dashboard.py
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {
    "admin": "your-secure-password"
}

@auth.verify_password
def verify(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def index():
    return render_template('dashboard.html')
```

### GitHub Action Security

- Uses repo secrets (encrypted)
- Limited permissions (read code, write PR comments)
- Runs in isolated environment

### Docker Security

- Don't expose port 5000 publicly without auth
- Use reverse proxy (nginx) with HTTPS
- Rotate GitHub tokens regularly

---

## 🎯 Recommended Setup

**For personal projects:**
→ Use **GitHub Action** (zero effort, fully automatic)

**For teams:**
→ Use **Web Dashboard** on shared server (visual monitoring)

**For enterprises:**
→ Use **Docker** on cloud with auth (secure, scalable)

---

## 📊 Monitoring & Maintenance

### Dashboard Metrics

- PRs reviewed today
- Critical issues found
- Average time per review
- Success rate

### GitHub Action Logs

```bash
# View on GitHub
Actions tab → Select workflow → View logs

# Check for failures
Look for ❌ in workflow runs
```

### Docker Health Checks

```bash
# Check if running
docker ps

# View resource usage
docker stats pr-review

# Restart if needed
docker-compose restart
```

---

## 🐛 Troubleshooting

**Dashboard won't start:**
```bash
# Check if port 5000 is in use
lsof -i :5000

# Use different port
export PORT=8080
python dashboard.py
```

**GitHub Action fails:**
```bash
# Check workflow file syntax
# Verify secrets are set
# Check action logs
```

**Docker issues:**
```bash
# Rebuild
docker-compose build --no-cache

# Check logs
docker-compose logs --tail=50
```

---

## 🎉 You're Done!

Choose your deployment method and you're ready! No more terminal commands needed after initial setup.

**Quick start commands:**

```bash
# Web Dashboard
python autonomous_reviewer/dashboard.py

# GitHub Action
# (Just push the workflow file)

# Docker
docker-compose up -d
```

All three options run 24/7 and monitor your repos automatically! 🚀
