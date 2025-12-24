# Sybil Project Usage Examples and Tutorials

## Overview

This document provides practical examples and step-by-step tutorials for using the Sybil project. These examples demonstrate common use cases, integration patterns, and best practices.

---

## Getting Started Examples

### Example 1: Basic Database Connection Test

```python
#!/usr/bin/env python3
"""
Basic example to test database connection and display system status.
"""

import sys
import os
import traceback

# Add components to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'components'))

import queryman

def main():
    """Main function to demonstrate basic QueryMan usage."""
    print("=== Sybil QueryMan Basic Example ===\n")
    
    # Test database connection status
    print("1. Testing Database Connection Status...")
    status = queryman.queryman_status()
    
    if status.get('ok'):
        print("✅ Database connection successful!")
        print("Server Details:")
        for key, value in status.get('status', {}).items():
            print(f"   {key}: {value}")
    else:
        print("❌ Database connection failed!")
        print(f"Error: {status.get('error')}")
        print(f"Trace: {status.get('trace')}")
        return False
    
    print("\n" + "="*50 + "\n")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)
```

### Example 2: Query Listing and Filtering

```python
#!/usr/bin/env python3
"""
Example demonstrating query listing and filtering capabilities.
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add components to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'components'))

import queryman

def list_all_queries():
    """List all queries in the database."""
    print("📋 Listing all queries...")
    
    # Empty filter to get all queries
    result = queryman.queryman_list_queries({})
    
    if result.get('ok'):
        queries = result.get('results', [])
        print(f"Found {len(queries)} queries:")
        
        for i, query in enumerate(queries, 1):
            print(f"\n{i}. {query.get('Title', 'No Title')}")
            print(f"   URL: {query.get('URL', 'No URL')}")
            print(f"   ID: {query.get('_id', 'No ID')}")
            print(f"   Timestamp: {query.get('Timestamp', 'No Timestamp')}")
        
        return queries
    else:
        print(f"❌ Failed to list queries: {result.get('error')}")
        return []

def list_recent_queries(hours=24):
    """List queries created within the specified hours."""
    print(f"\n📅 Listing queries from last {hours} hours...")
    
    # Calculate cutoff time
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    # MongoDB query for recent documents
    recent_filter = {
        "Timestamp": {
            "$gte": cutoff_time
        }
    }
    
    result = queryman.queryman_list_queries(recent_filter)
    
    if result.get('ok'):
        queries = result.get('results', [])
        print(f"Found {len(queries)} recent queries:")
        
        for query in queries:
            title = query.get('Title', 'No Title')
            timestamp = query.get('Timestamp', 'No Timestamp')
            print(f"   • {title} ({timestamp})")
        
        return queries
    else:
        print(f"❌ Failed to list recent queries: {result.get('error')}")
        return []

def search_queries_by_title(keyword):
    """Search for queries containing a specific keyword in title."""
    print(f"\n🔍 Searching queries with keyword: '{keyword}'...")
    
    # MongoDB regex search for title
    search_filter = {
        "Title": {
            "$regex": keyword,
            "$options": "i"  # Case insensitive
        }
    }
    
    result = queryman.queryman_list_queries(search_filter)
    
    if result.get('ok'):
        queries = result.get('results', [])
        print(f"Found {len(queries)} queries matching '{keyword}':")
        
        for query in queries:
            title = query.get('Title', 'No Title')
            url = query.get('URL', 'No URL')
            print(f"   • {title}")
            print(f"     URL: {url}")
        
        return queries
    else:
        print(f"❌ Search failed: {result.get('error')}")
        return []

def export_queries_to_json(queries, filename="queries_export.json"):
    """Export query results to JSON file."""
    print(f"\n💾 Exporting {len(queries)} queries to {filename}...")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(queries, f, indent=2, default=str)
        print(f"✅ Successfully exported to {filename}")
        return True
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return False

def main():
    """Main function demonstrating query operations."""
    print("=== QueryMan Query Listing Examples ===\n")
    
    # Test database connection first
    status = queryman.queryman_status()
    if not status.get('ok'):
        print("❌ Database connection failed. Cannot proceed.")
        return False
    
    print("✅ Database connection verified.\n")
    
    # Example 1: List all queries
    all_queries = list_all_queries()
    
    # Example 2: List recent queries
    recent_queries = list_recent_queries(hours=24)
    
    # Example 3: Search queries
    if all_queries:
        # Use first query title as search example
        sample_keyword = all_queries[0].get('Title', 'python').split()[0]
        search_queries_by_title(sample_keyword)
    
    # Example 4: Export results
    if all_queries:
        export_queries_to_json(all_queries)
    
    print("\n" + "="*50 + "\n")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

---

## Advanced Usage Examples

### Example 3: Database Operations with Error Handling

```python
#!/usr/bin/env python3
"""
Advanced example demonstrating comprehensive database operations with error handling.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List

# Add components to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'components'))

import components.config_db as config_db
from components.dbagent import (
    db_status, db_findmany, db_insertone, db_updateone, 
    db_deleteone, db_findone
)

class SybilDatabaseManager:
    """Enhanced database manager with comprehensive error handling."""
    
    def __init__(self):
        """Initialize the database manager."""
        self.connection_status = None
        self.last_error = None
        
    def check_connection(self) -> bool:
        """Check and store database connection status."""
        try:
            status = db_status()
            self.connection_status = status
            
            if status.get('connected', False):
                print("✅ Database connection successful")
                return True
            else:
                print(f"❌ Database connection failed: {status.get('error_msg')}")
                self.last_error = status.get('error_msg')
                return False
                
        except Exception as e:
            print(f"❌ Connection check failed: {e}")
            self.last_error = str(e)
            return False
    
    def safe_find_many(self, collection: str, filter_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Safely perform find many operation with error handling."""
        try:
            results = db_findmany(collection, filter_dict)
            
            if isinstance(results, str) and results.endswith('_error'):
                error_msg = f"Find many operation failed: {results}"
                print(f"❌ {error_msg}")
                self.last_error = error_msg
                return []
            
            print(f"✅ Found {len(results)} documents in {collection}")
            return results
            
        except Exception as e:
            error_msg = f"Exception during find many: {str(e)}"
            print(f"❌ {error_msg}")
            self.last_error = error_msg
            return []
    
    def safe_insert_one(self, collection: str, document: Dict[str, Any]) -> str:
        """Safely perform insert one operation with error handling."""
        try:
            # Add timestamp if not present
            if 'Timestamp' not in document:
                document['Timestamp'] = datetime.now()
            
            result_id = db_insertone(collection, document)
            
            if isinstance(result_id, str) and result_id.endswith('_error'):
                error_msg = f"Insert operation failed: {result_id}"
                print(f"❌ {error_msg}")
                self.last_error = error_msg
                return None
            
            print(f"✅ Successfully inserted document with ID: {result_id}")
            return result_id
            
        except Exception as e:
            error_msg = f"Exception during insert: {str(e)}"
            print(f"❌ {error_msg}")
            self.last_error = error_msg
            return None
    
    def safe_update_one(self, collection: str, filter_dict: Dict[str, Any], 
                       update_dict: Dict[str, Any]) -> bool:
        """Safely perform update one operation with error handling."""
        try:
            result = db_updateone(collection, filter_dict, update_dict)
            
            if isinstance(result, str) and result.endswith('_error'):
                error_msg = f"Update operation failed: {result}"
                print(f"❌ {error_msg}")
                self.last_error = error_msg
                return False
            
            print(f"✅ Successfully updated document(s)")
            return True
            
        except Exception as e:
            error_msg = f"Exception during update: {str(e)}"
            print(f"❌ {error_msg}")
            self.last_error = error_msg
            return False
    
    def safe_delete_one(self, collection: str, filter_dict: Dict[str, Any]) -> bool:
        """Safely perform delete one operation with error handling."""
        try:
            result = db_deleteone(collection, filter_dict)
            
            if isinstance(result, str) and result.endswith('_error'):
                error_msg = f"Delete operation failed: {result}"
                print(f"❌ {error_msg}")
                self.last_error = error_msg
                return False
            
            deleted_count = getattr(result, 'deleted_count', 0)
            print(f"✅ Successfully deleted {deleted_count} document(s)")
            return True
            
        except Exception as e:
            error_msg = f"Exception during delete: {str(e)}"
            print(f"❌ {error_msg}")
            self.last_error = error_msg
            return False
    
    def create_sample_queries(self, count: int = 5) -> List[str]:
        """Create sample query documents for testing."""
        print(f"📝 Creating {count} sample query documents...")
        
        sample_queries = [
            {
                "URL": "https://www.python.org",
                "Title": "Python Official Documentation",
                "Status": "active",
                "Source": "manual",
                "Metadata": {
                    "category": "documentation",
                    "tags": ["python", "programming"],
                    "priority": 1
                }
            },
            {
                "URL": "https://www.mongodb.com",
                "Title": "MongoDB Official Site",
                "Status": "active", 
                "Source": "manual",
                "Metadata": {
                    "category": "database",
                    "tags": ["mongodb", "nosql"],
                    "priority": 2
                }
            },
            {
                "URL": "https://pymongo.readthedocs.io",
                "Title": "PyMongo Documentation",
                "Status": "active",
                "Source": "manual", 
                "Metadata": {
                    "category": "documentation",
                    "tags": ["pymongo", "python", "mongodb"],
                    "priority": 1
                }
            }
        ]
        
        created_ids = []
        for i in range(min(count, len(sample_queries))):
            doc_id = self.safe_insert_one("queries", sample_queries[i])
            if doc_id:
                created_ids.append(doc_id)
        
        return created_ids
    
    def demonstrate_crud_operations(self):
        """Demonstrate all CRUD operations."""
        print("\n🔧 Demonstrating CRUD Operations...")
        
        # CREATE - Insert a sample document
        print("\n1. CREATE Operation:")
        sample_doc = {
            "URL": "https://example.com/sample",
            "Title": "Sample Query for CRUD Demo",
            "Status": "active",
            "Source": "demo",
            "Metadata": {
                "category": "demo",
                "tags": ["sample", "crud"],
                "priority": 3
            }
        }
        
        created_id = self.safe_insert_one("queries", sample_doc)
        
        # READ - Find the created document
        print("\n2. READ Operation:")
        if created_id:
            found_docs = self.safe_find_many("queries", {"_id": created_id})
            if found_docs:
                print(f"Found document: {found_docs[0].get('Title')}")
        
        # UPDATE - Modify the document
        print("\n3. UPDATE Operation:")
        if created_id:
            update_success = self.safe_update_one(
                "queries",
                {"_id": created_id},
                {"$set": {"Status": "updated", "Metadata.priority": 1}}
            )
            if update_success:
                print("Document updated successfully")
        
        # DELETE - Remove the document
        print("\n4. DELETE Operation:")
        if created_id:
            delete_success = self.safe_delete_one("queries", {"_id": created_id})
            if delete_success:
                print("Document deleted successfully")

