import pytesseract, re, discord, random                                                  #
from PIL import ImageGrab, ImportError                                                   #
from discord.ext import compile                                                          #
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract' #
##########################################################################################

client = commands.Bot(command_prefix="!")
@client.event

# Turn on the Discord-bot and start extracting queue time
async def on_ready():
    await queue_alert()
def get_current_time(img):
    # Get the correct size for your monitor, remove the colors from the pic and saturate it
    # So it's easier for tesseract to read. You can also adjust the 'conf' (confidence) level.
    width, height = img.size
    left = 750
    top = 390
    right = 1180
    bottom = 510
    img = img.crop((left, top, right, bottom))
    img = img.point(lambda p: p > 170 and 200)
    img = ImageEnhance.Color(img).enhance(0)

    # Extract text with tesseract
    imgData = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    imgText = ' '.join([x for i,x in enumerate(imgData['text']) if int(imgData['conf'][i]) >= 41])

    # Extract minutes remaning with regex
    imgTime = re.search(r'time[^\d+]*(\d+)', imgText)
    
    # img.show();
    # print(f'Nåværende minutter igjen: {imgTime.group(1)}')

    # Return minutes in number back to the scanner
    if imgTime:
        return int(imgTime.group(1))


async def sendMsg():
    #To get ætted (@) include your discord id after the @
    discordUserID= '<@<yourDiscordID>>'
    arrayOfMsgs=[
        ("You are up next, "+discordUserID+ "! :fire: "),
        ("5 minute warning "+discordUserID+"!"),
        (":speaking_head: RING I BJELLA "+discordUserID+"!!, baby! :sunglasses:"),
        (":military_helmet: Get ready "+discordUserID+"! :gun:"),
        ("Rise and shine, "+discordUserID+"! queue is about to pop! :triumph: "),
        ("Queue-pop = :right_fist: Blågutt + Blåveis :left_fist: , "+discordUserID+"!"),
        ("Let's goooo, "+discordUserID+ "!! :exploding_head: :exploding_head: "),
        (":people_hugging: Endelig... "+discordUserID+", endelig ferdig."),
        ("Ready-set! :man_police_officer: , "+discordUserID+"!"),
        ("Se, "+discordUserID+" du er først i køen!")
        
        ]
    msg = random.choice(arrayOfMsgs)
    await client.get_channel(482607392576634883).send(msg)

#Final function to monitor the queue
import time
async def queue_alert(alertAtMinute=5, scanSeconds=5):
    print('\nScanning the queue. Click CTRL+C to stop.')
    counter = 0
    while True:
        # Capture screenshot of the queue 
        time.sleep(scanSeconds)
        img = ImageGrab.grab()
        # Extract the queue time
        minutesLeft = get_current_time(img)

        #Send the message once the minutes in the queue is lower or equal to your treshold
        if not minutesLeft:
            print(f'Could not extract queue, adjust the display parameters')
        else:
            if minutesLeft <= alertAtMinute:
                counter+=1
                await sendMsg()              
        # Stop after 5 messages and break
        if counter > 5:
            break

# Your discord-bots ID 
client.run(<"clientID">)
