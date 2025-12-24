# Project SYBIL

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green.svg)](https://www.mongodb.com/)
[![Code Quality](https://api.codacy.com/project/badge/Grade/placeholder)](https://www.codacy.com/)

**Project SYBIL** is the next iteration of personal practical learning project SPADE, a home-brewed searching, enumerating, and crawling implementation in Python. This modular system demonstrates modern software development practices while serving as an experimental learning platform for database integration, API development, and component-based architecture.

> [!NOTE]
> This project is started by an absolute beginner experimenting in different learning approaches (read: general lack of responsibility).

## 🎯 Project Purpose

SYBIL serves as a practical demonstration of:
- **Component-Based Architecture**: Modular design with clear separation of concerns
- **Database Integration**: Robust MongoDB connectivity and operations using PyMongo
- **Search and Enumeration**: Advanced search capabilities with result management
- **Error Handling**: Comprehensive exception management and logging strategies
- **API Development**: RESTful interface design and implementation patterns

## ✨ Features

### Current Implementation ✅
- **Database Connection Management**: Robust MongoDB connection handling with status monitoring
- **Query Listing System**: Advanced query filtering, sorting, and result formatting
- **Comprehensive Error Handling**: Detailed exception management with traceback preservation
- **Modular Component Architecture**: Clean separation between database, search, and I/O operations
- **Logging Integration**: Multi-level logging for operation tracking and debugging
- **Test Framework**: Unit testing with MongoDB mocking for development

### In Development 🔄
- **Enhanced Google Search Integration**: Improved search capabilities and result processing
- **Query Management Operations**: Add, update, delete, and batch operations
- **Advanced Filtering**: Complex query filtering and result manipulation
- **Language Detection**: Experimental multilingual support integration
- **Web API Interface**: RESTful endpoints for external system integration

## 🏗️ Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Interface │────│   Query Manager │────│   Database Agent │
│   (queryman.py)  │    │  (components/)  │    │   (MongoDB)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Google Agent  │    │   IO Agent      │    │   Config DB     │
│  (Search API)   │    │ (I/O Handler)   │    │  (Settings)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components

#### 1. **Query Manager** (`queryman.py`)
- **Purpose**: Central coordinator for query operations and user interface
- **Functions**: Status checking, query listing, error handling
- **API**: Simple Python functions for database operations
- **Dependencies**: Database agent, configuration, logging

#### 2. **Database Agent** (`components/dbagent.py`)
- **Purpose**: MongoDB connection and CRUD operation management
- **Functions**: Connection handling, query execution, data manipulation
- **Technology**: PyMongo driver with custom wrapper functions
- **Operations**: insert_one/find_many/update_one/delete_one, etc.

#### 3. **Configuration Database** (`components/config_db.py`)
- **Purpose**: Centralized configuration management
- **Contains**: MongoDB connection parameters, system settings
- **Usage**: Database credentials, connection strings, operational parameters

#### 4. **Google Agent** (`components/googleagent.py`)
- **Purpose**: Google search integration and result processing
- **Status**: Limited implementation with basic search capabilities
- **Future**: Enhanced search result parsing and processing

#### 5. **IO Agent** (`components/ioagent.py`)
- **Purpose**: Input/output operations and inter-component communication
- **Functions**: Data formatting, file operations, system interactions

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **MongoDB 4.4+** (MongoDB 5.0+ recommended)
- **Git** (for version control)

### Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd Sybil
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv sybil_env
   # Windows:
   sybil_env\Scripts\activate
   # Linux/macOS:
   source sybil_env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**:
   Edit `components/config_db.py` with your MongoDB credentials:
   ```python
   mongodb_host = "localhost"
   mongodb_port = 27017
   mongodb_dbname = "sybil_db"
   mongodb_user = "your_username"
   mongodb_pass = "your_password"
   mongodb_admindb = "admin"
   ```

5. **Test installation**:
   ```bash
   python queryman.py
   ```

### Basic Usage

```python
import queryman

# Check database connection
status = queryman.queryman_status()
if status['ok']:
    print("Database connected successfully!")

# List all queries
result = queryman.queryman_list_queries({})
if result['ok']:
    print(f"Found {result['count']} queries")
    for query in result['results']:
        print(f"- {query['Title']}: {query['URL']}")
```

## 📊 Project Status

### Development Progress

#### ✅ Completed Features
- `queryman.py` - Query management interface with status checking and listing
- `components/dbagent.py` - Complete MongoDB CRUD operations implementation
- `components/config_db.py` - Database configuration management
- Comprehensive error handling and logging throughout all components
- Unit testing framework with MongoDB mocking

#### 🔄 In Development
- `components/googleagent.py` - Enhanced search integration and result processing
- `components/ioagent.py` - Input/output operations and inter-component communication
- `components/langdetect.py` - Language detection testing and integration
- Advanced query filtering and management operations

#### 📋 Planned Features
- **Graphing System**: Visual representation of user input-output workflows
- **Batch Operations**: Bulk query processing and management
- **Web API**: RESTful interface for external system integration
- **Enhanced Search**: Advanced Google search result parsing and categorization

## 📚 Documentation

### Available Documentation

- **[Project Overview](DOCS/project-overview.md)** - Comprehensive project architecture and design
- **[QueryMan API Reference](DOCS/queryman-api.md)** - Complete API documentation
- **[Installation Guide](DOCS/installation.md)** - Detailed setup and configuration instructions
- **[Workflow Documentation](DOCS/workflow.md)** - System workflows and data flow diagrams
- **[Database Schema](DOCS/database-schema.md)** - MongoDB schema design and operations
- **[Usage Examples](DOCS/usage-examples.md)** - Practical examples and tutorials

### Documentation Structure

```
DOCS/
├── project-overview.md       # High-level project architecture
├── queryman-api.md          # API reference and function documentation
├── installation.md          # Setup and installation guide
├── workflow.md              # System workflow and data flow
├── database-schema.md       # Database design and operations
├── usage-examples.md        # Practical usage examples
└── troubleshooting.md       # Common issues and solutions
```

## 🔧 Configuration

### Database Configuration

The system uses `components/config_db.py` for centralized configuration:

```python
# Database connection parameters
mongodb_host = "localhost"          # MongoDB server hostname
mongodb_port = 27017                # MongoDB server port
mongodb_dbname = "sybil_db"         # Primary database name
mongodb_user = "sybil_user"         # Database username
mongodb_pass = "your_password"      # Database password
mongodb_admindb = "admin"           # Authentication database
```

### Environment Variables (Optional)

Create `.env` file for sensitive configuration:

```env
# Database Configuration
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DBNAME=sybil_db
MONGODB_USER=sybil_user
MONGODB_PASS=your_password
MONGODB_ADMINDB=admin

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
```

## 🧪 Testing

The project includes a comprehensive testing framework:

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_dbagent.py

# Run with coverage
python -m pytest tests/ --cov=components
```

### Test Structure

```
tests/
├── test_dbagent.py           # Database agent unit tests
├── test_queryman.py          # Query manager integration tests
└── test_googleagent.py       # Google agent functionality tests
```

## 📈 Data Flow

### Primary Data Flow

```
User Input → Query Manager → Database Agent → MongoDB
     ↓           ↓              ↓            ↓
User Output ← Query Results ← Processed Data ← Stored Data
```

### Search Data Flow

```
Search String → Google Agent → Result Processing → Database Storage
      ↓              ↓              ↓              ↓
    QueryMan ← Query Management ← Data Formatting ← Query Storage
```

## 🔍 API Reference

### QueryMan Functions

#### `queryman_status()`
Checks and returns the database connection status.

**Returns:**
- Success: `{"ok": True, "status": {...}}`
- Failure: `{"error": "status_error", "trace": "..."}`

#### `queryman_list_queries(filter_dict)`
Lists queries from a collection with optional filtering.

**Parameters:**
- `filter_dict`: MongoDB find() parameters for filtering

**Returns:**
- Success: `{"ok": True, "count": N, "results": [...]}`
- Failure: `{"error": "list_queries_error", "trace": "..."}`

### Database Agent Functions

#### Core CRUD Operations
- `db_insertone(collection, document)` - Insert single document
- `db_findmany(collection, filter)` - Find multiple documents
- `db_updateone(collection, filter, update)` - Update single document
- `db_deleteone(collection, filter)` - Delete single document

## 🚨 Troubleshooting

### Common Issues

#### Database Connection Failed
1. Verify MongoDB is running: `mongod --version`
2. Check connection parameters in `config_db.py`
3. Ensure network connectivity to MongoDB server

#### Import Errors
1. Verify Python path includes project root directory
2. Check virtual environment activation
3. Ensure all dependencies are installed

#### Query Listing Returns Empty
1. Verify database contains query documents
2. Check collection name matches expected "queries"
3. Review MongoDB permissions for read access

For detailed troubleshooting, see [troubleshooting.md](DOCS/troubleshooting.md).

## 🤝 Contributing

This is a learning project, but contributions are welcome:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update documentation for API changes
- Maintain comprehensive error handling
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Learning Platform**: Inspired by hands-on software development learning
- **MongoDB Community**: For excellent NoSQL database documentation
- **Python Community**: For comprehensive libraries and tools
- **Open Source**: Built on the foundation of open source software

## 📞 Support

For questions, issues, or learning discussions:

1. **Check Documentation**: Review the comprehensive docs in `DOCS/`
2. **Review Examples**: See `DOCS/usage-examples.md` for practical examples
3. **Check Issues**: Search existing issues for similar problems
4. **Create Issue**: Provide detailed information about the problem

---

## 🔗 Related Documentation

- [Project Overview](DOCS/project-overview.md) - Complete system architecture
- [Installation Guide](DOCS/installation.md) - Step-by-step setup instructions
- [API Documentation](DOCS/queryman-api.md) - Detailed function reference
- [Usage Examples](DOCS/usage-examples.md) - Practical implementation examples
- [Workflow Documentation](DOCS/workflow.md) - System operation workflows
- [Database Schema](DOCS/database-schema.md) - Data model and operations
