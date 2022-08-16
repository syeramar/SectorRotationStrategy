from cProfile import run
import os, csv
import yfinance as yf
import pandas

from flask import Flask, escape, request, render_template
from sector_etfs import sector_etfs
from EMA_Strategy import run_strategy

app = Flask(__name__)

@app.route('/snapshot')
def snapshot():
    return {
        "code": "success"
    }

@app.route('/')
def index():
    results = {}
    for sector in sector_etfs:
        ticker = sector_etfs[sector]
        portval, pnl, perc_return = run_strategy(ticker, sdate='2020-01-01')
        results[sector] = {"Portfolio Value": portval, "Profit": pnl, "% Return": perc_return}

    return render_template('index.html', sectors=sector_etfs, results=results)