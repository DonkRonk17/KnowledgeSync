#!/usr/bin/env python3
"""
Comprehensive test suite for KnowledgeSync.

Tests cover:
- Knowledge entry creation and manipulation
- Query operations
- Knowledge graph operations
- Synchronization
- Extraction
- CLI interface
- Edge cases and error handling

Run: python test_knowledgesync.py
"""

import json
import os
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from knowledgesync import (
    KnowledgeSync,
    KnowledgeEntry,
    KnowledgeGraph,
    CATEGORIES,
    CONFIDENCE_LEVELS,
    add_knowledge,
    query_knowledge,
    what_does_agent_know,
    sync_knowledge,
    get_instance,
)


class TestKnowledgeEntry(unittest.TestCase):
    """Test KnowledgeEntry class."""
    
    def test_basic_creation(self):
        """Test basic entry creation."""
        entry = KnowledgeEntry(
            content="Test knowledge",
            source="ATLAS"
        )
        
        self.assertEqual(entry.content, "Test knowledge")
        self.assertEqual(entry.source, "ATLAS")
        self.assertEqual(entry.category, "FACT")
        self.assertEqual(entry.confidence, 0.8)
        self.assertIsNotNone(entry.entry_id)
        self.assertIsInstance(entry.created, datetime)
    
    def test_creation_with_all_params(self):
        """Test entry creation with all parameters."""
        expires = datetime.now() + timedelta(days=30)
        
        entry = KnowledgeEntry(
            content="Complete test",
            source="FORGE",
            category="DECISION",
            topics=["testing", "quality"],
            confidence=0.95,
            expires=expires,
            references=["abc123"],
            metadata={"priority": "high"}
        )
        
        self.assertEqual(entry.category, "DECISION")
        self.assertEqual(entry.topics, ["testing", "quality"])
        self.assertEqual(entry.confidence, 0.95)
        self.assertEqual(entry.expires, expires)
        self.assertEqual(entry.references, ["abc123"])
        self.assertEqual(entry.metadata, {"priority": "high"})
    
    def test_source_uppercase(self):
        """Test source is always uppercase."""
        entry = KnowledgeEntry(content="test", source="atlas")
        self.assertEqual(entry.source, "ATLAS")
    
    def test_topics_lowercase(self):
        """Test topics are always lowercase."""
        entry = KnowledgeEntry(
            content="test",
            source="ATLAS",
            topics=["Testing", "QUALITY", "Mixed"]
        )
        self.assertEqual(entry.topics, ["testing", "quality", "mixed"])
    
    def test_confidence_clamping(self):
        """Test confidence is clamped to 0-1 range."""
        entry1 = KnowledgeEntry(content="test", source="ATLAS", confidence=1.5)
        entry2 = KnowledgeEntry(content="test", source="ATLAS", confidence=-0.5)
        
        self.assertEqual(entry1.confidence, 1.0)
        self.assertEqual(entry2.confidence, 0.0)
    
    def test_invalid_category_defaults_to_fact(self):
        """Test invalid category defaults to FACT."""
        entry = KnowledgeEntry(
            content="test",
            source="ATLAS",
            category="INVALID_CATEGORY"
        )
        self.assertEqual(entry.category, "FACT")
    
    def test_to_dict(self):
        """Test serialization to dict."""
        entry = KnowledgeEntry(
            content="Test content",
            source="ATLAS",
            category="FINDING",
            topics=["test"]
        )
        
        data = entry.to_dict()
        
        self.assertEqual(data["content"], "Test content")
        self.assertEqual(data["source"], "ATLAS")
        self.assertEqual(data["category"], "FINDING")
        self.assertIn("entry_id", data)
        self.assertIn("created", data)
    
    def test_from_dict(self):
        """Test deserialization from dict."""
        data = {
            "entry_id": "test123",
            "content": "Restored content",
            "source": "FORGE",
            "category": "DECISION",
            "topics": ["restore", "test"],
            "confidence": 0.9,
            "created": "2026-01-20T10:00:00",
            "updated": "2026-01-20T11:00:00",
            "expires": None,
            "references": [],
            "metadata": {}
        }
        
        entry = KnowledgeEntry.from_dict(data)
        
        self.assertEqual(entry.entry_id, "test123")
        self.assertEqual(entry.content, "Restored content")
        self.assertEqual(entry.source, "FORGE")
        self.assertEqual(entry.category, "DECISION")
    
    def test_is_expired(self):
        """Test expiration check."""
        # Not expired
        entry1 = KnowledgeEntry(
            content="test",
            source="ATLAS",
            expires=datetime.now() + timedelta(days=1)
        )
        self.assertFalse(entry1.is_expired())
        
        # Expired
        entry2 = KnowledgeEntry(
            content="test",
            source="ATLAS",
            expires=datetime.now() - timedelta(days=1)
        )
        self.assertTrue(entry2.is_expired())
        
        # No expiration
        entry3 = KnowledgeEntry(content="test", source="ATLAS")
        self.assertFalse(entry3.is_expired())
    
    def test_matches_query(self):
        """Test query matching."""
        entry = KnowledgeEntry(
            content="TokenTracker costs about $0.50 per day",
            source="ATLAS",
            category="FINDING",
            topics=["tokentracker", "costs", "budget"]
        )
        
        self.assertTrue(entry.matches_query("tokentracker"))
        self.assertTrue(entry.matches_query("costs"))
        self.assertTrue(entry.matches_query("$0.50"))
        self.assertTrue(entry.matches_query("FINDING"))
        self.assertFalse(entry.matches_query("unrelated"))


