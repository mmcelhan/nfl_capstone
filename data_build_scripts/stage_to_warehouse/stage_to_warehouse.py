import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

madden = 0

import player_master
#import geo_master
import college_stats_build
import combine_stats_build
import college_players_build
import draft_stats_build

if madden:
    from madden_build import main as madden_main
    #madden_main()
    from madden_build import add_espn_id
    from madden_build import add_fms_id
    add_fms_id()



