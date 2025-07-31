# NOTE:
# Run this script to test out your code!
# Everything below here is for testing, you don't need to edit it.

from rich import print
from level_5_code import *
import asyncio
import threading
import time
import os
import re
from rich import print
from twitchio.ext import commands
from twitchio import *

TWITCH_MOD_OAUTH_TOKEN = os.getenv('TWITCH_MOD_ACCESS_TOKEN')

class BitsBot(commands.Bot):

    def __init__(self):
        super().__init__(token=TWITCH_MOD_OAUTH_TOKEN, prefix='?', initial_channels=[CHANNEL_NAME])
        
        # Initialize the donation queue and processing flag
        self.donation_queue = asyncio.Queue()
        self.queue_consumer_task = None
    
    async def event_ready(self):
        print(f'[green]Logged into Twitch as {self.nick}')
        self.my_channel = await self.fetch_users(names=[CHANNEL_NAME])
        
        # Start the donation queue consumer
        self.queue_consumer_task = asyncio.create_task(self.donation_queue_consumer())
    
    async def donation_queue_consumer(self):
        """
        Consumer coroutine that processes donations from the queue sequentially.
        This ensures only one donation is processed at a time.
        """
        print(f'[blue]Ready to process donations...\n')
        
        while True:
            try:
                # Wait for a donation to appear in the queue
                donation_data = await self.donation_queue.get()
                
                # Extract the donation information
                user_message, username, bits_amount, is_subscribed = donation_data

                # Remove the "CheerX" bits from the message
                user_message = re.sub(r'Cheer\d+', '', user_message).strip()
                
                # Process the donation (this will block until complete)
                bits_donated(user_message, username, bits_amount, is_subscribed)
                
                # Mark the task as done
                self.donation_queue.task_done()
                
                # print(f'[cyan]Finished processing donation for {username}')
                
            except Exception as e:
                print(f'[red]Error processing donation from queue: {e}')
                # Mark the task as done even if there was an error
                self.donation_queue.task_done()
    
    async def get_queue_status(self):
        """Returns current queue status for monitoring"""
        return {
            'queue_size': self.donation_queue.qsize(),
            'is_consumer_running': self.queue_consumer_task and not self.queue_consumer_task.done()
        }
    
    async def shutdown_queue_consumer(self):
        """Gracefully shutdown the queue consumer"""
        if self.queue_consumer_task:
            print(f'[yellow]Shutting down donation queue consumer...')
            self.queue_consumer_task.cancel()
            try:
                await self.queue_consumer_task
            except asyncio.CancelledError:
                print(f'[green]Donation queue consumer shutdown complete')
    
    def is_user_subscribed(self, message):
        """Check if the user is a subscriber using badges and tags"""
        # Check badges first (most reliable)
        if hasattr(message.author, 'badges'):
            badges = message.author.badges or {}
            if 'subscriber' in badges:
                return True
        # Fallback to tags
        if hasattr(message, 'tags'):
            tags = message.tags or {}
            subscriber_tag = tags.get('subscriber', '0')
            return subscriber_tag == '1'
        return False
    
    def extract_bits_from_message(self, message):
        """Extract bits amount from a message if it contains bits/cheers"""
        bits_amount = 0
        
        # Check if message has bits tag (most reliable method)
        if hasattr(message, 'tags') and message.tags:
            bits_tag = message.tags.get('bits')
            if bits_tag:
                try:
                    bits_amount = int(bits_tag)
                    return bits_amount
                except (ValueError, TypeError):
                    pass
        
        # Fallback: Look for cheer emotes in the message content
        if message.content:
            words = message.content.lower().split()
            for word in words:
                # Common cheer patterns: cheer100, kappa50, pogchamp25, etc.
                import re
                # Match anything that starts with a common cheer patern followed by a number
                match = re.search(r'^(cheer|kappa|pogchamp)(?P<bits>\d+)$', word)
                if match:
                    try:
                        bits_amount += int(match.group('bits'))
                    except (ValueError, TypeError):
                        pass
        
        return bits_amount
    
    async def event_message(self, message):
        await bot.process_message(message)

    async def process_message(self, message: Message):
        username = message.author.name
        user_message = message.content
        
        # Check for bits donation
        bits_amount = self.extract_bits_from_message(message)
        if bits_amount > 0:
            # Add donation to queue instead of processing immediately
            donation_data = (user_message, username, bits_amount, self.is_user_subscribed(message))
            await self.donation_queue.put(donation_data)
            
            # print(f'[yellow]🎯 Donation queued: {username} - {bits_amount} bits (Queue size: {self.donation_queue.qsize()})')
                
def startBot():
    global bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot = BitsBot()
    bot.run()

if __name__=='__main__':
    
    bot_thread = threading.Thread(target=startBot)
    bot_thread.start()

    while True:
        time.sleep(600)