class TestKnowledgeGraph(unittest.TestCase):
    """Test KnowledgeGraph class."""
    
    def test_add_node(self):
        """Test adding nodes."""
        graph = KnowledgeGraph()
        graph.add_node("python")
        graph.add_node("Python")  # Should be lowercase
        
        self.assertIn("python", graph.nodes)
        self.assertEqual(graph.nodes["python"]["references"], 2)
    
    def test_add_edge(self):
        """Test adding edges."""
        graph = KnowledgeGraph()
        graph.add_edge("python", "programming", "is_a")
        
        self.assertIn("python", graph.nodes)
        self.assertIn("programming", graph.nodes)
        self.assertEqual(len(graph.edges), 1)
        self.assertEqual(graph.edges[0]["relation"], "is_a")
    
    def test_get_related(self):
        """Test finding related topics."""
        graph = KnowledgeGraph()
        graph.add_edge("python", "programming")
        graph.add_edge("programming", "software")
        graph.add_edge("python", "automation")
        
        # Depth 1
        related = graph.get_related("python", depth=1)
        self.assertIn("programming", related)
        self.assertIn("automation", related)
        
        # Depth 2 - should include software (connected via programming)
        related = graph.get_related("python", depth=2)
        self.assertIn("programming", related)
        self.assertIn("automation", related)
        # Software is reachable in 2 hops: python -> programming -> software
        self.assertIn("software", related)
    
    def test_to_from_dict(self):
        """Test graph serialization."""
        graph = KnowledgeGraph()
        graph.add_edge("a", "b", "relates")
        
        data = graph.to_dict()
        restored = KnowledgeGraph.from_dict(data)
        
        self.assertEqual(len(restored.nodes), 2)
        self.assertEqual(len(restored.edges), 1)


