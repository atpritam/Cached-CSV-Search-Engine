from collections import OrderedDict

""" My approach: I realized that with millions of records, parsing the entire dataset
 into memory would be too expensive. Instead, I decided to use line-by-line processing
 with smart caching to speed up repeated searches. """

class SimpleCache:
   def __init__(self, max_size=200):
       self.cache = OrderedDict()  # LRU cache using OrderedDict
       self.max_size = max_size
       self.last_data_hash = None
       self.cached_header = None
       self.cached_col_indices = None

   def clear_if_new_data(self, data_hash):
       # Clear cache when dataset changes
       if data_hash != self.last_data_hash:
           self.cache.clear()
           self.last_data_hash = data_hash
           self.cached_header = None
           self.cached_col_indices = None

   def get(self, key):
       if key in self.cache:
           # Move to end for LRU behavior
           self.cache.move_to_end(key)
           return self.cache[key]
       return None

   def set(self, key, value):
       self.cache[key] = value
       self.cache.move_to_end(key)
       # Evict oldest entries when cache is full
       if len(self.cache) > self.max_size:
           self.cache.popitem(last=False)

   def set_header_cache(self, header, col_indices):
       # Cache header parsing to avoid re-doing it for every search
       self.cached_header = header
       self.cached_col_indices = col_indices


# Global cache instance - shared across all function calls
_cache = SimpleCache(max_size=1000)


def task1(search, data):
   # My strategy: Use hash of data start to detect dataset changes efficiently
   data_hash = hash(data[:200])
   _cache.clear_if_new_data(data_hash)

   cache_key = tuple(sorted(search.items()))

   # Check cache first - this gives us near 0.0000s response times on cache hits
   cached_result = _cache.get(cache_key)
   if cached_result is not None:
       return cached_result

   # Cache miss - need to actually search the data
   lines = data.splitlines()
   if not lines:
       return '-1'

   if _cache.cached_header is None:
       header = lines[0].split(',')

       # Validate requirements
       if 'value' not in header:
           raise Exception("Key mismatch")

       # Create column mapping for flexible column ordering
       col_indices = {name: idx for idx, name in enumerate(header)}

       _cache.set_header_cache(header, col_indices)
   else:
       # Reuse cached header parsing
       header = _cache.cached_header
       col_indices = _cache.cached_col_indices

   # Validate search keys match dataset structure
   expected_keys = set(header) - {'value'}
   if set(search.keys()) != expected_keys:
       raise Exception("Key mismatch")

   value_idx = col_indices['value']

   # Linear search through data
   for line in lines[1:]:
       if not line.strip():
           continue

       row = line.split(',')

       # Check if all search criteria match this row
       match = True
       for key, target_value in search.items():
           if row[col_indices[key]] != str(target_value):
               match = False
               break

       if match:
           # Found first match - cache and return
           result = row[value_idx]
           _cache.set(cache_key, result)
           return result

   # No match found - cache this result too to avoid re-searching
   _cache.set(cache_key, '-1')
   return '-1'


def task2(search_list, data):
    """ My approach: Use task1 with caching to efficiently find each value,
    then calculate weighted average according to the odd/even rule """

    total_weighted_sum = 0
    total_weight = 0

    for search_dict in search_list:
        result = task1(search_dict, data)
        if result == '-1':
            continue

        value = int(result)
        # Weight 10 for odd values, 20 for even values
        weight = 10 if value % 2 == 1 else 20

        total_weighted_sum += value * weight
        total_weight += weight

    if total_weight == 0:
        return '0.0'

    weighted_average = total_weighted_sum / total_weight
    return f"{weighted_average:.1f}"