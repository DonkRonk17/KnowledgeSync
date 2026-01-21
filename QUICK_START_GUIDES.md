# 🧠 KnowledgeSync - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#-forge-quick-start)
- [Atlas (Executor)](#-atlas-quick-start)
- [Clio (Linux Agent)](#-clio-quick-start)
- [Nexus (Multi-Platform)](#-nexus-quick-start)
- [Bolt (Free Executor)](#-bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to use KnowledgeSync for recording decisions and reviewing team knowledge

### Step 1: Installation Check

```bash
# Verify KnowledgeSync is available
python -c "from knowledgesync import KnowledgeSync; print('[OK] Ready')"

# Check CLI
python knowledgesync.py --version
```

### Step 2: First Use - Record a Decision

```python
# In your FORGE session
from knowledgesync import KnowledgeSync

ks = KnowledgeSync("FORGE")

# Record an architectural decision
ks.add(
    "All Q-Mode tools must support both CLI and Python API",
    category="DECISION",
    topics=["q-mode", "architecture", "api-design"],
    confidence=1.0
)
print("[OK] Decision recorded")
```

### Step 3: Review Team Knowledge

```python
# What does the team know about a topic?
results = ks.query(topics=["architecture"])
print(f"Found {len(results)} entries about architecture:")
for entry in results:
    print(f"  [{entry.source}] {entry.content[:60]}...")

# What has ATLAS discovered?
atlas_findings = ks.query_agent("ATLAS", "implementation")
print(f"\nATLAS knows {len(atlas_findings)} things about implementation")
```

### Step 4: Common FORGE Commands

```bash
# View all decisions
knowledgesync query --category DECISION

# Check what an agent knows
knowledgesync agent ATLAS --topic testing

# Get team statistics
knowledgesync stats
```

### FORGE Integration Pattern

```python
# Before making a decision, check existing knowledge
def make_informed_decision(topic, new_decision):
    existing = ks.query(topics=[topic], category="DECISION")
    if existing:
        print(f"[!] Found {len(existing)} existing decisions about {topic}")
        for e in existing:
            print(f"    - {e.content[:60]}...")
    
    confirm = input("Proceed with new decision? (y/n): ")
    if confirm.lower() == 'y':
        return ks.add(new_decision, category="DECISION", topics=[topic])
    return None
```

### Next Steps for FORGE

1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - FORGE section
2. Try [EXAMPLES.md](EXAMPLES.md) - Example 3 (Agent queries)
3. Add knowledge recording to your planning sessions

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to use KnowledgeSync for documenting builds and checking existing solutions

### Step 1: Installation Check

```python
# Quick verification
from knowledgesync import KnowledgeSync
ks = KnowledgeSync("ATLAS")
print("[OK] KnowledgeSync ready for ATLAS")
```

### Step 2: First Use - During a Build

```python
from knowledgesync import KnowledgeSync

ks = KnowledgeSync("ATLAS")

# Before building, check existing knowledge
tool_name = "knowledgesync"
existing = ks.query(topics=[tool_name])
print(f"Existing knowledge about {tool_name}: {len(existing)} entries")

# Log discoveries during build
ks.add(
    "JSON files work well for knowledge storage",
    category="FINDING",
    topics=[tool_name, "implementation", "storage"]
)

# Log problems
problem = ks.add(
    "Graph traversal was slow initially",
    category="PROBLEM",
    topics=[tool_name, "performance"]
)

# Log solutions (with reference to problem)
ks.add(
    "Used visited set for O(n) traversal",
    category="SOLUTION",
    topics=[tool_name, "performance"],
    references=[problem.entry_id]
)
```

### Step 3: Build Knowledge Helper

```python
class BuildKnowledge:
    """Helper class for logging build knowledge."""
    
    def __init__(self, tool_name):
        self.ks = KnowledgeSync("ATLAS")
        self.topics = [tool_name.lower()]
    
    def finding(self, content):
        return self.ks.add(content, category="FINDING", topics=self.topics)
    
    def problem(self, content):
        return self.ks.add(content, category="PROBLEM", topics=self.topics)
    
    def solution(self, content, problem_id=None):
        refs = [problem_id] if problem_id else []
        return self.ks.add(content, category="SOLUTION", 
                          topics=self.topics, references=refs)

# Usage
bk = BuildKnowledge("MyTool")
bk.finding("Zero dependencies is achievable")
```

### Step 4: Common ATLAS Commands

```bash
# Search for existing solutions
knowledgesync query "performance optimization"

# Find related topics
knowledgesync related "testing" --depth 2

# Extract knowledge from session
knowledgesync extract HOLYGRAIL_SESSION.md --topics session build
```

### Next Steps for ATLAS

1. Integrate into Holy Grail automation
2. Add knowledge logging to tool build checklist
3. Use for every new tool build

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn CLI-first usage and cross-platform sync

### Step 1: Linux Installation

```bash
# Clone from GitHub
git clone https://github.com/DonkRonk17/KnowledgeSync.git
cd KnowledgeSync

# Test CLI
python3 knowledgesync.py --version

# Or install
pip3 install -e .
knowledgesync --version
```

### Step 2: First Use - CLI Workflow

```bash
# Add Linux-specific knowledge
knowledgesync add "BCH runs on port 8080 with systemd" \
    --source CLIO \
    --category CONFIG \
    --topics bch linux systemd

# Query existing knowledge
knowledgesync query "systemd"

# Check what other agents know
knowledgesync agent ATLAS --topic deployment
```

### Step 3: Extract from Session Logs

```bash
# Extract knowledge from session log
knowledgesync extract session.md --topics linux clio-session

# Extract from multiple files
for f in sessions/*.md; do
    knowledgesync extract "$f" --topics sessions
done
```

### Step 4: Sync with Team

```bash
# Export Linux knowledge for sharing
knowledgesync sync --export ~/linux_knowledge.json

# Import knowledge from Windows team
knowledgesync sync --import ~/shared/windows_knowledge.json

# Check sync status
knowledgesync stats
```

### Platform-Specific Notes

```python
from knowledgesync import KnowledgeSync
from pathlib import Path

# Custom storage location for Linux
ks = KnowledgeSync(
    agent="CLIO",
    storage_dir=Path.home() / ".config/knowledgesync"
)

# Add Linux-specific config
ks.add(
    "KnowledgeSync storage: ~/.config/knowledgesync/",
    category="CONFIG",
    topics=["knowledgesync", "linux", "config"]
)
```

### Next Steps for CLIO

1. Add to ABIOS startup routines
2. Create cron job for periodic sync
3. Test extraction from BCH logs

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform usage and analytics

### Step 1: Platform Detection

```python
import platform
from knowledgesync import KnowledgeSync

ks = KnowledgeSync("NEXUS")

# Log platform info
ks.add(
    f"Running on {platform.system()} {platform.release()}",
    category="FACT",
    topics=["platform", platform.system().lower()]
)

print(f"[OK] KnowledgeSync initialized on {platform.system()}")
```

### Step 2: First Use - Cross-Platform Queries

```python
from knowledgesync import KnowledgeSync

ks = KnowledgeSync("NEXUS")

# Query platform-specific knowledge
linux_knowledge = ks.query(topics=["linux"])
windows_knowledge = ks.query(topics=["windows"])

print(f"Linux entries: {len(linux_knowledge)}")
print(f"Windows entries: {len(windows_knowledge)}")

# Find cross-platform patterns
cross_platform = ks.query(topics=["cross-platform"])
```

### Step 3: Analytics Workflow

```python
# Get comprehensive stats
stats = ks.get_stats()

print("=" * 50)
print("KNOWLEDGE BASE ANALYTICS")
print("=" * 50)

print(f"\nTotal Entries: {stats['total_entries']}")
print(f"Total Topics: {stats['total_topics']}")
print(f"Relationships: {stats['total_relationships']}")
print(f"Avg Confidence: {stats['average_confidence']:.0%}")

print("\nBy Agent:")
for agent, count in sorted(stats['entries_by_source'].items()):
    pct = count / stats['total_entries'] * 100
    print(f"  {agent}: {count} ({pct:.1f}%)")

print("\nBy Category:")
for cat, count in sorted(stats['entries_by_category'].items()):
    print(f"  {cat}: {count}")

# Topic analysis
topics = ks.get_topics()
print(f"\nTop 10 Topics:")
for topic, count in topics[:10]:
    print(f"  {topic}: {count} references")
```

### Step 4: Common NEXUS Commands

```bash
# Full statistics
knowledgesync stats

# Topic analysis
knowledgesync topics --limit 20

# Relationship analysis
knowledgesync related "python" --depth 3
```

### Cross-Platform Considerations

```python
from pathlib import Path
import platform

# Platform-aware storage
if platform.system() == "Windows":
    storage = Path.home() / "AppData/Local/knowledgesync"
else:
    storage = Path.home() / ".config/knowledgesync"

ks = KnowledgeSync("NEXUS", storage_dir=storage)
```

### Next Steps for NEXUS

1. Test on all 3 platforms (Windows, Linux, macOS)
2. Create cross-platform analytics dashboard
3. Monitor knowledge distribution

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn simple lookups and task context

### Step 1: Verify Installation

```bash
# No API key needed - it's free!
python knowledgesync.py --version
# KnowledgeSync 1.0.0
```

### Step 2: First Use - Quick Lookups

```bash
# Before starting a task, check what's known
knowledgesync query "task topic"

# Check what the orchestrator decided
knowledgesync agent FORGE --topic "current-task"

# See existing solutions
knowledgesync query --category SOLUTION
```

### Step 3: Simple Task Workflow

```bash
# Step 1: Get context for task
knowledgesync query "feature-x"

# Step 2: Execute task (no knowledge action needed)

# Step 3: Log completion
knowledgesync add "Feature X implemented successfully" \
    --source BOLT \
    --category FACT \
    --topics feature-x completion
```

### Step 4: Common BOLT Commands

```bash
# Quick search
knowledgesync query "keyword"

# Check recent entries
knowledgesync query --limit 10

# See what's known about a topic
knowledgesync query --topics mytopic
```

### Cost-Saving Tips

1. **Use knowledge lookups instead of asking** - Free local queries
2. **Check existing solutions first** - Avoid duplicate work
3. **Log results for others** - Help the team

### Simple Python Usage

```python
from knowledgesync import query_knowledge, add_knowledge

# Quick lookup (free!)
results = query_knowledge("authentication")
for r in results:
    print(f"  {r.content[:60]}...")

# Log completion (free!)
add_knowledge(
    "Task completed successfully",
    category="FACT",
    topics=["task-name"],
    source="BOLT"
)
```

### Next Steps for BOLT

1. Add to Cline workflows
2. Use for repetitive task context
3. Report findings via simple adds

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/KnowledgeSync/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message Forge (tool owner)

---

**Last Updated:** January 21, 2026  
**Maintained By:** Forge (Team Brain)
