# Importation des packages
from shiny import App, render, ui, reactive
import numpy as np
import pandas as pd
from pathlib import Path
import os

# Importation et pretraitement des donnees
current_directory = os.getcwd()
file_path = os.path.join(current_directory, "entreprises.csv")
def loadData():
    return pd.read_csv(file_path, encoding='latin-1', sep=';', index_col='No')

df = loadData()
colonne = df.columns

nom = df.RAISONSOCIALE.unique()
nomDict = {l:l for l in nom}

region = df.REGION.unique()
regionDict = {l:l for l in region}

secteur = df.SECTEUR.unique()
secteurDict = {l:l for l in secteur}

contact = df.CONTACTS.unique()
contactDict = {l:l for l in contact}

app_ui = ui.page_fluid(
    ui.panel_title("ANNUAIRE ELECTRONIQUE DES ENTREPRISES EN COTE D'IVOIRE"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_selectize("RAISONSOCIALE", "Choisissez le nom d'une entreprise", choices=nomDict),
            ui.input_selectize("REGION", "Choisissez une region", choices=regionDict),
            ui.input_selectize("SECTEUR", "Choisissez un secteur", choices=secteurDict),
            ),
        ui.panel_main(
            ui.output_text("NomEtp"),
            ui.output_text("NomReg"),
            ui.output_text("NomSect"),
            ui.output_text("Num"),
            ),
    ),
)

def server(input, output, session):
        @reactive.Calc
        def affichage():
             selectedValues = list(input.RAISONSOCIALE())
             return df.loc[df['RAISONSOCIALE'].isin(selectedValues)]
        
        @output
        @render.text
        def NomEtp():
              return affichage()

app = App(app_ui, server)