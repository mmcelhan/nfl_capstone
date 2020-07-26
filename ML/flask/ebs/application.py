#!/usr/bin/env python

# To test: "flask run"

import json
from flask import Flask, request
from flask import render_template, make_response
import urllib

import pickle
from sklearn.externals import joblib
from sklearn.ensemble import AdaBoostRegressor, AdaBoostClassifier
import pandas as pd
import itertools as it

application = Flask(__name__)

def z_score(data_mean, data_std, val):
    '''Returns a single z-scored result'''
    return (val - data_mean) / data_std

def z_list(in_list, cols, stats_df):
    '''Returns z-scored list'''
    out_list = []
    for i, c in zip(in_list, cols):
        mean = stats_df[c][0]
        sd = stats_df[c][1]
        out_list.append(z_score(mean,sd,i))
    return out_list


def get_result(mtype, params=[4.55, 0.66, 214.57, 50.41, 492.14, 40.94, 72.77, 0.60, 19.43, 37.80, 34.36, 7.06, 118.01, 12.74, 70.55]):
    '''The main program call.  Returns the category of the expected
    classification.  Defaults are mean params. Input parameters:
    mtype = which position
    params = non-normalized input params.  Sequence expected in list:
    rb_forty, rb_rushing_scrim_tds_pg_cf_scaled, rb_college_weight_pounds,
    rb_rushing_receptions, rb_rushing_rush_att, rb_ann_rain_inch,
    rb_rushing_scrim_yds_pg_cf_scaled, rb_rushing_rush_td_pg_cf_scaled,
    rb_bench, rb_rushing_games, rb_vertical, rb_threecone, rb_broad,
    rb_rushing_scrim_plays_pg_cf_scaled, rb_college_height_inches'''
    # Load model
    if mtype == 'rb':
        model = joblib.load(urllib.request.urlopen("https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/rb_model.pkl"))
        cols = ['rb_forty_zscore','rb_rushing_scrim_tds_pg_cf_scaled_zscore','rb_college_weight_pounds_zscore','rb_rushing_receptions_zscore','rb_rushing_rush_att_zscore','rb_ann_rain_inch_zscore','rb_rushing_scrim_yds_pg_cf_scaled_zscore','rb_rushing_rush_td_pg_cf_scaled_zscore','rb_bench_zscore','rb_rushing_games_zscore','rb_vertical_zscore','rb_threecone_zscore','rb_broad_zscore','rb_rushing_scrim_plays_pg_cf_scaled_zscore','rb_college_height_inches_zscore']
    if mtype == 'wr':
        model = joblib.load(urllib.request.urlopen("https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/wr_model.pkl"))
        cols = ['wr_forty_zscore', 'wr_vertical_zscore', 'wr_bench_zscore','wr_broad_zscore', 'wr_threecone_zscore', 'wr_shuttle_zscore','wr_receiving_rec_td_pg_cf_scaled_zscore','wr_college_weight_pounds_zscore', 'wr_college_height_inches_zscore','wr_receiving_rec_yards_pg_cf_scaled_zscore','wr_ann_rain_inch_zscore','wr_receiving_receptions_pg_cf_scaled_zscore','wr_receiving_scrim_plays_pg_cf_scaled_zscore']
    if mtype == 'cb':
        model = joblib.load(urllib.request.urlopen("https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/cb_model.pkl"))
        cols = ['cb_hw_ratio_zscore', 'cb_college_weight_pounds_zscore', 'cb_college_height_inches_zscore', 'cb_forty_zscore', 'cb_vertical_zscore', 'cb_broad_zscore', 'cb_threecone_zscore', 'cb_shuttle_zscore', 'cb_defense_ast_tackles_pg_cf_scaled_zscore', 'cb_defense_fum_forced_pg_cf_scaled_zscore', 'cb_defense_int_pg_cf_scaled_zscore', 'cb_defense_int_td_pg_cf_scaled_zscore', 'cb_defense_int_yards_pg_cf_scaled_zscore', 'cb_defense_loss_tackles_pg_cf_scaled_zscore', 'cb_defense_pd_pg_cf_scaled_zscore', 'cb_defense_solo_tackes_pg_cf_scaled_zscore', 'cb_defense_tackles_pg_cf_scaled_zscore', 'cb_ann_rain_inch_zscore']

    # Load statistics
    stats_df = pd.read_csv('https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/representative_statistics.csv', index_col = 0)

    # prepare argument parameters
    eval_df = pd.DataFrame(z_list(params, cols, stats_df)).T
    eval_df.columns = cols

    # run the model!

    madden_predict = model.predict(eval_df)
    print("Prediction for this player is:", madden_predict)
    return madden_predict

@application.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    return "This is the default response!\n"

@application.route("/query/rb/")
# Query point for running backs
# Test with mean: http://127.0.0.1:5000/query/rb/?rb_forty=4.55&rb_rushing_scrim_tds_pg_cf_scaled=0.66&rb_college_weight_pounds=214.57&rb_rushing_receptions=50.41&rb_rushing_rush_att=492.14&rb_ann_rain_inch=40.94&rb_rushing_scrim_yds_pg_cf_scaled=72.77&rb_rushing_rush_td_pg_cf_scaled=0.60&rb_bench=19.43&rb_rushing_games=37.80&rb_vertical=34.36&rb_threecone=7.06&rb_broad=118.01&rb_rushing_scrim_plays_pg_cf_scaled=12.74&rb_college_height_inches=70.55
def query_rb():
    """Show the model result for given properties"""
    """Order expected is listed below."""
    pargs = []
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
