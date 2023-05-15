
# %%

from PIL import Image
import os, csv
from datetime import date
import time
import requests

try:
    PREFIX = os.path.realpath(__file__)
except:  # maybe you are running this in a notebook/ipykernel...
    PREFIX = '.'

# fix empty prefix
if PREFIX == '':  PREFIX = '.'

path = os.path.dirname(PREFIX)

# icon placement options -------------
icon_offset = (0.76, 0.05)  # percent of background picture size
icon_newsize = 0.2          # percent of background picture horizontal size


# %%

class assets:
    # define assets files
    WEATHER      = path+'/Assets/Weather/{}.png'
    DAY_BOTTOM   = path+'/Assets/Day/{}Bottom.png'
    DAY          = path+'/Assets/Day/{}.png'
    DAY_TOP      = path+'/Assets/Day/{}Top.png'
    WEEK         = path+'/Assets/Week/{}.png'
    WEEK_TOP     = path+'/Assets/Week/{}Top.png'
    MONTH_BOTTOM = path+'/Assets/Month/{}Bottom.png'
    MONTH        = path+'/Assets/Month/{}.png'
    MONTH_TOP    = path+'/Assets/Month/{}Top.png'
    TOD          = path+'/Assets/ToD/{}.png'


def get_weather_identifier():
    """Request weather info to openweathermap. Handles request errors, returning 'None'."""
    weather = get_pred_identifier()[-1] # return previous weather if next lines of code fail

    if os.path.exists( path + '/weather/'):
        weather_location = open( path + '/weather/location.info', "r").read()
        weather_token    = open( path + '/weather/token.info', "r").read()

        url_weather = f'https://api.openweathermap.org/data/2.5/weather?q={weather_location}&appid={weather_token}&units=metric'.replace('\n','')
        try:
            weather = requests.get(url_weather).json()['weather'][0]['main']
        except Exception as err:
            print('ERROR (non-fatal): weather request has failed, skipping.')
            print(err)
    else:
        print('WARNING: weather configuration folder does not exist, skipping weather request.')

    # some adjustments
    if weather == 'Thunderstorm':
        weather = 'Rain'
    elif weather == 'Drizzle':
        weather = 'Rain'
    elif weather == 'Atmosphere':
        weather = 'Clouds'
    elif weather == 'Mist':
        weather = 'Clouds'

    return weather


def get_time_identifier():
    """Get the date identifiers, as requested by the rest of the script."""
    today = date.today()
    day   = today.strftime("%d")
    month = today.strftime("%m")
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    week  = today.weekday()

    hour  = int(time.strftime("%H", time.localtime()))
    if   hour >= 3 and hour < 9:
        TOD = '0'
    elif hour >= 9 and hour < 13:
        TOD = '1'
    elif hour >= 13 and hour < 16:
        TOD = '2'
    elif hour >= 16 and hour < 19:
        TOD = '3'
    else:
        TOD = '4'

    if hour >= 5 and hour < 8:
        BG='sunrise'
    elif hour >= 8 and hour < 18:
        BG='day'
    elif hour >= 18 and hour < 21:
        BG='sunset'
    else:
        BG='night'  
        if week == 5:
            BG = 'night_saturday'
        elif week == 6:
            BG = 'night_sunday'

    return day, month, weekdays[week], TOD, BG

def get_pred_identifier():
    try:
        with open(path+'/lastinfo', 'r') as file:
            reader = csv.reader(file)
            # We only need to read the first row
            for row in reader:
                return tuple(row)
    except:
        return (0, 0, 0, 0, 0, 0)

def write_to_lastinfo(list):
    with open(path+'/lastinfo', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(list)

def make_icon_composition(DAY_N, MONTH, DAY_W, TOD, WEATHER = 'None', DAY_SHIFT = 0, WEATHER_SHIFT = 0):
    """Compose the Persona-style icon with the given parameters."""

    composition = Image.new('RGBA', (900, 653))  # this is determined by assets files
    composition.alpha_composite( Image.open(assets.DAY_BOTTOM.format(DAY_N)), (DAY_SHIFT,70))
    composition.alpha_composite( Image.open(assets.MONTH_BOTTOM.format(MONTH)), (30,50))
    composition.alpha_composite( Image.open(assets.WEEK.format(DAY_W)), (100,100))
    if WEATHER != 'None':
        composition.alpha_composite( Image.open(assets.WEATHER.format(WEATHER)), (WEATHER_SHIFT,50))
    composition.alpha_composite( Image.open(assets.DAY.format(DAY_N)), (DAY_SHIFT,70))
    composition.alpha_composite( Image.open(assets.MONTH.format(MONTH)), (30,50))
    composition.alpha_composite( Image.open(assets.MONTH_TOP.format(MONTH)), (30,50))
    composition.alpha_composite( Image.open(assets.DAY_TOP.format(DAY_N)), (DAY_SHIFT,70))
    composition.alpha_composite( Image.open(assets.WEEK_TOP.format(DAY_W)), (100,100))
    composition.alpha_composite( Image.open(assets.TOD.format(TOD)), (0,-20))
    return composition



# %% make the icon

# get the parameters of the icon and base background
DAY_N, MONTH, DAY_W, TOD, BG = get_time_identifier()
WEATHER = get_weather_identifier()

PRED_DAY_N, PRED_MONTH, PRED_DAY_W, PRED_TOD, PRED_BG, PRED_WEATHER = get_pred_identifier()

#  if anychanges = True, this execution is no different than the previous and the code can end here
#  if false, we need to update the wallpaper
anychanges = not ( [DAY_N, MONTH, DAY_W, TOD, BG, WEATHER] == [PRED_DAY_N, PRED_MONTH, PRED_DAY_W, PRED_TOD, PRED_BG, PRED_WEATHER] )

if anychanges:
    write_to_lastinfo([DAY_N, MONTH, DAY_W, TOD, BG, WEATHER])
    # I/O: background file
    bgfile_in  = path+f'/bases/{BG}.jpeg' # input
    bgfile_out = path+'/background.jpg' # composed

    if int(DAY_N) > 9:
        DAY_SHIFT=100
        WEATHER_SHIFT=60
    else:
        DAY_SHIFT=30
        WEATHER_SHIFT=-60

    # generate icon
    icon = make_icon_composition(DAY_N, MONTH, DAY_W, TOD, WEATHER, DAY_SHIFT, WEATHER_SHIFT)
    icon

    background = Image.open( bgfile_in )
    bgw, bgl = background.size

    icon_ratio = icon.size[0]/icon.size[1]
    new_icon_width = int(bgw*icon_newsize)
    icon_resized = icon.resize( (new_icon_width, int(new_icon_width/icon_ratio)))

    # merge background with icon
    background.paste(icon_resized, (int(bgw*icon_offset[0]), int(bgl*icon_offset[1])), icon_resized)
    if WEATHER != 'Clear':
        CBG = 'night' if BG[:5] == 'night' else 'day'
        
        CLOUDS_PATHS = [path+f'/bases/clouds/{CBG}/cloud{i+1}.png' for i in range(3)]
        XS, YS = [.1, .4, .65], [.5, .05, .05]
        for i, CLOUD_PATH in enumerate(CLOUDS_PATHS):
            CLOUD = Image.open( CLOUD_PATH ).convert("RGBA")
            background.paste(CLOUD, (int(XS[i]*bgw), int(YS[i]*bgl)), CLOUD)
    background

    if bgfile_out is not None:
        background.save( bgfile_out )

    bashcommand = f'gsettings set org.gnome.desktop.background picture-uri-dark \'file://{path}/background.jpg\''
    os.system(bashcommand) 

