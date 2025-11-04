#!/usr/bin/env python3
"""
Enhanced Witty Limerick Generator
A more sophisticated Python app that creates humorous limericks with better rhyming.
"""

import random
import re
from typing import List, Dict, Tuple

class EnhancedLimerickGenerator:
    def __init__(self):
        # Topic suggestions for users
        self.topic_suggestions = [
            'cat', 'dog', 'programming', 'coffee', 'pizza', 'music', 'travel', 
            'books', 'dancing', 'cooking', 'gardening', 'sports', 'weather',
            'friendship', 'technology', 'art', 'movies', 'chocolate', 'beach'
        ]
        
        # Track recent combinations to avoid repetition
        self.recent_combinations = []
        self.max_recent = 10
        
        # Multiple limerick templates for variety
        self.templates = [
            "There once was a {adj1} {noun1} from {place1},\nWho {verb1} with incredible {noun2},\n{line3_a} {end1},\n{line4_a} {end2},\n{conclusion1} {place2}!",
            
            "A {adj1} {noun1} named {name1},\nWould {verb1} and cause such {noun2},\n{line3_b} {end1},\n{line4_b} {end2},\nWhat a sight in {name2}!",
            
            "In {place1} there lived a {noun1},\nWho {verb1} like a {adj1} {noun2},\n{line3_c} {end1},\n{line4_c} {end2},\nNow famous throughout {place2}!",
            
            "There's a {adj1} {noun1} I once knew,\nWhose {verb1} was quite something to {rhyme_ew},\n{line3_d} {end1},\n{line4_d} {end2},\nWhat else could that {noun1} do?",
            
            "A {noun1} from the town of {place1},\nHad a {adj1} and {adj2} {noun2},\n{line3_e} {end1},\n{line4_e} {end2},\nAnd that's how they conquered {place2}!",
            
            "Young {name1} was {adj1} and {adj2},\nTheir {verb1} would make people {verb2},\n{line3_f} {end1},\n{line4_f} {end2},\nSuch talent you rarely do see!"
        ]
        
        # Enhanced word banks organized by topic
        self.topic_words = {
            'cat': {
                'nouns': ['cat', 'kitten', 'feline', 'tabby', 'tom'],
                'verbs': ['purred', 'meowed', 'prowled', 'pounced', 'napped'],
                'adjectives': ['fluffy', 'sneaky', 'lazy', 'curious', 'playful'],
                'actions': ['chase mice', 'climb trees', 'knock things down', 'sleep all day']
            },
            'dog': {
                'nouns': ['dog', 'puppy', 'hound', 'mutt', 'pup'],
                'verbs': ['barked', 'wagged', 'fetched', 'dug', 'chased'],
                'adjectives': ['loyal', 'bouncy', 'friendly', 'slobbery', 'energetic'],
                'actions': ['fetch sticks', 'dig holes', 'chase squirrels', 'guard the house']
            },
            'programming': {
                'nouns': ['coder', 'programmer', 'developer', 'hacker', 'geek'],
                'verbs': ['coded', 'debugged', 'compiled', 'refactored', 'deployed'],
                'adjectives': ['clever', 'caffeinated', 'sleep-deprived', 'brilliant', 'obsessive'],
                'actions': ['fix bugs', 'write code', 'drink coffee', 'stay up late']
            },
            'coffee': {
                'nouns': ['barista', 'coffee lover', 'caffeine addict', 'bean counter', 'sipper'],
                'verbs': ['brewed', 'sipped', 'gulped', 'savored', 'chugged'],
                'adjectives': ['jittery', 'alert', 'addicted', 'energized', 'buzzing'],
                'actions': ['make lattes', 'grind beans', 'steam milk', 'pull shots']
            }
        }
        
        # Expanded rhyming word sets for more variety
        self.rhyme_sets = {
            'place_rhymes': [
                ['Maine', 'Spain', 'lane', 'brain', 'rain', 'pain', 'gain', 'plain', 'chain', 'strain'],
                ['Kent', 'went', 'sent', 'bent', 'tent', 'spent', 'lent', 'meant', 'rent', 'dent'],
                ['York', 'fork', 'cork', 'pork', 'work', 'quirk', 'smirk', 'lurk', 'clerk', 'perk'],
                ['Lee', 'sea', 'tree', 'free', 'spree', 'glee', 'key', 'bee', 'knee', 'flee'],
                ['Dale', 'tale', 'pale', 'scale', 'whale', 'trail', 'sail', 'nail', 'rail', 'hail']
            ],
            'name_rhymes': [
                ['Sue', 'Lou', 'Drew', 'Blue', 'Hugh', 'crew', 'stew', 'flew', 'grew', 'knew'],
                ['Kate', 'late', 'fate', 'gate', 'wait', 'date', 'rate', 'great', 'state', 'mate'],
                ['Bill', 'hill', 'will', 'still', 'fill', 'skill', 'thrill', 'chill', 'mill', 'drill'],
                ['Grace', 'place', 'space', 'race', 'face', 'case', 'pace', 'trace', 'base', 'chase']
            ],
            'action_rhymes': [
                ['dance', 'prance', 'chance', 'glance', 'stance', 'trance', 'lance', 'France', 'advance', 'romance'],
                ['sing', 'ring', 'wing', 'king', 'thing', 'bring', 'spring', 'sting', 'swing', 'fling'],
                ['play', 'day', 'way', 'say', 'may', 'stay', 'gray', 'bay', 'ray', 'clay'],
                ['fight', 'night', 'light', 'sight', 'right', 'bright', 'flight', 'might', 'height', 'tight'],
                ['run', 'fun', 'sun', 'done', 'won', 'gun', 'bun', 'stun', 'spun', 'begun']
            ],
            'ew_rhymes': ['view', 'new', 'few', 'crew', 'grew', 'flew', 'knew', 'threw', 'drew', 'stew']
        }
        
        # Expanded phrase collections for variety
        self.line_parts = {
            'line3_starters': ["They would", "One day they", "Each morning", "At night they", "With great joy", "So proudly", "Quite boldly", "Very quickly", "Each evening", "Most days they", "Without fail", "With a smile"],
            'line4_starters': ["And then they", "While others", "But somehow", "Despite this", "Even though", "All the while", "In the end", "To everyone's", "Much to their", "Before long", "Soon enough", "Right away"],
            'conclusions': ["What a sight to behold in", "They became quite famous in", "Now they're legend in", "Everyone talks about them in", "You can still see them in", "They're still remembered in", "People still speak of them in", "Their fame spread beyond"]
        }
        
        # More varied middle line templates
        self.middle_lines = {
            'a': ["They'd {verb} and {verb2}", "Each day they would {verb}", "With passion they'd {verb}", "So skillfully they'd {verb}"],
            'b': ["Their {noun} would {verb}", "People watched them {verb}", "Everyone saw them {verb}", "The crowd would see them {verb}"],
            'c': ["They'd {verb} with such {noun}", "Their {verb} brought great {noun}", "Each {verb} caused much {noun}", "This {verb} sparked pure {noun}"],
            'd': ["They {verb} with great {noun}", "Their {verb} was quite {adj}", "Each {verb} brought them {noun}", "This {verb} made them {adj}"],
            'e': ["They could {verb} and {verb2}", "Their talent to {verb}", "Amazing ability to {verb}", "Such skill when they'd {verb}"],
            'f': ["They'd {verb} every {noun}", "Each {noun} they would {verb}", "Their {verb} made people {verb2}", "When they'd {verb}, crowds would {verb2}"]
        }

    def generate_limerick(self, topic: str) -> str:
        """Generate a unique limerick based on the given topic."""
        topic = topic.strip().lower()
        
        # Try multiple times to get a unique combination
        for attempt in range(5):
            # Get topic-specific words or use defaults
            topic_data = self.topic_words.get(topic, self._get_default_words(topic))
            
            # Choose random template and rhyme sets
            template = random.choice(self.templates)
            rhyme_set = random.choice(self.rhyme_sets['place_rhymes'])
            action_rhymes = random.choice(self.rhyme_sets['action_rhymes'])
            name_rhymes = random.choice(self.rhyme_sets['name_rhymes'])
            
            # Create combination signature to check uniqueness
            combination = (template, tuple(rhyme_set), tuple(action_rhymes))
            
            if combination not in self.recent_combinations:
                # Build the limerick with new template system
                limerick = self._build_new_limerick(template, topic_data, rhyme_set, action_rhymes, name_rhymes)
                
                # Track this combination
                self.recent_combinations.append(combination)
                if len(self.recent_combinations) > self.max_recent:
                    self.recent_combinations.pop(0)
                
                return limerick
        
        # Fallback if we can't find unique combination
        return self._build_simple_limerick(topic_data)
    
    def get_random_topic_suggestion(self) -> str:
        """Get a random topic suggestion for the user."""
        return random.choice(self.topic_suggestions)
    
    def _get_default_words(self, topic: str) -> Dict[str, List[str]]:
        """Generate default words for unknown topics."""
        return {
            'nouns': [f'{topic} lover', 'person', 'fellow', 'character', 'individual'],
            'verbs': ['worked', 'played', 'studied', 'practiced', 'enjoyed'],
            'adjectives': ['curious', 'dedicated', 'passionate', 'clever', 'enthusiastic'],
            'actions': [f'study {topic}', f'practice {topic}', f'enjoy {topic}', f'master {topic}']
        }
    

    
    def _build_new_limerick(self, template: str, topic_data: Dict, rhyme_set: List[str], action_rhymes: List[str], name_rhymes: List[str]) -> str:
        """Build limerick using new template system."""
        # Select words for the limerick
        words = {
            'adj1': random.choice(topic_data['adjectives']),
            'adj2': random.choice(['clever', 'amazing', 'wonderful', 'peculiar', 'remarkable']),
            'noun1': random.choice(topic_data['nouns']),
            'noun2': random.choice(['grace', 'style', 'flair', 'skill', 'charm', 'wit', 'pace']),
            'verb1': random.choice(topic_data['verbs']),
            'verb2': random.choice(['laugh', 'cheer', 'stare', 'smile', 'gasp']),
            'place1': rhyme_set[0],
            'place2': rhyme_set[1],
            'name1': name_rhymes[0],
            'name2': name_rhymes[1],
            'end1': action_rhymes[0],
            'end2': action_rhymes[1],
            'rhyme_ew': random.choice(self.rhyme_sets['ew_rhymes']),
            'conclusion1': random.choice(self.line_parts['conclusions'])
        }
        
        # Add dynamic middle lines
        for key, templates in self.middle_lines.items():
            words[f'line3_{key}'] = random.choice(templates).format(
                verb=random.choice(topic_data['verbs']), 
                verb2=random.choice(['dance', 'prance', 'bounce', 'leap']),
                noun=random.choice(['joy', 'pride', 'glee', 'delight']),
                adj=random.choice(['grand', 'fine', 'bold', 'bright'])
            )
            words[f'line4_{key}'] = random.choice(templates).format(
                verb=random.choice(topic_data['verbs']),
                verb2=random.choice(['cheer', 'clap', 'watch', 'marvel']),
                noun=random.choice(['fame', 'praise', 'awe', 'wonder']),
                adj=random.choice(['proud', 'glad', 'wise', 'keen'])
            )
        
        return template.format(**words)
    
    def _build_simple_limerick(self, topic_data: Dict) -> str:
        """Fallback simple limerick builder."""
        adj = random.choice(topic_data['adjectives'])
        noun = random.choice(topic_data['nouns'])
        verb = random.choice(topic_data['verbs'])
        
        return f"""There once was a {adj} {noun} so bright,
Who {verb} from morning till night,
They'd dance and they'd play,
In their own special way,
What a truly delightful sight!"""

