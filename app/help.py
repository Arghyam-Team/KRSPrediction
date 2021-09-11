import streamlit as st 

#### Contains all tool tip objects
class PredictionsHelp:
    def __init__(self):
        self.predictionSelectModelDropdown = "Insert Relevant text here"
        self.predictionSelectYearCheckBox = "Check box to select Year from slider or use zoom option in plotly map"

        self.predictionSelectMonthCheckBox = "Check to select Month from slider or use zoom option in plotly map"

        self.predictionSelectGraphType = "Daily Graph shows absolute values while Average Weekly Forecast shows smoothened curve accuquired using weekly average"


class FeatureAnalysisHelp:
    def __init__(self):
        self.FaTimeFactorSelectDatasetDropdown = 'Insert Relevant text here'
        self.FaLocationFactorSelectDatasetDropdown = "Display and compare heatmaps plotted for various locations' weather data"

        self.FaSelectWeatherParameterDropdown = "The best results were acquired for Karnataka"

        self.FaSelectYearCheckBox = "Check box to select Year from slider or use zoom option in plotly map"
        self.FaSelectMonthCheckBox = "Check box to select Month from slider or use zoom option in plotly map"
        


### Contains all text objects
 
class FeatureAnanlysisTextualContent:

    def __init__(self):
        self.FaWeatherParamText = "Text about various weather parameters chosen,data collection and relevance."
        self.FaDamParamHeatMapFeatures = "inflow_"
        self.FaDamParamHeatMapAnalysis = "Text related to Heatmap analysis analysis" 
        self.FaInflowDynamicsIntroText = "Insert relevant text "
        self.FaTimeFactorText = "Insert Relevant Time Factor text"
        self.FaLocationFactorText = "Insert Relevant Location Factor text"
