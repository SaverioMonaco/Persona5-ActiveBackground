#!/bin/bash
export PATH=/usr/local/bin:$PATH

FPATH=/home/saverio/Documents/P5-widget/
PYFILE=$FPATH'get_info.py'
info=($(python3 $PYFILE))
last_run_info=($(cat $FPATH'lastinfo'))
A=${info[@]};
B=${last_run_info[@]};
if [ "$A" != "$B" ] ; then
    echo ${info[0]} ${info[1]} ${info[2]} ${info[3]} ${info[4]} > $FPATH'lastinfo'
    MONTH=${info[1]}
    DAY_N=${info[0]}
    DAY_W=${info[2]}
    WEATHER=${info[4]}
    TOD=${info[3]}
    
    BASE_IMG=$FPATH'base'
    if test ! -f "$BASE_IMG".*; then
        if [[ $TOD -lt 4 ]]; then
            if [ "$WEATHER" = "Clear" ]; then
                BASE_IMG=$FPATH'bases/day_clear'
            else
                BASE_IMG=$FPATH'bases/day_cloud'
            fi
        else
            if [ "$DAY_W" = "Sunday" || "$DAY_W" = "Saturday" ]; then
                BASE_IMG=$FPATH'bases/night_alt'
            else
                BASE_IMG=$FPATH'bases/night'
            fi
        fi
    fi
    
    info_bg=($(identify -format '%w %h' $BASE_IMG'.*'))
    BG_WIDTH=${info_bg[0]}
    BG_HEIGHT=${info_bg[1]}
    info_ratios=($(cat $FPATH'ratios'))
    RATIO_WIDTH=${info_ratios[0]}
    RATIO_HEIGHT=${info_ratios[1]}

    if [[ 10#$DAY_N -gt 9 ]];
    then
        DAY_SHIFT=100
        WEATHER_SHIFT=60
    else
        DAY_SHIFT=30
        WEATHER_SHIFT=-70
    fi;

    convert -page +$DAY_SHIFT+70 $FPATH'Assets/Day/'$DAY_N'Bottom.png' \
    -page +30+50 $FPATH'Assets/Month/'$MONTH'Bottom.png' \
    -page +100+90 $FPATH'Assets/Week/'$DAY_W'.png' \
    -page +$WEATHER_SHIFT+60 $FPATH'Assets/Weather/'$WEATHER'.png' \
    -page +$DAY_SHIFT+70 $FPATH'Assets/Day/'$DAY_N'.png' \
    -page +30+50 $FPATH'Assets/Month/'$MONTH'.png' \
    -page +30+50 $FPATH'Assets/Month/'$MONTH'Top.png' \
    -page +$DAY_SHIFT+70 $FPATH'Assets/Day/'$DAY_N'Top.png' \
    -page +100+90 $FPATH'Assets/Week/'$DAY_W'Top.png' \
    -page +0+10 $FPATH'Assets/ToD/'$TOD'.png' \
    -background none -layers merge +repage $FPATH'icon.png'

    convert -trim $FPATH'icon.png' $FPATH'icon.png'

    convert -page +0+0 $BASE_IMG'.*' \
    -page +$(($BG_WIDTH*$RATIO_WIDTH))+$(($BG_HEIGHT*$RATIO_HEIGHT)) $FPATH'icon.png' \
    -background none -layers merge +repage $FPATH'background.jpg'

    gsettings set org.gnome.desktop.background picture-uri-dark 'file://'$FPATH'background.jpg'
fi;


