"""
Shared data for the Mood Machine lab.

This file defines:
  - WordSignal: enum for word strength (WEAK, MEDIUM, STRONG)
  - POSITIVE_WORDS: map of positive words to their signal weight
  - NEGATIVE_WORDS: map of negative words to their signal weight
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

from enum import IntEnum


class WordSignal(IntEnum):
    WEAK = 5
    MEDIUM = 10
    STRONG = 15

# ---------------------------------------------------------------------
# Modifier data
# ---------------------------------------------------------------------

NEGATIONS = {"not", "never", "no", "nobody", "nothing", "neither", "nor", "hardly", "barely"}

AMPLIFIERS = {
    "very": 1.5,
    "really": 1.5,
    "extremely": 2.0,
    "absolutely": 2.0,
    "so": 1.3,
    "quite": 1.2,
    "super": 1.5,
    "fr":    1.5,
}

EMOJI_SCORES = {
    "😂": 8,
    "😊": 7,
    "😍": 9,
    "🥰": 9,
    "😄": 8,
    "😁": 7,
    "🎉": 7,
    "❤️": 8,
    "👍": 6,
    "😢": -8,
    "😭": -9,
    "😡": -9,
    "😠": -8,
    "💀": -7,
    "😤": -6,
    "🥲": -4,
    "😞": -7,
    "😔": -6,
}

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = {
    # Weak signals
    "okay":     WordSignal.WEAK,
    "fine":     WordSignal.WEAK,
    "chill":    WordSignal.WEAK,
    "hopeful":  WordSignal.WEAK,
    "relaxed":  WordSignal.WEAK,
    # Medium signals
    "happy":    WordSignal.MEDIUM,
    "great":    WordSignal.MEDIUM,
    "good":     WordSignal.MEDIUM,
    "excited":  WordSignal.MEDIUM,
    "fun":      WordSignal.MEDIUM,
    "proud":    WordSignal.MEDIUM,
    "enjoy":    WordSignal.MEDIUM,
    "grateful": WordSignal.MEDIUM,
    # Strong signals
    "love":     WordSignal.STRONG,
    "awesome":  WordSignal.STRONG,
    "amazing":  WordSignal.STRONG,
    "wonderful":WordSignal.STRONG,
    "fantastic":WordSignal.STRONG,
    "thriving": WordSignal.STRONG,
    "blessed":  WordSignal.STRONG,
    "joy":      WordSignal.STRONG,
    # Added after experimenting with sample posts
    "hit":       WordSignal.STRONG,
    "different": WordSignal.STRONG,
}

NEGATIVE_WORDS = {
    # Weak signals
    "tired":        WordSignal.WEAK,
    "boring":       WordSignal.WEAK,
    "bad":          WordSignal.WEAK,
    # Medium signals
    "sad":          WordSignal.MEDIUM,
    "angry":        WordSignal.MEDIUM,
    "upset":        WordSignal.MEDIUM,
    "stressed":     WordSignal.MEDIUM,
    "worried":      WordSignal.MEDIUM,
    "anxious":      WordSignal.MEDIUM,
    "lonely":       WordSignal.MEDIUM,
    "frustrated":   WordSignal.MEDIUM,
    "disappointed": WordSignal.MEDIUM,
    # Strong signals
    "terrible":     WordSignal.STRONG,
    "awful":        WordSignal.STRONG,
    "hate":         WordSignal.STRONG,
    "crying":       WordSignal.STRONG,
    "miserable":    WordSignal.STRONG,
    "horrible":     WordSignal.STRONG,
    "exhausted":    WordSignal.STRONG,
    "dread":        WordSignal.STRONG,
    # Added after experimenting with sample posts
}

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    # My added examples 
    "I absolutely love waiting in line for an hour 🙃",  
    "no cap this hit different fr",                      
    "I'm crying 💀💀💀",                                 
    "lowkey stressed but also kinda thriving?",          
    "today was okay I guess",     
]                       

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"

    # My added examples
    "negative",
    "mixed",
    "mixed",
    "mixed",
    "mixed",
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
