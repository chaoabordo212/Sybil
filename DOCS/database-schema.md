# Sybil Database Schema Documentation

## Overview

This document defines the database schema, operations, and configuration for the Sybil project's MongoDB integration. The database serves as the central storage system for queries, search results, and system metadata.

---

## Database Configuration

### Connection Parameters

The database configuration is managed through `components/config_db.py` and includes:

- **Host**: MongoDB server hostname
- **Port**: MongoDB server port
- **Database Name**: Primary database name
- **Authentication**: Username and password for database access
- **Admin Database**: Administrative database for authentication

### Connection String Format

```python
"mongodb://username:password@host:port/admin_database"
```

### Configuration Variables

Based on the dbagent implementation, the following configuration variables are expected:

```python
mongodb_host          # MongoDB server hostname
mongodb_port          # MongoDB server port
mongodb_dbname        # Primary database name
mongodb_user          # Database username
mongodb_pass          # Database password
mongodb_admindb       # Authentication database name
```

---

## Database Schema

### Collections Overview

The Sybil system uses MongoDB collections to store:

1. **Queries Collection**: Search queries and their metadata
2. **Results Collection**: Search results and processed data
3. **System Collection**: System configuration and status information
4. **Logs Collection**: System operation logs and audit trails

### Primary Collection: Queries

#### Document Structure

```javascript
{
  "_id": ObjectId("..."),          // MongoDB auto-generated unique identifier
  "URL": "string",                 // Query or result URL
  "Title": "string",               // Query or result title
  "Timestamp": ISODate("..."),     // Creation/modification timestamp
  "Status": "string",              // Query status (active, completed, failed)
  "Source": "string",              // Data source (google, manual, etc.)
  "Metadata": {                    // Additional metadata
    "search_terms": ["string"],    // Array of search terms
    "category": "string",          // Query category
    "tags": ["string"],            // Array of tags
    "priority": "number",          // Priority level
    "retry_count": "number"        // Number of retry attempts
  }
}
```

#### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `_id` | ObjectId | Yes | MongoDB auto-generated unique identifier |
| `URL` | String | Yes | The URL associated with the query or result |
| `Title` | String | Yes | Title or description of the query/result |
| `Timestamp` | Date | Yes | Creation or last modification timestamp |
| `Status` | String | No | Current status (default: "active") |
| `Source` | String | No | Origin of the data (default: "manual") |
| `Metadata` | Object | No | Additional structured metadata |

#### Indexes

```javascript
// Primary index on _id (automatically created)
// Compound index for common queries
db.queries.createIndex({ "Timestamp": -1, "Status": 1 })
db.queries.createIndex({ "URL": 1 }, { unique: true })
db.queries.createIndex({ "Title": "text" })
```

---

## Database Operations

### Core CRUD Operations

The database agent (`components/dbagent.py`) provides the following operations:

#### 1. Connection Management

##### `db_core()`
Establishes MongoDB connection using configuration parameters.

```python
def db_core():
    username = urllib.parse.quote_plus(mongodb_user)
    passwd = urllib.parse.quote_plus(mongodb_pass)
    connect_exp = "pymongo.MongoClient('mongodb://%s:%s@%s:%s/%s' % (username, passwd, mongodb_host, mongodb_port, mongodb_admindb), serverSelectionTimeoutMS = 2000)"
    try:
        client_connect = eval(connect_exp)
        return client_connect
    except Exception as error:
        return False, error
```

#### 2. Status Checking

##### `db_status()`
Returns database server information and connection status.

```python
def db_status():
    try:
        client_status = dict(db_core().server_info())
        connection_status = { "connected" : True }
        client_status.update(connection_status)
        return client_status
    except Exception as error:
        connection_status = { "connected" : False }
        client_status = { "error_msg":error }
        client_status.update(connection_status)
        return client_status
```

#### 3. Collection Access

##### `db_core_collection(mongodb_dbname, arg1_collection)`
Provides access to a specific collection.

```python
def db_core_collection(mongodb_dbname, arg1_collection):
    try:
        client_collection = db_core()[mongodb_dbname][arg1_collection]
        return client_collection
    except Exception as error:
        return False, error
```

#### 4. Create Operations

##### `db_insertone(arg1_collection, arg2_insertone_dict)`
Inserts a single document into a collection.

```python
def db_insertone(arg1_collection, arg2_insertone_dict):
    try:
        inserted_one = db_core_collection(mongodb_dbname, arg1_collection).insert_one(arg2_insertone_dict)
        return inserted_one.inserted_id
    except Exception as error:
        print(error)
        return "insertone_error"
```

