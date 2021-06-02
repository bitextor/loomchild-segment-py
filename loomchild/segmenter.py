#!/usr/bin/env python     

__author__ = "Marta Bañón (mbanon)"

import importlib.util
import json
import os
import sys

from toolwrapper import ToolWrapper

class LoomchildSegmenter(ToolWrapper):
    """A module for interfacing with a Java sentence segmenter. """

    def __init__(self, lang="en"):

        spec = importlib.util.find_spec('loomchild')
        target_path = os.path.join(spec.submodule_search_locations[0], "data")
        srx_path = os.path.join(target_path, "srx")

        self.lang = lang
        self.rules = self.getBestRules(lang)

        class_path = f"{target_path}/segment-2.0.2-SNAPSHOT/lib/*"
        rules_path = f"{srx_path}/{self.rules}"


        if self.rules != "DEFAULT":
            argv = ["java", "-cp", class_path, "net.loomchild.segment.ui.console.Segment", "-l", self.lang, "-s",  rules_path, "-c"]
        else:
            argv = ["java", "-cp", class_path, "net.loomchild.segment.ui.console.Segment", "-l", lang, "-c"]

        super().__init__(argv)

    def __str__(self):
        return "LoomchildSegmenter()".format()

    def __call__(self, sentence):
        assert isinstance(sentence, str)
        sentence = sentence.rstrip("\n")
        assert "\n" not in sentence
        if not sentence:
            return []
        self.writeline(sentence)

        return self.readline()

    def getBestRules(self, lang):
        # Based on benchmarks: https://docs.google.com/spreadsheets/d/1mGJ9MSyMlsK0EUDRC2J50uxApiti3ggnlrzAWn8rkMg/edit?usp=sharing

        omegaTLangs = ["bg", "cs", "sl", "sv"]
        ptdrLangs = ["el", "et", "fi", "hr", "hu", "lt", "lv"]
        nonAggressiveLangs = ["es", "it", "nb", "nn"]
        languageToolLangs = ["da", "de", "en", "fr", "nl", "pl", "pt", "ro", "sk", "sr", "uk"]

        if lang in omegaTLangs:
            return "OmegaT.srx"
        elif lang in ptdrLangs:
            return "PTDR.srx"
        elif lang in nonAggressiveLangs:
            return "NonAggressive.srx"
        elif lang in languageToolLangs:
            return "language_tools.segment.srx"
        else:
            return "DEFAULT"

    def get_segmentation(self, sentence):
        sentence_segments = json.loads(self(sentence))
        return sentence_segments

    def get_document_segmentation(self, document):
        sentences = []
        for line in document.split('\n'):
            if line == "":
                continue
            sentences.extend(self.get_segmentation(line))
        return sentences

