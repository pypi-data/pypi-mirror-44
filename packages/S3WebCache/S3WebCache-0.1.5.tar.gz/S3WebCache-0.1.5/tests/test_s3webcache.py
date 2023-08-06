from unittest import TestCase

from s3webcache import S3WebCache

class TestCache(TestCase):
    def test_is_string(self):
        with self.assertRaises(AttributeError):
            s3wc = S3WebCache(bucket_name='myBucket')
        
