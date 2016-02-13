def form_plotargs(x, y, text, title):
    data = [
            {
                "name": "Increase in OI",
                "x": x[0],
                "y": y[0],
                "hoverinfo": "x+text",
                "text": text[0],
                "type": "bar"
            },
            {
                "name": "Decrease in OI",
                "x": x[1],
                "y": y[1],
                "hoverinfo": "x+text",
                "text": text[1],
                "type": "bar"
            }
    ]
    
    layout = {
                "title": title,
                "showlegend": True,
                "width": 1200,
                "height": 550,
                "xaxis": {
                            "title": "Scrip"
                         },
                "yaxis": {
                            "title": "OI movement (%)",
                            "showline": True
                         }
    }
    
    isempty = 0

    plotargs = {"data": data, "layout": layout, "empty": isempty}
    return plotargs
