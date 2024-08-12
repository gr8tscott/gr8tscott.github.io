#!/bin/bash
# Script:
#  scraper.sh
#
# Purpose:
#   Validates and retrieves the URL and puts it into an HTML file within a directory.
#   Extracts the body text of a news article and limits it to the first 400 characters.
#
# Inputs:
#   Initial URL
#
# Outputs:
#   Extracted HTML file and body text.
#
# Changelog:
#    Date (MM-DD-YYYY)     Name      Change Description
#    02-15-2024            MScott    Initial Creation
#    07-14-2024            MScott    Updated to scrape news article body text and prevent overwriting files
#    07-21-2024            MScott    Updated to extract text from specific div and p tags
#    08-10-2024            MScott    Added conversion of '&#x27;' to single quote (') in text and title files
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

#---------------
# Validates a URL
#---------------
validateURL () {
    decho "Validating $1"
    
    local inputURL=$1
    
    if ! wget -q --spider $inputURL; 
    then
        decho "ERROR: Bad URL"
        exit 1
    fi
    
    return 0
}

#---------------
# Extracts the body text of the news article and saves specific sections to files
#---------------
# Extracts the body text of the news article and saves specific sections to files
extractArticleBody () {
    decho "Extracting Article Body"
    
    if [[ ! -e temp.html ]]; then
        decho "ERROR: missing temp.html from extract"
        exit 3
    fi
    
    # Extract the title from the <h1> tag
    local title=$(sed -n 's/.*<h1 class="ArticleHeader-headline">\([^<]*\)<\/h1>.*/\1/p' temp.html)
    
    # Check if the title was extracted
    if [[ -z "$title" ]]; then
        decho "ERROR: Couldn't extract article title"
        exit 2
    fi
    
    # Convert '&#x27;' to a single quote (')
    title=$(echo "$title" | sed 's/&#x27;/'\''/g')
    
    # Limit title to the first 4 words and format for file names
    finalTitle=$(echo "$title" | awk '{for(i=1;i<=4;i++) printf "%s ", $i; print ""}' | tr -d '\n' | sed 's/[[:space:]]*$//')
    finalTitle=$(echo "$finalTitle" | sed 's/[^a-zA-Z0-9]/_/g')  # Remove special characters and replace spaces with underscores
    
    decho "Article Title: $finalTitle"
    
    # Define the article path
    articlePath="Articles/$websiteName/$finalTitle/"
    
    # Create the directory if it doesn't exist
    mkdir -p "$articlePath"
    
    # Extract the content of the specific div with class 'ArticleBody-articleBody' and ID 'RegularArticle-ArticleBody-5'
    sed -n '/<div class="ArticleBody-articleBody" id="RegularArticle-ArticleBody-5"/,/<\/div>/p' temp.html > "${articlePath}wazzup.html"
    
    # Check if wazzup.html has been created
    if [[ ! -s "${articlePath}wazzup.html" ]]; then
        decho "ERROR: Couldn't extract article body content"
        exit 2
    fi

    # Extract all <div> with class 'group' from wazzup.html
    sed -n '/<div class="group"/,/<\/div>/p' "${articlePath}wazzup.html" > "${articlePath}groups.html"
    
    # Check if groups.html has been created
    if [[ ! -s "${articlePath}groups.html" ]]; then
        decho "ERROR: Couldn't extract groups content"
        exit 2
    fi
    
    decho "Groups content extracted to ${articlePath}groups.html"
    
    # Add delimiters around <p> tags
    sed -i 's/<p>/<p>\n/g; s/<\/p>/<\/p>\n/g' "${articlePath}groups.html"
    
    # Extract all <p> tags content within groups.html
    local groupPContent=$(sed -n '/<p>/,/<\/p>/p' "${articlePath}groups.html" | sed -e 's/<[^>]*>//g' | tr -d '\n' | sed -e 's/^[ \t]*//;s/[ \t]*$//')
    
    # Convert '&#x27;' to a single quote (') in the content
    groupPContent=$(echo "$groupPContent" | sed 's/&#x27;/'\''/g')
    
    # Remove unwanted phrases and erroneous content
    groupPContent=$(echo "$groupPContent" | sed -e 's/Follow your favorite stocks//g' \
                                                        -e 's/CREATE FREE ACCOUNT//g' \
                                                        -e 's/Getty Images//g' \
                                                        -e 's/&quot;//g')


    
    # Check if groupPContent is not empty
    if [[ -z "$groupPContent" ]]; then
        decho "Couldn't find <p> tags in ${articlePath}groups.html"
        exit 2
    fi
    
    decho "Extracted <p> tags content from ${articlePath}groups.html"
    finalGroupPContent=$groupPContent

    # Define the path for saving the group content file
    groupContentFile="${articlePath}${finalTitle}_groups.html"
    
    # Check if the group content file already exists
    if [[ -e $groupContentFile ]]; then
        echo "ERROR: $groupContentFile already exists"
        exit 6
    fi

    # Save the extracted <p> tags content to an HTML file
    echo "$finalGroupPContent" > "$groupContentFile"
    decho "Groups content extracted to $groupContentFile"
    
    # Convert the HTML content to plain text and save to a .txt file
    txtContentFile="${articlePath}${finalTitle}_content.txt"
    sed -e 's/<[^>]*>//g' -e 's/^[ \t]*//;s/[ \t]*$//' "$groupContentFile" > "$txtContentFile"
    
    # Convert '&#x27;' to a single quote (') in the text file
    sed -i "s/&#x27;/'/g" "$txtContentFile"
    
    decho "Converted HTML content to text and saved to $txtContentFile"
    
    # Output the path of the created text file and title file at the end
    echo "$txtContentFile"
    echo "$title" > "${articlePath}${finalTitle}_title.txt"
    echo "${articlePath}${finalTitle}_title.txt"  # Add this line to output the title file path
}

#-------------------
# Get the website name from input URL
#-------------------
extractWebsiteName () {
    local inputurl=$1
    decho "Input: $inputurl"
    
    iptURL=$(echo $inputurl | cut -d'/' -f3)   
    local tempURL="${iptURL#*www.}"
    
    decho "Shortened: $tempURL"
    
    websiteName="${tempURL%.*}"
    
    # Extract title from the HTML and clean it for file naming
    local title=$(sed -n 's/.*<h1 class="ArticleHeader-headline">\([^<]*\)<\/h1>.*/\1/p' temp.html | head -n1)
    
    if [[ -z "$title" ]]; then
        decho "ERROR: Couldn't extract article title"
        exit 2
    fi
    
    # Convert '&#x27;' to a single quote (') in the title
    title=$(echo "$title" | sed 's/&#x27;/'\''/g')
    
    # Get the first 4 words, replace spaces with underscores, and remove special characters
    finalTitle=$(echo "$title" | awk '{print $1" "$2" "$3" "$4}' | sed 's/ /_/g; s/[^a-zA-Z0-9_]//g')
    
    if [[ -z "$finalTitle" ]]; then
        decho "ERROR: Couldn't process title for file naming"
        exit 2
    fi
    
    decho "Final Title: $finalTitle"
}

#-----------------
# Move temp.html to finalTitle.html, and under appropriate hierarchy structure
#-----------------
moveRawHTML () {
    articlePath="Articles/$websiteName/$finalTitle/"
    rawHTML="$articlePath/${finalTitle}_raw.html"
    decho "RAWHTML: $rawHTML"
    
    SCRIPT_DIR=$(dirname "$0")

    if [ ! -f "$SCRIPT_DIR/verifyHeirarchy.sh" ]; 
    then
        echo "Could Not find $SCRIPT_DIR/verifyHeirarchy.sh"
        exit 4
    fi

    echo "Found verifyHeirarchy.sh"
    "$SCRIPT_DIR/verifyHeirarchy.sh" "$articlePath"
    
    decho "Moving raw HTML to subdir Articles/$websiteName/$finalTitle/"
    
    # Create the directory if it doesn't exist
    mkdir -p "$articlePath"
    
    # Check if the raw HTML file already exists
    if [[ -e $rawHTML ]]; 
    then
        echo "ERROR: $rawHTML already exists"
        exit 6
    fi
    
    mv temp.html $rawHTML
}

#==============================================================================
# MAIN SCRIPT
#==============================================================================
decho "==============Starting $0 ============="
#-------------------
# Take input and give name
#-------------------
decho "Reassigning input"
if [[ $1 ]];
then
    inputurl=$1
else
    echo "ERROR: No Input"
    exit 5
fi

validateURL $inputurl

#-------------------
# If valid url, get the html file
#-------------------
wget -q -O temp.html $inputurl

#-------------------
# Get the website name from input URL
#-------------------
extractWebsiteName $inputurl

#-------------------
# Extract the body text of the article
#-------------------
extractArticleBody

#-----------------
# Move temp.html to finalTitle.html, and under appropriate hierarchy structure
#-----------------
moveRawHTML

decho "Extraction Complete. Files at $articlePath"
echo "Articles/$websiteName/$finalTitle/${finalTitle}_content.txt"
echo "Articles/$websiteName/$finalTitle/${finalTitle}_title.txt"

exit 0
