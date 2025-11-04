#!/usr/bin/env python3
"""
Witty Limerick Generator
A Python app that creates humorous limericks based on user-provided topics.
"""

import random
import re
from typing import List, Dict

class LimerickGenerator:
    def __init__(self):
        # Limerick templates with placeholders
        self.templates = [
            "There once was a {adjective} {noun} from {place},\nWho {verb} with incredible {noun2},\n{line3},\n{line4},\n{line5}.",
            "A {adjective} {noun} named {name},\nWould {verb} and cause quite a {noun2},\n{line3},\n{line4},\n{line5}.",
            "In {place} there lived a {noun},\nWho {verb} like a {adjective} {noun2},\n{line3},\n{line4},\n{line5}."
        ]
        
        # Word banks for different categories
        self.word_banks = {
            'adjectives': ['silly', 'clever', 'quirky', 'witty', 'funny', 'strange', 'odd', 'bright', 'swift', 'bold'],
            'verbs': ['danced', 'sang', 'jumped', 'laughed', 'played', 'ran', 'flew', 'swam', 'climbed', 'wrote'],
            'places': ['Maine', 'Spain', 'the lane', 'Ukraine', 'the plain', 'the train', 'the rain', 'the brain'],
            'names': ['Sue', 'Lou', 'Drew', 'Blue', 'Hugh', 'Rue', 'Crew', 'Stew'],
            'rhyme_endings': {
                'ace': ['place', 'space', 'race', 'face', 'case', 'grace', 'pace', 'trace'],
                'ame': ['name', 'game', 'fame', 'same', 'came', 'frame', 'blame', 'flame'],
                'ight': ['night', 'light', 'sight', 'right', 'bright', 'flight', 'might', 'height']
            }
        }
    
    def generate_limerick(self, topic: str) -> str:
        """Generate a limerick based on the given topic."""
        # Clean and process the topic
        topic = topic.strip().lower()
        
        # Choose a random template
        template = random.choice(self.templates)
        
        # Generate words based on topic and template needs
        words = self._generate_words_for_topic(topic)
        
        # Fill in the template
        try:
            limerick = template.format(**words)
            return limerick
        except KeyError as e:
            return f"Error generating limerick: Missing word type {e}"
    
    def _generate_words_for_topic(self, topic: str) -> Dict[str, str]:
        """Generate appropriate words based on the topic."""
        words = {}
        
        # Basic word selection
        words['adjective'] = random.choice(self.word_banks['adjectives'])
        words['verb'] = random.choice(self.word_banks['verbs'])
        words['place'] = random.choice(self.word_banks['places'])
        words['name'] = random.choice(self.word_banks['names'])
        
        # Topic-specific noun
        words['noun'] = self._get_topic_noun(topic)
        words['noun2'] = random.choice(['grace', 'pace', 'space', 'case', 'face'])
        
        # Generate rhyming lines
        words.update(self._generate_rhyming_lines())
        
        return words
    
    def _get_topic_noun(self, topic: str) -> str:
        """Convert topic to an appropriate noun for the limerick."""
        # Simple topic to noun mapping
        topic_nouns = {
            'cat': 'cat', 'dog': 'dog', 'bird': 'bird',
            'computer': 'coder', 'programming': 'programmer',
            'coffee': 'barista', 'food': 'chef',
            'music': 'musician', 'art': 'artist',
            'book': 'reader', 'travel': 'traveler'
        }
        
        return topic_nouns.get(topic, 'fellow')
    
    def _generate_rhyming_lines(self) -> Dict[str, str]:
        """Generate the middle and ending lines that rhyme properly."""
        # Simple rhyming line generation
        lines = {
            'line3': "They'd wiggle and giggle with glee",
            'line4': "And dance by the old apple tree", 
            'line5': "What a sight it would be!"
        }
        return lines

def main():
    """Main function to run the limerick generator."""
    generator = LimerickGenerator()
    
    print("🎭 Welcome to the Witty Limerick Generator! 🎭")
    print("=" * 50)
    
    while True:
        topic = input("\nEnter a topic for your limerick (or 'quit' to exit): ").strip()
        
        if topic.lower() in ['quit', 'exit', 'q']:
            print("Thanks for using the Limerick Generator! Goodbye! 👋")
            break
        
        if not topic:
            print("Please enter a valid topic!")
            continue
        
        print(f"\n📝 Here's your limerick about '{topic}':")
        print("-" * 40)
        limerick = generator.generate_limerick(topic)
        print(limerick)
        print("-" * 40)

if __name__ == "__main__":
    main()