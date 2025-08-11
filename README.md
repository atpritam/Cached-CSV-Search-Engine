# Cached CSV Search Engine

## 🎯 Problem Overview
Efficiently process millions of CSV records to find specific data points and calculate weighted statistics, optimized for repeated queries and minimal memory usage.

## 🔧 Core Functions

### `task1(search, data)` - Single Record Search
**Purpose**: Find the first record matching all search criteria and return its 'value' field.

**Input**:
- `search`: Dictionary of column-value pairs to match (e.g., `{'a': 123, 'b': 456}`)
- `data`: Raw CSV string with millions of records

**Output**: 
- Returns the `value` field from the first matching record
- Returns `'-1'` if no match is found

**Example**:
```python
search = {'a': 938089, 'b': 213662, 'c': 979447, 'd': 164203, 'e': 4557}
result = task1(search, csv_data)  
# Returns: "866097" (the value from first matching row)
```

**Key Optimizations**:
- ✅ **LRU Caching**: Identical searches return instantly (0.0000s)
- ✅ **Streaming Processing**: Processes line-by-line without loading entire dataset
- ✅ **Header Caching**: Avoids re-parsing CSV structure on repeated calls
- ✅ **Early Termination**: Stops at first match found

---

### `task2(search_list, data)` - Weighted Average Calculator
**Purpose**: Search for multiple records and calculate their weighted average using a specific odd/even weighting scheme.

**Input**:
- `search_list`: List of search dictionaries to process
- `data`: Raw CSV string with millions of records

**Output**: 
- Weighted average as a string with 1 decimal place (e.g., `"543687.0"`)
- Returns `"0.0"` if no matches found

**Weighting Logic**:
- **Odd values**: Weight = 10
- **Even values**: Weight = 20

**Example**:
```python
search_list = [
    {'a': 938089, 'b': 213662, 'c': 979447, 'd': 164203, 'e': 4557},
    {'a': 21528, 'b': 434740, 'c': 253023, 'd': 60558, 'e': 616279}
]
result = task2(search_list, csv_data)
# Returns: "543687.0" (weighted average of found values)
```

**Calculation**:
```
Found values: [543687, 789123]  (example)
Weights: [10, 20]  (543687 is odd=10, 789123 is odd=10)
Weighted Average = (543687×10 + 789123×10) / (10 + 10) = 666405.0
```

**Key Features**:
- ✅ **Leverages task1 caching**: Each search benefits from the LRU cache
- ✅ **Skips missing records**: Ignores searches that return '-1'
- ✅ **Precise calculations**: Maintains accuracy for large numbers
- ✅ **Handles edge cases**: Returns "0.0" for no valid results

## 🏗️ Architecture Highlights

### Smart Caching System
- **Cache Size**: 1000 entries (optimal for competitive code tests)
- **Cache Key**: Sorted tuple of search criteria for consistency
- **Cache Invalidation**: Automatically detects dataset changes via hash
- **Memory Efficient**: ~230KB cache overhead regardless of dataset size

### Performance Characteristics
- **Cache Hits**: 0.0000s response time
- **Cache Misses**: 1-7s for millions of records (depends on match location)
- **Memory Usage**: <3MB additional memory regardless of dataset size
- **Scalability**: Handles datasets larger than available RAM

## 📊 Real Performance Data
```
Test Cases on 10 Million+ Record Dataset:
============================================================
Test     Result       Time (s)   Memory (MB)  Before (MB)  After (MB)
------------------------------------------------------------
Test 1   543687.0     1.6341     2.770        1379.617     1382.387    
Test 2   666172.0     4.2195     -0.082       1382.387     1382.305    
Test 3   714033.7     0.0000     0.000        1382.305     1382.305    
Test 4   543687.0     0.0000     0.000        1382.305     1382.305    
Test 5   396519.0     6.7825     0.016        1382.305     1382.320 
```

## 📊 Test Dataset
The performance benchmarks use a **400MB CSV file** with millions of records:
- **Download**: [find_match_average.dat](https://www.dropbox.com/scl/fi/zeea2tbh5n6smtkell54t/find_match_average.dat?rlkey=n19nqeholupa6ieom86j8k709&st=h0noxubv&dl=0) (400MB)
- **Format**: CSV with columns a,b,c,d,e,value
- **Size**: Multiple million records

This solution demonstrates production-ready code with intelligent caching, memory efficiency, and performance optimization for large-scale data processing tasks.