##### `db_insertmany(arg1_collection, arg2_insertmany_dict)`
Inserts multiple documents into a collection.

```python
def db_insertmany(arg1_collection, arg2_insertmany_dict):
    try:
        inserted_many = db_core_collection(mongodb_dbname, arg1_collection).insert_many(arg2_insertmany_dict)
        return inserted_many.inserted_id
    except Exception as error:
        print(error)
        return "insertmany_error"
```

#### 5. Read Operations

##### `db_findone(arg1_collection, arg2_findone_dict)`
Finds and returns a single document.

```python
def db_findone(arg1_collection, arg2_findone_dict):
    try:
        found_one = db_core_collection(mongodb_dbname, arg1_collection).find_one(arg2_findone_dict)
        return found_one
    except Exception as error:
        print(error)
        return "findone_error"
```

##### `db_findmany(arg1_collection, arg2_findmany_dict)`
Finds and returns multiple documents as a list.

```python
def db_findmany(arg1_collection, arg2_findmany_dict):
    found_many_list = []
    try:
        found_many = db_core_collection(mongodb_dbname, arg1_collection).find(arg2_findmany_dict)
        for x in found_many:
            found_many_list.append(x)
        return found_many_list
    except Exception as error:
        print(error)
        return "findmany_error"
```

##### `db_findlast(arg1_collection, arg2_sortfield)`
Finds the most recent document based on a sort field.

```python
def db_findlast(arg1_collection, arg2_sortfield):
    try:
        found_last = db_core_collection(mongodb_dbname, arg1_collection).find().sort(arg2_sortfield, -1).limit(1)
        for x in found_last:
            return x
    except Exception as error:
        print(error)
        return "findlast_error"
```

#### 6. Update Operations

##### `db_updateone(arg1_collection, arg2_findone_dict, arg3_updateone_dict)`
Updates a single document.

```python
def db_updateone(arg1_collection, arg2_findone_dict, arg3_updateone_dict):
    try:
        updated_one = db_core_collection(mongodb_dbname, arg1_collection).update_one(arg2_findone_dict, arg3_updateone_dict)
        return updated_one
    except Exception as error:
        print(error)
        return "updateone_error"
```

##### `db_updatemany(arg1_collection, arg2_findmany_dict, arg3_updatemany_dict)`
Updates multiple documents.

```python
def db_updatemany(arg1_collection, arg2_findmany_dict, arg3_updatemany_dict):
    try:
        updated_many = db_core_collection(mongodb_dbname, arg1_collection).update_many(arg2_findmany_dict, arg3_updatemany_dict)
        return updated_many
    except Exception as error:
        print(error)
        return "updatemany_error"
```

#### 7. Delete Operations

##### `db_deleteone(arg1_collection, arg2_deleteone_dict)`
Deletes a single document.

```python
def db_deleteone(arg1_collection, arg2_deleteone_dict):
    try:
        deleted_one = db_core_collection(mongodb_dbname, arg1_collection).delete_one(arg2_deleteone_dict)
        return deleted_one
    except Exception as error:
        print(error)
        return "deleteone_error"
```

##### `db_deletemany(arg1_collection, arg2_deletemany_dict)`
Deletes multiple documents.

```python
def db_deletemany(arg1_collection, arg2_deletemany_dict):
    try:
        deleted_many = db_core_collection(mongodb_dbname, arg1_collection).delete_many(arg2_deletemany_dict)
        return deleted_many
    except Exception as error:
        print(error)
        return "deletemany_error"
```

#### 8. Index Management

##### `db_createindex(arg1_collection, arg2_indexname, arg3_field, arg4_order)`
Creates an index on a collection.

```python
def db_createindex(arg1_collection, arg2_indexname, arg3_field, arg4_order):
    try:
        index_status = {"created":True}
        index_created = { "index_name" : db_core_collection(mongodb_dbname, arg1_collection).create_index([ (arg3_field, arg4_order) ], name=arg2_indexname) }
        index_status.update(index_created)
        return index_status
    except Exception as error:
        index_status = {"created" : False}
        index_created = { "error_msg" : error }
        index_status.update(index_created)
        return index_status
```

---

## QueryMan Integration

### Query Listing Integration

The `queryman.py` module uses the database agent to list queries:

