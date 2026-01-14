-- MarkShot Installer for macOS
-- Copies MarkShot.py to DaVinci Resolve Scripts folder

on run
    set scriptName to "MarkShot.py"
    set targetFolder to (path to home folder as text) & "Library:Application Support:Blackmagic Design:DaVinci Resolve:Fusion:Scripts:Utility:"

    -- Get the path to this app's Resources folder
    set myPath to path to me
    set myFolder to (POSIX path of myPath) & "Contents/Resources/"
    set sourceFile to myFolder & scriptName

    -- Check if source file exists
    try
        do shell script "test -f " & quoted form of sourceFile
    on error
        display alert "Error" message "MarkShot.py not found in installer." as critical
        return
    end try

    -- Check if DaVinci Resolve folder exists
    try
        do shell script "test -d " & quoted form of POSIX path of targetFolder
    on error
        display alert "Error" message "DaVinci Resolve Scripts folder not found. Please ensure DaVinci Resolve is installed." as critical
        return
    end try

    -- Confirm installation
    set dialogResult to display dialog "MarkShot Installer" & return & return & "This will install MarkShot.py to:" & return & POSIX path of targetFolder & return & return & "Continue?" buttons {"Cancel", "Install"} default button "Install" with icon note

    if button returned of dialogResult is "Install" then
        try
            -- Copy file
            do shell script "cp " & quoted form of sourceFile & " " & quoted form of (POSIX path of targetFolder & scriptName)

            -- Set permissions
            do shell script "chmod 644 " & quoted form of (POSIX path of targetFolder & scriptName)

            display alert "Installation Complete!" message "MarkShot has been installed successfully." & return & return & "To use: Open DaVinci Resolve > Workspace > Scripts > MarkShot" as informational

        on error errMsg
            display alert "Installation Failed" message errMsg as critical
        end try
    end if
end run
