#!/usr/bin/env python

# To test: "flask run"

import json
from flask import Flask, request
from flask import render_template

import pickle
from sklearn.externals import joblib
from sklearn.ensemble import AdaBoostRegressor, AdaBoostClassifier
import pandas as pd
import itertools as it

app = Flask(__name__)

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


def get_result(mtype='rb', params=[4.55, 0.66, 214.57, 50.41, 492.14, 40.94, 72.77, 0.60, 19.43, 37.80, 34.36, 7.06, 118.01, 12.74, 70.55]):
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
        file_name = 'rb_model.pkl'
    if mtype == 'test':
        file_name = 'test.pkl'
    model = joblib.load(file_name)

    # Load statistics
    stats_df = pd.read_csv('representative_statistics.csv', index_col = 0)

    # prepare argument parameters
    cols = ['rb_forty_zscore','rb_rushing_scrim_tds_pg_cf_scaled_zscore','rb_college_weight_pounds_zscore','rb_rushing_receptions_zscore','rb_rushing_rush_att_zscore','rb_ann_rain_inch_zscore','rb_rushing_scrim_yds_pg_cf_scaled_zscore','rb_rushing_rush_td_pg_cf_scaled_zscore','rb_bench_zscore','rb_rushing_games_zscore','rb_vertical_zscore','rb_threecone_zscore','rb_broad_zscore','rb_rushing_scrim_plays_pg_cf_scaled_zscore','rb_college_height_inches_zscore']
    eval_df = pd.DataFrame(z_list(params, cols, stats_df)).T
    eval_df.columns = cols

    # run the model!

    madden_predict = model.predict(eval_df)
    print("Prediction for this player is:", madden_predict)
    return madden_predict


@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    return "This is the default response!\n"


@app.route("/query/")
# Note: currently coded for Running Backs.  New URLs for others.
# Test with mean: http://127.0.0.1:5000/query/4.55-0.66-214.57-50.41-492.14-40.94-72.77-0.60-19.43-37.80-34.36-7.06-118.01-12.74-70.55
# Test with star: http://127.0.0.1:5000/query/4.47-1-200-140-600-80-90-1-50-90-90-15-200-15-120
def query_app():
    """Show the model result for given properties"""
    """Order expected: ..."""
    posts = []
    posts.append(float(request.args.get('rb_forty')))
    posts.append(float(request.args.get('rb_rushing_scrim_tds_pg_cf_scaled')))
    posts.append(float(request.args.get('rb_college_weight_pounds')))
    posts.append(float(request.args.get('rb_rushing_receptions')))
    posts.append(float(request.args.get('rb_rushing_rush_att')))
    posts.append(float(request.args.get('rb_ann_rain_inch')))
    posts.append(float(request.args.get('rb_rushing_scrim_yds_pg_cf_scaled')))
    posts.append(float(request.args.get('rb_rushing_rush_td_pg_cf_scaled')))
    posts.append(float(request.args.get('rb_bench')))
    posts.append(float(request.args.get('rb_rushing_games')))
    posts.append(float(request.args.get('rb_vertical')))
    posts.append(float(request.args.get('rb_threecone')))
    posts.append(float(request.args.get('rb_broad')))
    posts.append(float(request.args.get('rb_rushing_scrim_plays_pg_cf_scaled')))
    posts.append(float(request.args.get('rb_college_height_inches')))

    val = get_result(mtype='rb', params=posts)
    # Research this part at https://flask.palletsprojects.com/en/1.1.x/quickstart/#rendering-templates
    return render_template('/query/index.html', posts=posts)
