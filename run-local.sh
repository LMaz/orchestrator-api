#!/bin/bash
PYTHONPATH=app uvicorn main:app --port 8000 --reload
