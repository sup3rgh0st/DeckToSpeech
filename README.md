# DeckToSpeech
 A Discord bot that follows you into voice calls and plays audio clips when it recieves commands via websockets

### Geting Started
 Create secret.json in the project root formatted as the following where BotToken is your bot's unique token and LeaderID is your Discord ID.
{
	"BotToken": "ABCXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
	"LeaderID": "123000000000000000"
}

 Create soundlist.json in the project root formatted as the following where directory is a key for the folder where the audio files will live (the sounds folder in the example below) and the following pairs are websocket commands with their file name within the sounds directory.
 {
	 "directory": "./sounds/",
	 "SampleSoundsComammd01": "SampleSound01.wav",
	 "SampleSoundsComammd02": "SampleSound02.wav",
  ...
  ...
 }
 
  Download FFMPEG.exe and place it in the project root.
 
  To start the bot, run DeckToSpeech using Python3. This bot was developed on Python 3.9.7
 
  While the bot is running on a server that you are a part of, join a voice call and the bot will follow you. Sending websocket commands to ws://your_ip::3030 will control the bot.
  Send 'stop' to stop all currently playing audio.
  Send any command specified in soundlist.json to play the paired audio file.
