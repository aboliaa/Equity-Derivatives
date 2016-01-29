def form_plotargs(x1, y1, x2, y2, title):
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
            "height": 700, 
            "width": 1000, 
            "showlegend": True, 
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


    plotargs = {"data": data, "layout": layout}
    return plotargs
