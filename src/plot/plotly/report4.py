def form_plotargs(x, y, text, size, color, symbol, title):
    data = [
            {
                "name": "Near Series -",
                "x": x[0],
                "y": y[0],
                "text": text[0],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "color": color[0],
                            "size": size[0],
                            "symbol": symbol[0]
                          }
            },
            {
                "name": "Next Series -",
                "x": x[1],
                "y": y[1],
                "text": text[1],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "color": color[1],
                            "size": size[1],
                            "symbol": symbol[1]
                          }
            },
            {
                "name": "Far Series -",
                "x": x[2],
                "y": y[2],
                "text": text[2],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "color": color[2],
                            "size": size[2],
                            "symbol": symbol[2]
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
                            "color": color[3],
                            "size": size[3],
                            "symbol": symbol[3]
                          }
            },
            {
                "name": "Near Series +",
                "x": x[4],
                "y": y[4],
                "text": text[4],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "color": color[4],
                            "size": size[4],
                            "symbol": symbol[4]
                          }
            },
            {
                "name": "Next Series +",
                "x": x[5],
                "y": y[5],
                "text": text[5],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "color": color[5],
                            "size": size[5],
                            "symbol": symbol[5]
                          }
            },
            {
                "name": "Far Series +",
                "x": x[6],
                "y": y[6],
                "text": text[6],
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "color": color[6],
                            "size": size[6],
                            "symbol": symbol[6]
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
                            "color": color[7],
                            "size": size[7],
                            "symbol": symbol[7]
                          }
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

    plotargs = {"data": data, "layout":layout}
    return plotargs
