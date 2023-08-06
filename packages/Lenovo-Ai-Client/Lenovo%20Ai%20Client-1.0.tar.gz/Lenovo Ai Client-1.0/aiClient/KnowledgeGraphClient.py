# -*- coding: utf-8 -*-
from aiClient.AiBaseClient import AiBase
from aiClient.utils.ApiUrl import AiUrl
from aiClient.utils.KgRequestProcess import process_request,process_request_movie_music


class KnowledgeGraph(AiBase):

    """
    Knowledge Graph
    """

    def relationship_extraction(self, text, confidence=0.5):
        """
        :param options: request data
        :param confidence: 置信度
        :return:Knowledge Graph
        """
        data = process_request(text, confidence)
        relationship_extraction_url = AiUrl.relationship_extraction_kg
        return self._request(relationship_extraction_url, data)

    def entity_linking(self, text, confidence=0.5):
        """
        :param options: request data
        :param confidence: 置信度
        :return:Knowledge Graph
        """
        data = process_request(text, confidence)
        entity_linking_url = AiUrl.entity_linking
        return self._request(entity_linking_url, data)

    def movie_kg(self, text):
        data = process_request_movie_music(text)
        movie_kg_url = AiUrl.movie_KG
        return self._request(movie_kg_url, data)

    def music_kg(self, text):
        data = process_request_movie_music(text)
        music_kg_url = AiUrl.music_KG
        return self._request(music_kg_url, data)