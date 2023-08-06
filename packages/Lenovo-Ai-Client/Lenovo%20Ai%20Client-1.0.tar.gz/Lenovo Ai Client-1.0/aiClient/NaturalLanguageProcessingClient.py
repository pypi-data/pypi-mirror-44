# -*- coding: utf-8 -*-
from aiClient.AiBaseClient import AiBase
from aiClient.utils.NLPRequestProcess import process_request_sentiment,process_request_standford
from aiClient.utils.ApiUrl import AiUrl


class NaturalLanguageProcessing(AiBase):

    """

    """
    def chinese_sentiment_analysis(self, text):
        """

        """
        data = process_request_sentiment(text)
        chinese_sentiment_analysis_url = AiUrl.chinese_sentiment_analysis
        return self._request(chinese_sentiment_analysis_url, data)

    def word_segmentation(self, text):
        """

        """
        data = process_request_standford(text)
        word_segmentation_url = AiUrl.word_segmentation
        return self._request(word_segmentation_url, data)

    def part_of_speech_tagging(self, text):
        """

        """
        data = process_request_standford(text)
        part_of_speech_tagging_url = AiUrl.part_of_speech_tagging
        return self._request(part_of_speech_tagging_url, data)

    def lemmatization(self, text):
        """

        """
        data = process_request_standford(text)
        lemmatization_url = AiUrl.lemmatization
        return self._request(lemmatization_url, data)

    def named_entity_recognition(self, text):
        """

        """
        data = process_request_standford(text)
        named_entity_recognition_url = AiUrl.named_entity_recognition
        return self._request(named_entity_recognition_url, data)

    def parsing(self, text):
        """

        """
        data = process_request_standford(text)
        parsing_url = AiUrl.parsing
        return self._request(parsing_url, data)

    def relationship_extraction(self, text):
        """

        """
        data = process_request_standford(text)
        relationship_extraction_url = AiUrl.relationship_extraction
        return self._request(relationship_extraction_url, data)

    def coreference_resolution(self, text):
        """

        """
        data = process_request_standford(text)
        coreference_resolution_url = AiUrl.conference_resolution
        return self._request(coreference_resolution_url, data)

