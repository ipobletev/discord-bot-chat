
import asyncio
import io
import os
import subprocess
import discord
import shlex

class FFmpegPCMAudio(discord.AudioSource):
    
    def __init__(self, source, *, executable='ffmpeg', pipe=False, stderr=None, before_options=None, options=None, frame_size=3840):
        self.frame_size = frame_size
        stdin = None if not pipe else source
        args = [executable]
        if isinstance(before_options, str):
            args.extend(shlex.split(before_options))
        args.append('-i')
        args.append('-' if pipe else source)
        args.extend(('-f', 's16le', '-ar', '48000', '-ac', '2', '-loglevel', 'warning'))
        if isinstance(options, str):
            args.extend(shlex.split(options))
        args.append('pipe:1')
        self._process = None
        try:
            self._process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr)
            self._stdout = io.BytesIO(
                self._process.communicate(input=stdin)[0]
            )
        except FileNotFoundError:
            raise discord.ClientException(executable + ' was not found.') from None
        except subprocess.SubprocessError as exc:
            raise discord.ClientException('Popen failed: {0.__class__.__name__}: {0}'.format(exc)) from exc
    def read(self):
        ret = self._stdout.read(self.frame_size)
        if len(ret) != self.frame_size:
            return b''
        return ret
    def cleanup(self):
        proc = self._process
        if proc is None:
            return
        proc.kill()
        if proc.poll() is None:
            proc.communicate()

        self._process = None
            
class BotAudioPlayer:
    def __init__(self, bot):
        self.bot = bot
        self.audio_queue = asyncio.Queue()

    async def setup(self):
        self.bot.loop.create_task(self.thread_bot_audio_player())
        
    async def play_audio(self, file_name, user):
        await self.audio_queue.put(file_name)
        self.audio_queue.user = user

    async def stop_audio(self):
        while not self.audio_queue.empty():
            self.audio_queue.get_nowait()
        self.audio_queue.user = None
       
    async def thread_bot_audio_player(self):
        while True:
            file_name = await self.audio_queue.get()
            if file_name is None:
                break
            
            user = self.audio_queue.user
            channel = user.voice.channel
            vc = discord.utils.get(self.bot.voice_clients, guild=user.guild)
            
            if not vc:
                vc = await channel.connect()
            
            if vc.is_playing():
                vc.stop()
            
            mp3_fp = open(file_name, 'rb')
            stream = FFmpegPCMAudio(mp3_fp.read(), pipe=True)
            
            vc.play(stream)
            
            while vc.is_playing():
                await asyncio.sleep(0.4)
            
            # os.remove(file_name)
            
            mp3_fp.close()
            self.audio_queue.task_done()