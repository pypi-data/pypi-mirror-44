# -*- coding: utf-8 -*-
from aiClient.AiBaseClient import AiBase
from aiClient.utils.VoiceRequestProcess import process_request,process_request_realtime,process_request_long_speech
from aiClient.utils.ApiUrl import AiUrl


class VoiceTechnologies(AiBase):
    """

    """
    def automatic_speech_recognition(self, file_or_base64, rate=16000):
        """
        Automatic Speech Recognition
        """
        data = process_request(file_or_base64, rate)
        automatic_speech_recognition_url = AiUrl.automatic_speech_recognition
        return self._request(automatic_speech_recognition_url, data)

    def realtime_speech_recognition(self, file_or_base64, sessionId, index=1, finished=1):
        """
        Realtime Speech Recognition
        """
        data = process_request_realtime(file_or_base64, sessionId, index, finished)

        realtime_speech_recognition_url = AiUrl.realtime_speech_recognition
        return self._request(realtime_speech_recognition_url, data)

    def long_speech_recognition(self, file_or_base64):
        """
        Long Speech Recognition
        """
        data = process_request_long_speech(file_or_base64)

        long_speech_recognition_url = AiUrl.long_speech_recognition
        return self._request(long_speech_recognition_url, data)
