def form_plotargs(x1, y1, x2, y2):
    data = [
            {
                "x": x1,
                "y": y1,
                "name": "CALLs", 
                "type": "bar" 
            },
            {
                "x": x2,
                "y": y2,
                "name": "PUTs", 
                "type": "bar" 
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
            }
        }

    layout = {
            "autosize": True, 
            "bargap": 0.2, 
            "bargroupgap": 0, 
            "barmode": "group", 
            "boxgap": 0.3, 
            "boxgroupgap": 0.3, 
            "boxmode": "overlay", 
            "height": 700, 
            "showlegend": True, 
            "title": "Distribution of PUTs and CALLs" 
        }


    plotargs = {"data": data, "layout": layout}
    return plotargs
