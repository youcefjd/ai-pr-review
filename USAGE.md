# How to Use the Autonomous PR Review System

## Quick Reference

```bash
# Review single PR (recommended for testing)
python autonomous_pr_monitor.py owner/repo --single-pr PR_NUMBER

# Monitor continuously (24/7)
python autonomous_pr_monitor.py owner/repo

# Monitor multiple repos
python autonomous_pr_monitor.py repo1 repo2 repo3

# Custom interval (5 minutes)
python autonomous_pr_monitor.py owner/repo --interval 300

# Auto-post without approval (CAREFUL!)
python autonomous_pr_monitor.py owner/repo --auto-post
```

---

## Daily Workflow

### For Your Own Repos

**Morning routine:**
```bash
# Check what got reviewed overnight
python autonomous_pr_monitor.py yourusername/yourrepo --single-pr LATEST_PR

# Start monitoring for the day
python autonomous_pr_monitor.py yourusername/yourrepo &
```

**Before merging:**
```bash
# Review specific PR before you merge
python autonomous_pr_monitor.py yourusername/yourrepo --single-pr PR_NUMBER
```

### For Team Repos

**Set it and forget it:**
```bash
# Run in tmux/screen
tmux new -s pr-review
cd ai-pr-review/autonomous_reviewer
source ../venv/bin/activate
python autonomous_pr_monitor.py org/team-repo

# Detach: Ctrl+B, D
# Reattach later: tmux attach -t pr-review
```

---

## Common Scenarios

### Scenario 1: Review Before Merging

You have a PR ready to merge, want a quick security check:

```bash
python autonomous_pr_monitor.py owner/repo --single-pr 42
```

Result: Gets instant review, shows issues, you decide whether to merge.

### Scenario 2: Monitor All Team PRs

You want all PRs reviewed automatically:

```bash
# On a server or in background
nohup python autonomous_pr_monitor.py org/repo > reviews.log 2>&1 &

# Check logs
tail -f reviews.log
```

Result: Every new PR gets reviewed within 60 seconds.

### Scenario 3: Test on Sample Code

You want to test the reviewer on intentionally bad code:

```bash
# Create test PR with vulnerabilities
# Then review it
python autonomous_pr_monitor.py yourusername/test-repo --single-pr 1
```

Result: Validates the reviewer catches real issues.

---

## Advanced Usage

### Custom Review Rules

Edit `pr_review_agent.py` to customize the system prompt:

```python
system_prompt = """You are an expert code reviewer with focus on:
- Security (OWASP Top 10)
- Performance optimization
- Python best practices  # <-- Customize this
- Type safety
- Test coverage

Be extra strict about:
- Database queries (SQL injection)
- User input handling
- Authentication/authorization
"""
```

### Different Models for Different Repos

```python
# For critical repos: Use Claude
if repo_name == "company/production-api":
    self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# For internal tools: Use local model
else:
    self.llm = ChatOllama(model="gemma3:4b")
```

### Cost Tracking

Add cost monitoring:

```python
# Track token usage
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = agent.execute(task)
    print(f"Cost: ${cb.total_cost}")
```

---

## Integration with Your Workflow

### With GitHub Actions

Trigger on PR webhook instead of polling:

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review
on: pull_request
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run AI Review
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          pip install -r requirements.txt
          python autonomous_pr_monitor.py ${{ github.repository }} --single-pr ${{ github.event.number }}
```

### With CI/CD

Block merges if critical issues found:

```bash
# In your CI pipeline
python autonomous_pr_monitor.py owner/repo --single-pr $PR_NUMBER --output json > review.json

# Check for critical issues
critical_count=$(jq '.metadata.critical_issues' review.json)
if [ "$critical_count" -gt 0 ]; then
  echo "❌ Critical issues found, blocking merge"
  exit 1
fi
```

### With Slack/Discord

Get notifications:

```python
# In autonomous_pr_monitor.py
def _review_and_post(self, repo_name, pr_number):
    # ... existing code ...

    if meta['critical_issues'] > 0:
        send_slack_alert(
            f"🚨 Critical issues in {repo_name} PR #{pr_number}"
        )
```

---

## Performance Tips

### 1. Use Local Model for Speed

```python
# Ollama is fast and free
self.llm = ChatOllama(model="codellama:13b")
```

### 2. Use Cloud Model for Quality

```python
# Claude/GPT-4 for better accuracy
self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
```

### 3. Hybrid Approach

```python
# Quick triage with local, deep review with cloud
if quick_scan_finds_issues():
    use_cloud_model_for_detailed_review()
```

---

## Monitoring & Logs

### Check What It's Doing

```bash
# Follow the logs
tail -f reviews.log

# Search for critical issues
grep "CRITICAL" reviews.log

# Count reviews today
grep "Review complete" reviews.log | wc -l
```

### Statistics

```python
# Add to autonomous_pr_monitor.py
def print_stats_weekly():
    """Print weekly statistics."""
    print(f"This week:")
    print(f"  PRs reviewed: {self.stats['prs_reviewed']}")
    print(f"  Critical issues: {self.stats['critical_issues_found']}")
    print(f"  Average issues per PR: {avg}")
```

---

## Maintenance

### Update Dependencies

```bash
pip install --upgrade PyGithub langchain-ollama
```

### Update the Model

```bash
# If using Ollama
ollama pull llama3:70b  # Get newer/bigger model

# Then update base_agent.py
self.llm = ChatOllama(model="llama3:70b")
```

### Clean Up Old Reviews

GitHub API rate limits may require cleanup:

```bash
# Delete old review comments if needed
# (Use GitHub UI or API)
```

---

## Best Practices

✅ **DO:**
- Test on a personal repo first
- Start with `--single-pr` before continuous monitoring
- Review the agent's feedback before posting
- Use governance (don't use `--auto-post` initially)
- Monitor costs if using paid APIs

❌ **DON'T:**
- Use `--auto-post` on repos you don't control
- Share your GITHUB_TOKEN
- Ignore critical security findings
- Skip testing before deploying
- Run without rate limit awareness

---

## Next Steps

After you're comfortable:

1. **Week 1**: Test on personal repos, review manually
2. **Week 2**: Enable continuous monitoring in background
3. **Week 3**: Add to team repos with approval gates
4. **Month 2**: Build dashboard for observability
5. **Month 3**: Integrate with CI/CD pipeline

---

## Getting Help

**Check logs first:**
```bash
tail -f reviews.log
```

**Common issues:**
- Token expired → Create new token
- Rate limited → Reduce check frequency
- Poor reviews → Upgrade model
- False positives → Tune system prompt

**Still stuck?** Open a GitHub issue with:
- What you're trying to do
- What's happening
- Error messages
- Logs

---

**You have a working autonomous AI system. Use it!** 🚀
