#!/usr/bin/env python

# To test: "flask run"

import json
from flask import Flask, request
from flask import render_template, make_response
import urllib

import pickle
import joblib
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, AdaBoostClassifier, ExtraTreesClassifier, VotingClassifier
import pandas as pd
import itertools as it

application = Flask(__name__)

def z_score(data_mean, data_std, val):
    '''Returns a single z-scored result'''
    return (val - data_mean) / data_std

def scale_it(in_value, in_conf):
    if in_conf == 'sec':
        return in_value*1
    if in_conf == 'acc':
        return in_value*0.9
    if in_conf == 'big_10':
        return in_value*0.95
    if in_conf == 'pac_12':
        return in_value*0.9
    if in_conf == 'big_12':
        return in_value*0.85
    if in_conf == 'mountain_west':
        return in_value*0.8
    return in_value*0.7

def z_list(in_list, cols, stats_df):
    '''Returns z-scored list'''
    out_list = []
    scaled = "scaled"

    for i, c in zip(in_list, cols):
        if c == 'conference':
            out_list.append(i)
            continue
        if scaled in c:
            val = scale_it(i, out_list[0])
            mean = stats_df[c][0]
            sd = stats_df[c][1]
            out_list.append(z_score(mean,sd,val))
            continue
        mean = stats_df[c][0]
        sd = stats_df[c][1]
        out_list.append(z_score(mean,sd,i))
    return out_list


def get_result(mtype, params):
    '''The main program call.  Returns the category of the expected
    classification.  Defaults are mean params. Input parameters:
    mtype = which position
    params = non-normalized input params.'''

    # Load model
    if mtype == 'rb':
        model = joblib.load(urllib.request.urlopen("https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/rb_model.pkl"))
        cols = ['conference','rb_forty_zscore','rb_rushing_scrim_tds_pg_cf_scaled_zscore','rb_college_weight_pounds_zscore','rb_rushing_receptions_zscore','rb_rushing_rush_att_zscore','rb_ann_rain_inch_zscore','rb_rushing_scrim_yds_pg_cf_scaled_zscore','rb_rushing_rush_td_pg_cf_scaled_zscore','rb_bench_zscore','rb_rushing_games_zscore','rb_vertical_zscore','rb_threecone_zscore','rb_broad_zscore','rb_rushing_scrim_plays_pg_cf_scaled_zscore','rb_college_height_inches_zscore']
    if mtype == 'wr':
        model = joblib.load(urllib.request.urlopen("https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/wr_model.pkl"))
        cols = ['conference','wr_forty_zscore', 'wr_vertical_zscore', 'wr_bench_zscore','wr_broad_zscore', 'wr_threecone_zscore', 'wr_shuttle_zscore','wr_receiving_rec_td_pg_cf_scaled_zscore','wr_college_weight_pounds_zscore', 'wr_college_height_inches_zscore','wr_receiving_rec_yards_pg_cf_scaled_zscore','wr_ann_rain_inch_zscore','wr_receiving_receptions_pg_cf_scaled_zscore','wr_receiving_scrim_plays_pg_cf_scaled_zscore']
    if mtype == 'cb':
        model = joblib.load(urllib.request.urlopen("https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/cb_model.pkl"))
        cols = ['conference','cb_hw_ratio_zscore', 'cb_college_weight_pounds_zscore', 'cb_college_height_inches_zscore', 'cb_forty_zscore', 'cb_vertical_zscore', 'cb_broad_zscore', 'cb_threecone_zscore', 'cb_shuttle_zscore', 'cb_defense_ast_tackles_pg_cf_scaled_zscore', 'cb_defense_fum_forced_pg_cf_scaled_zscore', 'cb_defense_int_pg_cf_scaled_zscore', 'cb_defense_int_td_pg_cf_scaled_zscore', 'cb_defense_int_yards_pg_cf_scaled_zscore', 'cb_defense_loss_tackles_pg_cf_scaled_zscore', 'cb_defense_pd_pg_cf_scaled_zscore', 'cb_defense_solo_tackes_pg_cf_scaled_zscore', 'cb_defense_tackles_pg_cf_scaled_zscore', 'cb_ann_rain_inch_zscore']

    # Load statistics
    stats_df = pd.read_csv('https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/representative_statistics.csv', index_col = 0)

    # prepare argument parameters
    eval_df = pd.DataFrame(z_list(params, cols, stats_df)).T
    eval_df.columns = cols
    eval_df = eval_df.drop(['conference'], axis=1)

    # run the model!
    madden_predict = model.predict(eval_df),0
    print("Prediction for this player is:", madden_predict)
    return int(round(madden_predict[0][0],0))

