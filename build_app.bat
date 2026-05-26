@echo off
cls
echo ================================================
echo         BETTING TRACKER - BUILD EXE
echo ================================================
echo.
echo  [*] Se construieste executabilul...
echo  [*] Acest proces dureaza 1-2 minute...
echo.
call "C:\Users\gadiu\Desktop\Betting App\.venv\Scripts\activate.bat" >nul 2>&1
pyinstaller --onefile --console --name "BettingTracker" ^
  --hidden-import=business ^
  --hidden-import=business.type_analyzer ^
  --hidden-import=business.weekly_summary ^
  --hidden-import=business.tracker ^
  --hidden-import=business.accumulator_tracker ^
  --hidden-import=business.bank_manager ^
  --hidden-import=business.stats_analyzer ^
  --hidden-import=business.predictor ^
  --hidden-import=business.chart ^
  --hidden-import=business.calculator ^
  --hidden-import=repository ^
  --hidden-import=repository.file_repo ^
  --hidden-import=repository.accumulator_repo ^
  --hidden-import=repository.bank_repo ^
  --hidden-import=repository.api_repo ^
  --hidden-import=domain ^
  --hidden-import=domain.bet ^
  --hidden-import=domain.accumulator ^
  main.py
echo  [OK] Build finalizat!
echo.
echo  Executabilul se afla in: dist\BettingTracker.exe
echo.
echo ================================================
pause