#!/bin/bash
# Script:
#  genArticles.sh
#
# Purpose:
#   Generates the Recipe directory for listed recipes here
#
# Inputs:
#   Add urls to URLs array
#
# Outputs:
#   Recipe files
#
# Notes:
#   
#
# Exits
#   0 = success
#   1 = error
#    
# Changelog:
#    Date (MM-DD-YYYY)     Name      Change Description
#    03-07-2024            EDonkus   Initial Creation
#
#------------------------------------------------------------------
#------------------------------------------------------------------

#------------
# URL that worked
#------------
URLs=(
    # 'https://www.cnbc.com/2024/06/19/solar-is-growing-faster-than-any-energy-source-as-clean-power-for-data-centers.html'
    'https://www.tipranks.com/news/apples-aapl-market-cap-to-hit-4t-says-wedbush'
#     'https://www.skinnytaste.com/shrimp-stir-fry/'
#     'https://moonandspoonandyum.com/slow-cooker-roasted-potatoes/?utm_source=msn&utm_medium=page&utm_campaign=msn#recipe'
#     'https://www.skinnytaste.com/chicken-florentine/'
#     'https://damndelicious.net/2022/10/14/perfect-pot-roast/'
#     'https://www.budgetbytes.com/cranberry-apple-baked-oatmeal/'
#     'https://www.budgetbytes.com/creamy-garlic-chicken/'
#     'https://www.skinnytaste.com/5-ingredient-almond-cake-with-fresh/'
#     'https://www.skinnytaste.com/veggie-kabobs/'
#     'https://www.skinnytaste.com/macaroni-salad-with-tomatoes/'
#     'https://www.skinnytaste.com/baby-red-potato-salad/'
#     'https://www.skinnytaste.com/lentil-curry/'
#     'https://www.skinnytaste.com/roasted-mushrooms/'
#     'https://www.skinnytaste.com/hearts-of-palm-salad-with-avocado/'
#     'https://www.budgetbytes.com/basic-chili/'
#     'https://www.budgetbytes.com/goulash/'
#     'https://www.budgetbytes.com/caesar-salad/'
#     'https://www.budgetbytes.com/flan/'
#     'https://www.recipetineats.com/mexican-ground-beef-casserole-with-rice/'
#     'https://www.recipetineats.com/quick-broccoli-pasta/'
#     'https://damndelicious.net/2023/04/28/crispy-baked-chicken-tacos/'
#     'https://damndelicious.net/2022/05/27/roasted-cauliflower/'
#     'https://moonandspoonandyum.com/chickpea-kale-salad/'
#     'https://moonandspoonandyum.com/rujak/'
#     'https://moonandspoonandyum.com/cherry-tomato-confit/'
#     'https://moonandspoonandyum.com/gluten-free-bannock-bread/'
#     'https://natashaskitchen.com/pan-seared-steak/'
#     'https://natashaskitchen.com/egg-salad-recipe/'
#     'https://natashaskitchen.com/zucchini-muffins-recipe/'
#     'https://www.orchidsandsweettea.com/pan-seared-steak-recipe/'
#     'https://www.budgetbytes.com/navy-bean-soup/'



    )
    #    'https://moonandspoonandyum.com/slow-cooker-roasted-potatoes/?utm_source=msn&utm_medium=page&utm_campaign=msn#recipe'
    #     'https://www.skinnytaste.com/chicken-florentine/'
    # 'https://damndelicious.net/2022/10/14/perfect-pot-roast/'
    # 'https://www.budgetbytes.com/cranberry-apple-baked-oatmeal/'
    # 'https://www.budgetbytes.com/creamy-garlic-chicken/'
    # 'https://www.skinnytaste.com/5-ingredient-almond-cake-with-fresh/'
    # 'https://www.skinnytaste.com/veggie-kabobs/'
    # 'https://www.skinnytaste.com/macaroni-salad-with-tomatoes/'
    # 'https://www.skinnytaste.com/baby-red-potato-salad/'
    # 'https://www.skinnytaste.com/lentil-curry/'
    # 'https://www.skinnytaste.com/roasted-mushrooms/'
    # 'https://www.skinnytaste.com/hearts-of-palm-salad-with-avocado/'
    # 'https://www.budgetbytes.com/basic-chili/'
    # 'https://www.budgetbytes.com/goulash/'
    # 'https://www.budgetbytes.com/caesar-salad/'
    # 'https://www.budgetbytes.com/flan/'
    # 'https://www.recipetineats.com/mexican-ground-beef-casserole-with-rice/'
    # 'https://www.recipetineats.com/quick-broccoli-pasta/'
    # 'https://damndelicious.net/2023/04/28/crispy-baked-chicken-tacos/'
    # 'https://damndelicious.net/2022/05/27/roasted-cauliflower/'
    # 'https://moonandspoonandyum.com/chickpea-kale-salad/'
    # 'https://moonandspoonandyum.com/rujak/'
    # 'https://moonandspoonandyum.com/cherry-tomato-confit/'
    # 'https://moonandspoonandyum.com/gluten-free-bannock-bread/'
    # 'https://natashaskitchen.com/pan-seared-steak/'
    # 'https://natashaskitchen.com/egg-salad-recipe/'
    # 'https://natashaskitchen.com/zucchini-muffins-recipe/'
    # 'https://www.orchidsandsweettea.com/pan-seared-steak-recipe/'
    # 'https://www.budgetbytes.com/navy-bean-soup/'
    # 'https://natashaskitchen.com/zuppa-toscana-recipe-video/'
#------------
# Size of array
#------------
size=${#URLs[@]} 

#------------
# For each url, run retrieval script
#------------
for (( i-0; i < $size; i++ ))    
{
    # extract_scripts/retrieveURL.sh ${URLs[$i]}
    # ./scraper.sh ${URLs[$i]}
    extract_scripts/scraper.sh ${URLs[$i]}

}