#!/usr/bin/env python3
"""
Test script to demonstrate the limerick generators
"""

from limerick_generator import LimerickGenerator
from enhanced_limerick_generator import EnhancedLimerickGenerator

def test_generators():
    print("🧪 Testing Limerick Generators")
    print("=" * 40)
    
    # Test basic generator
    print("\n📝 Basic Generator:")
    basic_gen = LimerickGenerator()
    topics = ['cat', 'programming', 'coffee']
    
    for topic in topics:
        print(f"\nTopic: {topic}")
        print("-" * 20)
        print(basic_gen.generate_limerick(topic))
    
    # Test enhanced generator  
    print("\n\n✨ Enhanced Generator:")
    enhanced_gen = EnhancedLimerickGenerator()
    
    for topic in topics:
        print(f"\nTopic: {topic}")
        print("-" * 20)
        print(enhanced_gen.generate_limerick(topic))

if __name__ == "__main__":
    test_generators()