import discord

import asyncio
import json
import websockets
from os.path import exists

#Deck To Speech - Discord Bot
# 2022 sup3rgh0st

f = open('secret.json')
secret = json.load(f)
f.close()

f = open('soundlist.json')
soundlist = json.load(f)
f.close()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'

	
class MyClient(discord.Client):

	my_voice_channel = None
	
	
	def log_info(self, msg):
		print('{0}[INFO]{1} {2}'.format(bcolors.OKGREEN, bcolors.WHITE, msg))

		
	def log_warning(self, msg):
		print('{0}[WARN]{1} {2}'.format(bcolors.WARNING, bcolors.WHITE, msg))

		
	def log_error(self, msg):
		print('{0}[ERROR]{1} {2}'.format(bcolors.FAIL, bcolors.WHITE, msg))

		
	def play_indexed_audio(self, index):
		if self.my_voice_channel is None:
			self.log_warning('Tried to play indexed audio while not connected to a Voice Channel')
			return
		if index not in soundlist:
			self.log_warning('Tried to play an audio clip that was not indexed. \'{0}\''.format(index))
			return
		
		if self.my_voice_channel.is_playing():
			self.my_voice_channel.stop()
			
		file_path = soundlist['directory'] + soundlist[index]
		if exists(file_path):
			self.log_info('Playing sound with path {0}'.format(file_path))
			self.my_voice_channel.play(discord.FFmpegOpusAudio(executable="E:/Projects/DeckToSpeech/ffmpeg.exe", source=file_path))
		else:
			self.log_error('Path {0} does not exist'.format(file_path))

			
	def stop_active_audio(self):
		if self.my_voice_channel is None:
			self.log_warning('Attempted to stop audio while there was no active Voice Channel.')
			return
			
		if not self.my_voice_channel.is_playing():
			self.log_warning('Attempted to stop audio while there was no audio.')
			return
		
		self.log_info('Stopping active audio')
		self.my_voice_channel.stop()

		
	async def echo(self, websocket):
		try:
			async for message in websocket:
				if message == 'stop':
					self.stop_active_audio()
				else:
					self.play_indexed_audio(message)
		except websockets.exceptions.ConnectionClosedError:
			return
	
			
	async def on_ready(self):
		self.log_info('Logged on as {0}!'.format(self.user))
		async with websockets.serve(self.echo, "localhost", 3030):
			await asyncio.Future()


	async def on_message(self, message):
		self.log_info('Message from {0.author}: {0.content}'.format(message))

		
	async def on_voice_state_update(self, member, before, after):
		if member.id == int(secret['LeaderID']):
			if after.channel is None: # Leader left the channel.
				self.log_info('Leaving voice channel')
				await self.my_voice_channel.disconnect()
				self.my_voice_channel = None
				
			else: # Leader joined a chennel.
				if self.my_voice_channel != None:
					await self.my_voice_channel.disconnect()
				self.log_info('Joining voice channel {0.channel}'.format(after))
				self.my_voice_channel = await after.channel.connect()
	

client = MyClient()
client.run(secret['BotToken'])


	
	