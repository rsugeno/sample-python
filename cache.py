from datetime import datetime, timedelta
from logging import getLogger
from json.decode.JSONDecodeError
import json
import fcntl
import os

logger = getLogger(__name__)


class Cache:
	def __init__(self, cache_file_path):
		self._cache_file_path = cache_file_path
		self._mtime = None
		self._cache = None
		
	def _load(self, file_obj):
		mtime = os.path.getmtime(self._cache_file_path)
		if self._mtime is not None and self._cache is not None and mtime == self._mtime:
			return self._cache
		else:
			try:
				return json.load(file_obj)
			except JSONDecodeError:
				return {}

	def get(self, key):
		try:
			with open(self._cache_file_path, 'r') as file_obj:
				fcntl.flock(file_obj, fcntl.LOCK_SH)
				cache = self._load(file_obj)
		except FileNotFoundError:
			logger.info(f"キャッシュファイルが存在しませんでした: ファイル=[{self._cache_file_path}]")
			return None

		try:	
			data = cache[key]
		except KeyError:
			logger.info(f"キャッシュデータがありませんでした: key=[{key}]")
			return None

		expiration = datetime.fromisoformat(data["expiration"])
		if expiration < datetime.now():
			logger.info(f"キャッシュデータの有効期限切れです: 現在時刻=[{datetime.now().isoformat()}], 有効期限=[{data['expiration']}]")
			return None
		else:
			return data['value']

	def set(self, key: str, value: str, expiration: timedelta | datetime):
		if isinstance(expiration, timedelta):
			expiration = datetime.now() + expiration

		file_obj = None
		try:
			try:
				file_obj = open(self._cache_file_path, "x")
				fcntl.flock(file_obj, fcntl.LOCK_EX)
				cache = {}
			except FileExistsError:
				file_obj = open(self._cache_file_path, 'r+')
				fcntl.flock(file_obj, fcntl.LOCK_EX)
				cache = self._load(file_obj)
					
			cache[key] = {"value": value, "expiration": expiration.isoformat()}
			file_obj.seek(0)
			file_obj.truncate()
			json.dump(cache, file_obj, indent=4)
			file_obj.flush()
			os.fsync(file_obj.fileno())

			self._cache = cache
			self._mtime = os.path.getmtime(self._cache_file_path)
		finally:
			if file_obj is not None:
				file_obj.close()