def main():
    """Main function demonstrating advanced database operations."""
    print("=== Advanced Sybil Database Operations ===\n")
    
    # Initialize database manager
    db_manager = SybilDatabaseManager()
    
    # Check connection
    if not db_manager.check_connection():
        print("❌ Cannot proceed without database connection")
        return False
    
    print(f"Connection status: {db_manager.connection_status}\n")
    
    # Demonstrate safe operations
    print("🔍 Testing safe database operations...")
    
    # List existing queries
    existing_queries = db_manager.safe_find_many("queries", {})
    print(f"Current query count: {len(existing_queries)}")
    
    # Create sample queries
    sample_ids = db_manager.create_sample_queries(3)
    
    # Demonstrate CRUD operations
    db_manager.demonstrate_crud_operations()
    
    # Final query count
    final_queries = db_manager.safe_find_many("queries", {})
    print(f"\nFinal query count: {len(final_queries)}")
    
    # Report any errors
    if db_manager.last_error:
        print(f"\n⚠️  Last error encountered: {db_manager.last_error}")
    
    print("\n" + "="*50 + "\n")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

---

## Integration Examples

### Example 4: Web API Integration Pattern

```python
#!/usr/bin/env python3
"""
Example demonstrating how to integrate QueryMan with a web API framework.
This example shows a Flask-based REST API structure.
"""

from flask import Flask, jsonify, request
import sys
import os

# Add components to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'components'))

import queryman

# Initialize Flask app
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        status = queryman.queryman_status()
        return jsonify({
            'status': 'healthy' if status.get('ok') else 'unhealthy',
            'database': status.get('status', {}),
            'timestamp': status.get('timestamp', 'unknown')
        }), 200 if status.get('ok') else 503
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/queries', methods=['GET'])
def list_queries():
    """List queries endpoint with optional filtering."""
    try:
        # Get query parameters for filtering
        filter_params = {}
        
        # Title search
        title_filter = request.args.get('title')
        if title_filter:
            filter_params['Title'] = {'$regex': title_filter, '$options': 'i'}
        
        # Status filter
        status_filter = request.args.get('status')
        if status_filter:
            filter_params['Status'] = status_filter
        
        # Date range filter
        date_from = request.args.get('from')
        date_to = request.args.get('to')
        if date_from or date_to:
            filter_params['Timestamp'] = {}
            if date_from:
                filter_params['Timestamp']['$gte'] = date_from
            if date_to:
                filter_params['Timestamp']['$lte'] = date_to
        
        # Limit results
        limit = request.args.get('limit', default=100, type=int)
        
        # Perform query
        result = queryman.queryman_list_queries(filter_params)
        
        if result.get('ok'):
            queries = result.get('results', [])
            # Apply limit
            limited_queries = queries[:limit]
            
            return jsonify({
                'success': True,
                'count': len(limited_queries),
                'total_found': result.get('count', 0),
                'queries': limited_queries,
                'filters_applied': filter_params
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error'),
                'message': 'Failed to retrieve queries'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'internal_error',
            'message': str(e)
        }), 500

@app.route('/queries/count', methods=['GET'])
def count_queries():
    """Count queries endpoint."""
    try:
        # Get filters
        filter_params = {}
        
        status_filter = request.args.get('status')
        if status_filter:
            filter_params['Status'] = status_filter
        
        # Get count
        result = queryman.queryman_list_queries(filter_params)
        
        if result.get('ok'):
            return jsonify({
                'success': True,
                'count': result.get('count', 0),
                'filters_applied': filter_params
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'internal_error',
            'message': str(e)
        }), 500

@app.route('/system/status', methods=['GET'])
def system_status():
    """Get detailed system status."""
    try:
        db_status = queryman.queryman_status()
        
        return jsonify({
            'success': True,
            'system': {
                'database': db_status,
                'api_version': '1.0',
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'internal_error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("=== Sybil Web API Example ===\n")
    print("Starting Flask server on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /health           - Health check")
    print("  GET  /queries          - List queries (with filters)")
    print("  GET  /queries/count    - Count queries")
    print("  GET  /system/status    - System status")
    print("\nExample requests:")
    print("  curl http://localhost:5000/health")
    print("  curl 'http://localhost:5000/queries?status=active&limit=10'")
    print("  curl 'http://localhost:5000/queries?title=python&from=2023-01-01'")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Example 5: Batch Processing Example

```python
#!/usr/bin/env python3
"""
Example demonstrating batch processing operations for large datasets.
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any

# Add components to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'components'))

import queryman
from components.dbagent import db_findmany, db_insertmany

class BatchProcessor:
    """Batch processor for handling large datasets efficiently."""
    
    def __init__(self, batch_size: int = 100):
        """Initialize batch processor with specified batch size."""
        self.batch_size = batch_size
        self.processed_count = 0
        self.error_count = 0
        self.start_time = None
        
    def process_queries_in_batches(self, filter_dict: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process queries in batches with progress reporting."""
        if filter_dict is None:
            filter_dict = {}
        
        print(f"🔄 Starting batch processing with batch size: {self.batch_size}")
        self.start_time = time.time()
        
        try:
            # Get initial count
            count_result = queryman.queryman_list_queries(filter_dict)
            if not count_result.get('ok'):
                return {
                    'success': False,
                    'error': count_result.get('error')
                }
            
            total_count = count_result.get('count', 0)
            print(f"📊 Processing {total_count} queries in batches")
            
            processed_data = []
            
            # Process in batches using skip/limit
            skip = 0
            while skip < total_count:
                print(f"Processing batch starting at {skip}...")
                
                # Create batch filter with pagination
                batch_filter = filter_dict.copy()
                batch_filter['limit'] = self.batch_size
                batch_filter['skip'] = skip
                
                # Get batch data
                batch_result = queryman.queryman_list_queries(batch_filter)
                
                if batch_result.get('ok'):
                    batch_data = batch_result.get('results', [])
                    
                    if not batch_data:
                        print("No more data to process")
                        break
                    
                    # Process batch data
                    processed_batch = self.process_batch(batch_data)
                    processed_data.extend(processed_batch)
                    
                    self.processed_count += len(processed_batch)
                    print(f"✅ Processed {len(processed_batch)} items (Total: {self.processed_count})")
                    
                else:
                    print(f"❌ Batch processing failed: {batch_result.get('error')}")
                    self.error_count += 1
                
                skip += self.batch_size
            
            # Generate processing report
            processing_time = time.time() - self.start_time
            report = self.generate_report(total_count, processing_time)
            
            return {
                'success': True,
                'data': processed_data,
                'report': report
            }
            
        except Exception as e:
            print(f"❌ Batch processing failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'processed_count': self.processed_count,
                'error_count': self.error_count
            }
    
    def process_batch(self, batch_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a single batch of data."""
        processed = []
        
        for item in batch_data:
            try:
                # Example processing: add processing timestamp
                processed_item = item.copy()
                processed_item['ProcessedAt'] = datetime.now()
                processed_item['OriginalTimestamp'] = item.get('Timestamp')
                
                # Example processing: categorize by URL domain
                url = item.get('URL', '')
                if url:
                    domain = self.extract_domain(url)
                    processed_item['Domain'] = domain
                
                # Example processing: validate required fields
                if self.validate_item(processed_item):
                    processed.append(processed_item)
                else:
                    print(f"⚠️  Invalid item skipped: {item.get('Title', 'No Title')}")
                    
            except Exception as e:
                print(f"❌ Error processing item: {e}")
                self.error_count += 1
        
        return processed
    
    def extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return "unknown"
    
    def validate_item(self, item: Dict[str, Any]) -> bool:
        """Validate that item has required fields."""
        required_fields = ['URL', 'Title']
        return all(field in item and item[field] for field in required_fields)
    
    def generate_report(self, total_count: int, processing_time: float) -> Dict[str, Any]:
        """Generate processing report."""
        return {
            'total_items': total_count,
            'processed_items': self.processed_count,
            'error_count': self.error_count,
            'success_rate': (self.processed_count / total_count * 100) if total_count > 0 else 0,
            'processing_time_seconds': round(processing_time, 2),
            'items_per_second': round(self.processed_count / processing_time, 2) if processing_time > 0 else 0,
            'batch_size': self.batch_size
        }

def main():
    """Main function demonstrating batch processing."""
    print("=== Sybil Batch Processing Example ===\n")
    
    # Initialize batch processor
    processor = BatchProcessor(batch_size=50)
    
    # Test with different filter conditions
    test_cases = [
        {"description": "All queries", "filter": {}},
        {"description": "Active queries only", "filter": {"Status": "active"}},
        {"description": "Recent queries (last 7 days)", "filter": {
            "Timestamp": {"$gte": datetime.now() - timedelta(days=7)}
        }}
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['description']}")
        print("-" * 50)
        
        result = processor.process_queries_in_batches(test_case['filter'])
        
        if result.get('success'):
            report = result['report']
            print(f"✅ Processing completed successfully!")
            print(f"   Total items: {report['total_items']}")
            print(f"   Processed: {report['processed_items']}")
            print(f"   Errors: {report['error_count']}")
            print(f"   Success rate: {report['success_rate']:.1f}%")
            print(f"   Processing time: {report['processing_time_seconds']}s")
            print(f"   Rate: {report['items_per_second']} items/sec")
            
            # Save processed data
            if result['data']:
                filename = f"processed_data_{i}.json"
                try:
                    with open(filename, 'w') as f:
                        json.dump(result['data'], f, indent=2, default=str)
                    print(f"   💾 Data saved to {filename}")
                except Exception as e:
                    print(f"   ❌ Failed to save data: {e}")
        else:
            print(f"❌ Processing failed: {result.get('error')}")
    
    print("\n" + "="*50 + "\n")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

---

## Data Migration Examples

### Example 6: Data Import/Export

```python
#!/usr/bin/env python3
"""
Example demonstrating data import and export operations.
"""

import sys
import os
import json
import csv
from datetime import datetime
from typing import List, Dict, Any

# Add components to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'components'))

import queryman
from components.dbagent import db_insertmany

class DataManager:
    """Data import/export manager."""
    
    def __init__(self):
        """Initialize data manager."""
        self.import_count = 0
        self.export_count = 0
    
    def export_to_json(self, filename: str = "sybil_export.json") -> bool:
        """Export all queries to JSON file."""
        print(f"📤 Exporting data to {filename}...")
        
        try:
            # Get all queries
            result = queryman.queryman_list_queries({})
            
            if not result.get('ok'):
                print(f"❌ Export failed: {result.get('error')}")
                return False
            
            queries = result.get('results', [])
            
            # Prepare export data
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'total_records': len(queries),
                'queries': queries
            }
            
            # Write to file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            self.export_count = len(queries)
            print(f"✅ Successfully exported {self.export_count} queries to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def export_to_csv(self, filename: str = "sybil_export.csv") -> bool:
        """Export queries to CSV file."""
        print(f"📤 Exporting data to {filename}...")
        
        try:
            # Get all queries
            result = queryman.queryman_list_queries({})
            
            if not result.get('ok'):
                print(f"❌ Export failed: {result.get('error')}")
                return False
            
            queries = result.get('results', [])
            
            # Prepare CSV data
            if not queries:
                print("No data to export")
                return False
            
            fieldnames = ['_id', 'URL', 'Title', 'Timestamp', 'Status', 'Source']
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for query in queries:
                    # Flatten the data for CSV
                    row = {field: query.get(field, '') for field in fieldnames}
                    writer.writerow(row)
            
            self.export_count = len(queries)
            print(f"✅ Successfully exported {self.export_count} queries to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def import_from_json(self, filename: str, collection: str = "queries") -> bool:
        """Import queries from JSON file."""
        print(f"📥 Importing data from {filename}...")
        
        try:
            # Read JSON file
            with open(filename, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            queries = import_data.get('queries', [])
            
            if not queries:
                print("No queries found in import file")
                return False
            
            # Clean and prepare data for import
            cleaned_queries = []
            for query in queries:
                # Remove MongoDB ObjectId for new insertion
                clean_query = {k: v for k, v in query.items() if k != '_id'}
                
                # Add import metadata
                clean_query['ImportedAt'] = datetime.now()
                clean_query['OriginalId'] = query.get('_id')
                
                cleaned_queries.append(clean_query)
            
            # Batch insert (using individual inserts due to dbagent limitations)
            imported_count = 0
            for query in cleaned_queries:
                try:
                    # Using individual insert since dbagent doesn't support batch insert directly
                    from components.dbagent import db_insertone
                    result = db_insertone(collection, query)
                    
                    if not (isinstance(result, str) and result.endswith('_error')):
                        imported_count += 1
                    else:
                        print(f"⚠️  Failed to import query: {result}")
                        
                except Exception as e:
                    print(f"⚠️  Error importing query: {e}")
            
            self.import_count = imported_count
            print(f"✅ Successfully imported {self.import_count} queries from {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Import failed: {e}")
            return False
    
    def backup_database(self, backup_dir: str = "backups") -> bool:
        """Create a complete database backup."""
        print(f"💾 Creating database backup in {backup_dir}...")
        
        try:
            # Create backup directory
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Export to JSON
            json_file = os.path.join(backup_dir, f"backup_{timestamp}.json")
            csv_file = os.path.join(backup_dir, f"backup_{timestamp}.csv")
            
            # Create both JSON and CSV backups
            json_success = self.export_to_json(json_file)
            csv_success = self.export_to_csv(csv_file)
            
            if json_success and csv_success:
                print(f"✅ Database backup completed successfully")
                print(f"   JSON backup: {json_file}")
                print(f"   CSV backup: {csv_file}")
                return True
            else:
                print("❌ Backup completed with errors")
                return False
                
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False

def main():
    """Main function demonstrating data operations."""
    print("=== Sybil Data Import/Export Examples ===\n")
    
    data_manager = DataManager()
    
    # Test database connection first
    status = queryman.queryman_status()
    if not status.get('ok'):
        print("❌ Database connection failed. Cannot proceed.")
        return False
    
    print("✅ Database connection verified.\n")
    
    # Example 1: Export to JSON
    print("1. Exporting to JSON:")
    data_manager.export_to_json("example_export.json")
    
    # Example 2: Export to CSV
    print("\n2. Exporting to CSV:")
    data_manager.export_to_csv("example_export.csv")
    
    # Example 3: Create backup
    print("\n3. Creating backup:")
    data_manager.backup_database()
    
    # Example 4: Import (if backup file exists)
    if os.path.exists("example_export.json"):
        print("\n4. Testing import:")
        print("Creating test import file...")
        
        # Create a small test import
        test_data = {
            "queries": [
                {
                    "URL": "https://test1.com",
                    "Title": "Test Import 1",
                    "Status": "active",
                    "Source": "import_test"
                },
                {
                    "URL": "https://test2.com", 
                    "Title": "Test Import 2",
                    "Status": "active",
                    "Source": "import_test"
                }
            ]
        }
        
        test_file = "test_import.json"
        with open(test_file, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        data_manager.import_from_json(test_file)
        
        # Clean up test file
        os.remove(test_file)
    
    print("\n" + "="*50 + "\n")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

---

## Best Practices Examples

### Example 7: Error Handling and Logging

```python
#!/usr/bin/env python3
"""
Example demonstrating comprehensive error handling and logging practices.
"""

import sys
import os
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('sybil_operations.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Add components to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'components'))

import queryman

class RobustQueryManager:
    """Query manager with comprehensive error handling and logging."""
    
    def __init__(self):
        """Initialize robust query manager."""
        self.connection_retries = 3
        self.retry_delay = 1  # seconds
        self.last_error = None
        self.operation_count = 0
        self.success_count = 0
        
    def with_retry(self, operation, *args, **kwargs):
        """Execute operation with retry logic."""
        for attempt in range(self.connection_retries):
            try:
                logger.info(f"Attempting operation (attempt {attempt + 1}/{self.connection_retries})")
                result = operation(*args, **kwargs)
                self.success_count += 1
                return result
                
            except Exception as e:
                logger.warning(f"Operation failed on attempt {attempt + 1}: {e}")
                self.last_error = str(e)
                
                if attempt < self.connection_retries - 1:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Operation failed after {self.connection_retries} attempts")
                    raise
        
        return None
    
    def safe_operation(self, operation_name: str, operation_func, *args, **kwargs):
        """Execute operation with comprehensive error handling."""
        self.operation_count += 1
        
        try:
            logger.info(f"Starting {operation_name} operation")
            
            # Execute operation with retry
            result = self.with_retry(operation_func, *args, **kwargs)
            
            logger.info(f"{operation_name} completed successfully")
            return {
                'success': True,
                'result': result,
                'operation': operation_name,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"{operation_name} failed: {str(e)}"
            logger.error(error_msg)
            logger.debug(f"Full traceback: {traceback.format_exc()}")
            
            return {
                'success': False,
                'error': str(e),
                'operation': operation_name,
                'timestamp': datetime.now().isoformat(),
                'traceback': traceback.format_exc()
            }
    
    def robust_status_check(self) -> Dict[str, Any]:
        """Robust database status check with comprehensive error handling."""
        return self.safe_operation("status_check", queryman.queryman_status)
    
    def robust_query_list(self, filter_dict: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Robust query listing with comprehensive error handling."""
        if filter_dict is None:
            filter_dict = {}
        
        return self.safe_operation("query_list", queryman.queryman_list_queries, filter_dict)
    
    def get_operation_statistics(self) -> Dict[str, Any]:
        """Get operation statistics."""
        success_rate = (self.success_count / self.operation_count * 100) if self.operation_count > 0 else 0
        
        return {
            'total_operations': self.operation_count,
            'successful_operations': self.success_count,
            'success_rate': round(success_rate, 2),
            'last_error': self.last_error
        }

def demonstrate_robust_operations():
    """Demonstrate robust operation handling."""
    logger.info("Starting robust operations demonstration")
    
    # Initialize robust manager
    robust_manager = RobustQueryManager()
    
    # Test various operations
    operations = [
        ("Database Status Check", lambda: robust_manager.robust_status_check()),
        ("List All Queries", lambda: robust_manager.robust_query_list()),
        ("List Active Queries", lambda: robust_manager.robust_query_list({"Status": "active"})),
        ("Search Queries", lambda: robust_manager.robust_query_list({"Title": {"$regex": "python", "$options": "i"}}))
    ]
    
    results = []
    
    for operation_name, operation_func in operations:
        logger.info(f"\n--- Executing: {operation_name} ---")
        
        try:
            result = operation_func()
            results.append(result)
            
            if result['success']:
                logger.info(f"✅ {operation_name} completed successfully")
                if 'result' in result:
                    if isinstance(result['result'], dict):
                        if result['result'].get('ok'):
                            count = result['result'].get('count', 0)
                            logger.info(f"   Found {count} items")
                    else:
                        logger.info(f"   Result: {result['result']}")
            else:
                logger.error(f"❌ {operation_name} failed: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"❌ {operation_name} raised exception: {e}")
            results.append({
                'success': False,
                'error': str(e),
                'operation': operation_name,
                'timestamp': datetime.now().isoformat()
            })
    
    # Generate operation report
    stats = robust_manager.get_operation_statistics()
    logger.info(f"\n=== Operation Statistics ===")
    logger.info(f"Total operations: {stats['total_operations']}")
    logger.info(f"Successful operations: {stats['successful_operations']}")
    logger.info(f"Success rate: {stats['success_rate']}%")
    
    if stats['last_error']:
        logger.info(f"Last error: {stats['last_error']}")
    
    return results

def main():
    """Main function demonstrating robust error handling."""
    print("=== Sybil Robust Operations Example ===\n")
    
    try:
        results = demonstrate_robust_operations()
        
        # Summary
        successful = sum(1 for r in results if r.get('success', False))
        total = len(results)
        
        print(f"\n📊 Summary: {successful}/{total} operations successful")
        
        if successful == total:
            print("✅ All operations completed successfully!")
        else:
            print("⚠️  Some operations failed. Check logs for details.")
        
        print("\n" + "="*50 + "\n")
        return successful == total
        
    except Exception as e:
        logger.error(f"Main function failed: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)
```

---

## Running the Examples

### Prerequisites
Before running any examples, ensure:

1. **Database Setup**: MongoDB is running and accessible
2. **Dependencies**: All Python dependencies are installed
3. **Configuration**: Database credentials are properly configured
4. **Permissions**: Write permissions for log and export files

### Running Individual Examples

```bash
# Basic examples
python example_1_basic_connection.py
python example_2_query_listing.py

# Advanced examples  
python example_3_advanced_operations.py
python example_4_web_api.py
python example_5_batch_processing.py

# Data management examples
python example_6_data_migration.py
python example_7_error_handling.py
```

### Expected Outputs

Each example provides:
- ✅ **Success indicators** for completed operations
- ❌ **Error messages** with detailed information
- 📊 **Statistics** and performance metrics
- 💾 **File outputs** where applicable
- 📝 **Log files** for detailed operation history

### Common Output Patterns

```bash
=== Sybil QueryMan Basic Example ===

1. Testing Database Connection Status...
✅ Database connection successful!
Server Details:
   version: 5.0.0
   gitVersion: ...
   connected: True

==================================================
```

---

## Troubleshooting Examples

### Common Issues and Solutions

#### Issue 1: Connection Timeout
```python
# Solution: Implement retry logic with exponential backoff
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator

@retry_on_failure(max_retries=3, delay=1)
def robust_database_operation():
    return queryman.queryman_status()
```

#### Issue 2: Large Dataset Handling
```python
# Solution: Use cursor-based processing with batching
def process_large_dataset(filter_dict, batch_size=1000):
    skip = 0
    total_processed = 0
    
    while True:
        batch_filter = filter_dict.copy()
        batch_filter['skip'] = skip
        batch_filter['limit'] = batch_size
        
        result = queryman.queryman_list_queries(batch_filter)
        
        if not result.get('ok') or not result.get('results'):
            break
        
        # Process batch
        process_batch(result['results'])
        
        total_processed += len(result['results'])
        skip += batch_size
        
        if len(result['results']) < batch_size:
            break
    
    return total_processed
```

#### Issue 3: Memory Management
```python
# Solution: Process data incrementally without loading everything into memory
def stream_process_queries(filter_dict):
    """Process queries one at a time to minimize memory usage."""
    batch_size = 100
    skip = 0
    
    while True:
        # Get small batch
        batch_filter = filter_dict.copy()
        batch_filter['skip'] = skip
        batch_filter['limit'] = batch_size
        
        result = queryman.queryman_list_queries(batch_filter)
        
        if not result.get('ok') or not result.get('results'):
            break
        
        # Process each query individually
        for query in result['results']:
            process_single_query(query)
        
        # Clear batch from memory
        del result['results']
        
        if len(result.get('results', [])) < batch_size:
            break
        
        skip += batch_size
```

---

## Performance Optimization Examples

### Example 8: Optimized Query Patterns

```python
def optimized_query_examples():
    """Examples of optimized query patterns."""
    
    # 1. Use projection to limit returned fields
    print("1. Using projection to limit fields...")
    result = queryman.queryman_list_queries({
        # Projection: only return specific fields
        "fields": {"URL": 1, "Title": 1, "Timestamp": 1}
    })
    
    # 2. Use indexes for faster filtering
    print("2. Using indexed fields for filtering...")
    result = queryman.queryman_list_queries({
        "Timestamp": {"$gte": datetime.now() - timedelta(days=7)}
        # This uses the Timestamp index for fast lookups
    })
    
    # 3. Use text search instead of regex when possible
    print("3. Using text search for better performance...")
    result = queryman.queryman_list_queries({
        "$text": {"$search": "python programming"}
        # Requires text index on Title field
    })
```

---

## Related Documentation

- [Project Overview](project-overview.md)
- [QueryMan API Reference](queryman-api.md)
- [Workflow Documentation](workflow.md)
- [Database Schema](database-schema.md)
- [Installation Guide](installation.md)
- [Component Integration](component-integration.md)
- [Troubleshooting Guide](troubleshooting.md)