```python
def queryman_list_queries(arg1_collection_findmany_dict: Dict[str, Any]) -> Dict[str, Any]:
    """List queries from a collection using `query_list` helper."""
    try:
        cursor = query_list(arg1_collection_findmany_dict)
        results = list(cursor)
        # Process results and extract required fields
        output: List[Dict[str, Any]] = []
        for result in results:
            result_instance = {
                "_id": result.get('_id'),
                "URL": result.get('URL'),
                "Title": result.get('Title'),
                "Timestamp": result.get('Timestamp'),
            }
            output.append(result_instance)
        return {"ok": True, "count": num_queries, "results": output}
    except Exception as err:
        return {"error": "list_queries_error", "trace": list_trace}
```

---

## Database Best Practices

### Connection Management

1. **Connection Pooling**: Reuse database connections to reduce overhead
2. **Timeout Settings**: Set appropriate server selection timeout (2000ms in current implementation)
3. **Error Handling**: Always wrap database operations in try-catch blocks
4. **Connection Testing**: Regularly test connection status before operations

### Data Integrity

1. **Unique Constraints**: Ensure URL uniqueness to prevent duplicates
2. **Required Fields**: Validate required fields before insertion
3. **Data Validation**: Implement comprehensive input validation
4. **Backup Strategy**: Regular database backups and recovery procedures

### Performance Optimization

1. **Indexing Strategy**: Create indexes on frequently queried fields
2. **Query Optimization**: Use projection to limit returned fields
3. **Cursor Management**: Process large result sets using cursors
4. **Aggregation**: Use MongoDB aggregation pipeline for complex queries

### Security Considerations

1. **Authentication**: Use strong authentication credentials
2. **Connection Encryption**: Enable SSL/TLS for production environments
3. **Access Control**: Implement proper user permissions
4. **Input Sanitization**: Prevent injection attacks through input validation

---

## Example Database Operations

### Insert Query Example

```python
# Insert a new query
query_data = {
    "URL": "https://example.com",
    "Title": "Example Query",
    "Timestamp": datetime.now(),
    "Status": "active",
    "Source": "manual",
    "Metadata": {
        "search_terms": ["example", "test"],
        "category": "web_search",
        "priority": 1
    }
}

query_id = db_insertone("queries", query_data)
print(f"Inserted query with ID: {query_id}")
```

### Find Queries Example

```python
# Find all active queries
active_queries = db_findmany("queries", {"Status": "active"})

# Find queries by category
python_queries = db_findmany("queries", {"Metadata.category": "python"})

# Find recent queries (last 24 hours)
recent_time = datetime.now() - timedelta(days=1)
recent_queries = db_findmany("queries", {"Timestamp": {"$gte": recent_time}})
```

### Update Query Example

```python
# Update query status
update_result = db_updateone(
    "queries",
    {"_id": query_id},
    {"$set": {"Status": "completed", "Timestamp": datetime.now()}}
)
```

### Delete Query Example

```python
# Delete old completed queries
delete_result = db_deletemany(
    "queries",
    {"Status": "completed", "Timestamp": {"$lt": cutoff_date}}
)
```

---

## Database Maintenance

### Regular Maintenance Tasks

1. **Index Rebuilding**: Regularly rebuild fragmented indexes
2. **Data Archival**: Move old data to archival collections
3. **Connection Monitoring**: Monitor connection health and performance
4. **Backup Verification**: Regularly test backup restoration procedures

### Monitoring Queries

```python
# Count documents in collection
total_queries = db_findmany("queries", {})

# Get collection statistics
collection_stats = db_findone("admin", {"collStats": "queries"})

# Check index usage
index_stats = db_findone("admin", {"indexStats": "queries"})
```

---

## Migration and Versioning

### Schema Evolution

As the project evolves, the database schema may need to be updated:

1. **Version Tracking**: Include schema version in document metadata
2. **Migration Scripts**: Create scripts to update existing documents
3. **Backward Compatibility**: Maintain compatibility with existing code
4. **Testing**: Thoroughly test migration procedures

### Future Schema Enhancements

Potential future additions to the schema:

1. **Full-text Search**: Enhanced search capabilities
2. **Relationship Modeling**: References between documents
3. **Audit Trail**: Comprehensive operation logging
4. **Analytics Data**: Performance and usage analytics

---

## Related Documentation

- [Project Overview](project-overview.md)
- [QueryMan API Reference](queryman-api.md)
- [Workflow Documentation](workflow.md)
- [Component Integration Guide](component-integration.md)
- [Installation Guide](installation.md)
- [Usage Examples](usage-examples.md)
- [Troubleshooting Guide](troubleshooting.md)