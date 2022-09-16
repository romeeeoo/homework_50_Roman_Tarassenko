from random import randint
from django.shortcuts import render
from source.webapp.db import Database

MIN_AGE = 1
MAX_AGE = 18
MAX_STATS = 100
MIN_STATS = 0


def index_view(request):
    return render(request, 'index.html')


def cat_stats_view(request):
    if request.method == "GET":
        Database.cat = {
            "name": request.GET.get("name"),
            "age": randint(MIN_AGE, MAX_AGE),
            "is_asleep": False,
            "satiety": randint(MIN_STATS, MAX_STATS),
            "mood": randint(MIN_STATS, MAX_STATS),
            "avatar": "img/awake.jpg"
        }
        return render(request, 'cat_stats.html', context=Database.cat)

    elif request.method == 'POST':
        if request.POST.get("action") == "play":
            chance = randint(1, 3)
            if Database.cat.get("is_asleep") == False:
                if chance != 1:
                    Database.cat["satiety"] += 15
                    Database.cat["satiety"] -= 10
                    return render(request, 'cat_stats.html', context=Database.cat)
                else:
                    Database.cat["mood"] = 0
                    Database.cat["satiety"] -= 10
                    return render(request, 'cat_stats.html', context=Database.cat)
            else:
                Database.cat["is_asleep"] = False
                Database.cat["mood"] -= 5
                return render(request, 'cat_stats.html', context=Database.cat)

        elif request.POST.get("action") == "feed":
            if Database.cat.get("is_asleep") == False:
                Database.cat["satiety"] += 15
                if Database.cat.get("satiety") > MAX_STATS:
                    Database.cat["mood"] -= 30
                else:
                    Database.cat["mood"] += 5
                return render(request, 'cat_stats.html', context=Database.cat)
            else:
                print("Can't feed cat while is asleep")
                return render(request, 'cat_stats.html', context=Database.cat)

        elif request.POST.get("action") == "rest":
            if Database.cat.get("is_asleep") == True:
                return render(request, 'cat_stats.html', context=Database.cat)
            else:
                Database.cat["is_asleep"] = True
                Database.cat["avatar"] = "img/sleep.png"
                return render(request, 'cat_stats.html', context=Database.cat)