def main():
    """Main function with enhanced interface."""
    generator = EnhancedLimerickGenerator()
    
    print("🎭✨ Enhanced Witty Limerick Generator ✨🎭")
    print("=" * 55)
    print("🎯 I can create witty limericks about any topic you choose!")
    print("\n💡 Popular topics: cat, dog, programming, coffee, travel, music")
    print("   But feel free to try anything - I love a challenge!")
    
    while True:
        print("\n" + "─" * 50)
        print("What would you like your limerick to be about?")
        suggestion = generator.get_random_topic_suggestion()
        topic = input(f"🎯 Enter your topic (try '{suggestion}' or 'quit' to exit): ").strip()
        
        if topic.lower() in ['quit', 'exit', 'q']:
            print("\n🎉 Thanks for the laughs! Keep rhyming! 👋")
            break
        
        if not topic:
            print("❌ Please enter a valid topic!")
            continue
        
        print(f"\n📜 Here's your limerick about '{topic}':")
        print("┌" + "─" * 48 + "┐")
        limerick_lines = generator.generate_limerick(topic).split('\n')
        for line in limerick_lines:
            print(f"│ {line:<46} │")
        print("└" + "─" * 48 + "┘")
        
        # Ask if they want another
        print("\n🤔 What would you like to do next?")
        choice = input("   Press Enter for another limerick, or type 'quit' to exit: ").strip().lower()
        if choice in ['quit', 'exit', 'q']:
            print("\n🎉 Thanks for the laughs! Keep rhyming! 👋")
            break

if __name__ == "__main__":
    main()