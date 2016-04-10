from flask import Flask, render_template, url_for, request
app = Flask(__name__)

import hmm_class
import numpy as np


@app.route('/graph')
def graph():
    print url_for('static', filename='js/graph_display.js')
    return render_template('graph.html')


@app.route('/run')
def run():
    return render_template('web_run.html')


def parse_2d_array(string):
    """ Convert string to 2d numpy array """
    return np.matrix(str(string))


def parse_1d_array(string):
    """ Convert string to tuple """
    return tuple(string.split(' '))


@app.route('/run/viterbi', methods=['GET', 'POST'])
def viterbi():
    print(parse_1d_array(request.form['states']),
          parse_1d_array(request.form['possible_observations']),
          parse_2d_array(request.form['start_probability']),
          parse_2d_array(request.form['transition_probability']),
          parse_2d_array(request.form['emission_probability']))

    hmm = hmm_class.hmm(parse_1d_array(request.form['states']),
                        parse_1d_array(request.form['possible_observations']),
                        parse_2d_array(request.form['start_probability']),
                        parse_2d_array(request.form['transition_probability']),
                        parse_2d_array(request.form['emission_probability']))
    print (hmm.viterbi(request.form['observations']))
    return str(request.form)


if __name__ == '__main__':
    app.debug = True
    app.run()
