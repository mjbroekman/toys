import os
import discord
import re
import time
import random
import requests
import json
import emoji
from replit import db


client = discord.Client()
if 'url_words' not in db.keys():
  db['url_words'] = ['discord', 'steam', 'nitro', '.ru']

def send_command(command):
    commands = [
      '$help', '$hello', '$hi', '$howdy', '$sup', '$commands', '$youtube',
      '$github', '$replit', '$random', '$socials', '$quote', '$quotes',
      '$addquote', '$delquote', '$listquotes', '$checkurl', '$listurls',
      '$addurl', '$delurl'
    ]

    if command in ['$help', '$commands']:
      return 'These are the commands I understand:\n' + ', '.join(commands) + \
             '\n\nI also respond to questions or if you mention me.\n\n' + \
             'If you say "pass the ", I will try to give it to you or ' + \
             'someone else. If possible, I will even turn it into emoji.'

    if command in ['$hello', '$hi', '$howdy', '$sup']:
      return "'" + command[1:].title() + "' yourself, bucko."

    if command in ['$youtube']:
      return "My author's YouTube channel is: https://www.youtube.com/c/MaartenBroekman"

    if command in ['$github']:
      return "My author's GitHub page is: https://github.com/mjbroekman"

    if command in ['$replit']:
      return "My author's ReplIt page is: https://replit.com/@mjbroekman/"

    if command in ['$socials']:
      return 'You can find my author at:\n' + \
             '* https://www.youtube.com/c/MaartenBroekman\n' + \
             '* https://github.com/mjbroekman\n' + \
             '* https://replit.com/@mjbroekman/'

    if command in ['$quote']:
      return get_quote()

    if command.startswith('$addquote'):
      return add_quote(command)

    if command.startswith('$delquote'):
      return del_quote(command)

    if command in ['$quotes', '$listquotes']:
      if 'quotes' in db.keys():
        if len(db['quotes']) > 0:
          return "Current stored quotes:\n* " + "\n* ".join(db['quotes'])
      return "There are no quotes stored in the bot yet. " + \
             "Using the $quote command will get quotes from " + \
             "https://quotable.io.\n" + \
             "Using $addquote will add quotes to the bot."

    if command.startswith('$random'):
      return get_random(command)

    if command.startswith('$listurl'):
      if 'url_words' in db.keys():
        if len(db['url_words']) > 0:
          return "URL 'words' to watch out for:\n" + ', '.join(db['url_words'])

      return "There are no 'words' that we are looking for in URLs."

    if command.startswith('$addurl'):
      return add_url(command.replace('$addurl ',''))

    if command.startswith('$delurl'):
      return del_url(command.replace('$delurl ',''))
      
    if command.startswith('$checkurl'):
      return check_url(command.replace('$checkurl ',''))

    return "What was that? I didn't understand that command:\n\t" + command + "\n\nTry $help"

def add_url(url):
  if 'url_words' not in db.keys():
    db['url_words'] = []

  if url not in db['url_words']:
    db['url_words'].append(url)
    return "Adding '" + url + "' to URL 'words' list\nNew list:\n" + ', '.join(db['url_words'])

  return "'" + url + "' is already present in the words list\nList:\n" + ', '.join(db['url_words'])

def del_url(url):
  if 'url_words' not in db.keys():
    db['url_words'] = []

  if url in db['url_words']:
    db['url_words'].remove(url)
    return "Removing '" + url + "' from URL 'words' list\nNew list:\n" + ', '.join(db['url_words'])

  return "'" + url + "' is not present in the words list\nList:\n" + ', '.join(db['url_words'])


def check_url(url):
  print("Checking " + url)

  api_key = {'API-Key': os.environ['API_TOKEN'],'Content-Type':'application/json'}
  data = {"url": url, "visibility": "public"}
  response = requests.post('https://urlscan.io/api/v1/scan/',headers=api_key, data=json.dumps(data))
  
  resp_json = json.loads(response.text)
  print(resp_json)

  if 'api' in resp_json.keys():
    result_url = resp_json['api']
    result = requests.get(result_url)
  else:
    return "Unable to get a response"

  print('Waiting for ' + result_url)
  while result.status_code != requests.codes.ok:
    time.sleep(5.0)
    result = requests.get(result_url)

  print("Done waiting...")

  result_json = json.loads(result.text)

  if 'requests' not in result_json['data'].keys():
    return "URL Safe? False (unable to find 'requests' block)"

  for request in result_json['data']['requests']:
    resp_found = True
    if request['response']['dataLength'] > 0:
      break

    resp_found = False
      
  if not resp_found:
    return "URL Safe? False (unable to find valid responses)"
    
  if 'verdicts' in result_json.keys():
    safety = False
    for verdict in result_json['verdicts']:
      safety = safety or result_json['verdicts'][verdict]['malicious']
      print(verdict + ' malicious = ' + str(result_json['verdicts'][verdict]['malicious']))

  return "URL Safe? " + str(not safety)


