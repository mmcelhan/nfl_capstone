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

def z_list(model_type, in_list, cols, stats_df):
    '''Returns z-scored list'''
    out_list = []
    rain_val = []
    scaled = "scaled"
    for i, c in zip(in_list, cols):
        if c == 'conference':
            conference = return_conference(i)
            print(conference)
            out_list.append(conference)
            rain_val.append(return_rainfall(i))
            if model_type == 'cb':
                val = in_list[2]/in_list[1]
                mean = stats_df['cb_hw_ratio_zscore'][0]
                sd = stats_df['cb_hw_ratio_zscore'][1]
                print("ratio",val)
                out_list.append(z_score(mean,sd,val))
            continue
        if scaled in c:
            print(c,i)
            val = scale_it(i, out_list[0])
            mean = stats_df[c][0]
            sd = stats_df[c][1]
            out_list.append(z_score(mean,sd,val))
            if c=='wr_receiving_rec_yards_pg_cf_scaled_zscore':
                mean = stats_df['wr_ann_rain_inch_zscore'][0]
                sd = stats_df['wr_ann_rain_inch_zscore'][1]
                print("rain",rain_val[0])
                out_list.append(z_score(mean,sd,rain_val[0]))
            if c=='cb_defense_tackles_pg_cf_scaled_zscore':
                mean = stats_df['cb_ann_rain_inch_zscore'][0]
                sd = stats_df['cb_ann_rain_inch_zscore'][1]
                print("rain",rain_val[0])
                out_list.append(z_score(mean,sd,rain_val[0]))
        else:
            mean = stats_df[c][0]
            sd = stats_df[c][1]
            print(c,i)
            out_list.append(z_score(mean,sd,i))
            if c=='rb_rushing_rush_att_zscore':
                mean = stats_df['rb_ann_rain_inch_zscore'][0]
                sd = stats_df['rb_ann_rain_inch_zscore'][1]
                print("rain",rain_val[0])
                out_list.append(z_score(mean,sd,rain_val[0]))
    print(out_list)
    return out_list

def return_conference(college):
    ''' function that recieves college and returns conference'''
    df = pd.read_csv('https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/dimensions_colleges.csv')
    df = df[['college', 'conference']]
    conference = df[df['college'] == college]['conference']
    if conference.empty:
        conference = ""
    else:
        conference = conference.values[0]
    return conference

def return_rainfall(college):
    '''function that recieves college and returns that annual rainfall'''
    rainfall = 0
    df_colleges = pd.read_csv('https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/dimensions_colleges.csv')
    df_colleges = df_colleges[['fms_city_id', 'college']]
    df_cities = pd.read_csv('https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/facts_cities_metrics.csv')
    df_cities = df_cities[['fms_city_id', 'ann_rain_inch']]
    df = pd.merge(df_colleges, df_cities, how='left', on='fms_city_id')
    rainfall = df[df['college'] == college]['ann_rain_inch']
    if rainfall.empty:
        rainfall = df['ann_rain_inch'].mean()  # return mean rain for country if no match
    else:
        rainfall = rainfall.values[0]
    return rainfall

