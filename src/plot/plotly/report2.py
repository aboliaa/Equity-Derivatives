from defaults import *

def form_plotargs(x, y1, y2, title):
    data = [
            {
                "x": x,
                "y": y2,
                "hoverinfo": "x+y",
                "name": "Total OI", 
                "type": "bar", 
                "opacity": 0.75,
                "uid": "7155f3", 
                "yaxis": "y2"
            }, 
            {
                "x": x,
                "y": y1,
                "hoverinfo": "x+y",
                "line": {
                    "color": "rgb(255, 127, 14)", 
                    "width": 3
                }, 
                "mode": "lines+markers", 
                "name": "Settlement Price", 
                "type": "scatter",
                "uid": "784d8d"
            }
        ] 
        
        
    layout = {
            "autosize": True,
            "boxgap": 0.3,
            "boxgroupgap": 0.3,                                                 
            "boxmode": "overlay",
            "margin":{
                "l": 50
            },
            "height": 550,
            "legend": {
                "x": 0.95, 
                "y": 1, 
                "bgcolor": "rgba(255, 255, 255, 0)", 
                "bordercolor": "#444", 
                "borderwidth": 0, 
                "traceorder": "normal", 
                "xanchor": "left", 
                "yanchor": "top"
            }, 
            "showlegend": True, 
            "title": title, 
            "width": 1200, 
            "xaxis": {
                "anchor": "y",
                "type": "date",
                "domain": [
                    0, 
                    0.9
                ],
                "tickformat": "%d-%b-%Y",
                "exponentformat": "B", 
                "overlaying": False, 
                "position": 0, 
                "title": "Trading Date", 
                "showline": True, 
                "zeroline": False, 
                "zerolinecolor": "#444", 
                "zerolinewidth": 1
            }, 
            "yaxis": {
                "anchor": "x", 
                "autorange": True, 
                "autotick": True, 
                "domain": [
                    0, 
                    1
                ], 
                "dtick": 5, 
                "exponentformat": "B", 
                "gridcolor": "#eee", 
                "gridwidth": 1, 
                "linecolor": "#444", 
                "linewidth": 1, 
                "mirror": False, 
                "nticks": 0, 
                "overlaying": False, 
                "position": 0, 
                "rangemode": "normal", 
                "showexponent": "all", 
                "showgrid": True, 
                "showline": True, 
                "showticklabels": True, 
                "tick0": 0, 
                "tickangle": "auto", 
                "tickcolor": "#444", 
                "tickfont": {
                    "color": "", 
                    "family": "", 
                    "size": 0
                }, 
                "ticklen": 5, 
                "ticks": "", 
                "tickwidth": 1, 
                "title": "Settlement Price", 
                "type": "linear", 
                "zeroline": True, 
                "zerolinecolor": "#444", 
                "zerolinewidth": 1
            }, 
            "yaxis2": {
                "anchor": "x", 
                "autorange": True, 
                "autotick": True, 
                "domain": [
                    0, 
                    1
                ], 
                "dtick": 5, 
                "exponentformat": "B", 
                "gridcolor": "#eee", 
                "gridwidth": 1, 
                "linecolor": "#444", 
                "linewidth": 1, 
                "mirror": False, 
                "nticks": 0, 
                "overlaying": "y", 
                "position": 0, 
                "rangemode": "normal", 
                "showexponent": "all", 
                "showgrid": True, 
                "showline": True, 
                "showticklabels": True, 
                "side": "right", 
                "tick0": 0, 
                "tickangle": "auto", 
                "tickcolor": "#444", 
                "tickfont": {
                    "color": "", 
                    "family": "", 
                    "size": 0
                }, 
                "ticklen": 5, 
                "ticks": "", 
                "tickwidth": 1, 
                "title": "Total OI", 
                "type": "linear", 
                "zeroline": True, 
                "zerolinecolor": "#444", 
                "zerolinewidth": 1
            } 
        }

    if any(y1) or any(y2):
        isempty = 0
    else:
        isempty = 1


    plotargs = {"data": data, "layout": layout, "empty": isempty}
    return plotargs
