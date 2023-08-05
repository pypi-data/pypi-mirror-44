import regex as re
import pkgutil
import importlib
import os.path as op

from Stemmer import Stemmer

import tldry.stopwords as stopwords


stopwords_dirname = op.dirname(stopwords.__file__)
AVAILABLE_LANGUAGES = frozenset(
    name for _, name, _ in pkgutil.iter_modules([stopwords_dirname]))


class TextCleaner:
    word_regex = re.compile(r'[^\W\d_]+')
    sent_regex = re.compile(r'(?<=(?:[\p{lower}\p{upper}\d]|[^\w])\s*[.!?\n]+)'
                            r'\s*(?=(?:[\p{upper}\d]|[^\w]))')

    def __init__(self, language, min_sent_len):
        if language not in AVAILABLE_LANGUAGES:
            err = (f"Language '{language}' is not available, "
                   f"choose from [{', '.join(AVAILABLE_LANGUAGES)}]")
            raise ValueError(err)

        self.min_sent_len = min_sent_len

        self.stem = Stemmer(language).stemWord

        stopwords = importlib.import_module(f'tldry.stopwords.{language}')
        self.stopwords = frozenset(self.stem(w) for w in stopwords.stopwords)

        self.raw_sentences = []

    def fit_transform(self, text):
        raw_sentences_ = self.sent_tokenize(text)
        clean_sentences_ = [self.clean_sentence(self.word_tokenize(sent))
                            for sent in raw_sentences_]

        used_sentences = set()
        raw_sentences = []
        clean_sentences = []
        for c, r in zip(clean_sentences_, raw_sentences_):
            c = tuple(c)
            if len(c) < self.min_sent_len or c in used_sentences:
                continue
            clean_sentences.append(c)
            raw_sentences.append(r)
            used_sentences.add(c)

        self.raw_sentences = raw_sentences

        return clean_sentences

    def sent_tokenize(self, text):
        sentences = []
        for line in text.splitlines():
            for sent in self.sent_regex.split(line.strip()):
                if sent.endswith('?'):
                    continue
                sentences.append(sent)
        return sentences

    def word_tokenize(self, sentence):
        return self.word_regex.findall(sentence)

    def clean_sentence(self, sentence):
        new_sentence = []
        for tok in sentence:
            stem = self.stem(tok.lower())
            if len(stem) <= 2 or stem in self.stopwords:
                continue
            new_sentence.append(stem)

        return new_sentence
