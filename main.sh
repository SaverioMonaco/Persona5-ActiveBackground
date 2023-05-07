#!/bin/bash
export PATH=/usr/local/bin:$PATH

FPATH=/home/saverio/Documents/P5-widget/
PYFILE=$FPATH'get_info.py'
echo $PYFILE
info=($(python3 $PYFILE))
MONTH=${info[1]}
DAY_N=${info[0]}
DAY_W=${info[2]}
WEATHER=${info[4]}
TOD=${info[3]}
info_bg=($(identify -format '%w %h' $FPATH'base.*'))
BG_WIDTH=${info_bg[0]}
BG_HEIGHT=${info_bg[1]}

if [[ $DAY_N -gt 9 ]];
then
    DAY_SHIFT=100
    WEATHER_SHIFT=60
else
    DAY_SHIFT=30
    WEATHER_SHIFT=-60
fi;

convert -page +$WEATHER_SHIFT+50 $FPATH'Assets/Weather/icons0/'$WEATHER'.png' \
-page +$DAY_SHIFT+70 $FPATH'Assets/Day/0/'$DAY_N'.png' \
-page +30+50 $FPATH'Assets/Month/0/'$MONTH'.png' \
-page +100+100 $FPATH'Assets/Week/0/'$DAY_W'.png' \
-page +30+50 $FPATH'Assets/Month/0/'$MONTH'Top.png' \
-page +$DAY_SHIFT+70 $FPATH'Assets/Day/0/'$DAY_N'Top.png' \
-page +100+100 $FPATH'Assets/Week/1/'$DAY_W'Top.png' \
-page +0+$'-20' $FPATH'Assets/ToD/'$TOD'.png' \
-background none -layers merge +repage $FPATH'icon.png'

convert -page +0+0 $FPATH'base.*' \
-page +$(($BG_WIDTH-1000))+$(($BG_HEIGHT/20)) $FPATH'icon.png' \
-background none -layers merge +repage $FPATH'background.jpg'

gsettings set org.gnome.desktop.background picture-uri-dark 'file://'$FPATH'background.jpg'

