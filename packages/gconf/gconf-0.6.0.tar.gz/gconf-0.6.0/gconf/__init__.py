import itertools

import collections
import logging
import yaml
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Union, List, Dict

from gconf.util import update

log = logging.getLogger(__name__)

_merged_dict: dict = {}

DELETED = object()  # Sentinel


def load(*configs: Union[Path, str], required=True) -> List[Path]:
	paths = [Path(config) for config in configs]

	non_existing = [p for p in paths if not p.exists()]
	if required and non_existing:
		raise FileNotFoundError(', '.join(map(str, non_existing)))

	existing = [p for p in paths if p.exists()]
	for p in existing:
		with open(p) as c:
			log.debug(f'Loading config from {p}')
			global _merged_dict
			_merged_dict = update(_merged_dict, yaml.safe_load(c))

	return existing


def load_first(*configs: Union[Path, str], required=True) -> Path:
	paths = [Path(config) for config in configs]

	for p in paths:
		if p.exists():
			if not p.is_file():
				raise FileNotFoundError(p)

			loaded = load(p, required=False)
			if loaded:
				return loaded[0]

	if required:
		raise FileNotFoundError(', '.join(map(str, paths)))


def add(dict_: dict):
	global _merged_dict
	_merged_dict = update(_merged_dict, dict_)


@contextmanager
def override_conf(dict_: dict):
	global _merged_dict
	before_dict = _merged_dict
	_merged_dict = update(deepcopy(_merged_dict), dict_)
	try:
		yield
	finally:
		_merged_dict = before_dict


def reset():
	global _merged_dict
	_merged_dict = {}


def get(*args: str, default=None):
	split_args = list(itertools.chain(*[a.split('.') for a in args]))

	try:
		try:
			result = _deep_get(split_args, _merged_dict)
		except KeyError as e:
			raise KeyError('.'.join(split_args)) from e

		if result is DELETED:
			raise KeyError('.'.join(split_args))
		else:
			return result

	except KeyError:
		if default:
			return default
		else:
			raise


def _deep_get(keys: List[str], container: Union[Dict, List]):
	if len(keys) == 0:
		return container
	elif isinstance(container, collections.Mapping):
		next_value = container[keys[0]]
	elif isinstance(container, collections.Sequence):
		i = int(keys[0])
		next_value = container[i]
	else:
		raise KeyError(keys[0])

	return _deep_get(keys[1:], next_value)
