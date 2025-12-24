# Sybil Project Installation and Setup Guide

## Overview

This guide provides step-by-step instructions for installing and setting up the Sybil project. Sybil is a Python-based search and enumeration system that integrates with MongoDB for data storage.

---

## System Requirements

### Operating System
- **Windows 10/11** (Primary development platform)
- **Linux** (Ubuntu 18.04+ or equivalent)
- **macOS** (10.14+)

### Software Dependencies

#### Required Software
- **Python 3.7+** (Python 3.8+ recommended)
- **MongoDB 4.4+** (MongoDB 5.0+ recommended)
- **Git** (for version control)

#### Development Tools
- **VS Code** (recommended IDE)
- **PowerShell** or **Command Prompt** (Windows)
- **Terminal** (Linux/macOS)

---

## Python Environment Setup

### 1. Python Installation

#### Windows
1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Run the installer with "Add Python to PATH" checked
3. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
pip3 --version
```

#### macOS
```bash
# Using Homebrew
brew install python3
python3 --version
pip3 --version
```

### 2. Virtual Environment Setup

#### Create Virtual Environment
```bash
# Navigate to project directory
cd /path/to/Sybil

# Create virtual environment
python -m venv sybil_env

# Activate virtual environment
# Windows:
sybil_env\Scripts\activate

# Linux/macOS:
source sybil_env/bin/activate
```

#### Verify Virtual Environment
```bash
# Should show path to virtual environment Python
which python
# or on Windows:
where python
```

---

## Project Installation

### 1. Clone or Download Project

#### Option A: Clone Repository
```bash
git clone <repository-url>
cd Sybil
```

#### Option B: Download and Extract
1. Download project files
2. Extract to desired directory
3. Open terminal/command prompt in project directory

### 2. Install Dependencies

#### Install from requirements.txt
```bash
pip install -r requirements.txt
```

#### Individual Package Installation
If you encounter issues with requirements.txt, install packages individually:

```bash
# Core database dependencies
pip install pymongo==3.10.1

# Google integration
pip install google==2.0.3

# Utility libraries
pip install Unidecode==1.1.1
pip install simplejson==3.17.0
pip install certifi==2020.6.20
```

#### Verify Installation
```bash
# Check installed packages
pip list

# Test PyMongo installation
python -c "import pymongo; print('PyMongo version:', pymongo.__version__)"
```

---

## MongoDB Setup

### 1. MongoDB Installation

#### Windows
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Run installer with default settings
3. Install MongoDB as a Windows service (recommended)

#### Linux (Ubuntu)
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start and enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### macOS
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb/brew/mongodb-community
```

### 2. MongoDB Configuration

#### Create Database User
```bash
# Connect to MongoDB
mongo

# Switch to admin database
use admin

# Create admin user
db.createUser({
  user: "admin",
  pwd: "your_secure_password",
  roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
})

# Create application user
db.createUser({
  user: "sybil_user",
  pwd: "your_application_password",
  roles: [ { role: "readWrite", db: "sybil_db" } ]
})

# Exit MongoDB shell
exit
```

#### Create Application Database
```bash
# Connect as application user
mongo -u sybil_user -p your_application_password --authenticationDatabase admin

# Create application database
use sybil_db

# Verify database creation
db.getName()

# Exit MongoDB shell
exit
```

### 3. MongoDB Security Configuration

#### Enable Authentication (Production)
Edit MongoDB configuration file:

**Linux/macOS:** `/etc/mongod.conf`
**Windows:** `C:\Program Files\MongoDB\Server\5.0\bin\mongod.cfg`

```yaml
security:
  authorization: enabled

net:
  port: 27017
  bindIp: 127.0.0.1

storage:
  dbPath: /var/lib/mongodb  # Linux/macOS
  # dbPath: C:\data\db      # Windows

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log  # Linux/macOS
  # path: C:\Program Files\MongoDB\Server\5.0\log\mongod.log  # Windows

processManagement:
  fork: true  # Linux/macOS only
```

#### Restart MongoDB
```bash
# Linux/macOS
sudo systemctl restart mongod

# Windows
net stop MongoDB
net start MongoDB
```

---

## Project Configuration

### 1. Database Configuration

Create or update `components/config_db.py`:

```python
# Database configuration parameters
mongodb_host = "localhost"
mongodb_port = 27017
mongodb_dbname = "sybil_db"
mongodb_user = "sybil_user"
mongodb_pass = "your_application_password"
mongodb_admindb = "admin"
```

### 2. Environment Variables (Optional)

Create `.env` file in project root:

```env
# Database Configuration
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DBNAME=sybil_db
MONGODB_USER=sybil_user
MONGODB_PASS=your_application_password
MONGODB_ADMINDB=admin

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
```

### 3. Logging Configuration

Create `logging_config.py`:

```python
import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'sybil.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

---

## Development Environment Setup

### 1. VS Code Configuration

#### Recommended Extensions
- Python
- Python Docstring Generator
- MongoDB for VS Code
- GitLens
- Python Test Explorer

#### VS Code Settings
Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./sybil_env/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true
    }
}
```

#### Launch Configuration
Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: QueryMan",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/queryman.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

### 2. Git Configuration

#### .gitignore
Ensure `.gitignore` includes:

```gitignore
# Virtual environments
sybil_env/
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# MongoDB
*.db
*.log

# Environment variables
.env
.env.local

# IDE
.vscode/settings.json
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

#### Git Setup
```bash
# Initialize git repository (if not already done)
git init

# Add remote origin (if applicable)
git remote add origin <repository-url>

