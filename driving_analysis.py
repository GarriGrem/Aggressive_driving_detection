def analysis(distance, speed, acceleration):
    if distance < 3 and distance != 0 \
            or speed > 60 \
            or 20 < acceleration < -20:
        rating = 'aggressive'
        return rating
    else:
        rating = 'safe'
        return rating