def get_random(command):
  if command == '$random':
    return "Here's a random number: " + str(
            random.randint(0, int(time.time())))

  num1 = re.match(r'.random (-?\d+)$', command)
  nums = re.match(r'.random (-?\d+) (-?\d+)', command)
  if num1 is not None:
    if int(num1.group(1)) > 0:
      return "Here's a random number between 0 and " + num1.group(1) + \
             ":\n\t" + str(random.randint(0, int(num1.group(1))))
    if int(num1.group(1)) < 0:
      return "Here's a random number between " + num1.group(1) + \
             "and 0:\n\t" + str(random.randint(int(num1.group(1)), 0))

    return "That's not very random, don't you think?"

  if nums is not None:
    if int(nums.group(1)) < int(nums.group(2)):
      return "Here's a random number between " + nums.group(1) + \
             " and " + nums.group(2) + ":\n\t" + \
             str(random.randint(int(nums.group(1)), int(nums.group(2))))

    if int(nums.group(1)) > int(nums.group(2)):
      return "Here's a random number between " + nums.group(2) + \
             " and " + nums.group(1) + ":\n\t" + \
             str(random.randint(int(nums.group(2)), int(nums.group(1))))

    return "That's not very random, don't you think?"

  return "I didn't find numbers in there to generate random numbers with."


def add_quote(command):
  quote_text = command.replace('$addquote ','')
  if quote_text.startswith('-'):
    return "Don't start your quote with a -. I will automatically add the attribution."

  if 'quotes' not in db.keys():
    db['quotes'] = []

  if quote_text in db['quotes']:
    return "That quote is already stored locally"

  db['quotes'].append(quote_text)
  return "Added quote to local storage."


def del_quote(command):
  quote_text = command.replace('$delquote ','')

  if 'quotes' not in db.keys():
    return "No quotes stored locally"

  if quote_text not in db['quotes']:
    return "Unable to find quote to delete. Did you type it correctly?"
  
  db['quotes'].remove(quote_text)
  return "Removed quote: '" + quote_text + "'"

  
def get_quote():
  if random.randint(0,1) == 0 or 'quotes' not in db.keys() or len(db['quotes']) < 1:
    try:
      response = requests.get("https://quotable.io/random")
      quote_data = json.loads(response.text)
      return quote_data['content'] + ' -' + quote_data['author']
    except Exception as e:
      return "There was a problem getting quotes from https://quotable.io/random" + str(e)
  else:
    if 'quotes' in db.keys():
      return db['quotes'][random.randint(0,(len(db['quotes']) - 1))]
      

def check_words(word_string,target):
  print('Checking words for emoji: ' + word_string)
  print('Targeting ' + target)
  try:
    if " " in word_string:
      if len(emoji.emojize(':' + word_string.replace(' ','_') + ':')) != len(':' + word_string + ':'):
        return "Passing :" + word_string.replace(' ','_') + ": to " + target
  
    new_string = 'Passing'
    for word in word_string.split(' '):
      if len(emoji.emojize(':' + word + ':')) != len(':' + word + ':'):
        new_string = new_string + " :" + word + ":"
      else:
        new_string = new_string + " " + word
    return "" + new_string + " to " + target
  except Exception as e:
    return 'Ran into an error: ' + str(e)


@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  try:
    if message.author == client.user:
      return

    if message.content.startswith('$'):
      command = message.content
      print('Received a command: ' + message.content)
      if command.startswith('$addquote'):
        command = command + " -" + message.author.display_name

      command_resp = send_command(command)
      await message.channel.send(command_resp)

      if command.startswith('$checkurl') and 'False' in command_resp:
        await message.channel.send('Unsafe URL detected!')
        await message.delete()
      return

    if "pass the " in message.content.lower():
      print('Passing something...', end='')
      passing = re.match(r'.*pass the (.+)', message.content, re.I)
      passto = re.match(r'.*pass the (.+) to (\S+)', message.content, re.I)
      print(' ... maybe a ' + passing.group(1))

      if passing is not None and passto is None:
        await message.channel.send(check_words(passing.group(1), message.author.display_name))
        return
      elif passto is not None:
        await message.channel.send(check_words(passto.group(1), passto.group(2)))
        await message.channel.send("Don't forget to thank " + \
                                   message.author.display_name + " for this.")
        return
      else:
        print('Asked for ' + message.content + "\n\nFound " + passing)
        await message.channel.send('What on earth?\n\nHow do you expect me to pass that?!')
      return

    if "http://" in message.content.lower() or "https://" in message.content.lower():
      url = re.search('(https?://\S+)',message.content,re.I)
      if any(word in url.group(1) for word in db['url_words']):
        result = check_url(url.group(1))
        if 'False' in result:
          await message.channel.send('Unsafe URL detected. Buh-bye!')
          await message.delete()
      return

    if message.content.endswith('?'):
      print('Saw a question... time to give some backtalk...')
      await message.channel.send('Oh. My. Gawd... why would you ask me that?')
      await message.channel.send('Who asks someone else: "' + message.content + '"?')
      return

    if client.user in message.mentions:
      print('I got mentioned...')
      await message.channel.send('What? Do you need $help or something?')
      return

  except Exception as e:
    await message.channel.send('Uh oh. There was a problem ...\n\nTake a look at THAT:\n' + str(e))
    return

try:
  client.run(os.environ['CLIENT_TOKEN'])
except Exception as e:
  print('There is a problem running the client. Did you make sure to set the CLIENT_TOKEN environment variable?')
  print(e)

