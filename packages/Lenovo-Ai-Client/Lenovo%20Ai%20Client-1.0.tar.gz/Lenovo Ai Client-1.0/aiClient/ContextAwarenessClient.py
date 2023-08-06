# -*- coding: utf-8 -*-

from aiClient.AiBaseClient import AiBase
from aiClient.utils.ApiUrl import AiUrl
from aiClient.utils.CaRequestProcess import process_request


class ContextAwareness(AiBase):
    """
    Context Awareness
    """

    def gender_classification(self, file_or_base64, bit=16, rate=8000, windowSize=2.56):
        """

        """
        data = process_request(file_or_base64, bit, rate, windowSize)
        ca_gender_detection_url = AiUrl.gender_classification
        return self._request(ca_gender_detection_url, data)

    def scene_classification(self, file_or_base64, bit=16, rate=8000, windowSize=2.56):
        """

        """
        data = process_request(file_or_base64, bit, rate, windowSize)
        scene_classification_url = AiUrl.scene_classification
        return self._request(scene_classification_url, data)

    def ambient_detection(self, file_or_base64, bit=16, rate=8000, windowSize=2.56):
        """

        """
        data = process_request(file_or_base64, bit, rate, windowSize)
        ambient_detection_url = AiUrl.ambient_detection
        return self._request(ambient_detection_url, data)

    def infant_crying_detection(self, file_or_base64, bit=16, rate=8000, windowSize=2.56):
        """

        """
        data = process_request(file_or_base64, bit, rate, windowSize)
        infant_crying_detection_url = AiUrl.infant_crying_detection
        return self._request(infant_crying_detection_url, data)
