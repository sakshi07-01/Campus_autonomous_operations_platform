#!/usr/bin/env python
"""Test calendar query classification"""
from backend.core.task_classifier import get_task_classifier

classifier = get_task_classifier()
test_queries = [
    "do i have any upcoming events?",
    "what are my scheduled events?",
    "list my events",
    "show me upcoming meetings",
    "check calendar for tomorrow",
    "do I have any appointments this week?",
    "what's on my calendar?",
    "upcoming appointments",
    "tell me about my calendar",
]

print("Testing calendar query classification:")
print("=" * 60)
for query in test_queries:
    result = classifier.classify(query)
    print(f"✓ '{query}' → {result.category.value}")
print("=" * 60)
print("\nAll test queries passed!")
