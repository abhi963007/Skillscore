import random
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

stop_words = set(stopwords.words('english'))

def generate_mcqs_with_description(text, num_questions=5):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    keywords = [w for w in words if w.isalnum() and w not in stop_words]
    keywords = list(set(keywords))

    mcqs = []

    for sentence in sentences[:num_questions]:
        sentence_words = word_tokenize(sentence)

        for word in sentence_words:
            if word.lower() in keywords and len(word) > 3:
                question = sentence.replace(word, "_____")

                options = random.sample(keywords, 3)
                if word.lower() not in options:
                    options.append(word.lower())

                random.shuffle(options)

                description = (
                    f"The correct answer is '{word}'. "
                    f"This is because the statement from the notes says: "
                    f"\"{sentence}\""
                )

                mcqs.append({
                    "question": question,
                    "options": options,
                    "answer": word,
                    "description": description
                })
                break

    return mcqs
