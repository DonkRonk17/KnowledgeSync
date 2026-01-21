# 🧠 KnowledgeSync - Usage Examples

## Quick Navigation

- [Example 1: Basic Knowledge Entry](#example-1-basic-knowledge-entry)
- [Example 2: Querying Knowledge](#example-2-querying-knowledge)
- [Example 3: Agent-Specific Queries](#example-3-agent-specific-queries)
- [Example 4: Working with Topics](#example-4-working-with-topics)
- [Example 5: Knowledge Extraction](#example-5-knowledge-extraction)
- [Example 6: Synchronization](#example-6-synchronization)
- [Example 7: Subscriptions](#example-7-subscriptions)
- [Example 8: Integration with SynapseLink](#example-8-integration-with-synapselink)
- [Example 9: CLI Operations](#example-9-cli-operations)
- [Example 10: Full Team Brain Workflow](#example-10-full-team-brain-workflow)

---

## Example 1: Basic Knowledge Entry

**Scenario:** ATLAS discovers an important fact about TokenTracker and wants to share it with the team.

### Python API

```python
from knowledgesync import KnowledgeSync

# Initialize for ATLAS
ks = KnowledgeSync("ATLAS")

# Add the knowledge
entry = ks.add(
    content="TokenTracker shows average daily cost is $0.45 per agent",
    category="FINDING",
    topics=["tokentracker", "costs", "daily-usage"],
    confidence=0.9
)

print(f"[OK] Added entry: {entry.entry_id[:8]}")
print(f"     Category: {entry.category}")
print(f"     Topics: {', '.join(entry.topics)}")
print(f"     Confidence: {entry.confidence:.0%}")
```

**Expected Output:**
```
[OK] Added entry: a7b3c2d1
     Category: FINDING
     Topics: tokentracker, costs, daily-usage
     Confidence: 90%
```

### CLI Alternative

```bash
knowledgesync add "TokenTracker shows average daily cost is $0.45 per agent" \
    --source ATLAS \
    --category FINDING \
    --topics tokentracker costs daily-usage \
    --confidence 0.9
```

**What You Learned:**
- How to initialize KnowledgeSync with an agent name
- How to add knowledge with category, topics, and confidence
- Knowledge is automatically saved for other agents to find

---

## Example 2: Querying Knowledge

**Scenario:** FORGE needs to find all knowledge about costs before a budget meeting.

### Python API

```python
from knowledgesync import KnowledgeSync

ks = KnowledgeSync("FORGE")

# Query by content
results = ks.query("costs")
print(f"Found {len(results)} entries about 'costs':\n")

for entry in results:
    print(f"[{entry.source}] [{entry.category}]")
    print(f"  {entry.content}")
    print(f"  Confidence: {entry.confidence:.0%}")
    print()

# Query by topics
results = ks.query(topics=["budget", "costs"])
print(f"Found {len(results)} entries with budget/costs topics")

# Query with filters
results = ks.query(
    search="token",
    source="ATLAS",
    category="FINDING",
    min_confidence=0.7,
    limit=10
)
print(f"Found {len(results)} high-confidence findings from ATLAS about tokens")
```

**Expected Output:**
```
Found 3 entries about 'costs':

[ATLAS] [FINDING]
  TokenTracker shows average daily cost is $0.45 per agent
  Confidence: 90%

[FORGE] [DECISION]
  Monthly budget set at $60 for all agents combined
  Confidence: 100%

[NEXUS] [CONFIG]
  Cost alerts configured at $50 threshold
  Confidence: 85%

Found 2 entries with budget/costs topics
Found 1 high-confidence findings from ATLAS about tokens
```

### CLI Alternative

```bash
# Query by content
knowledgesync query "costs"

# Query by topics
knowledgesync query --topics budget costs

# Combined filters
knowledgesync query "token" --source ATLAS --category FINDING --min-confidence 0.7
```

**What You Learned:**
- Multiple ways to query: by content, topics, source, category
- Filters can be combined for precise results
- Results are sorted by relevance (confidence + recency)

---

## Example 3: Agent-Specific Queries

**Scenario:** CLIO needs to know what FORGE decided about the architecture.

### Python API

```python
from knowledgesync import KnowledgeSync, what_does_agent_know

ks = KnowledgeSync("CLIO")

# Method 1: Using query_agent
forge_decisions = ks.query_agent("FORGE", "architecture")
print("What FORGE knows about architecture:\n")
for entry in forge_decisions:
    print(f"  [{entry.category}] {entry.content[:80]}...")

# Method 2: Using convenience function
forge_all = what_does_agent_know("FORGE")
print(f"\nFORGE has {len(forge_all)} total knowledge entries")

# Method 3: Using query with source filter
decisions = ks.query(source="FORGE", category="DECISION")
print(f"\nFORGE has made {len(decisions)} recorded decisions")
```

**Expected Output:**
```
What FORGE knows about architecture:

  [DECISION] BCH will use microservices architecture with separate front...
  [DECISION] Each Q-Mode tool must be standalone with zero dependencies...
  [INSIGHT] Monolithic approaches failed in past due to maintenance burd...

FORGE has 47 total knowledge entries

FORGE has made 15 recorded decisions
```

### CLI Alternative

```bash
# What does FORGE know about architecture?
knowledgesync agent FORGE --topic architecture

# All of FORGE's knowledge
knowledgesync agent FORGE

# FORGE's decisions only
knowledgesync query --source FORGE --category DECISION
```

**What You Learned:**
- `query_agent()` is the fastest way to ask "what does X know about Y?"
- Agents can query each other's knowledge without manual communication
- Different methods for different query needs

---

## Example 4: Working with Topics

**Scenario:** Understand how topics are organized and find related knowledge.

### Python API

```python
from knowledgesync import KnowledgeSync

ks = KnowledgeSync("ATLAS")

# First, add some interconnected knowledge
ks.add("Python is used for all Q-Mode tools", topics=["python", "q-mode"])
ks.add("Q-Mode tools have zero dependencies", topics=["q-mode", "dependencies"])
ks.add("Dependencies should use standard library", topics=["dependencies", "stdlib"])

# Get all topics
topics = ks.get_topics()
print("Top topics by reference count:")
for topic, count in topics[:10]:
    print(f"  {topic}: {count} references")

# Find related topics
related = ks.get_related_topics("python", depth=2)
print(f"\nTopics related to 'python': {', '.join(related)}")

# Query with related topics included
results = ks.query(topics=["python"], include_related=True)
print(f"\nEntries about Python (including related): {len(results)}")
```

**Expected Output:**
```
Top topics by reference count:
  q-mode: 15 references
  tools: 12 references
  python: 10 references
  costs: 8 references
  architecture: 7 references
  bch: 6 references
  dependencies: 5 references
  integration: 4 references
  testing: 4 references
  documentation: 3 references

Topics related to 'python': q-mode, dependencies, stdlib

Entries about Python (including related): 8
```

### CLI Alternative

```bash
# List all topics
knowledgesync topics --limit 10

# Find related topics
knowledgesync related python --depth 2

# Query with related topics
knowledgesync query --topics python --related
```

**What You Learned:**
- The knowledge graph automatically tracks topic relationships
- Topics that appear together in entries become related
- `include_related=True` expands queries to include related topics

---

## Example 5: Knowledge Extraction

**Scenario:** Automatically extract knowledge from a session log.

### Python API

```python
from knowledgesync import KnowledgeSync
from pathlib import Path

ks = KnowledgeSync("ATLAS")

# Extract from text directly
session_summary = """
Session Summary: Tool Build Session

Finding: ErrorRecovery successfully handles 12 different error patterns.
Decision: We will integrate ErrorRecovery into all agent startup routines.
Problem: Some error patterns overlap and cause duplicate handling.
Solution: Added pattern priority system to resolve overlaps.
TODO: Add pattern for database connection errors.
Note: ErrorRecovery is Q-Mode tool #15.
Insight: Most errors can be recovered with simple retry logic.
"""

entries = ks.extract_from_text(session_summary, topics=["errorrecovery", "session"])
print(f"Extracted {len(entries)} knowledge entries:\n")

for entry in entries:
    print(f"[{entry.category}] {entry.content[:60]}...")

# Extract from file
session_file = Path("HOLYGRAIL_ERRORRECOVERY_2026-01-20.md")
if session_file.exists():
    file_entries = ks.extract_from_session(session_file, topics=["errorrecovery"])
    print(f"\nExtracted {len(file_entries)} entries from session file")
```

**Expected Output:**
```
Extracted 7 knowledge entries:

[FINDING] ErrorRecovery successfully handles 12 different error patterns...
[DECISION] We will integrate ErrorRecovery into all agent startup routines...
[PROBLEM] Some error patterns overlap and cause duplicate handling...
[SOLUTION] Added pattern priority system to resolve overlaps...
[TODO] Add pattern for database connection errors...
[FACT] ErrorRecovery is Q-Mode tool #15...
[INSIGHT] Most errors can be recovered with simple retry logic...

Extracted 12 entries from session file
```

### CLI Alternative

```bash
# Extract from file
knowledgesync extract session_log.md --topics session tool-build

# Extract from bookmark
knowledgesync extract HOLYGRAIL_TOOL_2026-01-20.md
```

**What You Learned:**
- KnowledgeSync can parse text for knowledge patterns
- Supported patterns: Finding, Decision, Problem, Solution, TODO, Note, Insight, Config
- Session files and bookmarks can be batch-processed

---

## Example 6: Synchronization

**Scenario:** Share knowledge between agents or backup/restore.

### Python API

```python
from knowledgesync import KnowledgeSync
import json

# Agent 1 creates knowledge
ks_atlas = KnowledgeSync("ATLAS")
ks_atlas.add("Important discovery from ATLAS", topics=["discovery"])

# Export for sharing
export_data = ks_atlas.export_for_sync()
print(f"Exported {len(export_data['entries'])} entries")

# Save to file
with open("atlas_knowledge.json", "w") as f:
    json.dump(export_data, f)

# Agent 2 imports the knowledge
ks_forge = KnowledgeSync("FORGE")

with open("atlas_knowledge.json", "r") as f:
    import_data = json.load(f)

stats = ks_forge.import_from_sync(import_data)
print(f"\nImport results:")
print(f"  Added: {stats['added']}")
print(f"  Updated: {stats['updated']}")
print(f"  Conflicts: {stats['conflicts']}")

# Verify import
results = ks_forge.query(source="ATLAS")
print(f"\nFORGE now has {len(results)} entries from ATLAS")
```

**Expected Output:**
```
Exported 25 entries

Import results:
  Added: 20
  Updated: 5
  Conflicts: 0

FORGE now has 25 entries from ATLAS
```

### CLI Alternative

```bash
# Export knowledge
knowledgesync sync --export backup.json

# Import knowledge
knowledgesync sync --import atlas_knowledge.json

# Simple sync (save current state)
knowledgesync sync
```

**What You Learned:**
- Knowledge can be exported to JSON for backup or sharing
- Import handles duplicates automatically (newer wins)
- Conflicts are tracked but don't block import

---

## Example 7: Subscriptions

**Scenario:** Get notified when knowledge about specific topics is updated.

### Python API

```python
from knowledgesync import KnowledgeSync

ks = KnowledgeSync("CLIO")

# Track received notifications
notifications = []

# Define callback
def on_budget_update(entry):
    notifications.append(entry)
    print(f"[NOTIFICATION] Budget update from {entry.source}:")
    print(f"  {entry.content}")

# Subscribe to budget topic
ks.subscribe("budget", on_budget_update)
print("Subscribed to 'budget' topic\n")

# Add some knowledge (simulating other agents)
ks.add("Monthly budget increased to $75", 
       topics=["budget", "costs"],
       metadata={"approved_by": "LOGAN"})

ks.add("Emergency budget reserve of $20 allocated",
       topics=["budget", "emergency"])

# Non-budget entry (no notification)
ks.add("New tool completed: KnowledgeSync",
       topics=["tools", "q-mode"])

print(f"\nReceived {len(notifications)} notifications")

# Unsubscribe when done
ks.unsubscribe("budget", on_budget_update)
print("Unsubscribed from 'budget' topic")
```

**Expected Output:**
```
Subscribed to 'budget' topic

[NOTIFICATION] Budget update from CLIO:
  Monthly budget increased to $75
[NOTIFICATION] Budget update from CLIO:
  Emergency budget reserve of $20 allocated

Received 2 notifications
Unsubscribed from 'budget' topic
```

**What You Learned:**
- Subscriptions enable reactive knowledge updates
- Callbacks receive the full KnowledgeEntry object
- Useful for triggering SynapseLink notifications or other actions

---

## Example 8: Integration with SynapseLink

**Scenario:** Share knowledge discoveries with the team via SynapseLink.

### Python API

```python
from knowledgesync import KnowledgeSync
# from synapselink import quick_send  # Uncomment for actual integration

ks = KnowledgeSync("ATLAS")

# Make an important discovery
entry = ks.add(
    content="BCH Phase 3 is ready for deployment",
    category="FINDING",
    topics=["bch", "deployment", "phase-3"],
    confidence=0.95,
    metadata={"tested": True, "environment": "staging"}
)

# Notify team via SynapseLink
message = f"""
Knowledge Update from ATLAS:

[{entry.category}] {entry.content}

Topics: {', '.join(entry.topics)}
Confidence: {entry.confidence:.0%}
Entry ID: {entry.entry_id[:8]}

Query this knowledge:
  knowledgesync query "{entry.entry_id[:8]}"
"""

print("Would send via SynapseLink:")
print(message)

# In production:
# quick_send("TEAM", f"New {entry.category}: BCH Phase 3", message)
```

**Expected Output:**
```
Would send via SynapseLink:

Knowledge Update from ATLAS:

[FINDING] BCH Phase 3 is ready for deployment

Topics: bch, deployment, phase-3
Confidence: 95%
Entry ID: f3a2b1c4

Query this knowledge:
  knowledgesync query "f3a2b1c4"
```

**What You Learned:**
- Combine KnowledgeSync with SynapseLink for team notifications
- Include entry ID for easy reference
- Confidence level helps team assess reliability

---

## Example 9: CLI Operations

**Scenario:** Complete workflow using only CLI commands.

### Session: Discovering and Sharing Knowledge

```bash
# 1. Check what we already know
knowledgesync stats

# 2. Search for existing knowledge about BCH
knowledgesync query "bch"

# 3. Add new discovery
knowledgesync add "BCH mobile app requires service worker for offline mode" \
    --source CLIO \
    --category FINDING \
    --topics bch mobile offline service-worker \
    --confidence 0.85

# 4. Find related topics
knowledgesync related "bch" --depth 2

# 5. See what other agents know about mobile
knowledgesync agent ATLAS --topic mobile
knowledgesync agent FORGE --topic mobile

# 6. List all topics
knowledgesync topics --limit 20

# 7. Export for backup
knowledgesync sync --export weekly_backup.json

# 8. View final stats
knowledgesync stats
```

**Expected Output:**
```
============================================================
KNOWLEDGESYNC STATISTICS
============================================================
Total Entries: 127
Total Topics: 45
...

[OK] Found 8 entries:
  [a3b2c1d4] (FORGE) [DECISION]
    BCH architecture uses React frontend with Python backend...
...

[OK] Added knowledge entry: e5f6a7b8
     Category: FINDING
     Topics: bch, mobile, offline, service-worker
     Confidence: 85%

[OK] Topics related to 'bch':
  - mobile
  - architecture
  - deployment
  - frontend
...

[OK] Exported 128 entries to weekly_backup.json

============================================================
KNOWLEDGESYNC STATISTICS
============================================================
Total Entries: 128
...
```

**What You Learned:**
- Full CLI workflow for knowledge management
- Commands can be chained for comprehensive operations
- Regular backups keep knowledge safe

---

## Example 10: Full Team Brain Workflow

**Scenario:** Complete end-to-end workflow showing how Team Brain uses KnowledgeSync.

### Python API

```python
from knowledgesync import KnowledgeSync, what_does_agent_know
from pathlib import Path

# ============================================================
# FORGE: Planning Session
# ============================================================

print("=" * 60)
print("FORGE: Planning Session")
print("=" * 60)

forge = KnowledgeSync("FORGE")

# Record architectural decision
forge.add(
    "All Q-Mode tools must support both CLI and Python API",
    category="DECISION",
    topics=["q-mode", "architecture", "api-design"],
    confidence=1.0
)

# Record task assignment
forge.add(
    "KnowledgeSync assigned to ATLAS for implementation",
    category="DECISION",
    topics=["knowledgesync", "task-assignment", "atlas"],
    confidence=1.0
)

print("FORGE recorded 2 decisions\n")

# ============================================================
# ATLAS: Implementation Session
# ============================================================

print("=" * 60)
print("ATLAS: Implementation Session")
print("=" * 60)

atlas = KnowledgeSync("ATLAS")

# Check what FORGE decided
forge_decisions = atlas.query(source="FORGE", category="DECISION")
print(f"Found {len(forge_decisions)} decisions from FORGE:")
for d in forge_decisions[:3]:
    print(f"  - {d.content[:60]}...")

# Record implementation findings
atlas.add(
    "KnowledgeSync uses JSON files for storage - no database needed",
    category="FINDING",
    topics=["knowledgesync", "storage", "implementation"]
)

atlas.add(
    "Knowledge graph enables related topic queries in O(n) time",
    category="FINDING",
    topics=["knowledgesync", "performance", "graph"]
)

atlas.add(
    "50 tests passing with 100% coverage on core functionality",
    category="FACT",
    topics=["knowledgesync", "testing", "quality"]
)

print("\nATLAS recorded 3 implementation findings\n")

# ============================================================
# CLIO: Review and Integration
# ============================================================

print("=" * 60)
print("CLIO: Review and Integration")
print("=" * 60)

clio = KnowledgeSync("CLIO")

# Review what team knows about KnowledgeSync
all_ks_knowledge = clio.query(topics=["knowledgesync"])
print(f"Team has {len(all_ks_knowledge)} entries about KnowledgeSync:")

for entry in all_ks_knowledge:
    print(f"  [{entry.source}] [{entry.category}] {entry.content[:50]}...")

# Add integration finding
clio.add(
    "KnowledgeSync works on both Windows and Linux without issues",
    category="FINDING",
    topics=["knowledgesync", "cross-platform", "integration"]
)

print("\nCLIO confirmed cross-platform compatibility\n")

# ============================================================
# Summary Report
# ============================================================

print("=" * 60)
print("KNOWLEDGE SUMMARY")
print("=" * 60)

report = KnowledgeSync("SYSTEM")
stats = report.get_stats()

print(f"\nTotal Knowledge Entries: {stats['total_entries']}")
print(f"Total Topics: {stats['total_topics']}")
print(f"Total Relationships: {stats['total_relationships']}")

print("\nBy Agent:")
for agent, count in sorted(stats['entries_by_source'].items()):
    print(f"  {agent}: {count} entries")

print("\nBy Category:")
for cat, count in sorted(stats['entries_by_category'].items()):
    print(f"  {cat}: {count} entries")

print("\n[OK] Team Brain knowledge synchronized!")
```

**Expected Output:**
```
============================================================
FORGE: Planning Session
============================================================
FORGE recorded 2 decisions

============================================================
ATLAS: Implementation Session
============================================================
Found 2 decisions from FORGE:
  - All Q-Mode tools must support both CLI and Python API...
  - KnowledgeSync assigned to ATLAS for implementation...

ATLAS recorded 3 implementation findings

============================================================
CLIO: Review and Integration
============================================================
Team has 5 entries about KnowledgeSync:
  [FORGE] [DECISION] KnowledgeSync assigned to ATLAS for implementat...
  [ATLAS] [FINDING] KnowledgeSync uses JSON files for storage - no d...
  [ATLAS] [FINDING] Knowledge graph enables related topic queries in...
  [ATLAS] [FACT] 50 tests passing with 100% coverage on core func...
  [CLIO] [FINDING] KnowledgeSync works on both Windows and Linux w...

CLIO confirmed cross-platform compatibility

============================================================
KNOWLEDGE SUMMARY
============================================================

Total Knowledge Entries: 6
Total Topics: 15
Total Relationships: 23

By Agent:
  ATLAS: 3 entries
  CLIO: 1 entries
  FORGE: 2 entries

By Category:
  DECISION: 2 entries
  FACT: 1 entries
  FINDING: 3 entries

[OK] Team Brain knowledge synchronized!
```

**What You Learned:**
- Complete workflow from planning to implementation to review
- Agents can seamlessly access each other's knowledge
- Knowledge graph automatically tracks relationships
- Statistics provide visibility into team knowledge

---

## Additional Tips

### Best Practices

1. **Always specify source agent** - Makes queries easier
2. **Use consistent topics** - Lowercase, hyphenated (e.g., "q-mode", "cross-platform")
3. **Set appropriate confidence** - Be honest about certainty
4. **Add expiration for temporary knowledge** - Use `expires_in_days`
5. **Link related entries** - Use `references` parameter

### Common Patterns

```python
# Pattern: Log session learnings
def log_session_knowledge(agent, session_summary, topics):
    ks = KnowledgeSync(agent)
    entries = ks.extract_from_text(session_summary, topics)
    return entries

# Pattern: Check before deciding
def check_existing_decisions(topic):
    ks = KnowledgeSync()
    return ks.query(topics=[topic], category="DECISION")

# Pattern: Notify on important discoveries
def share_discovery(agent, content, topics, notify=True):
    ks = KnowledgeSync(agent)
    entry = ks.add(content, category="FINDING", topics=topics)
    if notify:
        # Integration with SynapseLink
        pass
    return entry
```

---

**Last Updated:** January 21, 2026  
**Maintained By:** Team Brain  
**See Also:** [README.md](README.md) | [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