# Stage and commit files
git add .
git commit -m "Initial commit: Sybil project setup"
```

---

## Testing Installation

### 1. Database Connection Test

Create `test_connection.py`:

```python
#!/usr/bin/env python3

import sys
import os

# Add components to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'components'))

import components.config_db as config_db
from components.dbagent import db_status

def test_database_connection():
    """Test database connection and display status."""
    print("Testing database connection...")
    
    try:
        status = db_status()
        
        if status.get('connected', False):
            print("✅ Database connection successful!")
            print("Server Information:")
            for key, value in status.items():
                if key != 'connected':
                    print(f"  {key}: {value}")
        else:
            print("❌ Database connection failed!")
            print(f"Error: {status.get('error_msg', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
```

Run the test:
```bash
python test_connection.py
```

### 2. QueryMan Test

Create `test_queryman.py`:

```python
#!/usr/bin/env python3

import sys
import os

# Add components to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'components'))

import queryman

def test_queryman_functions():
    """Test QueryMan functions."""
    print("Testing QueryMan functions...")
    
    # Test status function
    print("\n1. Testing queryman_status()...")
    status = queryman.queryman_status()
    
    if status.get('ok'):
        print("✅ Status check successful!")
    else:
        print(f"❌ Status check failed: {status.get('error')}")
        return False
    
    # Test list queries function
    print("\n2. Testing queryman_list_queries()...")
    result = queryman.queryman_list_queries({})
    
    if result.get('ok'):
        print(f"✅ Query listing successful! Found {result.get('count', 0)} queries.")
    else:
        print(f"❌ Query listing failed: {result.get('error')}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_queryman_functions()
    sys.exit(0 if success else 1)
```

Run the test:
```bash
python test_queryman.py
```

---

## Troubleshooting Common Issues

### Python Issues

#### Issue: "Python command not found"
**Solution:**
- Ensure Python is installed and added to PATH
- Try `python3` instead of `python`
- Check Python installation: `python --version`

#### Issue: "pip command not found"
**Solution:**
```bash
python -m ensurepip --upgrade
python -m pip --version
```

#### Issue: Virtual environment activation fails
**Solution:**
- Ensure you're in the correct directory
- Try using full path to activation script
- Check file permissions

### MongoDB Issues

#### Issue: "Connection refused"
**Solutions:**
1. Verify MongoDB is running:
   ```bash
   # Windows
   net start MongoDB
   
   # Linux/macOS
   sudo systemctl status mongod
   ```

2. Check MongoDB port (default 27017):
   ```bash
   netstat -an | grep 27017
   ```

#### Issue: "Authentication failed"
**Solutions:**
1. Verify credentials in `config_db.py`
2. Check user exists and has correct permissions
3. Ensure authentication is enabled

#### Issue: "Database not found"
**Solutions:**
1. Create the database manually:
   ```bash
   mongo -u sybil_user -p your_password
   use sybil_db
   ```

### Dependency Issues

#### Issue: "No module named 'pymongo'"
**Solution:**
```bash
pip install pymongo==3.10.1
```

#### Issue: "Permission denied" during pip install
**Solutions:**
1. Use virtual environment
2. Install with `--user` flag: `pip install --user package_name`
3. Use admin/sudo privileges (not recommended for development)

#### Issue: Version conflicts
**Solution:**
```bash
# Uninstall conflicting packages
pip uninstall package_name

# Install specific version
pip install package_name==version_number
```

### Development Environment Issues

#### Issue: VS Code Python interpreter not found
**Solution:**
1. Open Command Palette (Ctrl+Shift+P)
2. Select "Python: Select Interpreter"
3. Choose virtual environment Python

#### Issue: Import errors
**Solutions:**
1. Add project root to Python path
2. Use relative imports correctly
3. Check `PYTHONPATH` environment variable

---

## Performance Optimization

### 1. Database Performance

#### Indexing
```bash
# Connect to MongoDB
mongo -u sybil_user -p your_password sybil_db

# Create indexes
db.queries.createIndex({ "Timestamp": -1 })
db.queries.createIndex({ "URL": 1 }, { unique: true })
db.queries.createIndex({ "Title": "text" })
```

#### Connection Pooling
Ensure MongoDB connection reuse in production.

### 2. Python Performance

#### Use virtual environment for isolation
#### Install performance monitoring tools:
```bash
pip install memory_profiler
pip install psutil
```

---

## Security Considerations

### 1. Database Security

- Use strong passwords
- Enable authentication in production
- Restrict network access to MongoDB
- Use SSL/TLS for connections

### 2. Application Security

- Store sensitive data in environment variables
- Implement input validation
- Use secure coding practices
- Regular security updates

---

## Next Steps

After successful installation:

1. **Read the API Documentation**: Review [queryman-api.md](queryman-api.md)
2. **Understand the Workflow**: Check [workflow.md](workflow.md)
3. **Explore Database Schema**: See [database-schema.md](database-schema.md)
4. **Try Usage Examples**: Follow [usage-examples.md](usage-examples.md)
5. **Read Component Integration**: Check [component-integration.md](component-integration.md)

---

## Support

For additional help:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review component integration documentation
3. Examine log files for error details
4. Test individual components in isolation

---

## Related Documentation

- [Project Overview](project-overview.md)
- [QueryMan API Reference](queryman-api.md)
- [Workflow Documentation](workflow.md)
- [Database Schema](database-schema.md)
- [Usage Examples](usage-examples.md)
- [Component Integration](component-integration.md)
- [Troubleshooting Guide](troubleshooting.md)