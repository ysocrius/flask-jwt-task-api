# Error Solutions Log

This document tracks all errors encountered during development with their solutions.

---

## Error #1: Windows PowerShell mkdir Command Failure

**Date**: 2026-02-05
**Phase**: Setup
**Severity**: Low

**Error Message**:
```
mkdir : A positional parameter cannot be found that accepts argument 'plans'.
At line:1 char:1
+ mkdir -p rules plans docs src/backend src/frontend submission demo
```

**Context**:
Trying to create multiple directories at once using Unix-style `mkdir -p` command in Windows PowerShell.

**Root Cause**:
PowerShell's `mkdir` is an alias for `New-Item` and doesn't support the `-p` flag or multiple directory arguments like Unix `mkdir`.

**Solution**:
Used PowerShell-native command:
```powershell
# Before (Unix style - FAILED)
mkdir -p rules plans docs src/backend src/frontend

# After (PowerShell style - SUCCESS)
New-Item -ItemType Directory -Force -Path rules, plans, docs, src\backend, src\frontend
```

**Prevention**:
Always use PowerShell-native commands on Windows or create cross-platform scripts.

**Learning**:
Cross-platform compatibility matters. Document platform-specific commands in README.

---

## Error #2: Python Relative Import Error

**Date**: 2026-02-05
**Phase**: Development
**Severity**: High

**Error Message**:
```
Traceback (most recent call last):
  File "src\backend\app.py", line 6, in <module>
    from .config import get_config
ImportError: attempted relative import with no known parent package
```

**Context**:
Running Flask app directly with `python src\backend\app.py` after implementing relative imports.

**Root Cause**:
Python treats `app.py` as a top-level script when run directly, not as part of a package. Relative imports (`.config`) only work when the module is imported as part of a package.

**Solution**:
1. Created `run.py` at project root:
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'backend'))
from app import create_app
```

2. Converted all relative imports to absolute:
```python
# Before
from .config import get_config
from ..models import db

# After
from config import get_config
from models import db
```

**Prevention**:
- Use absolute imports for Flask apps not packaged as installable modules
- Create dedicated run script from project start
- Add `src/backend` to PYTHONPATH in development

**Learning**:
Understand Python's import system. Relative imports require package context. For Flask apps, absolute imports or proper package structure with `__init__.py` files.

---

## Error #3: PostgreSQL Connection Failed

**Date**: 2026-02-05
**Phase**: Testing
**Severity**: Medium

**Error Message**:
```
connection to server at "localhost" (::1), port 5432 failed: 
FATAL: password authentication failed for user "username"
```

**Context**:
Attempting to run Flask app with `.env` file containing PostgreSQL connection string.

**Root Cause**:
`.env.example` had PostgreSQL URL as default, but PostgreSQL wasn't installed/configured on development machine.

**Solution**:
Switched to SQLite for development:
```bash
# In .env
# Before
DATABASE_URL=postgresql://username:password@localhost:5432/primetrade_db

# After
DATABASE_URL=sqlite:///primetrade.db
```

**Prevention**:
- Use SQLite as default in `.env.example` for easier onboarding
- Document PostgreSQL setup as optional in README
- Add database choice to QUICKSTART guide

**Learning**:
Minimize setup friction. SQLite requires zero configuration, perfect for development and demos.

---

## Error #4: localStorage.setItem Missing Parameter

**Date**: 2026-02-05
**Phase**: Development
**Severity**: High

**Error Message**:
```javascript
// Silent failure - token not stored in localStorage
// No console error, but authentication fails
```

**Context**:
Implementing JWT token storage in frontend `api.js`. User registration/login appeared to work but subsequent authenticated requests failed with 401 errors.

**Root Cause**:
Typo in `setToken()` function - missing the `token` parameter in `localStorage.setItem()` call:
```javascript
function setToken(token) {
    localStorage.setItem('token');  // BUG: missing token value
}
```

**Solution**:
Added missing token parameter:
```javascript
// Before (BROKEN)
function setToken(token) {
    localStorage.setItem('token');  // Only sets key, no value
}

