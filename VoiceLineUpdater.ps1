#!/usr/bin/env pwsh

function Update-RenpyVoiceAssignments {
    [OutputType([PSCustomObject])]
    param(
        [Parameter(Mandatory = $true, ParameterSetName = "Path")]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({ Test-Path -Path $_ })]
        [string[]]$PathOld,

        [Parameter(Mandatory = $true, ParameterSetName = "LiteralPath")]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({ Test-Path -LiteralPath $_ })]
        [string[]]$LiteralPathOld,

        [Parameter(Mandatory = $true, ParameterSetName = "Path")]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({ Test-Path -Path $_ })]
        [string[]]$PathNew,

        [Parameter(Mandatory = $true, ParameterSetName = "LiteralPath")]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({ Test-Path -LiteralPath $_ })]
        [string[]]$LiteralPathNew,

        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]$ScriptFilePrefix
    )

    if ($PSCmdlet.ParameterSetName -eq "Path") {
        $oldDialogueLines = Import-Csv -Path $PathOld -Delimiter "`t";
        $newDialogueLines = Import-Csv -Path $PathNew -Delimiter "`t";
    }
    else {
        $oldDialogueLines = Import-Csv -LiteralPath $LiteralPathOld -Delimiter "`t";
        $newDialogueLines = Import-Csv -LiteralPath $LiteralPathNew -Delimiter "`t";
    }

    $oldDialogueLines = $oldDialogueLines | Where-Object {
        $_.Identifier.StartsWith($ScriptFilePrefix) -and `
            -not [string]::IsNullOrWhiteSpace($_.Character) };
    
    $newDialogueLines = $newDialogueLines | Where-Object {
        $_.Identifier.StartsWith($ScriptFilePrefix) -and `
            -not [string]::IsNullOrWhiteSpace($_.Character) };

    $lineMappings = @();
    foreach ($oldDialogueLine in $oldDialogueLines) {
        $newDialogueLine = $newDialogueLines | Where-Object {
            $_.Dialogue -eq $oldDialogueLine.Dialogue -and
            $_.Identifier.StartsWith(
                ($oldDialogueLine.Identifier | `
                    Select-String -Pattern "^scene_\dS\d_([bc]_)?").Matches) };
        
        if (-not $newDialogueLine) {
            throw [System.InvalidOperationException] `
                "No corresponding line of dialogue found for old dialogue line $($oldDialogueLine.Identifier)";
        }
        
        $lineMappings += [PSCustomObject]@{
            OldId = $oldDialogueLine.Identifier
            NewId = $newDialogueLine.Identifier
        }
    }

    return $lineMappings;
}

function Update-VoiceLineFileNames {
    [OutputType([void])]
    param(
        [Parameter(Mandatory = $true, ParameterSetName = "Path")]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({ Test-Path -Path $_ })]
        [string[]]$Path,

        [Parameter(Mandatory = $true, ParameterSetName = "LiteralPath")]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({ Test-Path -LiteralPath $_ })]
        [string[]]$LiteralPath,

        [Parameter(Mandatory = $true, ValueFromPipeline = $true)]
        [ValidateNotNullOrEmpty()]
        $LineMappings,

        [bool]$Mock = $false
    )

    process {
        if ($LineMappings.Length -eq 0) {
            throw [System.ArgumentException]
        }

        if ($PSCmdlet.ParameterSetName -eq "Path") {    
            $voiceFolder = Get-ChildItem -Path $Path -Recurse -File;
        }
        else {
            $voiceFolder = Get-ChildItem -LiteralPath $Path -Recurse -File;
        }

        $relevantLineMappings = $LineMappings | Where-Object {
            ($voiceFolder | Select-Object -ExpandProperty "BaseName") -contains $_.OldId
        };

        foreach ($line in $relevantLineMappings) {
            $targetFile = $voiceFolder | Where-Object { $_.BaseName -eq $line.OldId };
            if (-not $targetFile) {
                throw [System.InvalidOperationException] `
                    "[ERROR] Line with old ID $($line.OldId) has no corresponding file."
            }

            if ($line.NewId -isnot [string] -and $line.NewId.Length -gt 1) {
                Write-Output "[WARN] File for old ID $($line.OldId) has multiple matches, ($($line.NewId)), skipping.";
                continue;
            }

            Write-Output "[INFO] Renaming file $($targetFile.Name) to $($line.NewId)$($targetFile.Extension)";
            if (-not $Mock) {
                Rename-Item $targetFile -NewName "$($line.NewId)$($targetFile.Extension)";
            }
        }
    }
}

Update-RenpyVoiceAssignments -PathOld "" `
    -PathNew "" -ScriptFilePrefix "scene_" | `
    Update-VoiceLineFileNames -Path ".\game\voice" -Mock $true;
