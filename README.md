# music_analytics
Small personal music analytics projects


This repository contains a number a jupyter notebook files of music analytics projects I have carried out in my spare time.

ArcticMonkeysAnalytics.ipynb contains analysis on the audio properties of the Arctic Monkeys discography, such as valence, energy, danceability. Looking at
how they have varied over time, from album to album

Best_Selling_Albums_Analytics.ipynb contains analysis on the audio properties of best selling albums over time. Data of the best selling albums of each decade was 
scraped from Wikipedia pages and the Spotify API was used to gather audio features of these albums, which were then compared to see if they differed
over time and if they gave any indication of what features typically make up a best selling album.

These two projects were carried out so I could become familiar with how to use the Spotify API and because I found the concepts interesting.


Future work that I will carry out and upload to this repository is:
* A comprehensive analysis of my listening history on Spotify over the past year (as this is the
longest period Spotify allows me to download of my own listening history)

* An experiment on using machine learning for creating music listening suggestions when 
given a song

* Finally, I would like to attempt to synthesize music using GANs.

# Python Web Scraper
I have also included a script I wrote to create new album playlists each week based on the r/indieheads subreddit. 

Every Friday new albums are released and people will post links to some of these albums in the subreddit. These posts can get lost within other posts on the forum so I created this script to extract the titles and artists of these albums and add the tracks to a Spotify playlist. I chose to only add albums with more than 50 upvotes as a "quality" filter to reduce the number of albums. 

This script continuously updates one main playlist. When I scheduled this for my computer I did this daily to allow for albums to gain upvotes over a week and potentially be added to the playlist. An album can only be added to this playlist it if came out the previous Friday. Once the next Friday has been reached (where more albums will be released) the albums released on the previous Friday will no longer be included in updates, to keep the playlist fresh and not too long.

So that albums released in previous weeks aren't forgotten if I didn't get to listen to them, every Thursday I create a new playlist that corresponds to the week that has occurred. This playlist is filled with all the albums that fit the criteria on that Thursday and will never be updated after.