// After (FIXED)
function setToken(token) {
    localStorage.setItem('token', token);  // Correctly stores key-value pair
}
```

**Prevention**:
- Use TypeScript for type safety
- Add unit tests for localStorage operations
- Test authentication flow end-to-end immediately after implementation
- Use browser DevTools to verify localStorage contents

**Learning**:
Silent failures are dangerous. Always verify data persistence operations (localStorage, database writes) immediately after implementation. This bug would have been caught instantly with a simple console.log or DevTools inspection.

---

## Error #5: Flask .env Changes Not Reloading

**Date**: 2026-02-05
**Phase**: Testing
**Severity**: Medium

**Error Message**:
```
Access to fetch at 'http://localhost:5000/api/v1/auth/register' from origin 'http://localhost:8080' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

**Context**:
Added `http://localhost:8080` to `ALLOWED_ORIGINS` in `.env` file while Flask development server was running. Expected Flask's auto-reload to pick up the change, but CORS errors persisted.

**Root Cause**:
Flask's debug mode auto-reload watches Python files, not `.env` files. Environment variables are loaded once at startup via `python-dotenv`. Changes to `.env` require full server restart.

**Solution**:
Manually restart Flask server:
```bash
# Terminal 1: Stop server (Ctrl+C)
# Then restart
venv\Scripts\python.exe run.py
```

**Prevention**:
- Document in README that .env changes require server restart
- Use environment-specific .env files (.env.development, .env.production)
- Consider using Flask-Env extension for hot-reloading .env
- Add CORS origins to config before starting development

**Learning**:
Understand framework limitations. Flask's auto-reload is file-watcher based (watches .py files). Environment variables are process-level and require process restart. This is standard behavior across most frameworks (Django, Express, etc.).

**Alternative Solution**:
Could have used `python-dotenv`'s `load_dotenv(override=True)` in a signal handler, but full restart is simpler and more reliable.

---

## Common Issues & Quick Fixes

### Issue: JWT Token Not Working
**Symptom**: 401 Unauthorized on protected routes
**Quick Fix**: 
1. Verify JWT_SECRET_KEY in .env
2. Check token format in Authorization header: `Bearer <token>`
3. Verify token hasn't expired

### Issue: Database Connection Failed
**Symptom**: SQLAlchemy connection error
**Quick Fix**:
1. Verify DATABASE_URL in .env
2. Ensure PostgreSQL is running
3. Check database credentials

### Issue: CORS Error in Frontend
**Symptom**: Browser blocks API requests
**Quick Fix**:
1. Install Flask-CORS
2. Configure allowed origins in backend
3. Verify frontend URL in CORS config

---

## Error #6: NameError: name 'current_app' is not defined

**Date**: 2026-02-05
**Phase**: Testing / CI
**Severity**: High

**Error Message**:
```
NameError: name 'current_app' is not defined
```

**Context**:
Encountered during automated CI testing on GitHub Actions after implementing structured logging in `src/backend/routes/tasks.py`.

**Root Cause**:
The `current_app` proxy was used to access the logger in `tasks.py`, but it was not imported from `flask`. This worked in dev because that specific code path (task creation/deletion) wasn't hit during the first local test run, but CI's comprehensive test suite caught it immediately.

**Solution**:
Added `current_app` to the Flask imports in `src/backend/routes/tasks.py`:
```python
# Before
from flask import Blueprint, request, jsonify, g

# After
from flask import Blueprint, request, jsonify, g, current_app
```

**Prevention**:
- Always run the full test suite locally before pushing to CI.
- Use a linter (Pylint/Flake8) to catch undefined names automatically.

**Learning**:
Even minor changes (like adding a log line) can break a module if imports are missing. Comprehensive automated testing is the only reliable way to catch these regressions early.

---

**Last Updated**: 2026-02-05
**Total Errors Logged**: 6
