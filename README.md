# AI PR Review - Autonomous Code Review System

**Autonomous AI system that reviews pull requests automatically, detects security vulnerabilities, and posts structured feedback to GitHub.**

## 🎯 What This Does

- ✅ Monitors GitHub repositories 24/7
- ✅ Detects new pull requests automatically
- ✅ Reviews code for security vulnerabilities (SQL injection, command injection, XSS, etc.)
- ✅ Analyzes code quality and best practices
- ✅ Posts structured feedback to GitHub
- ✅ Learns from reviews over time

**This is Level 4 autonomy** - the system operates independently, only requiring approval for risky operations.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Clone the repo
git clone git@github.com:youcefjd/ai-pr-review.git
cd ai-pr-review

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up GitHub Token

Create a GitHub Personal Access Token:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: "PR Review Bot"
4. Select permissions:
   - ✅ `repo` (all sub-permissions)
5. Copy the token

```bash
# Export the token
export GITHUB_TOKEN='ghp_your_token_here'
```

### 3. Test It!

Review a single PR:

```bash
cd autonomous_reviewer
python autonomous_pr_monitor.py youcefjd/ai-pr-review --single-pr 1
```

---

## 📖 Usage Examples

### Review a Single PR

```bash
python autonomous_pr_monitor.py owner/repo --single-pr 123
```

### Continuous Monitoring (24/7)

```bash
python autonomous_pr_monitor.py owner/repo
```

### Monitor Multiple Repos

```bash
python autonomous_pr_monitor.py owner/repo1 owner/repo2 owner/repo3
```

See [USAGE.md](USAGE.md) for complete documentation.

---

## 📊 What It Detects

- SQL Injection
- Command Injection
- Path Traversal
- XSS (Cross-Site Scripting)
- Insecure Deserialization
- Hardcoded Secrets
- Missing error handling
- Performance issues
- Code quality problems

---

## 🧪 Live Tests

This system has been tested on real PRs in this repo:
- **PR #1**: Detected 4 critical issues (SQL injection, command injection)
- **PR #2**: Found shell injection and pickle deserialization (no hints in code!)

View the reviews:
- https://github.com/youcefjd/ai-pr-review/pull/1
- https://github.com/youcefjd/ai-pr-review/pull/2

---

## 📁 Project Structure

```
ai-pr-review/
├── autonomous_reviewer/       # Core autonomous system
│   ├── pr_review_agent.py    # Review logic
│   ├── github_integration.py # GitHub API
│   └── autonomous_pr_monitor.py # Monitoring loop
├── src/                       # Example code (with vulnerabilities)
├── requirements.txt
├── README.md                  # This file
└── USAGE.md                  # Complete usage guide
```

---

## 🚢 Deployment

### Local Testing
```bash
python autonomous_pr_monitor.py owner/repo --single-pr 123
```

### Background Service
```bash
nohup python autonomous_pr_monitor.py owner/repo > reviews.log 2>&1 &
```

### Server (24/7)
```bash
tmux new -s pr-review
python autonomous_pr_monitor.py owner/repo
# Ctrl+B, D to detach
```

---

## ⚙️ Configuration

### Change LLM Model

Edit `autonomous_reviewer/base_agent.py`:

```python
# For better reviews, use Claude
from langchain_anthropic import ChatAnthropic
self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Set API key
export ANTHROPIC_API_KEY='your_key_here'
```

---

## 🎓 How It Works

```
GitHub PR → Monitor → PRReviewAgent → Governance → Post Review
   ↓          ↓            ↓             ↓            ↓
 New code  Polls 60s   Analyzes    Approval gate  Comment
                      (Security)
```

---

## 📚 Documentation

- **README.md** (this file) - Quick start
- **USAGE.md** - Complete usage guide
- **autonomous_reviewer/** - Source code with comments

---

## 🙏 About

Built to prove that autonomous AI systems can be practical and useful today.

**From "feeling behind as a programmer" to "building autonomous AI systems" in one day.**

That's the 10x boost.

---

## 📄 License

MIT License - Use freely!

---

**The autonomous PR review system is ready to use. Deploy it and watch it work!** 🚀
