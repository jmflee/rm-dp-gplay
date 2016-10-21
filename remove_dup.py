#!/usr/bin/env python

from sys import version_info

# Checks python version
if version_info[0] > 2:
    print ("Using python3.x+, incompatible with gmusicapi, please run a lower version")
    raise SystemExit

from gmusicapi import Mobileclient
from getpass import getpass

client = Mobileclient()

#Keeps on asking for username/password until it is valid
while not client.login(raw_input("Enter Username: "), getpass(), Mobileclient.FROM_MAC_ADDRESS):
    print ("Invalid username/password")

print ("Getting playlist entries")
all_plists = client.get_all_user_playlist_contents() # Gets all playlists and tracks

duplicates = [] # List of all duplicate songs in playlist

for plist in all_plists: # Cycles playlists
    uniqueTracks = []
    duplicatesLen = len(duplicates)

    for entry in plist.get('tracks'): # Cycles songs in playlist
        trackId = entry.get('trackId')
        entryId = entry.get('id')
        if trackId in uniqueTracks:
            duplicates.append(entryId) # It's a duplicate if it's not unique
        else:
            uniqueTracks.append(entryId) # Not a duplicate if unique

    duplicatesLen = len(duplicates) - duplicatesLen

    if duplicatesLen:
        print ("\n " + plist.get('kind').encode('utf-8') + " - " + str(duplicatesLen) + " duplicates")
    # Reset these for the new playlist
    del duplicatesLen
    del uniqueTracks

if len(duplicates):
    # Deletes duplicates 
    if raw_input( "Delete duplicate entries?: ") is 'y':
        client.remove_entries_from_playlist(duplicates)
        print ("Duplicates were deleted")
else:
    print ("No duplicates found, nothing was removed")
