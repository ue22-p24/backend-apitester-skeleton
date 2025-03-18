import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Vous devez ajouter les routes ici : 

@app.route('/api/alive')
def alive():
    # no need to explicitly jsonify a dict,
    # Flask will do it for you
    return {'message': 'Alive'}

@app.route('/api/associations')
def list_associations():
    df = pd.read_csv("data/associations_etudiantes.csv")
    # in theory it is possible to return an iterable (e.g. a list)
    # in which case flask would produce an HTTP stream
    # but that would require the frontend to handle it properly
    # so we build a list of ints and explicitly jsonify it
    L = list(df['id'].to_dict().values())
    return jsonify(L)

@app.route('/api/association/<int:assoc_id>')
def association_details(assoc_id):
    df = pd.read_csv(data / "associations_etudiantes.csv")
    row_df = df[df.id == assoc_id]
    if len(row_df) == 0:
        print(f" id {assoc_id} not found")
        return ({'error': f'unknown assoc id {assoc_id}'}, 404)
    return row_df.to_dict(orient='records')[0]

@app.route("/api/evenements")
def list_evenements():
    df = pd.read_csv(data / "evenements_associations.csv")
    L = list(df['id'].to_dict().values())
    return jsonify(L)

@app.route("/api/evenement/<int:event_id>")
def evenement_details(event_id):
    df = pd.read_csv(data / "evenements_associations.csv")
    row_df = df[df.id == event_id]
    if len(row_df) == 0:
        print(f" id {event_id} not found")
        return ({'error': f'unknown event id {event_id}'}, 404)
    return row_df.to_dict(orient='records')[0]

@app.route("/api/association/<int:assoc_id>/evenements")
def evenements_association(assoc_id):
    events = pd.read_csv(data / "evenements_associations.csv")
    assocs = pd.read_csv(data / "associations_etudiantes.csv")
    row_df = assocs[assocs.id == assoc_id]
    if len(row_df) == 0:
        print(f" id {assoc_id} not found")
        return ({'error': f'unknown assoc id {assoc_id}'}, 404)
    df = (
        pd.merge(assocs, events, left_on='id', right_on='association_id')
        .drop(columns=['association_id'])
        .rename(columns={'id_x': 'id'})
    )
    assoc_events = df[df.id == assoc_id]
    return jsonify(
        assoc_events.to_dict(orient='records')
    )


if __name__ == '__main__':
    app.run(debug=False)
