@echo off
echo 🚑 AI-Powered Smart Ambulance System
echo ====================================
echo.
echo Starting the system...
echo.

REM Start the Flask application in background
echo 🚀 Starting Flask server...
start /B python app.py

REM Wait for server to start
echo ⏳ Waiting for server to initialize...
timeout /t 5 /nobreak > nul

REM Open web interfaces
echo 🌐 Opening web interfaces...
start http://localhost:5000/
start http://localhost:5000/ambulance
start http://localhost:5000/doctor

REM Wait a bit more
timeout /t 3 /nobreak > nul

REM Run the demo script
echo 🎬 Running demo scenarios...
python demo_script.py

echo.
echo ✅ Demo completed!
echo 📊 Check the web interfaces for real-time updates
echo.
pause