@application.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    return "This is the default response!\n"

@application.route("/query/rb/")
# Query point for running backs
def query_rb():
    """Show the model result for given properties"""
    """Order expected is listed below."""
    pargs = []
    pargs.append(request.args.get('conference'))
    pargs.append(float(request.args.get('rb_forty')))
    pargs.append(float(request.args.get('rb_rushing_scrim_tds_pg_cf_scaled')))
    pargs.append(float(request.args.get('rb_college_weight_pounds')))
    pargs.append(float(request.args.get('rb_rushing_receptions')))
    pargs.append(float(request.args.get('rb_rushing_rush_att')))
    pargs.append(float(request.args.get('rb_ann_rain_inch')))
    pargs.append(float(request.args.get('rb_rushing_scrim_yds_pg_cf_scaled')))
    pargs.append(float(request.args.get('rb_rushing_rush_td_pg_cf_scaled')))
    pargs.append(float(request.args.get('rb_bench')))
    pargs.append(float(request.args.get('rb_rushing_games')))
    pargs.append(float(request.args.get('rb_vertical')))
    pargs.append(float(request.args.get('rb_threecone')))
    pargs.append(float(request.args.get('rb_broad')))
    pargs.append(float(request.args.get('rb_rushing_scrim_plays_pg_cf_scaled')))
    pargs.append(float(request.args.get('rb_college_height_inches')))
    val = get_result(mtype='rb', params=pargs)
    return render_template('/query/index.html', ret_value=val)

@application.route("/query/wr/")
# Query point for wide receivers
# Test with mean:
def query_wr():
    """Show the model result for given properties"""
    """Order expected is listed below."""
    pargs = []
    pargs.append(request.args.get('conference'))
    pargs.append(float(request.args.get('wr_forty')))
    pargs.append(float(request.args.get('wr_vertical')))
    pargs.append(float(request.args.get('wr_bench')))
    pargs.append(float(request.args.get('wr_broad')))
    pargs.append(float(request.args.get('wr_threecone')))
    pargs.append(float(request.args.get('wr_shuttle')))
    pargs.append(float(request.args.get('wr_receiving_rec_td_pg_cf_scaled')))
    pargs.append(float(request.args.get('wr_college_weight_pounds')))
    pargs.append(float(request.args.get('wr_college_height_inches')))
    pargs.append(float(request.args.get('wr_receiving_rec_yards_pg_cf_scaled')))
    pargs.append(float(request.args.get('wr_ann_rain_inch')))
    pargs.append(float(request.args.get('wr_receiving_receptions_pg_cf_scaled')))
    pargs.append(float(request.args.get('wr_receiving_scrim_plays_pg_cf_scaled')))
    val = get_result(mtype='wr', params=pargs)
    return render_template('/query/index.html', ret_value=val)

@application.route("/query/cb/")
# Query point for corner backs
# Test with mean:
def query_cb():
    """Show the model result for given properties"""
    """Order expected is listed below."""
    pargs = []
    pargs.append(request.args.get('conference'))
    pargs.append(float(request.args.get('cb_hw_ratio')))
    pargs.append(float(request.args.get('cb_college_weight_pounds')))
    pargs.append(float(request.args.get('cb_college_height_inches')))
    pargs.append(float(request.args.get('cb_forty')))
    pargs.append(float(request.args.get('cb_vertical')))
    pargs.append(float(request.args.get('cb_broad')))
    pargs.append(float(request.args.get('cb_threecone')))
    pargs.append(float(request.args.get('cb_shuttle')))
    pargs.append(float(request.args.get('cb_defense_ast_tackles_pg_cf_scaled')))
    pargs.append(float(request.args.get('cb_defense_fum_forced_pg_cf_scaled')))
    pargs.append(float(request.args.get('cb_defense_int_pg_cf_scaled')))
    pargs.append(float(request.args.get('cb_defense_int_td_pg_cf_scaled')))
    pargs.append(float(request.args.get('cb_defense_int_yards_pg_cf_scaled')))
    pargs.append(float(request.args.get('cb_defense_loss_tackles_pg_cf_scaled')))
    pargs.append(float(request.args.get('cb_defense_pd_pg_cf_scaled')))
    pargs.append(float(request.args.get('cb_defense_solo_tackes_pg_cf_scaled')))
    pargs.append(float(request.args.get('cb_defense_tackles_pg_cf_scaled')))
    pargs.append(float(request.args.get('cb_ann_rain_inch')))
    val = get_result(mtype='cb', params=pargs)
    return render_template('/query/index.html', ret_value=val)

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