def get_result(mtype, params):
    '''The main program call.  Returns the category of the expected
    classification.  Defaults are mean params. Input parameters:
    mtype = which position
    params = non-normalized input params.'''
    print(mtype)
    # Load model
    if mtype == 'rb':
        model = joblib.load(urllib.request.urlopen("https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/rb_model.pkl"))
        cols1 = ['conference','rb_forty_zscore','rb_rushing_scrim_tds_pg_cf_scaled_zscore','rb_college_weight_pounds_zscore','rb_rushing_receptions_zscore','rb_rushing_rush_att_zscore','rb_rushing_scrim_yds_pg_cf_scaled_zscore','rb_rushing_rush_td_pg_cf_scaled_zscore','rb_bench_zscore','rb_rushing_games_zscore','rb_vertical_zscore','rb_threecone_zscore','rb_broad_zscore','rb_rushing_scrim_plays_pg_cf_scaled_zscore','rb_college_height_inches_zscore']
        cols2 = ['conference','rb_forty_zscore','rb_rushing_scrim_tds_pg_cf_scaled_zscore','rb_college_weight_pounds_zscore','rb_rushing_receptions_zscore','rb_rushing_rush_att_zscore','rb_ann_rain_inch_zscore','rb_rushing_scrim_yds_pg_cf_scaled_zscore','rb_rushing_rush_td_pg_cf_scaled_zscore','rb_bench_zscore','rb_rushing_games_zscore','rb_vertical_zscore','rb_threecone_zscore','rb_broad_zscore','rb_rushing_scrim_plays_pg_cf_scaled_zscore','rb_college_height_inches_zscore']
    if mtype == 'wr':
        model = joblib.load(urllib.request.urlopen("https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/wr_model.pkl"))
        cols1 = ['conference','wr_forty_zscore', 'wr_vertical_zscore', 'wr_bench_zscore','wr_broad_zscore', 'wr_threecone_zscore', 'wr_shuttle_zscore','wr_receiving_rec_td_pg_cf_scaled_zscore','wr_college_weight_pounds_zscore', 'wr_college_height_inches_zscore','wr_receiving_rec_yards_pg_cf_scaled_zscore','wr_receiving_receptions_pg_cf_scaled_zscore','wr_receiving_scrim_plays_pg_cf_scaled_zscore']
        cols2 = ['conference','wr_forty_zscore', 'wr_vertical_zscore', 'wr_bench_zscore','wr_broad_zscore', 'wr_threecone_zscore', 'wr_shuttle_zscore','wr_receiving_rec_td_pg_cf_scaled_zscore','wr_college_weight_pounds_zscore', 'wr_college_height_inches_zscore','wr_receiving_rec_yards_pg_cf_scaled_zscore','wr_ann_rain_inch_zscore','wr_receiving_receptions_pg_cf_scaled_zscore','wr_receiving_scrim_plays_pg_cf_scaled_zscore']
    if mtype == 'cb':
        model = joblib.load(urllib.request.urlopen("https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/cb_model.pkl"))
        cols1 = ['conference', 'cb_college_weight_pounds_zscore', 'cb_college_height_inches_zscore', 'cb_forty_zscore', 'cb_vertical_zscore', 'cb_broad_zscore', 'cb_threecone_zscore', 'cb_shuttle_zscore', 'cb_defense_ast_tackles_pg_cf_scaled_zscore', 'cb_defense_fum_forced_pg_cf_scaled_zscore', 'cb_defense_int_pg_cf_scaled_zscore', 'cb_defense_int_td_pg_cf_scaled_zscore', 'cb_defense_int_yards_pg_cf_scaled_zscore', 'cb_defense_loss_tackles_pg_cf_scaled_zscore', 'cb_defense_pd_pg_cf_scaled_zscore', 'cb_defense_solo_tackes_pg_cf_scaled_zscore', 'cb_defense_tackles_pg_cf_scaled_zscore']
        cols2 = ['conference','cb_hw_ratio_zscore', 'cb_college_weight_pounds_zscore', 'cb_college_height_inches_zscore', 'cb_forty_zscore', 'cb_vertical_zscore', 'cb_broad_zscore', 'cb_threecone_zscore', 'cb_shuttle_zscore', 'cb_defense_ast_tackles_pg_cf_scaled_zscore', 'cb_defense_fum_forced_pg_cf_scaled_zscore', 'cb_defense_int_pg_cf_scaled_zscore', 'cb_defense_int_td_pg_cf_scaled_zscore', 'cb_defense_int_yards_pg_cf_scaled_zscore', 'cb_defense_loss_tackles_pg_cf_scaled_zscore', 'cb_defense_pd_pg_cf_scaled_zscore', 'cb_defense_solo_tackes_pg_cf_scaled_zscore', 'cb_defense_tackles_pg_cf_scaled_zscore', 'cb_ann_rain_inch_zscore']

    # Load statistics
    stats_df = pd.read_csv('https://groups.ischool.berkeley.edu/NFL-Auto-Scout/resources/representative_statistics.csv', index_col = 0)

    # prepare argument parameters
    eval_df = pd.DataFrame(z_list(mtype, params, cols1, stats_df)).T
    eval_df.columns = cols2
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
    pargs.append(request.args.get('college'))
    pargs.append(float(request.args.get('rb_forty')))
    pargs.append(float(request.args.get('rb_rushing_scrim_tds_pg_cf_scaled')))
    pargs.append(float(request.args.get('rb_college_weight_pounds')))
    pargs.append(float(request.args.get('rb_rushing_receptions')))
    pargs.append(float(request.args.get('rb_rushing_rush_att')))
    pargs.append(float(request.args.get('rb_rushing_scrim_yds_pg_cf_scaled')))
    pargs.append(float(request.args.get('rb_rushing_rush_td_pg_cf_scaled')))
    pargs.append(float(request.args.get('rb_bench')))
    pargs.append(float(request.args.get('rb_rushing_games')))
    pargs.append(float(request.args.get('rb_vertical')))
    pargs.append(float(request.args.get('rb_threecone')))
    pargs.append(float(request.args.get('rb_broad')))
    pargs.append(float(request.args.get('rb_rushing_scrim_plays_pg_cf_scaled')))
    pargs.append(float(request.args.get('rb_college_height_inches')))
    print(pargs)
    val = get_result(mtype='rb', params=pargs)
    return render_template('/query/index.html', ret_value=val)

@application.route("/query/wr/")
# Query point for wide receivers
def query_wr():
    """Show the model result for given properties"""
    """Order expected is listed below."""
    pargs = []
    pargs.append(request.args.get('college'))
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
    pargs.append(float(request.args.get('wr_receiving_receptions_pg_cf_scaled')))
    pargs.append(float(request.args.get('wr_receiving_scrim_plays_pg_cf_scaled')))
    val = get_result(mtype='wr', params=pargs)
    return render_template('/query/index.html', ret_value=val)

@application.route("/cb/")
# Test entry point
def form_cb():
    return render_template('cb_iframe.html')

@application.route("/query/cb/")
# Query point for corner backs
def query_cb():
    """Show the model result for given properties"""
    """Order expected is listed below."""
    pargs = []
    pargs.append(request.args.get('college'))
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
    val = get_result(mtype='cb', params=pargs)
    return render_template('/query/index.html', ret_value=val)

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
