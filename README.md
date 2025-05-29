![# 𝕽𝖔̎𝖍𝖗𝖊𝖋𝖚𝖓𝖐𝖊𝖓](https://github.com/rari-teh/rari-teh.github.io/raw/master/img/proj/roehrefunken.png "𝕽𝖔̎𝖍𝖗𝖊𝖋𝖚𝖓𝖐𝖊𝖓")
Let’s say you are forced to use an Internet connection that blocks most sites, including YouTube. Let’s also say Google Drive is one of the few sites that aren’t blocked. What would you do if you wanted to listen to YouTube while you do something else when you only have this stringently limited connection at hand?

Enter **Röhrefunken**. Set it up on an external device and make it your very own janky and convoluted YouTube proxy. Fast, discreet and effective. Just don’t get fired.

## Requirements
Very few:
* Python 3 and pip
* ffmpeg
* [Termux](https://f-droid.org/en/packages/com.termux/), if you’re running on Android
* A Google account that you are allowed to access both on and off the limited Internet connection you’re trying to circumvent. Seriously, don’t get fired.

Röhrefunken also requires the following pip packages:
* google-api-python-client
* google-auth-oauthlib
* google-auth-httplib2
* yt-dlp

## Setup
This part is long and boring and annoying and Google Cloud Console is as nimble and lightweight as the *Evergreen*, but mercifully you’ll only need to do it once.
1. Log into any Google account and access [Google Cloud Console](https://console.cloud.google.com/). If this is your first time here, you’ll need to select your region, accept the terms etc.
2. Click on *APIs and Services* and create a new project. For the name, I suggest *Röhrefunken*.
3. Enable both the [Google Docs API](https://console.cloud.google.com/apis/library/docs.googleapis.com) and the [Google Drive API](https://console.cloud.google.com/apis/api/drive.googleapis.com). Don’t worry, they’re free (as of May 2025).
4. Now go to [Google Auth Platform](https://console.cloud.google.com/auth/overview) and set up OAuth permissions. The process here should be pretty self-explanatory, except you should make sure to set your audience as external.
5. Once that’s done, click on *Clients* on the side pane and create a new OAuth client ID. I recommend *RöhrePY* for the name. The application type should be desktop app.
6. A popup will appear telling you the client was created. Click *Download JSON*, rename the file to `client_secret.json` and place it together with `rf.py`.
7. Close the popup and click on *Data Access* on the side pane. Click on *Add or remove scopes* and check the scopes `.../auth/documents` and `.../auth/drive`. Click on *Update* and then *Save* down at the bottom.
8. Finally, Click on *Audience* on the side pane and then on *Add users*. Enter the email address of the Google ID whose Drive you’ll use to listen to YouTube through the limited connection.

## First run
Before anything else, you’ll need to edit the script to point at the Google document that will serve as your little console of sorts. Log onto the Google account you’ll use in your limited connection and create a new text document. Give it any title you want and let it autosave. Copy the document ID (the long alphanumeric string between `/document/d/` and `/edit` on the URL) and paste it in quotes inside `rf.py` on the indicated spot.

### Desktop
To kickstart the service, just run `python3 ./rf.py`. The pickler isn’t needed on desktop; you might as well not even download it. A browser window should pop open asking you to authorise Röhrefunken to meddle with Google Docs and Google Drive on your behalf. Once that’s done, a persistent token should be saved and you won’t be bothered by that anymore for a very long time, if ever.

### Android
Now that’s a little jankier, but hell if it isn’t handy to have it running on your phone whenever you want. Run `python3 ./pickler.py` on the same directory as `client_secret.json`. Copy the long-ass URL it spews out, paste it on your browser of choice and authorise Röhrefunken using the right Google account. Go back to Termux and run `python3 ./pickler.py` again. The persistent token should be successfully set up, and now you can run `python3 ./rf.py` to kickstart the service as normal.

## Usage
To get an audio track from YouTube, change the title of the Google document you set up as your console to your query and end it with a `$`, e.g. `britney spears baby one more time lyrics$`. In about 10 seconds, Röhrefunken will notice the change, search YouTube for you, download the first result, convert the audio track to MP3 and upload it to your Google Drive. When it’s done, the document’s title will be automatically chaned to `!rf - ready` if everything went fine and `!rf - error` if it encountered an unrecoverable problem (you can still try again if you want to). If nothing happens, it may have failed downloading the video — in that case, it will automatically retry every other 10 seconds.

I made Röhrefunken so that it strips the video stream and only uploads MP3 audio, but it should be relatively easy to change it so that it uploads the whole video in a format you can stream through Google Drive’s web interface. Have fun doing that if you wanna!

## License
CC-BY (do whatever you want, just credit me)

The pickler is a slightly modified version of FollowNaim’s [TokenPickle](https://github.com/FollowNaim/TokenPickle).