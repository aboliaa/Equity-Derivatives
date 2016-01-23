def form_plotargs(x, y1, y2):
    data = [
            {
                "x": x,
                "y": y2,
                "line": {
                    "color": "rgb(44, 160, 44)", 
                    "width": 3
                }, 
                "marker": {
                    "line": {
                        "width": 2
                    }, 
                    "size": 12, 
                    "symbol": "square"
                }, 
                "mode": "lines+markers", 
                "name": "PCR of OI", 
                "type": "scatter", 
                "uid": "7155f3", 
                "yaxis": "y2"
            }, 
            {
                "x": x,
                "y": y1,
                "line": {
                    "color": "rgb(255, 127, 14)", 
                    "width": 3
                }, 
                "marker": {
                    "line": {
                        "width": 2
                    }, 
                    "size": 12, 
                    "symbol": "square"
                }, 
                "mode": "lines+markers", 
                "name": "Settlement price", 
                "type": "scatter", 
                "uid": "784d8d"
            }
        ] 
        
        
    layout = {
            "autosize": True, 
            "bargap": 0.2, 
            "bargroupgap": 0, 
            "barmode": "group", 
            "boxgap": 0.3, 
            "boxgroupgap": 0.3, 
            "boxmode": "overlay", 
            "dragmode": "zoom", 
            "font": {
                "color": "#444", 
                "family": "\"Open sans\", verdana, arial, sans-serif", 
                "size": 12
            }, 
            "height": 700, 
            "hidesources": True, 
            "hovermode": "x", 
            "legend": {
                "x": 1.0476190476190477, 
                "y": 0.9666666666666667, 
                "bgcolor": "rgba(255, 255, 255, 0)", 
                "bordercolor": "#444", 
                "borderwidth": 0, 
                "font": {
                    "color": "", 
                    "family": "", 
                    "size": 0
                }, 
                "traceorder": "normal", 
                "xanchor": "left", 
                "yanchor": "top"
            }, 
            "margin": {
                "r": 80, 
                "t": 100, 
                "autoexpand": True, 
                "b": 80, 
                "l": 80, 
                "pad": 0
            }, 
            "paper_bgcolor": "#fff", 
            "plot_bgcolor": "#fff", 
            "separators": ".,", 
            "showlegend": True, 
            "smith": False, 
            "title": "", 
            "titlefont": {
                "color": "", 
                "family": "", 
                "size": 0
            }, 
            "width": 900, 
            "xaxis": {
                "anchor": "y", 
                "autorange": False, 
                "autotick": True, 
                "domain": [
                    0.08, 
                    0.8
                ], 
                "dtick": 2, 
                "exponentformat": "B", 
                "gridcolor": "#eee", 
                "gridwidth": 1, 
                "linecolor": "#444", 
                "linewidth": 1, 
                "mirror": False, 
                "nticks": 0, 
                "overlaying": False, 
                "position": 0, 
                "range": [
                    0, 
                    6.409927053599747
                ], 
                "rangemode": "normal", 
                "showexponent": "all", 
                "showgrid": False, 
                "showline": False, 
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
                "title": "x-axis", 
                "titlefont": {
                    "color": "", 
                    "family": "", 
                    "size": 0
                }, 
                "type": "linear", 
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
                "showline": False, 
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
                "title": "Settlement price", 
                "titlefont": {
                    "color": "", 
                    "family": "", 
                    "size": 0
                }, 
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
                "showline": False, 
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
                "title": "PCR of OI", 
                "titlefont": {
                    "color": "", 
                    "family": "", 
                    "size": 0
                }, 
                "type": "linear", 
                "zeroline": True, 
                "zerolinecolor": "#444", 
                "zerolinewidth": 1
            } 
        }

    plotargs = {"data": data, "layout": layout}
    return plotargs
