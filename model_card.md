# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn


## 1. Model Overview

**Model type:**  
Rule-based sentiment classifier using hand-crafted rules for word scoring, negation, and sarcasm detection. Compared to a machine learning model (LogisticRegression with bag-of-words) for educational purposes.

**Intended purpose:**  
To classify short text snippets (e.g., social media posts) into mood categories: positive, negative, neutral, or mixed. The rule-based version emphasizes interpretability and manual tuning, while the ML version explores data-driven learning. Intended for educational demonstration and light analysis, not production use.

**How it works (brief):**  
##### Rule Based Model
Starts with score = 0 (neutral baseline).

Token-by-token processing:
- Negations ("not", "never") set a flag to flip the next sentiment word's polarity.
- Positive words add +1; if negated, add -1 (flip to negative).
- Negative words add -1; if negated, add +1 (flip to positive).
- Sarcasm detection: If sarcastic emoji (e.g., 🙃) present, positive words contribute -1 instead (flip for irony).
- No weights or amplifiers in current version; simple ±1 scoring.

Label mapping:
- score > 0 → "positive"
- score < 0 → "negative"
- score == 0 → "neutral"

##### ML Model

The ML model learns by example rather than by hand-written rules. You give it a set of labeled sentences — like "I love this" → positive, "Today was terrible" → negative — and it figures out which words tend to show up in which labels. It does this by converting each sentence into word counts (how many times each word appears), then finding weights for every word that best explain the labels it was given. Words that consistently appear in positive examples get a positive pull, and words that appear in negative examples get a negative pull. Once trained, when it sees a new sentence it applies those learned weights to predict the most likely label. The key difference from the rule-based model is that no human had to decide which words matter or how much — the model discovered that from the data itself.



## 2. Data

**Dataset description:**  
SAMPLE_POSTS contains 21 short text examples (originally 16, expanded by 5 to test edge cases like sarcasm, negation, and mixed emotions). TRUE_LABELS provides corresponding mood labels (positive, negative, neutral, mixed). Data was iteratively expanded based on model failures to improve coverage.

**Labeling process:**  
Labels assigned manually based on overall sentiment: positive for clear enthusiasm, negative for dissatisfaction, neutral for indifference, mixed for conflicting emotions. New examples labeled after testing model weaknesses (e.g., sarcastic posts labeled as negative despite positive words).

**Important characteristics of your dataset:**  
- Contains slang ("lit", "lowkey", "fr") and emojis (😄, 🙃, 💀).  
- Includes sarcasm and irony.  
- Some posts express mixed feelings ("stressed but thriving").  
- Contains short or ambiguous messages ("This is fine").

**Possible issues with the dataset:**  
Small size (21 examples) limits diversity; potential labeling subjectivity (e.g., "mixed" vs "neutral"); biased toward casual, youthful language; lacks formal or multilingual text.

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
Accuracy on SAMPLE_POSTS (training set) for rule-based; separate testing for ML. Iterative: Identified failures, added examples, retrained. Observed patterns in misclassifications.

**Examples of correct predictions:**

| Example | Predicted | True | Why it worked |
|---|---|---|---|
| "I love this class so much" | positive | positive | `"love"` contributes +1, score = 1 → positive |
| "Today was a terrible day" | negative | negative | `"terrible"` contributes -1, score = -1 → negative |
| "So excited for the weekend" | positive | positive | `"excited"` +1, score = 1 → positive |

**Patterns observed:**  
Strong on clear positive/negative with single sentiment words. Struggles with mixed emotions (often predicts positive/negative instead of neutral/mixed). Negation works for simple cases but misses complex irony.

**Sentences that consistently confused the model:**  
- "Not sure how I feel, it’s both good and bad" → predicted negative (true mixed); model sees "not" flipping "good" to -1, ignoring "bad" +1, net -1.  
- "lowkey stressed but also kinda thriving" → predicted mixed (true mixed); correctly neutral but could misclassify as positive if "thriving" dominates.  
- Sarcastic: "I absolutely love waiting in line 🙃" → now negative (fixed with sarcasm rule); previously positive due to "love" +1 without flip.

## 5. Limitations

**Known limitations with examples:**  
- **Sarcasm/Irony:** "I absolutely love waiting in line 🙃" was misclassified as positive (true negative) before sarcasm fix, because the model treated "love" as +1 without recognizing 🙃 as ironic. Even with the fix, it only handles specific emojis; subtle sarcasm (e.g., "Oh, great") fails.  
- **Mixed Emotions:** "Not sure how I feel, it’s both good and bad" predicted negative instead of mixed; the model nets sentiments (-1 from "not good" +1 from "bad" = 0, but logic prioritizes negation).  
- **Context and Nuance:** Short ambiguous messages like "This is fine" predicted mixed (true neutral); lacks world knowledge (e.g., meme context).  
- **Slang and Cultural References:** Handles some ("lit", "fr"), but misses evolving slang or non-English; "no cap this hit different fr" predicted mixed correctly, but similar unseen phrases may fail.  
- **Negation Complexity:** "not bad at all" works (+1), but double negatives or distant negations (e.g., "I don't think it's not good") confuse the sequential flag reset.

## 6. Ethical Considerations

**Bias and Scope:**  
The model is optimized for casual English social media with slang, emojis, and youthful tone (e.g., "lowkey", "thriving"). It may misinterpret formal/business text (e.g., "This is fine" as sarcasm) or older users' language. Scope limited to short, informal posts; not for sensitive applications like mental health analysis. Bias in dataset: Manual labeling may reflect annotator's cultural lens; small size amplifies overfitting to included styles. No multilingual support, potentially excluding non-English speakers.

## 7. ML Comparison

**Did the learned model behave differently?** Yes, ML (LogisticRegression) adapts via data, learning word patterns automatically, while rule-based requires manual coding.

**Did it fix certain failures or introduce new ones?** ML better at slang/emojis (learns from examples), potentially fixing unseen sarcasm if labeled. But introduces black-box issues (less interpretable) and sensitivity to noisy labels—mislabel one example, and weights skew.

**How sensitive was it to the labels you created?** Highly sensitive; accurate labels crucial for training. With clean labels, ML often outperforms rule-based on covered patterns but fails on out-of-scope data without retraining.

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

