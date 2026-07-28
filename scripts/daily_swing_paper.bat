@echo off
REM ============================================================
REM  M3 forward-paper daily loop - runs ALL 3 sleeves together
REM  (e6_1x, e18_vixts, m10_1_nagel) in ONE invocation, so they
REM  all act at the same moment. --execute = mirror live paper
REM  orders to each sleeve's own Alpaca paper account.
REM  Registered to Task Scheduler as "SwingTradingDailyPaper"
REM  (weekday evenings). PURE ASCII - cmd.exe corrupts its parse
REM  on a single non-ASCII byte (project CLAUDE.md hard rule).
REM  Output is appended to var\daily_swing_paper.log (gitignored).
REM ============================================================
cd /d "D:\ClaudeCode\Swing Trading"
if not exist "var" mkdir "var"
echo.>> "var\daily_swing_paper.log"
echo ==================== %DATE% %TIME% ====================>> "var\daily_swing_paper.log"
".venv\Scripts\python.exe" "scripts\daily_swing_paper.py" --execute >> "var\daily_swing_paper.log" 2>&1
REM Space before >> is REQUIRED: "%ERRORLEVEL%>>" makes cmd read the trailing
REM digit as a redirection HANDLE, so the line vanished from the log (0 hits
REM across 12 runs; audit finding #5, 2026-07-28). Do not close that gap.
echo exit code %ERRORLEVEL% >> "var\daily_swing_paper.log"
