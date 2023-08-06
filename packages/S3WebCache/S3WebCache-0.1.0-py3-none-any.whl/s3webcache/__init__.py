import requests
import boto3
from botocore.exceptions import ClientError
from time import sleep
from collections import namedtuple
from urllib.parse import urlparse, urlunparse
import posixpath
import sys
import os

S3WebCacheRequest = namedtuple('Request', ["success", "message"])


class S3WebCache(object):

    def __init__(self, bucket_name: str, path_prefix: str = None, trim_website: bool = False, allow_forwarding: bool = False):
        aws_key = os.getenv('AWS_ACCESS_KEY_ID', None)
        if not aws_key:
            raise Exception(
                'Environment variable not found: AWS_ACCESS_KEY_ID')

        aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', None)
        if not aws_secret_key:
            raise Exception(
                'Environment variable not found: AWS_SECRET_ACCESS_KEY')

        aws_default_region = os.getenv('AWS_DEFAULT_REGION', None)
        if not aws_default_region:
            raise Exception(
                'Environment variable not found: AWS_DEFAULT_REGION')

        self._s3_client = boto3.client(
            's3', aws_access_key_id=aws_key, aws_secret_access_key=aws_secret_key, region_name=aws_default_region)

        buckets = self._s3_client.list_buckets()['Buckets']

        if not any(b['Name'] == bucket_name for b in buckets):
            raise Exception("Bucket not found.")

        self.bucket = bucket_name
        self.path_prefix = path_prefix

        if self.path_prefix:
            if self.path_prefix[0] != '/':
                self.path_prefix = '/' + path_prefix

        self.bucket = bucket_name
        self.trim_website = trim_website
        self.s3_connection = boto3.resource('s3')
        self.allow_forwarding = allow_forwarding

    def get(self, _url):
        """

        :rtype: S3WebCacheRequest: (success: bool, message: str).
        """
        resolved_s3 = self.resolved_s3_from_url(_url)
        s3_request = self._get_from_s3(resolved_s3)

        if s3_request.success:
            return s3_request
        else:
            page = self._get_from_url(_url)
            if page.success:
                self._put_to_s3(resolved_s3, page.message)
                return page
            return S3WebCacheRequest(success=False, message=f"Unable to get s3 or url resource. {page.message}")

    def resolved_s3_from_url(self, _url):
        """

        :rtype: 6-tuple: (scheme, netloc, path, params, query, fragment).
        """
        _url_parsed = urlparse(_url)
        prefixed_s3_path = _url_parsed.path
        if self.path_prefix:
            prefixed_s3_path = posixpath.normpath(
                posixpath.join(self.path_prefix, '.' + _url_parsed.path))

        if not self.trim_website:
            hostname = _url_parsed.hostname.replace('.', '_')
            prefixed_s3_path = posixpath.normpath(
                posixpath.join('/' + hostname, '.' + prefixed_s3_path))

        s3_path = ('s3', self.bucket, prefixed_s3_path, '', '', '')

        return urlparse(urlunparse(s3_path))

    def _put_to_s3(self, s3_url_tuple, page_body):
        try:
            self._s3_client.put_object(
                Bucket=self.bucket, Key=s3_url_tuple.path[1:], Body=page_body.encode())
        except Exception as err:
            print(
                f"Unable to write object to {s3_url_tuple.path} in bucket: {self.bucket}. {err}", sys.stderr)

    def _get_from_s3(self, s3_url_tuple):
        try:
            page_body = self._s3_client.get_object(
                Bucket=self.bucket, Key=s3_url_tuple.path).decode()
            return S3WebCacheRequest(success=True, message=page_body)
        except ClientError as err:
            return S3WebCacheRequest(success=False, message=f"No s3 item for path: {s3_url_tuple.path}")

    def _get_from_url(self, _url):
        r = requests.get(_url, allow_redirects=self.allow_forwarding)

        attempts = 0

        while r.status_code != 200 and attempts < 3:
            try:
                r = requests.get(_url, allow_redirects=False)
            except Exception as err:
                pass
            finally:
                attempts += 1
                sleep(10 + (attempts * 10))

        if r.status_code == 200:
            return S3WebCacheRequest(success=True, message=r.text)
        elif 2 < attempts:
            return S3WebCacheRequest(success=False, message=f"FAILED after 3 attempts: {_url}")

        else:
            return S3WebCacheRequest(success=False, message=f"FAILED unknown reason: {_url}")