class TestKnowledgeSync(unittest.TestCase):
    """Test KnowledgeSync main class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use temp directory for tests
        self.temp_dir = tempfile.mkdtemp()
        self.ks = KnowledgeSync(
            agent="TEST",
            storage_dir=Path(self.temp_dir),
            auto_sync=False  # Disable auto-save for tests
        )
    
    def tearDown(self):
        """Clean up after tests."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test proper initialization."""
        self.assertEqual(self.ks.agent, "TEST")
        self.assertEqual(self.ks.storage_dir, Path(self.temp_dir))
        self.assertIsInstance(self.ks.entries, dict)
        self.assertIsInstance(self.ks.graph, KnowledgeGraph)
    
    def test_add_knowledge(self):
        """Test adding knowledge."""
        entry = self.ks.add(
            content="Test knowledge entry",
            category="FACT",
            topics=["test", "knowledge"]
        )
        
        self.assertIn(entry.entry_id, self.ks.entries)
        self.assertEqual(entry.source, "TEST")
        self.assertIn("test", self.ks.graph.nodes)
        self.assertIn("knowledge", self.ks.graph.nodes)
    
    def test_add_empty_content_raises(self):
        """Test that empty content raises ValueError."""
        with self.assertRaises(ValueError):
            self.ks.add("")
        
        with self.assertRaises(ValueError):
            self.ks.add("   ")
    
    def test_update_knowledge(self):
        """Test updating knowledge."""
        entry = self.ks.add("Original content", topics=["test"])
        original_updated = entry.updated
        
        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)
        
        updated = self.ks.update(
            entry.entry_id,
            content="Updated content",
            confidence=0.95
        )
        
        self.assertEqual(updated.content, "Updated content")
        self.assertEqual(updated.confidence, 0.95)
        self.assertGreaterEqual(updated.updated, original_updated)
    
    def test_update_nonexistent(self):
        """Test updating non-existent entry returns None."""
        result = self.ks.update("nonexistent", content="test")
        self.assertIsNone(result)
    
    def test_delete_knowledge(self):
        """Test deleting knowledge."""
        entry = self.ks.add("To be deleted")
        entry_id = entry.entry_id
        
        self.assertTrue(self.ks.delete(entry_id))
        self.assertNotIn(entry_id, self.ks.entries)
    
    def test_delete_nonexistent(self):
        """Test deleting non-existent entry returns False."""
        self.assertFalse(self.ks.delete("nonexistent"))
    
    def test_get_knowledge(self):
        """Test getting knowledge by ID."""
        entry = self.ks.add("Test entry")
        
        retrieved = self.ks.get(entry.entry_id)
        self.assertEqual(retrieved.content, "Test entry")
        
        self.assertIsNone(self.ks.get("nonexistent"))
    
    def test_query_by_content(self):
        """Test querying by content."""
        self.ks.add("TokenTracker is useful", topics=["tokentracker"])
        self.ks.add("ContextCompressor saves tokens", topics=["contextcompressor"])
        
        results = self.ks.query("TokenTracker")
        
        self.assertEqual(len(results), 1)
        self.assertIn("TokenTracker", results[0].content)
    
    def test_query_by_source(self):
        """Test querying by source."""
        # Add with different source
        ks2 = KnowledgeSync(agent="FORGE", storage_dir=Path(self.temp_dir))
        ks2.add("From FORGE")
        
        self.ks.add("From TEST")
        
        # Load entries from file
        self.ks._load()
        
        results = self.ks.query(source="FORGE")
        self.assertTrue(all(e.source == "FORGE" for e in results))
    
    def test_query_by_category(self):
        """Test querying by category."""
        self.ks.add("A decision", category="DECISION")
        self.ks.add("A finding", category="FINDING")
        
        results = self.ks.query(category="DECISION")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].category, "DECISION")
    
    def test_query_by_topics(self):
        """Test querying by topics."""
        self.ks.add("About costs", topics=["costs", "budget"])
        self.ks.add("About tools", topics=["tools", "automation"])
        
        results = self.ks.query(topics=["costs"])
        
        self.assertEqual(len(results), 1)
        self.assertIn("costs", results[0].topics)
    
    def test_query_min_confidence(self):
        """Test querying with minimum confidence."""
        self.ks.add("High confidence", confidence=0.9)
        self.ks.add("Low confidence", confidence=0.3)
        
        results = self.ks.query(min_confidence=0.5)
        
        self.assertEqual(len(results), 1)
        self.assertGreaterEqual(results[0].confidence, 0.5)
    
    def test_query_include_related(self):
        """Test querying with related topics."""
        self.ks.add("About Python", topics=["python"])
        self.ks.add("About programming", topics=["programming"])
        self.ks.graph.add_edge("python", "programming")
        
        # Without related
        results1 = self.ks.query(topics=["python"], include_related=False)
        self.assertEqual(len(results1), 1)
        
        # With related
        results2 = self.ks.query(topics=["python"], include_related=True)
        self.assertEqual(len(results2), 2)
    
    def test_query_agent(self):
        """Test query_agent method."""
        self.ks.add("Knowledge from TEST")
        
        results = self.ks.query_agent("TEST")
        self.assertEqual(len(results), 1)
        
        results = self.ks.query_agent("NONEXISTENT")
        self.assertEqual(len(results), 0)
    
    def test_get_topics(self):
        """Test getting topic list."""
        self.ks.add("Topic 1", topics=["alpha"])
        self.ks.add("Topic 2", topics=["alpha", "beta"])
        self.ks.add("Topic 3", topics=["beta"])
        
        topics = self.ks.get_topics()
        
        self.assertGreater(len(topics), 0)
        # Most referenced should be first
        topic_names = [t[0] for t in topics]
        self.assertIn("alpha", topic_names)
        self.assertIn("beta", topic_names)
    
    def test_save_and_load(self):
        """Test persistence."""
        self.ks.add("Persistent entry", topics=["persistence"])
        self.ks._save()
        
        # Create new instance
        ks2 = KnowledgeSync(agent="TEST2", storage_dir=Path(self.temp_dir))
        
        self.assertEqual(len(ks2.entries), 1)
        self.assertEqual(list(ks2.entries.values())[0].content, "Persistent entry")
    
    def test_export_import_sync(self):
        """Test export and import for sync."""
        self.ks.add("Entry to sync", topics=["sync"])
        
        export_data = self.ks.export_for_sync()
        
        self.assertEqual(export_data["agent"], "TEST")
        self.assertEqual(len(export_data["entries"]), 1)
        
        # Import to new instance
        ks2 = KnowledgeSync(
            agent="OTHER",
            storage_dir=Path(tempfile.mkdtemp()),
            auto_sync=False
        )
        
        stats = ks2.import_from_sync(export_data)
        
        self.assertEqual(stats["added"], 1)
        self.assertEqual(len(ks2.entries), 1)
    
    def test_extract_from_text(self):
        """Test knowledge extraction from text."""
        text = """
        Session Summary:
        Finding: TokenTracker helps track API costs effectively.
        Decision: We will use TokenTracker for all agents.
        Problem: Some agents not reporting costs.
        Solution: Add automatic cost logging.
        """
        
        entries = self.ks.extract_from_text(text)
        
        self.assertGreaterEqual(len(entries), 4)
        categories = [e.category for e in entries]
        self.assertIn("FINDING", categories)
        self.assertIn("DECISION", categories)
        self.assertIn("PROBLEM", categories)
        self.assertIn("SOLUTION", categories)
    
    def test_cleanup_expired(self):
        """Test cleanup of expired entries."""
        # Add expired entry (manually set expiration)
        entry = self.ks.add("Expired entry")
        entry.expires = datetime.now() - timedelta(days=1)
        self.ks.entries[entry.entry_id] = entry
        
        # Add non-expired entry
        self.ks.add("Valid entry")
        
        removed = self.ks.cleanup_expired()
        
        self.assertEqual(removed, 1)
        self.assertEqual(len(self.ks.entries), 1)
    
    def test_clear_requires_confirmation(self):
        """Test clear requires confirmation."""
        self.ks.add("Entry 1")
        self.ks.add("Entry 2")
        
        # Without confirmation
        self.assertFalse(self.ks.clear(confirm=False))
        self.assertEqual(len(self.ks.entries), 2)
        
        # With confirmation
        self.assertTrue(self.ks.clear(confirm=True))
        self.assertEqual(len(self.ks.entries), 0)
    
    def test_get_stats(self):
        """Test statistics."""
        self.ks.add("Entry 1", category="FINDING", topics=["test"])
        self.ks.add("Entry 2", category="DECISION", topics=["test", "other"])
        
        stats = self.ks.get_stats()
        
        self.assertEqual(stats["total_entries"], 2)
        self.assertGreater(stats["total_topics"], 0)
        self.assertIn("TEST", stats["entries_by_source"])
        self.assertIn("FINDING", stats["entries_by_category"])
    
    def test_subscriptions(self):
        """Test subscription system."""
        received = []
        
        def callback(entry):
            received.append(entry)
        
        self.ks.subscribe("test_topic", callback)
        self.ks.add("Triggers callback", topics=["test_topic"])
        
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].topics, ["test_topic"])
    
    def test_unsubscribe(self):
        """Test unsubscription."""
        received = []
        
        def callback(entry):
            received.append(entry)
        
        self.ks.subscribe("topic", callback)
        self.assertTrue(self.ks.unsubscribe("topic", callback))
        
        self.ks.add("Should not trigger", topics=["topic"])
        self.assertEqual(len(received), 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def setUp(self):
        """Set up with fresh instance."""
        import knowledgesync
        knowledgesync._default_instance = None
    
    def test_get_instance(self):
        """Test singleton instance."""
        inst1 = get_instance("ATLAS")
        inst2 = get_instance("FORGE")
        
        # Should be same instance
        self.assertIs(inst1, inst2)
    
    def test_add_knowledge_function(self):
        """Test add_knowledge convenience function."""
        # Use temp storage
        import knowledgesync
        temp_dir = tempfile.mkdtemp()
        knowledgesync._default_instance = KnowledgeSync(
            agent="TEST",
            storage_dir=Path(temp_dir),
            auto_sync=False
        )
        
        entry = add_knowledge(
            "Test via function",
            category="FACT",
            topics=["test"],
            source="ATLAS"
        )
        
        self.assertIsInstance(entry, KnowledgeEntry)
        self.assertEqual(entry.content, "Test via function")
    
    def test_query_knowledge_function(self):
        """Test query_knowledge convenience function."""
        import knowledgesync
        temp_dir = tempfile.mkdtemp()
        ks = KnowledgeSync(
            agent="TEST",
            storage_dir=Path(temp_dir),
            auto_sync=False
        )
        knowledgesync._default_instance = ks
        
        ks.add("Searchable content", topics=["search"])
        
        results = query_knowledge("Searchable")
        self.assertEqual(len(results), 1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.ks = KnowledgeSync(
            agent="TEST",
            storage_dir=Path(self.temp_dir),
            auto_sync=False
        )
    
    def tearDown(self):
        """Clean up."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_large_content(self):
        """Test handling of large content."""
        large_content = "A" * 10000
        entry = self.ks.add(large_content)
        
        self.assertEqual(len(entry.content), 10000)
    
    def test_special_characters_in_content(self):
        """Test special characters in content."""
        special = "Test with special chars: @#$%^&*()[]{}|;':\",./<>?"
        entry = self.ks.add(special)
        
        self.assertEqual(entry.content, special)
    
    def test_unicode_content(self):
        """Test unicode in content."""
        unicode_content = "Test with unicode: \u4e2d\u6587 \u65e5\u672c\u8a9e"
        entry = self.ks.add(unicode_content)
        
        self.assertEqual(entry.content, unicode_content)
    
    def test_empty_query(self):
        """Test empty query returns all."""
        self.ks.add("Entry 1")
        self.ks.add("Entry 2")
        
        results = self.ks.query()
        self.assertEqual(len(results), 2)
    
    def test_many_entries(self):
        """Test handling many entries."""
        for i in range(100):
            self.ks.add(f"Entry {i}", topics=[f"topic_{i % 10}"])
        
        self.assertEqual(len(self.ks.entries), 100)
        
        # Query should still work
        results = self.ks.query(topics=["topic_5"])
        self.assertEqual(len(results), 10)
    
    def test_corrupt_file_handling(self):
        """Test handling of corrupt storage files."""
        # Write corrupt data
        entries_file = self.ks._get_entries_file()
        with open(entries_file, 'w') as f:
            f.write("not valid json {{{")
        
        # Should not raise, just warn
        ks2 = KnowledgeSync(
            agent="TEST2",
            storage_dir=Path(self.temp_dir),
            auto_sync=False
        )
        
        # Should have empty entries
        self.assertEqual(len(ks2.entries), 0)
    
    def test_missing_storage_dir(self):
        """Test creation of missing storage directory."""
        new_dir = Path(self.temp_dir) / "new_subdir" / "deep"
        ks = KnowledgeSync(
            agent="TEST",
            storage_dir=new_dir,
            auto_sync=False
        )
        
        self.assertTrue(new_dir.exists())


class TestCLI(unittest.TestCase):
    """Test CLI interface."""
    
    def test_cli_help(self):
        """Test CLI help runs without error."""
        from knowledgesync import main
        
        with patch('sys.argv', ['knowledgesync']):
            with patch('sys.stdout'):
                result = main()
        
        self.assertEqual(result, 0)
    
    def test_cli_stats(self):
        """Test CLI stats command."""
        from knowledgesync import main
        
        with patch('sys.argv', ['knowledgesync', 'stats']):
            with patch('sys.stdout'):
                result = main()
        
        self.assertEqual(result, 0)


def run_tests():
    """Run all tests with nice output."""
    print("=" * 70)
    print("TESTING: KnowledgeSync v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeEntry))
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeSync))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestCLI))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"[OK] Passed: {passed}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
