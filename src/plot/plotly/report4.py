def form_plotargs(x, y, text, size):
    data = [
            {
                "name": "Near series -",
                "x": x[0],
                "y": y[0],
                "text": text[0],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size[0]
                          }
            },
            {
                "name": "Next series -",
                "x": x[1],
                "y": y[1],
                "text": text[1],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size[1]
                          }
            },
            {
                "name": "Far series -",
                "x": x[2],
                "y": y[2],
                "text": text[2],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size[2]
                          }
            },
            {
                "name": "Cumulative -",
                "x": x[3],
                "y": y[3],
                "text": text[3],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size[3]
                          }
            },
            {
                "name": "Near series +",
                "x": x[4],
                "y": y[4],
                "text": text[4],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size[4]
                          }
            },
            {
                "name": "Next series +",
                "x": x[5],
                "y": y[5],
                "text": text[5],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size[5]
                          }
            },
            {
                "name": "Far series +",
                "x": x[6],
                "y": y[6],
                "text": text[6],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size[6]
                          }
            },
            {
                "name": "Cumulative +",
                "x": x[7],
                "y": y[7],
                "text": text[7],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size[7]
                          }
            }

    ]
    
    layout = {
                "title": "OI movements",
                "showlegend": True,
                "width": 1000,
                "height": 800,
                "xaxis": {
                            "title": "Scrip"
                         },
                "yaxis": {
                            "title": "Change (in %)",
                            "showline": True
                         }
    }

    plotargs = {"data": data, "layout":layout}
    return plotargs
