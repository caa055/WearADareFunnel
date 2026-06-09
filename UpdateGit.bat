@echo off
python generate_data_csv.py
pause
python deploy.py
pause