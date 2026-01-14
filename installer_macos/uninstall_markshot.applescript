-- MarkShot Uninstaller for macOS
-- Removes MarkShot.py from DaVinci Resolve Scripts folder

on run
    set scriptName to "MarkShot.py"
    set targetFile to (path to home folder as text) & "Library:Application Support:Blackmagic Design:DaVinci Resolve:Fusion:Scripts:Utility:" & scriptName
    set targetPath to POSIX path of targetFile

    -- Check if file exists
    try
        do shell script "test -f " & quoted form of targetPath
    on error
        display alert "Not Installed" message "MarkShot is not installed." as informational
        return
    end try

    -- Confirm uninstall
    set dialogResult to display dialog "MarkShot Uninstaller" & return & return & "This will remove MarkShot.py from:" & return & targetPath & return & return & "Continue?" buttons {"Cancel", "Uninstall"} default button "Cancel" with icon caution

    if button returned of dialogResult is "Uninstall" then
        try
            -- Remove file
            do shell script "rm " & quoted form of targetPath

            display alert "Uninstall Complete" message "MarkShot has been removed." as informational

        on error errMsg
            display alert "Uninstall Failed" message errMsg as critical
        end try
    end if
end run
