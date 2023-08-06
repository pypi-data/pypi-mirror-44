# -*- coding: utf-8 -*-
import json

from aiClient.AiBaseClient import AiBase
from aiClient.utils.ApiUrl import AiUrl
from aiClient.utils.VisionRequestProcess import process_request


class VisionTechnologies(AiBase):

    def face_detection(self, file_or_base64):
        """

        """
        data = process_request(file_or_base64)
        face_detection_url = AiUrl.face_detection
        return self._request(face_detection_url, data)

    def face_attribute_recognition(self, file_or_base64):
        """

        """
        data = process_request(file_or_base64)
        face_attribute_recognition_url = AiUrl.face_attributes_recognition
        return self._request(face_attribute_recognition_url, data)

    def face_comparision(self, file_or_base64One, file_or_base64Two):
        """

        """
        data_one = json.loads(process_request(file_or_base64One))
        data_two = json.loads(process_request(file_or_base64Two))
        data_dict = {
            "image1": data_one,
            "image2": data_two
        }
        data = json.dumps(data_dict)
        face_comparision_url = AiUrl.face_comparison
        return self._request(face_comparision_url, data)

    def face_segmentation(self, file_or_base64):
        """
        Photo Segmentation
        """
        data = process_request(file_or_base64)
        photo_segmentation_url = AiUrl.face_segmentation
        return self._request(photo_segmentation_url, data)

    def photo_evaluation(self, file_or_base64):
        """
        Photo Evaluation
        """
        data = process_request(file_or_base64)
        photo_evaluation_url = AiUrl.photo_evaluation
        return self._request(photo_evaluation_url, data)

    def face_identification(self, file_or_base64, groupNames, format="jpg"):
        """
        Face Identification
        """
        data = json.loads(process_request(file_or_base64))
        data_dict = {
            "base64Data": data['base64Data'],
            "format": format,
            "groupNames": groupNames,
        }
        face_identification = AiUrl.face_identification
        return self._request(face_identification, json.dumps(data_dict))

    def object_recognition(self, file_or_base64):
        """

        """
        data = process_request(file_or_base64)
        object_recognition_url = AiUrl.object_recognition
        return self._request(object_recognition_url, data)

    def scene_recognition(self, file_or_base64):
        """

        """
        data = process_request(file_or_base64)
        scene_recognition_url = AiUrl.scene_recognition
        return self._request(scene_recognition_url, data)
