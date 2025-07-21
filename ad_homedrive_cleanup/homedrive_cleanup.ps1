## Home Drive Cleaup
# Pulls Home Drive Data from Active Directory and Deletes the home drive for disabled users
# Calculates retention based on defined date and "whenchanged" AD attribute
# This script will need the following permissions:
# - Read User Accounts in MS Active Directory
# - Delete Directories in Home Drive Share
# This will need to be run in Powershell 7 on a Domain Joined Windows Server / Workstation

## Variables
# Days to retain Home Drive Data
$retention_days = 30

# Parallel Threads
$threads = 4

## Script
# Get Active Directory User Data
Write-Output "Home Drive Cleanup Script"
$delete_date = $(Get-Date).AddDays(-$retention_days)
Write-Output "Setting Delete Date to $(get-date -Date $delete_date -Format MM/dd/yyyy)"
Write-Output "Getting disabled Users from Active Directory. This may take a minute....."
$disabled_users = $null

try {
    $disabled_users = get-aduser -Filter "Enabled -eq '$false'"
}
catch {
    Write-Error "Unable to connect to Active Directory"
}


$disabled_users | Foreach-Object -Parallel {
    # Set Thread Variables
    $status = 0
    $samAccountName = $PSItem.samAccountName
    $userinfo = get-aduser $samAccountName -properties whenChanged,HomeDirectory
    $homeDirectory = $userinfo.HomeDirectory
    $whenChanged = $(get-date -date $userinfo.whenChanged) 
    # Check for Defined Home Directory Attribute
    if (![string]::IsNullOrEmpty($homeDirectory)) {
        Write-Output "$samAccountName | Home Directory: $homeDirectory"
        # Validate retention period has passed
        Write-Output "$samAccountName | Modified Date: $whenChanged"
        Write-Output "$samAccountName | Target Deletion Date: $retention"
        if ($whenChanged -le $USING:delete_date) {
            try {
                Write-Output "$samAccountName | Deleting Home Directory"
                Remove-Item -Path $homeDirectory -Recurse
            }
            catch {
                Write-Error "$samAccountName | An error occured while deleting $homeDirectory"
                $status = 1
            }
            if ($status -eq 0) {
                Write-Output "$samAccountName | Clearing AD Home Directory Attribute"
                try {
                    set-aduser -Identity $samAccountName -HomeDirectory $null
                } catch {
                    Write-Error "An error has occured setting the AD Attribute"
                } 
            }

        } else {
            Write-Output "$samAccountName | Modified Date: $whenChanged"
            Write-Output "$samAccountName | User is not past retention date"
            
        }
    } else {
        Write-Output "$samAccountName | No Home Directory Assigned"
    }
} -ThrottleLimit $threads
