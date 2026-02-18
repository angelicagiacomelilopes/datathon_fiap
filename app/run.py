#!/usr/bin/env python
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main_simple import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002, log_level="info")
