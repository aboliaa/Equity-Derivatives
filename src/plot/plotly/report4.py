def form_plotargs(x, y, text, title):
    data = [
            {
                "name": "Increase in OI",
                "x": x[0],
                "y": y[0],
                "text": text[0],
                "type": "bar"
            },
            {
                "name": "Decrease in OI",
                "x": x[1],
                "y": y[1],
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
                            "title": "Change (in %)",
                            "showline": True
                         }
    }
    
    isempty = 0

    plotargs = {"data": data, "layout": layout, "empty": isempty}
    return plotargs
