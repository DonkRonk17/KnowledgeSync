# 🧠 KnowledgeSync - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

KnowledgeSync is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: KnowledgeSync + SynapseLink](#pattern-1-knowledgesync--synapselink)
2. [Pattern 2: KnowledgeSync + AgentHealth](#pattern-2-knowledgesync--agenthealth)
3. [Pattern 3: KnowledgeSync + SessionReplay](#pattern-3-knowledgesync--sessionreplay)
4. [Pattern 4: KnowledgeSync + TaskQueuePro](#pattern-4-knowledgesync--taskqueuepro)
5. [Pattern 5: KnowledgeSync + ErrorRecovery](#pattern-5-knowledgesync--errorrecovery)
6. [Pattern 6: KnowledgeSync + ContextCompressor](#pattern-6-knowledgesync--contextcompressor)
7. [Pattern 7: KnowledgeSync + ConfigManager](#pattern-7-knowledgesync--configmanager)
8. [Pattern 8: KnowledgeSync + CollabSession](#pattern-8-knowledgesync--collabsession)
9. [Pattern 9: KnowledgeSync + MemoryBridge](#pattern-9-knowledgesync--memorybridge)
10. [Pattern 10: Full Team Brain Knowledge Stack](#pattern-10-full-team-brain-knowledge-stack)

---

## Pattern 1: KnowledgeSync + SynapseLink

**Use Case:** Notify team about important knowledge updates

**Why:** Keep all agents informed of critical discoveries and decisions

**Code:**

```python
from knowledgesync import KnowledgeSync
# from synapselink import quick_send  # Uncomment for actual use

ks = KnowledgeSync("ATLAS")

# Add important knowledge
entry = ks.add(
    "BCH Phase 3 deployment ready - all tests passing",
    category="FINDING",
    topics=["bch", "deployment", "phase-3"],
    confidence=0.95
)

# Notify team based on category
def notify_knowledge_update(entry):
    priority_map = {
        "DECISION": "HIGH",
        "PROBLEM": "HIGH",
        "FINDING": "NORMAL",
        "SOLUTION": "NORMAL",
        "FACT": "LOW"
    }
    
    priority = priority_map.get(entry.category, "NORMAL")
    
    message = f"""
Knowledge Update from {entry.source}:

[{entry.category}] {entry.content}

Topics: {', '.join(entry.topics)}
Confidence: {entry.confidence:.0%}
ID: {entry.entry_id[:8]}

Query: knowledgesync query "{entry.entry_id[:8]}"
    """
    
    # quick_send("TEAM", f"New {entry.category}", message, priority=priority)
    print(f"Would send {priority} priority notification")
    return message

# Notify
notify_knowledge_update(entry)
```

**Result:** Team receives notifications for important knowledge updates

---

## Pattern 2: KnowledgeSync + AgentHealth

**Use Case:** Track knowledge creation as a health metric

**Why:** Correlate agent productivity with knowledge output

**Code:**

```python
from knowledgesync import KnowledgeSync
# from agenthealth import AgentHealth  # Uncomment for actual use

ks = KnowledgeSync("ATLAS")
# health = AgentHealth()

class KnowledgeTrackedSession:
    """Track knowledge creation during an agent session."""
    
    def __init__(self, agent):
        self.agent = agent
        self.ks = KnowledgeSync(agent)
        self.start_count = len(self.ks.entries)
        self.session_entries = []
    
    def start(self, task_description):
        # health.start_session(self.agent)
        print(f"[{self.agent}] Session started: {task_description}")
    
    def log_knowledge(self, content, category="FACT", topics=None):
        entry = self.ks.add(content, category=category, topics=topics or [])
        self.session_entries.append(entry)
        return entry
    
    def end(self):
        end_count = len(self.ks.entries)
        new_entries = end_count - self.start_count
        
        # health.end_session(self.agent, metadata={
        #     "knowledge_entries_created": new_entries,
        #     "categories": [e.category for e in self.session_entries]
        # })
        
        print(f"[{self.agent}] Session ended: {new_entries} knowledge entries created")
        return new_entries

# Usage
session = KnowledgeTrackedSession("ATLAS")
session.start("Building KnowledgeSync tool")

session.log_knowledge(
    "JSON storage is sufficient for knowledge base",
    category="FINDING",
    topics=["knowledgesync", "storage"]
)

session.log_knowledge(
    "50 tests passing, 100% coverage",
    category="FACT",
    topics=["knowledgesync", "testing"]
)

entries_created = session.end()
print(f"Created {entries_created} knowledge entries this session")
```

**Result:** Agent health metrics include knowledge productivity

---

## Pattern 3: KnowledgeSync + SessionReplay

**Use Case:** Extract knowledge from recorded sessions

**Why:** Automatically capture learnings from past sessions

**Code:**

```python
from knowledgesync import KnowledgeSync
from pathlib import Path
# from sessionreplay import SessionReplay  # Uncomment for actual use

ks = KnowledgeSync("ATLAS")
# replay = SessionReplay()

def extract_session_knowledge(session_file, topics=None):
    """Extract knowledge from a session replay file."""
    
    # Get session data
    # session_data = replay.export_session(session_id, format="markdown")
    
    # For demo, read from file
    session_path = Path(session_file)
    if not session_path.exists():
        # Create sample session data
        session_data = """
        Session: Tool Build
        
        Finding: KnowledgeSync can handle 1000+ entries efficiently.
        Decision: We will use timestamp-based conflict resolution.
        Problem: Graph traversal was initially slow.
        Solution: Implemented visited set for O(n) performance.
        TODO: Add backup scheduling feature.
        """
    else:
        session_data = session_path.read_text()
    
    # Extract knowledge
    entries = ks.extract_from_text(
        session_data,
        topics=topics or ["session-replay", "extracted"]
    )
    
    print(f"Extracted {len(entries)} knowledge entries:")
    for entry in entries:
        print(f"  [{entry.category}] {entry.content[:50]}...")
    
    return entries

# Usage
entries = extract_session_knowledge(
    "HOLYGRAIL_KNOWLEDGESYNC_2026-01-21.md",
    topics=["knowledgesync", "session"]
)
```

**Result:** Session learnings automatically captured in knowledge base

---

## Pattern 4: KnowledgeSync + TaskQueuePro

**Use Case:** Add knowledge context to tasks

**Why:** Task executors have relevant knowledge upfront

**Code:**

```python
from knowledgesync import KnowledgeSync
# from taskqueuepro import TaskQueuePro  # Uncomment for actual use

ks = KnowledgeSync("FORGE")
# queue = TaskQueuePro()

def create_task_with_knowledge(title, topic, agent, priority=2):
    """Create a task with relevant knowledge context attached."""
    
    # Query relevant knowledge
    relevant = ks.query(topics=[topic], limit=5)
    
    # Prepare knowledge context
    context = []
    for entry in relevant:
        context.append({
            "id": entry.entry_id[:8],
            "source": entry.source,
            "category": entry.category,
            "content": entry.content[:100],
            "confidence": entry.confidence
        })
    
    # Create task with context
    task = {
        "title": title,
        "agent": agent,
        "priority": priority,
        "knowledge_context": context
    }
    
    # task_id = queue.create_task(**task)
    
    print(f"Task created: {title}")
    print(f"  Agent: {agent}")
    print(f"  Knowledge context: {len(context)} entries")
    for ctx in context:
        print(f"    [{ctx['source']}] {ctx['content'][:50]}...")
    
    return task

# Usage
task = create_task_with_knowledge(
    title="Fix BCH mobile connectivity",
    topic="bch-mobile",
    agent="CLIO",
    priority=2
)
```

**Result:** Task executors receive relevant knowledge with assignments

---

## Pattern 5: KnowledgeSync + ErrorRecovery

**Use Case:** Learn from recovered errors

**Why:** Build institutional knowledge of error patterns and solutions

**Code:**

```python
from knowledgesync import KnowledgeSync
# from errorrecovery import ErrorRecovery  # Uncomment for actual use

ks = KnowledgeSync("SYSTEM")

class LearningErrorRecovery:
    """Error recovery that learns and shares knowledge."""
    
    def __init__(self, agent):
        self.agent = agent
        self.ks = KnowledgeSync(agent)
    
    def recover(self, error, error_type, strategy_used, success):
        """Log recovery attempt as knowledge."""
        
        if success:
            # Successful recovery becomes a SOLUTION
            entry = self.ks.add(
                f"Recovered from {error_type} using {strategy_used} strategy",
                category="SOLUTION",
                topics=["errorrecovery", error_type, strategy_used],
                confidence=0.8,
                metadata={
                    "error_message": str(error)[:200],
                    "strategy": strategy_used,
                    "agent": self.agent
                }
            )
            print(f"[OK] Recovery logged: {entry.entry_id[:8]}")
        else:
            # Failed recovery becomes a PROBLEM
            entry = self.ks.add(
                f"Failed to recover from {error_type} with {strategy_used}",
                category="PROBLEM",
                topics=["errorrecovery", error_type, "unresolved"],
                confidence=1.0,
                metadata={
                    "error_message": str(error)[:200],
                    "strategy_tried": strategy_used
                }
            )
            print(f"[!] Unresolved error logged: {entry.entry_id[:8]}")
        
        return entry
    
    def find_similar_errors(self, error_type):
        """Find known solutions for error type."""
        solutions = self.ks.query(
            topics=[error_type],
            category="SOLUTION",
            min_confidence=0.6
        )
        return solutions

# Usage
recovery = LearningErrorRecovery("ATLAS")

# Successful recovery
recovery.recover(
    error="Connection timeout",
    error_type="network",
    strategy_used="retry",
    success=True
)

# Find similar past solutions
solutions = recovery.find_similar_errors("network")
print(f"\nFound {len(solutions)} solutions for network errors")
```

**Result:** Error recovery patterns captured as organizational knowledge

---

## Pattern 6: KnowledgeSync + ContextCompressor

**Use Case:** Compress knowledge for efficient sharing

**Why:** Save tokens when sharing large knowledge sets

**Code:**

```python
from knowledgesync import KnowledgeSync
# from contextcompressor import ContextCompressor  # Uncomment for actual use

ks = KnowledgeSync("ATLAS")

def share_knowledge_compressed(topics, recipient_agent):
    """Share knowledge on a topic with compression."""
    
    # Query knowledge
    results = ks.query(topics=topics, limit=20)
    
    if not results:
        print(f"No knowledge found for topics: {topics}")
        return None
    
    # Format as text
    full_text = "\n\n".join([
        f"[{e.category}] ({e.source}) {e.content}"
        for e in results
    ])
    
    # Compress
    # compressor = ContextCompressor()
    # compressed = compressor.compress_text(full_text, method="summary")
    
    # Simulated compression
    original_chars = len(full_text)
    compressed_chars = original_chars // 3  # Simulated 3x compression
    
    print(f"Knowledge sharing for topics: {topics}")
    print(f"  Entries: {len(results)}")
    print(f"  Original: {original_chars} chars")
    print(f"  Compressed: {compressed_chars} chars")
    print(f"  Savings: {(1 - compressed_chars/original_chars)*100:.1f}%")
    print(f"  Recipient: {recipient_agent}")
    
    return {
        "topics": topics,
        "entry_count": len(results),
        "original_size": original_chars,
        "compressed_size": compressed_chars
    }

# Usage
# Add some test knowledge first
ks.add("Architecture uses microservices", topics=["architecture"])
ks.add("Each service has its own database", topics=["architecture"])
ks.add("API gateway handles routing", topics=["architecture"])

result = share_knowledge_compressed(["architecture"], "FORGE")
```

**Result:** 60-70% token savings when sharing knowledge between agents

---

## Pattern 7: KnowledgeSync + ConfigManager

**Use Case:** Document configuration as knowledge

**Why:** Config decisions become searchable, reusable knowledge

**Code:**

```python
from knowledgesync import KnowledgeSync
# from configmanager import ConfigManager  # Uncomment for actual use

ks = KnowledgeSync("SYSTEM")

def document_config_change(tool, key, value, reason):
    """Document a configuration change as knowledge."""
    
    # Save to config
    # config = ConfigManager()
    # config.set(f"{tool}.{key}", value)
    # config.save()
    
    # Document as knowledge
    entry = ks.add(
        f"{tool} config: {key} = {value}. Reason: {reason}",
        category="CONFIG",
        topics=[tool, "configuration", key.replace(".", "-")],
        confidence=1.0,
        metadata={
            "tool": tool,
            "key": key,
            "value": value,
            "reason": reason
        }
    )
    
    print(f"[OK] Config documented: {entry.entry_id[:8]}")
    return entry

def find_config_knowledge(tool):
    """Find all configuration knowledge for a tool."""
    return ks.query(topics=[tool], category="CONFIG")

# Usage
document_config_change(
    tool="knowledgesync",
    key="auto_sync",
    value=True,
    reason="Ensure knowledge is always persisted"
)

document_config_change(
    tool="knowledgesync",
    key="default_confidence",
    value=0.8,
    reason="Balance between certainty and accessibility"
)

# Query config knowledge
configs = find_config_knowledge("knowledgesync")
print(f"\nKnowledgeSync has {len(configs)} documented config entries")
```

**Result:** Configuration decisions documented and searchable

---

## Pattern 8: KnowledgeSync + CollabSession

**Use Case:** Share knowledge during multi-agent collaboration

**Why:** All collaborators have same knowledge context

**Code:**

```python
from knowledgesync import KnowledgeSync
# from collabsession import CollabSession  # Uncomment for actual use

ks = KnowledgeSync("FORGE")

class KnowledgeAwareCollab:
    """Collaboration session with shared knowledge context."""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.ks = KnowledgeSync(orchestrator)
        self.participants = []
        self.shared_knowledge = []
    
    def start(self, task_topic, participants):
        """Start collaboration with knowledge context."""
        
        self.participants = participants
        
        # Gather relevant knowledge
        self.shared_knowledge = self.ks.query(
            topics=[task_topic],
            limit=10
        )
        
        # collab = CollabSession()
        # session = collab.start_session(task_topic, participants=participants)
        
        # Share knowledge context
        # collab.share_context(session.session_id, {
        #     "knowledge": [e.to_dict() for e in self.shared_knowledge]
        # })
        
        print(f"Collaboration started: {task_topic}")
        print(f"  Participants: {', '.join(participants)}")
        print(f"  Shared knowledge: {len(self.shared_knowledge)} entries")
        
        for entry in self.shared_knowledge:
            print(f"    [{entry.source}] {entry.content[:50]}...")
    
    def add_shared_finding(self, content, contributor):
        """Add finding that all participants can see."""
        entry = self.ks.add(
            content,
            category="FINDING",
            topics=["collab-session"],
            metadata={"contributor": contributor}
        )
        self.shared_knowledge.append(entry)
        return entry

# Usage
collab = KnowledgeAwareCollab("FORGE")

# First add some relevant knowledge
ks.add("BCH mobile requires CORS headers", topics=["bch-mobile"])
ks.add("Mobile app uses React Native", topics=["bch-mobile"])

collab.start(
    task_topic="bch-mobile",
    participants=["FORGE", "ATLAS", "CLIO"]
)
```

**Result:** All collaborators start with same knowledge context

---

## Pattern 9: KnowledgeSync + MemoryBridge

**Use Case:** Persist critical knowledge to memory core

**Why:** Important knowledge survives beyond agent sessions

**Code:**

```python
from knowledgesync import KnowledgeSync
from pathlib import Path
# from memorybridge import MemoryBridge  # Uncomment for actual use

ks = KnowledgeSync("ATLAS")

def persist_critical_knowledge():
    """Persist high-confidence decisions to memory bridge."""
    
    # Get critical knowledge
    critical = ks.query(
        min_confidence=0.95,
        category="DECISION"
    )
    
    # Prepare for memory bridge
    critical_data = [e.to_dict() for e in critical]
    
    # memory = MemoryBridge()
    # memory.set("critical_decisions", critical_data)
    # memory.set("critical_decisions_count", len(critical_data))
    # memory.set("critical_decisions_updated", datetime.now().isoformat())
    # memory.sync()
    
    print(f"Persisted {len(critical)} critical decisions to memory bridge")
    for entry in critical:
        print(f"  [{entry.source}] {entry.content[:50]}...")
    
    return critical_data

def restore_from_memory():
    """Restore knowledge from memory bridge."""
    
    # memory = MemoryBridge()
    # critical_data = memory.get("critical_decisions", default=[])
    
    # Simulated restore
    critical_data = []
    
    count = 0
    for data in critical_data:
        from knowledgesync import KnowledgeEntry
        entry = KnowledgeEntry.from_dict(data)
        if entry.entry_id not in ks.entries:
            ks.entries[entry.entry_id] = entry
            count += 1
    
    print(f"Restored {count} entries from memory bridge")
    return count

# Usage
# First add some critical decisions
ks.add(
    "All tools must have zero external dependencies",
    category="DECISION",
    topics=["architecture", "policy"],
    confidence=1.0
)

persist_critical_knowledge()
```

**Result:** Critical knowledge persists in long-term memory

---

## Pattern 10: Full Team Brain Knowledge Stack

**Use Case:** Complete knowledge workflow with all tools

**Why:** Production-grade agent operation

**Code:**

```python
from knowledgesync import KnowledgeSync
from pathlib import Path
from datetime import datetime

# Full integration example
class TeamBrainKnowledgeStack:
    """Complete knowledge management with all Team Brain tools."""
    
    def __init__(self, agent):
        self.agent = agent
        self.ks = KnowledgeSync(agent)
        self.session_start = datetime.now()
        self.session_knowledge = []
    
    def start_session(self, task_description):
        """Start a knowledge-aware session."""
        
        print(f"{'='*60}")
        print(f"SESSION START: {self.agent}")
        print(f"Task: {task_description}")
        print(f"{'='*60}")
        
        # Check relevant knowledge
        keywords = task_description.lower().split()[:3]
        for keyword in keywords:
            results = self.ks.query(keyword)
            if results:
                print(f"\nExisting knowledge about '{keyword}':")
                for r in results[:3]:
                    print(f"  [{r.source}] {r.content[:50]}...")
        
        # Health integration
        # health.start_session(self.agent)
        
        # Session replay integration
        # replay.start_session(self.agent, task=task_description)
    
    def log_finding(self, content, topics=None):
        """Log a finding with full integration."""
        entry = self.ks.add(content, category="FINDING", topics=topics or [])
        self.session_knowledge.append(entry)
        print(f"[FINDING] {content[:50]}...")
        return entry
    
    def log_decision(self, content, topics=None):
        """Log a decision with notification."""
        entry = self.ks.add(
            content, 
            category="DECISION", 
            topics=topics or [],
            confidence=1.0
        )
        self.session_knowledge.append(entry)
        
        # Notify team
        # quick_send("TEAM", f"New Decision from {self.agent}", content)
        
        print(f"[DECISION] {content[:50]}...")
        return entry
    
    def log_problem(self, content, topics=None):
        """Log a problem."""
        entry = self.ks.add(content, category="PROBLEM", topics=topics or [])
        self.session_knowledge.append(entry)
        print(f"[PROBLEM] {content[:50]}...")
        return entry
    
    def log_solution(self, content, problem_id=None, topics=None):
        """Log a solution with reference to problem."""
        refs = [problem_id] if problem_id else []
        entry = self.ks.add(
            content, 
            category="SOLUTION", 
            topics=topics or [],
            references=refs
        )
        self.session_knowledge.append(entry)
        print(f"[SOLUTION] {content[:50]}...")
        return entry
    
    def end_session(self):
        """End session with summary."""
        
        duration = datetime.now() - self.session_start
        
        print(f"\n{'='*60}")
        print(f"SESSION END: {self.agent}")
        print(f"{'='*60}")
        print(f"Duration: {duration}")
        print(f"Knowledge created: {len(self.session_knowledge)}")
        
        # Categorize session knowledge
        by_category = {}
        for entry in self.session_knowledge:
            cat = entry.category
            by_category[cat] = by_category.get(cat, 0) + 1
        
        print("\nBy category:")
        for cat, count in by_category.items():
            print(f"  {cat}: {count}")
        
        # Extract any remaining knowledge from session
        # replay_data = replay.export_session(format="markdown")
        # self.ks.extract_from_text(replay_data, topics=["session-end"])
        
        # End health session
        # health.end_session(self.agent, metadata={
        #     "knowledge_created": len(self.session_knowledge)
        # })
        
        # Notify team of session completion
        # quick_send("TEAM", f"{self.agent} Session Complete", 
        #            f"Created {len(self.session_knowledge)} knowledge entries")
        
        print("\n[OK] Session complete")
        return self.session_knowledge

# Usage
stack = TeamBrainKnowledgeStack("ATLAS")
stack.start_session("Build KnowledgeSync tool")

stack.log_finding("JSON storage is efficient for knowledge base")
stack.log_decision("Will use timestamp-based conflict resolution")
prob = stack.log_problem("Graph traversal initially O(n^2)")
stack.log_solution("Used visited set for O(n) performance", prob.entry_id)
stack.log_finding("50 tests achieve 100% coverage")

results = stack.end_session()
```

**Result:** Fully instrumented knowledge workflow with all integrations

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✅ SynapseLink - Team notifications
2. ✅ SessionReplay - Knowledge extraction
3. ✅ AgentHealth - Productivity tracking

**Week 2 (Productivity):**
4. ☐ TaskQueuePro - Task context
5. ☐ ErrorRecovery - Learning from errors
6. ☐ ConfigManager - Config documentation

**Week 3 (Advanced):**
7. ☐ ContextCompressor - Token optimization
8. ☐ CollabSession - Multi-agent coordination
9. ☐ MemoryBridge - Long-term persistence
10. ☐ Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**
```python
# Ensure all tools are in Python path
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Then import
from knowledgesync import KnowledgeSync
```

**Version Conflicts:**
```bash
# Check versions
python -c "from knowledgesync import __version__; print(__version__)"

# Update if needed
cd AutoProjects/KnowledgeSync
git pull origin main
```

**Storage Location Issues:**
```python
# Use explicit storage path
from pathlib import Path
ks = KnowledgeSync("AGENT", storage_dir=Path.home() / ".knowledgesync")
```

---

**Last Updated:** January 21, 2026  
**Maintained By:** Forge (Team Brain)
