# QueryMan API Documentation

## Overview

The `queryman.py` module provides query management functionality for the Sybil project. It handles database connection status checking and query listing operations, serving as an intermediary between the user interface and database operations.

## Module Information

- **File**: `queryman.py`
- **Purpose**: Query management - list, find, add, remove, start operations
- **Dependencies**: 
  - `components.config_db` - Database configuration
  - `components.dbagent` - Database agent operations
  - `components.ioagent` - Input/output operations

## Functions

### `queryman_status()`

Checks and returns the current database connection status.

#### Returns
- **Success**: `Dict[str, Any]` containing:
  - `ok`: `True`
  - `status`: Dictionary with database connection details
- **Failure**: `Dict[str, Any]` containing:
  - `error`: Error type identifier ("status_error")
  - `trace`: Full exception traceback as string

#### Usage Example
```python
import queryman

# Check database status
status = queryman.queryman_status()

if status["ok"]:
    print("Database connected:", status["status"])
else:
    print("Status check failed:", status["error"])
```

#### Logging
- **Info Level**: Logs each database status key-value pair
- **Error Level**: Logs exception details with function name

---

### `queryman_list_queries(arg1_collection_findmany_dict: Dict[str, Any]) -> Dict[str, Any]`

Lists queries from a collection using the `query_list` helper function from dbagent.

#### Parameters
- `arg1_collection_findmany_dict`: Dictionary containing MongoDB find() parameters

#### Returns
- **Success**: `Dict[str, Any]` containing:
  - `ok`: `True`
  - `count`: Number of queries found
  - `results`: List of query result dictionaries
- **Failure**: `Dict[str, Any]` containing:
  - `error`: Error type identifier ("list_queries_error")
  - `trace`: Full exception traceback as string

#### Extracted Fields
Each query result includes:
- `_id`: Document ID from MongoDB
- `URL`: Query URL
- `Title`: Query title
- `Timestamp`: Query timestamp

#### Usage Example
```python
import queryman

# List all queries
find_params = {}  # Empty dict for all documents
result = queryman.queryman_list_queries(find_params)

if result["ok"]:
    print(f"Found {result['count']} queries")
    for query in result["results"]:
        print(f"- {query['Title']}: {query['URL']}")
else:
    print("Query listing failed:", result["error"])

# List queries with specific criteria
criteria = {"Title": {"$regex": "python"}}
result = queryman.queryman_list_queries(criteria)
```

#### Logging
- **Info Level**: 
  - Number of documents found
  - Each query result as formatted dictionary
- **Debug Level**: Type information for results variable
- **Error Level**: Logs exception details with function name

---

## Planned Functions (Not Yet Implemented)

The following functions are referenced in the code but not yet implemented:

### `queryman_list_google_queries(arg1_google_doc)`
**Status**: Commented out
**Purpose**: List Google-specific queries
**Parameters**: Google document object

### `queryman_add_*` Functions
**Status**: Referenced but not implemented
**Purpose**: Add new queries to the database
**Note**: Multiple add functions planned

### `query_management_list(arg1_list_dict)`
**Status**: Commented out
**Purpose**: Alternative query listing function
**Parameters**: List configuration dictionary

---

## Error Handling

All functions implement comprehensive error handling:

1. **Try-Catch Blocks**: Capture all exceptions
2. **Traceback Logging**: Full exception details preserved
3. **Structured Error Responses**: Consistent error format
4. **Logging Integration**: Errors logged with context

### Error Response Format
```python
{
    "error": "error_type_identifier",
    "trace": "Full Python traceback string"
}
```

---

## Dependencies and Integration

### Import Dependencies
```python
import traceback
import logging
from typing import Dict, Any, List

import components.config_db as config_db
from components.dbagent import db_status, query_list
import components.ioagent as ioagent
```

### Integration Points
- **Database Agent**: Uses `db_status()` and `query_list()` functions
- **Configuration**: Accesses database configuration through `config_db`
- **IO Agent**: Ready for integration with `ioagent` for input/output operations

---

## Performance Considerations

1. **Cursor Management**: Uses MongoDB cursor which is memory-efficient for large datasets
2. **List Conversion**: Converts cursor to list for easier manipulation
3. **Field Extraction**: Only extracts required fields to minimize data transfer
4. **Logging Impact**: Uses appropriate log levels to avoid performance overhead

---

## Future Enhancements

1. **Add Query Functions**: Implement query addition functionality
2. **Remove Query Functions**: Implement query deletion
3. **Update Query Functions**: Implement query modification
4. **Google Query Integration**: Complete `queryman_list_google_queries`
5. **Batch Operations**: Support for bulk query operations
6. **Query Validation**: Add input sanitization and validation
7. **Result Filtering**: Implement query result filtering and sorting

---

## Testing Recommendations

1. **Unit Tests**: Test each function with various inputs
2. **Error Handling**: Verify error responses for different failure scenarios
3. **Database Integration**: Test with live MongoDB instance
4. **Logging Verification**: Ensure appropriate log messages are generated
5. **Performance Testing**: Test with large datasets

---

## Related Documentation

- [Database Schema Documentation](database-schema.md)
- [Component Integration Guide](component-integration.md)
- [Workflow Documentation](workflow.md)
- [Installation Guide](installation.md)