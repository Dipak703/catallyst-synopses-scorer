import spacy
import re

# Load spaCy's English NER model
nlp = spacy.load("en_core_web_sm")


def anonymize_text(text):
    """
    Replaces names, dates, organizations, locations, etc. with placeholders.
    """
    doc = nlp(text)
    anonymized_text = text

    # Entity label to placeholder mapping
    label_map = {
        "PERSON": "[NAME]",
        "DATE": "[DATE]",
        "ORG": "[ORG]",
        "GPE": "[LOCATION]",
        "LOC": "[LOCATION]",
        "TIME": "[TIME]",
        "MONEY": "[MONEY]",
        "QUANTITY": "[QUANTITY]",
        "PERCENT": "[PERCENT]",
        "FAC": "[FACILITY]",
        "EVENT": "[EVENT]",
        "LANGUAGE": "[LANGUAGE]"
    }

    # Keep track of replaced spans to avoid overlapping replacements
    replacements = []

    for ent in doc.ents:
        if ent.label_ in label_map:
            replacements.append((ent.start_char, ent.end_char, label_map[ent.label_]))

    # Sort by start_char in reverse order to avoid messing up indexes
    replacements = sorted(replacements, key=lambda x: x[0], reverse=True)
    for start, end, placeholder in replacements:
        anonymized_text = anonymized_text[:start] + placeholder + anonymized_text[end:]

    return anonymized_text


if __name__ == "__main__":
    sample = "John Doe from OpenAI gave a presentation on 5th May 2025 in San Francisco."
    print("Original:", sample)
    print("Anonymized:", anonymize_text(sample))
