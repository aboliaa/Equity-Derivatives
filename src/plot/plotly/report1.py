from defaults import *

def form_plotargs(x1, y1, t1, x2, y2, t2, title):
    data = [
            {
                "x": x1,
                "y": y1,
                "hoverinfo": "x+text",
                "name": "CALLs",
                "text": t1,
                "type": "bar" 
            },
            {
                "x": x2,
                "y": y2,
                "hoverinfo": "x+text",
                "name": "PUTs", 
                "text": t2,
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
            "height": 550, 
            "width": 1000, 
            "showlegend": True,
            "margin": {
                "t": 80
            },
            "title": title,
            "xaxis": {
                        "title": "Strike Price",
                        "showline": True
                     },
            "yaxis": {
                        "title": "Open Interest",
                        "showline": True
                     }
        }

    if any(y1) or any(y2):
        isempty = 0
    else:
        isempty = 1

    plotargs = {"data": data, "layout": layout, "empty": isempty}
    return plotargs
