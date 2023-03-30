const { Client, GatewayIntentBits, Partials } = require("discord.js");
const { joinVoiceChannel } = require("@discordjs/voice");
const { addSpeechEvent } = require("discord-speech-recognition");
const { token } = require('./config.json');

const client = new Client({
    intents: [
        GatewayIntentBits.DirectMessages,
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildBans,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
      ],
      partials: [Partials.Channel],
});
addSpeechEvent(client);

client.on("messageCreate", (msg) => {
    const voiceChannel = msg.member?.voice.channel;
    if (voiceChannel) {
        joinVoiceChannel({
        channelId: voiceChannel.id,
        guildId: voiceChannel.guild.id,
        adapterCreator: voiceChannel.guild.voiceAdapterCreator,
        selfDeaf: false,
        });
    }
});

client.on("speech", (msg) => {
  // If bot didn't recognize speech, content will be empty
  console.log(msg.content);
  if (!msg.content) return;

  msg.author.send(msg.content);
});

client.on("ready", () => {
  console.log("Ready!");
});

client.login(token);