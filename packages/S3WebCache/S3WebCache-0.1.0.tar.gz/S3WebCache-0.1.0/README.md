# S3 Web Cache
This is a simple package for archiving web pages (HTML) to S3. It acts as a cache serving the S3 version of the page if it exists. If not it writes a version to s3.

## Quickstart

###Install

`pip install s3webcache`

## usage

```
from s3webcache import S3WebCache
s3wc  = S3WebCache(bucket_name='myBucket')   
html = s3wc.get("https://en.wikipedia.org/wiki/Whole_Earth_Catalog")
```