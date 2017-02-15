@echo off
if exist c:\Python27\Scripts\ride.py (
	c:\Python27\python.exe c:\Python27\Scripts\ride.py
) else if exist c:\Python34\Scripts\ride.py (
	c:\Python34\python.exe c:\Python34\Scripts\ride.py
) else (
	echo You should install Python first!
)
