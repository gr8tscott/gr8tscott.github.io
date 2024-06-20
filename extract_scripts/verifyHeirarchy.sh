#!/bin/bash
# Script:
#  dir.sh
#
# Purpose:
#   Build a directory hierarchy to store files for each recipe
#
# Inputs:
#   $1 = Recipe File Path
#
# Outputs:
#   Print what directory has been created
#
# Notes:
#   Assumes working directory is the home directory of the repository
#
# Exits
#   0 = success
#   1 = no name entered for directory creation
#   3 = no Recipe dir
#   4 = File already exists
#    
# Changelog:
#    Date (MM-DD-YYYY)     Name      Change Description
#    02-18-2024            halleeray   Initial Creation
#    02-25-2024            emdonkus    Updated with functions and plugged into other scripts
#
#------------------------------------------------------------------
#------------------------------------------------------------------
DEBUG=1

#---------------
# Only echoes if debug is turned on
#---------------
decho () {
    if [[ $DEBUG == 1 ]];
    then
        echo $1
        echo ""
    fi
}

#-------------------------
#   Validate Data Directory Exists, Return error if not
#-------------------------
verifyRecipeDir () {

    decho "Checking for Recipes Directory"

    if [[ ! -e "Recipes" ]];
    then
        decho "Recipes Directory does not exist. Pleae run from correct directory."
        exit 3
    fi
}
#-------------------------
#   Validate SubDir Path
#-------------------------
verifySubDirs () {
    path=$1
    echo $path
    if [[ ! $path ]];
    then 
        decho "Error: No path specified"
        exit 3
    fi
    
    if [[ -d $path ]];
    then
        #-------------------------
        #   File already exists, dont do anything else
        #-------------------------
        decho "Path $path already exists!"
        if [[ "$(ls $path)" ]];
        then
            decho "Checking if the files exist"
            #-------------------------
            #   Path Exists,checking if the files exist
            #------------------------
            decho "Files Exist"
            exit 4
        fi
    else
        #-------------------------
        #   Path doesnt exist, create it
        #-------------------------
        decho "Creating $path"
        mkdir -p $path
        
    fi
    

}


decho "==============Starting $0 ============="
#---------------
# Reassign inputs
#---------------
filePath=$1 

#-------------------------
# Verify Data Dir exists
#-------------------------
decho "Checking Directory Structures"
verifyRecipeDir

#-------------------------
#   Verify/create subdirectories
#-------------------------
decho "Checking subdirectories"
verifySubDirs $filePath


decho "============Exiting $0 ================="
exit 0

