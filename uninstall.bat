@echo off
echo.
echo == Uninstalling the 'todo_app' package from Python environment...
pip uninstall todo_app -y
echo.
echo =================================================================
echo.
echo == Cleaning up build artifacts (build, dist, egg-info)...

if exist build (
    echo Removing 'build' directory...
    rmdir /s /q build
)

if exist dist (
    echo Removing 'dist' directory...
    rmdir /s /q dist
)

if exist todo_app.egg-info (
    echo Removing 'todo_app.egg-info' directory...
    rmdir /s /q todo_app.egg-info
)

echo.
echo Uninstallation and cleanup complete.
echo Press any key to exit.
pause > nul