from math import ceil

def form_plotargs(x, y1, t1, y2, t2, y3, t3, title):
    max_pcr = max(max(y2), max(y3))
    ceil_max_pcr = ceil(max_pcr)
    if ceil_max_pcr - max_pcr >= 0.5:
        max_pcr = ceil_max_pcr - 0.5
    else:
        max_pcr = ceil_max_pcr

    data = [
            {
                "x": x,             
                "y": y3,
                "hoverinfo": "x+text",
                "text": t3,
                "line": {
                    "color": "rgb(0, 128, 0)", 
                    "width": 3
                }, 
                "mode": "lines+markers", 
                "name": "PCR of Trade", 
                "type": "scatter", 
                "uid": "9023be", 
                "yaxis": "y3"
            }, 
            {
                "x": x,
                "y": y2,
                "hoverinfo": "x+text",
                "text": t2,
                "line": {
                    "color": "rgb(128, 0, 128)", 
                    "width": 3
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
                "hoverinfo": "x+text",
                "text": t1,
                "line": {
                    "color": "rgb(255, 0, 0)", 
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
            "bargap": 0.2, 
            "bargroupgap": 0, 
            "barmode": "group", 
            "boxgap": 0.3, 
            "boxgroupgap": 0.3, 
            "boxmode": "overlay", 
            "height": 550, 
            "hidesources": True, 
            "legend": {
                "x": 1.05, 
                "y": 1, 
                "bgcolor": "rgba(255, 255, 255, 0)", 
                "bordercolor": "#444", 
                "borderwidth": 0, 
                "traceorder": "normal", 
                "xanchor": "left", 
                "yanchor": "top"
            }, 
            "margin": {
                "l": 50 
            }, 
            "showlegend": True, 
            "title": title, 
            "width": 1200, 
            "xaxis": {
                "nticks": 6,
                "anchor": "y",
                "overlaying": False,                                            
                "position": 0,
                "zeroline": False,                                              
                "zerolinecolor": "#444",                                        
                "showline": True, 
                "zerolinewidth": 1,
                "domain": [                                                     
                    0.0,                                                       
                    0.9                                                         
                ],
                "title": "Trading Date" 
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
                "autorange": False, 
                "range" : [0,max_pcr],
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
            }, 
            "yaxis3": {
                "anchor": "free", 
                "autorange": False, 
                "range" : [0,max_pcr],
                "autotick": True, 
                "domain": [
                    0, 
                    1
                ], 
                "dtick": 1, 
                "exponentformat": "B", 
                "gridcolor": "#eee", 
                "gridwidth": 1, 
                "linecolor": "#444", 
                "linewidth": 1, 
                "mirror": False, 
                "nticks": 0, 
                "overlaying": "y", 
                "position": 1, 
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
                "title": "PCR of Trade", 
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
    
    if any(y1) or any(y2) or any(y3):
        isempty = 0
    else:
        isempty = 1

    plotargs = {"data": data, "layout": layout, "empty": isempty}
    return plotargs
