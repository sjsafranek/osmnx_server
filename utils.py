import hashlib

def calculateMD5ForString(string):
	""" Returns MD5 checksum for given string."""
	md5 = hashlib.md5()
	md5.update(string.encode('utf-8'))
	return md5.hexdigest()
