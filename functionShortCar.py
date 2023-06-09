def shortingScore(car):
    if car.ko:
        return car.score;
    else:
        return car.score + 9999;