# -*- coding: utf-8 -*-

"""
    AipBase
"""
import json
import simplejson
import sys
import requests

requests.packages.urllib3.disable_warnings()
from aiClient.utils.ApiUrl import AiUrl


class AiBase(object):
    """
        AiBase
    """

    def __init__(self, accesskey, secretKey):
        """
            AipBase( accesskey, secretKey)
        """
        self._accessKey = accesskey.strip()
        self._secretKey = secretKey.strip()
        self._authObj = {}
        self.__client = requests
        self.__connectTimeout = 60.0
        self.__socketTimeout = 60.0
        self._proxies = {}

    def get_version(self):
        """
            version
        """
        return AiUrl.version

    def set_connection_timeout_in_millis(self, ms):
        """
            setConnectionTimeoutInMillis
        """

        self.__connectTimeout = ms / 1000.0

    def set_socket_timeout_in_millis(self, ms):
        """
            setSocketTimeoutInMillis
        """

        self.__socketTimeout = ms / 1000.0

    def set_proxies(self, proxies):
        """
            proxies
        """

        self._proxies = proxies

    def _request(self, url, data, headers=None):
        """
            self._request('', {})
        """
        try:
            result = self._validate(url, data)
            if not result:
                return result
            try:
                token = self._authObj['result']['token']
            except:
                token = self._auth()['result']['token']
            params = self._get_params()

            data = self._proccess_request(data)
            headers = self._get_headers('POST', headers)
            url = url + token
            response = self.__client.post(url, data=data, params=params,
                                          headers=headers, verify=False, timeout=(
                    self.__connectTimeout,
                    self.__socketTimeout,
                ), proxies=self._proxies
                                          )
            if sys.version_info.major == 2:
                if response.status_code == 401:
                    token = self._auth()['result']['token']
                    url = url.split("=")[0] + "=" + token
                    response = self.__client.post(url, data=data, params=params,
                                                  headers=headers, verify=False, timeout=(
                            self.__connectTimeout,
                            self.__socketTimeout,
                        ), proxies=self._proxies
                                                  )
                    obj = self._proccess_result(response.content)
                else:
                    obj = self._proccess_result(response.content)
            else:
                if response.status_code == 401:
                    token = self._auth()['result']['token']
                    url = url.split("=")[0] + "=" + token
                    response = self.__client.post(url, data=data, params=params,
                                                  headers=headers, verify=False, timeout=(
                            self.__connectTimeout,
                            self.__socketTimeout,
                        ), proxies=self._proxies
                                                  )
                    obj = self._proccess_result(response.content)
                else:
                    obj = self._proccess_result(response.content)

        except Exception as e :
            print(e)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            print(e)
            return {
                'error_msg': 'connection or read data timeout or token expired',
            }

        return obj

    def _request_get(self, url, params, headers=None):
        """
            self._request('', {})
        """
        try:

            try:
                token = self._authObj['result']['token']
            except:
                token = self._auth()['result']['token']

            headers = self._get_headers('GET', headers)
            params["token"] = token
            response = self.__client.get(url, params=params,
                                         headers=headers, verify=False, timeout=(
                    self.__connectTimeout,
                    self.__socketTimeout,
                ), proxies=self._proxies
                                         )
            obj = self._proccess_result(response.content)

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'error_msg': 'connection or read data timeout or token expired',
            }

        return obj

    def _request_post(self, url, params, data, headers=None):
        """
            self._request('', {})
        """
        try:

            try:
                token = self._authObj['result']['token']
            except:
                token = self._auth()['result']['token']

            headers = self._get_headers('POST', headers)
            params["token"] = token
            response = self.__client.post(url, params=params, data=json.dumps(data),
                                          headers=headers, verify=False, timeout=(
                    self.__connectTimeout,
                    self.__socketTimeout,
                ), proxies=self._proxies
                                          )
            obj = self._proccess_result(response.content)

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'error_msg': 'connection or read data timeout or token expired',
            }

        return obj

    def _request_put(self, url, params, data, headers=None):
        """
            self._request('', {})
        """
        try:

            try:
                token = self._authObj['result']['token']
            except:
                token = self._auth()['result']['token']

            headers = self._get_headers('POST', headers)
            params["token"] = token
            response = self.__client.put(url, params=params, data=json.dumps(data),
                                         headers=headers, verify=False, timeout=(
                    self.__connectTimeout,
                    self.__socketTimeout,
                ), proxies=self._proxies
                                         )
            obj = self._proccess_result(response.content)

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'error_msg': 'connection or read data timeout or token expired',
            }

        return obj

    def _request_delete(self, url, params, headers=None):
        """
            self._request('', {})
        """
        try:

            try:
                token = self._authObj['result']['token']
            except:
                token = self._auth()['result']['token']

            headers = self._get_headers('POST', headers)
            params["token"] = token
            response = self.__client.delete(url, params=params,
                                            headers=headers, verify=False, timeout=(
                    self.__connectTimeout,
                    self.__socketTimeout,
                ), proxies=self._proxies
                                            )
            obj = self._proccess_result(response.content)

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'error_msg': 'connection or read data timeout or token expired',
            }

        return obj

    def _request_post_file(self, url, params, files):
        """
            self._request('', {})
        """
        try:

            try:
                token = self._authObj['result']['token']
            except:
                token = self._auth()['result']['token']

            params["token"] = token
            response = self.__client.post(url, params=params, files=files,
                                          verify=False, timeout=(
                    self.__connectTimeout,
                    self.__socketTimeout,
                ), proxies=self._proxies
                                          )
            obj = self._proccess_result(response.content)

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'error_msg': 'connection or read data timeout or token expired',
            }

        return obj

    def _request_get_file(self, url, params, download_path, file_name, file_extension):
        """
            self._request('', {})
        """
        try:

            try:
                token = self._authObj['result']['token']
            except:
                token = self._auth()['result']['token']

            params["token"] = token
            response = self.__client.get(url, params=params,
                                          verify=False, timeout=(
                    self.__connectTimeout,
                    self.__socketTimeout,
                ), proxies=self._proxies
                                          )
            with open(download_path + file_name + "." + file_extension, "wb")as f :
                f.write(response.content)

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'error_msg': 'connection or read data timeout or token expired',
            }
        return "{} successfully download".format(download_path + file_name + "." + file_extension)

    def _validate(self, url, data):
        """
            validate
        """

        return True

    def _proccess_request(self, data):
        """
            参数处理
        """

        return data

    def _proccess_result(self, content):
        """
            formate result
            返回结果转字典
        """
        if sys.version_info.major == 2:

            return simplejson.loads(content) or {}
        else:
            return json.loads(content.decode()) or {}

    def _auth(self, refresh=False):
        """
            api access auth
        """

        headers = None
        headers = self._get_headers('POST', headers)
        data_dict = {
            'accesskey': self._accessKey,
            'secretkey': self._secretKey,
        }
        data = json.dumps(data_dict)
        obj = self.__client.post(AiUrl.Ai_online_auth_url,
                                 verify=False,
                                 headers=headers,
                                 data=data,
                                 timeout=(self.__connectTimeout, self.__socketTimeout,),
                                 proxies=self._proxies).json()
        self._authObj = obj

        return obj

    def _get_params(self):
        """
            api request http url params
        """

        params = {}

        return params

    def _get_headers(self, method, headers=None):
        """
            api request http headers
        """

        headers = headers or {}
        headers['Content-Type'] = 'application/json'
        headers['charset'] = 'utf8'
        headers['Accept'] = 'application/json;charset=utf-8'

        return headers
