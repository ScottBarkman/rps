from sys import argv
import readline
import random
import re
import operator
options = ('r', 'p', 's')

#weighting
overall_weight = 1
player_sequence_weight = 1
comp_sequence_weight = 1.2

# how deep to look for sequences
layersdeep = 3

#how many hands in a row to start mixing things up
heat_detection = 3

player_history = my_history =  ''
player_wins = 0
playerscore = 0
scores = {'you': 0, 'me': 0}
colors = {'lose' : '\033[91m%s\033[0m', 'win': '\033[92m%s\033[0m'}
score = {'rr': 0, 'pp': 0, 'ss': 0, 'pr': 1, 'rs': 1, 'sp': 1, 'rp':-1, 'sr':-1, 'ps': -1}
beat_lookup = {'r': 'p', 'p': 's', 's': 'r'}
general_percentages = {'r': 0, 'p': 0, 's': 0}

throw_percentages = {'r': 30, 's': 35, 'p': 35}

suggested_throw = {'r': 0, 's': 0, 'p':0}


print " ========================= "
print "         WELCOME"
print " Choose 'r', 'p' or 's'    "
print " ========================= "
while True:
    # choose what to throw
    player_throw = raw_input('> ').lower()

    if player_throw in options:

        suggested_throw = {'r': 0, 's': 0, 'p':0}

        if len(player_history) > 5:
            # start using determining factors

            #overall throwing percentages
            for t in throw_percentages:
                throw_percentages[t] = float(player_history.count(t))/float(len(player_history))*100

            rank = sorted(throw_percentages.items(), key=operator.itemgetter(1))
            suggested_throw[beat_lookup[rank[2][0]]]+=(rank[2][1]-33)*((float(0)/float(10))+overall_weight)
            # followup percentages (if user throws rock, at what frequency does he follow up with s?)

            for i in range(1, layersdeep+1):
                layercounts = {'r': 0, 'p': 0, 's': 0}
                layer_percentages = {'r': 0, 'p': 0, 's': 0}
                positions = [m.start() for m in re.finditer(player_history[-i:], player_history[:-1])]
                for p in positions:
                    if player_history[(p+i)]:
                        layercounts[player_history[(p+i)]]+=1

                if len(positions):
                    for l in layercounts:
                        layer_percentages[l] = (float(layercounts[l])/float(len(positions)))*100

            rank = sorted(layer_percentages.items(), key=operator.itemgetter(1))

            suggested_throw[beat_lookup[rank[-1][0]]]+=(rank[-1][1])*((float(0)/float(10))+(player_sequence_weight))

            #comp followup percentages - (If I throw rock, at what frequency does he follow up with s?)
            for i in range(1, layersdeep+1):
                layercounts = layer_percentages = {'r': 0, 'p': 0, 's': 0}
                positions = [m.start() for m in re.finditer(my_history[-i:], my_history[:-1])]
                for p in positions:
                    try:
                        if player_history[((p+i)+1)]:
                            layercounts[player_history[((p+i))]]+=1
                    except:
                        pass

                if len(positions):
                    for l in layercounts:
                        layer_percentages[l] = (float(layercounts[l])/float(len(positions)))*100


            # heat_meter few wins in a row? they're adapting!!
            heatscore = 0
            # for i in range(1, heat_detection):
            #     print i
            #     if int(score['%s%s' % (player_history[-i:1], my_history[-i:1])]):
            #         heatscore += 1


            rank = sorted(layer_percentages.items(), key=operator.itemgetter(1))

            suggested_throw[beat_lookup[rank[-1][0]]]+=(rank[-1][1])*((float(0)/float(10))+(comp_sequence_weight))


            sorted_suggested = sorted(suggested_throw.items(), key=operator.itemgetter(1))
            # print sorted_suggested

            if heatscore == heat_detection:
                my_throw = beat_lookup(sorted_suggested[2][0])
            else:
                my_throw = sorted_suggested[2][0]
        else:
            my_throw = random.choice(options)

        player_history+=player_throw
        my_history += my_throw


        roundscore = int(score['%s%s'%(player_throw, my_throw)])
        if roundscore > 0:
            player_wins += 1

        playerpercentage = "%.2f" % (100*float(player_wins)/len(player_history))

        playerscore += roundscore
        if playerscore > 0:
            playercolor = colors['win']
        elif playerscore < 0:
            playercolor = colors['lose']
        else:
            playercolor = '%s'

        if roundscore > 0:

            print str('You -> '+colors['win']+' - '+colors['lose']+' <- Me (Score: '+playercolor+' - %s%%)') % (player_throw.upper(), my_throw.upper(), playerscore, playerpercentage)
        elif roundscore < 0:
            print str('You -> '+colors['lose']+' - '+colors['win']+' <- Me (Score: '+playercolor+' - %s%%)') % (player_throw.upper(), my_throw.upper(), playerscore, playerpercentage)
        else:
            print str('You -> %s - %s <- Me (Score: '+playercolor+' - %s%%)') % (player_throw.upper(), my_throw.upper(), playerscore, playerpercentage)


    elif player_throw == 'debug':
        print '==================================='
        print 'Player History: \033[92m%s\033[0m' % player_history
        print 'Play Percentages: \033[92m%s\033[0m ' % throw_percentages
        print 'Last Suggested Throw: \033[92m%s\033[0m' % sorted_suggested
        print '==================================='
    elif player_throw == 'quit':
        break
    else:
        print 'Invalid throw'
