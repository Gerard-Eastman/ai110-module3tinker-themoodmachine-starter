# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn


## 1. Model Overview

**Model type:**  
I used both the rule based and the machine learning model to compare. For rule based I got up to 74% accuracy on the test data and when expirementing I found that it has a hard time understanding slang. My attention mechinism was probably to weak too because it segments the expressions in chunks which can make it hard. The ml model was a perfect fit and was able to get slang correct too. 

**Intended purpose:**  
This model is trying to classify a text message as positive, negative, or mixed. But it does so in different ways. Using a rule based system and using a machine learning model to see how closely I can get to the model with rules. 74% is pretty good in my opinion.

**How it works (brief):**  
##### Rule Based Model
Base score: Starts at 50 (neutral midpoint).

Token-by-token rules (in priority order):

Negations (not, never, no, etc.) — set a negated flag that flips the effect of the next sentiment word.

Amplifiers (very, extremely, really, etc.) — multiply the amplifier multiplier (capped at 3.0), boosting the impact of the next sentiment word.

Emojis — looked up in EMOJI_SCORES and their score is added directly (resets amplifier/negation state).

Positive words — add their weighted value (from POSITIVE_WORDS dict) × amplifier. If negated, the sign is flipped (subtracts instead).

Negative words — subtract their weighted value × amplifier. If negated, the sign is flipped (adds instead).

After each sentiment word (positive, negative, or emoji), the amplifier resets to 1.0 and negated resets to False.

Label thresholds (mood_analyzer.py:152-157):

score ≥ 60 → "positive"
score ≤ 40 → "negative"
41–59 → "mixed"

##### ML Model

The ML model learns by example rather than by hand-written rules. You give it a set of labeled sentences — like "I love this" → positive, "Today was terrible" → negative — and it figures out which words tend to show up in which labels. It does this by converting each sentence into word counts (how many times each word appears), then finding weights for every word that best explain the labels it was given. Words that consistently appear in positive examples get a positive pull, and words that appear in negative examples get a negative pull. Once trained, when it sees a new sentence it applies those learned weights to predict the most likely label. The key difference from the rule-based model is that no human had to decide which words matter or how much — the model discovered that from the data itself.



## 2. Data

**Dataset description:**  
I added new samples inside sample_post based on issues I saw in the training data. If I see the model having a hard time with emojis I added more emojis. This iterative process helps me build the rules, tune senstivity, and define the rules better. 

However, in the end, a machine learning classifer that uses math to understand will always be faster in creating the weights then a human loop will. 

**Labeling process:**  
I labeled based on weaknesses. For exmaple, I saw negation to be an issue so I created a new list of negations with weight for the rules. I saw emojis can play as an amplifer so I added a new list with different levels of amplification. 

**Important characteristics of your dataset:**  
- Contains slang or emojis  
- Includes sarcasm
- Some posts express mixed feelings  
- Contains short or ambiguous messages

**Possible issues with the dataset:**  
Scarcasm is very hard to replucate using rule based algorithms. Also human entered data is very low, its much easiser to get the data from a public source to train it on. 

## 3. How the ML Model Works (if used)

**Features used:**  
Describe the representation.  
Example: “Bag of words using CountVectorizer.”

The machine learning model is using Bag of Words as apart of its vectorization. This simple process creates a dictionary of all the words it sees in the example dataset. It does not focus on the order but it can create a weight for the words using this process. 

It then creates this matrix for examples, and checks all the words in the exmaple to compute a score. Again this does not consider order of the words but often preforms better on smaller examples because of how simple it is and the ability to quickly fine tune the weight of the words based on the training dataset. 



**Training data:**  
State that the model trained on `SAMPLE_POSTS` and `TRUE_LABELS`.

**Training behavior:**  
As more data is added in, more issues are presented with the rule based model. Since everthing was hand coded, things needed to be changed because the wordly view changed as well when new examples were added in. 

With the machine learning model, it automically adjusted by being trained again through the vecrorization process which added new exmaples and tuned weights using Bag of Words. 

**Strengths and weaknesses:**  
Strenghts for ML Classifier is how quick I can expierement. Weaknesses is re-training everytime I add new scenerios and wordly views change.

## 4. Evaluation

**How you evaluated the model:**  
I just used accuracy on the training dataset to evaulate the process of learning. And I tested the trained model on my own examples afterwards for a testing. Any scenerio it failed or had a hard time with I added more of those examples in the training dataset. 

**Examples of correct predictions:**

| Example | Predicted | True | Why it worked |
|---|---|---|---|
| "I love this class so much" | positive | positive | `"love"` is a STRONG signal (+15), pushing score to 65 — well above the ≥60 threshold |
| "Today was a terrible day" | negative | negative | `"terrible"` is a STRONG negative (−15), dropping score to 35 — below the ≤40 threshold |
| "So excited for the weekend" | positive | positive | `"so"` amplified `"excited"` (1.3×), boosting a medium word enough to cross the threshold |

**Examples of incorrect predictions:**

| Example | Predicted | True | Why it failed |
|---|---|---|---|
| "I absolutely love waiting in line 🙃" | positive | negative | Sarcasm — `"absolutely"` (2x amplifier) + `"love"` (STRONG +15) scores 80. Neither model understands sarcasm. |
| "no cap this hit different fr" | negative | mixed | `"no"` triggered negation, then `"hit"` (STRONG positive) got flipped to −15. The model read "no cap" as a negation phrase instead of slang for "honestly." |
| "This is fine" | mixed | neutral | `"fine"` adds +5, landing at 55 — in the mixed zone. The rule-based model has no "neutral" class, so it can never predict what a human would naturally label this. |

**How the two models fail differently:**
- The **rule-based model** fails on slang and sarcasm because those patterns were never coded in. It's also blind to any class it wasn't given a threshold for (like "neutral").
- The **ML model** fails on sarcasm too, but for a different reason — it never saw sarcastic examples in training. It also misreads "no cap" unless that exact phrase appeared labeled as non-negation in the dataset.

## 5. Limitations

Because of the small dataset and human lableing training can be so slow. A way to fix this is using active learning. Having a script that pulls in comments or generate examples from a source and then clusters them into groups. Unlabled groups has the user go through 10-20 examples to label and it reclusters until it makes sense. That way within 30 minutes a user fully labels a giant dataset. 



## 6. Ethical Considerations

In production, you don't want to train your model with information presented by the user. You want to keep training data and production data seperate, however you want inference on things that goes wrong through evaulation, but the exmaples used to fix should be your own so you don't invade privacy. 

## 7. Ideas for Improvement
### Storage
Add more labeled data through an active learning process with the example I gave above

### Compute
Use a more advance technique that incorperates attention like current LLM models

