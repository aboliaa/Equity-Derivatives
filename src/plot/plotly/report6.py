def form_plotargs(x1, y1, text1, size1, x2, y2, text2, size2):
    data = [
            {
                "name": "CALLs",
                "x": x1,
                "y": y1,
                "text": text1,
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size1
                          }
            },
            {
                "name": "PUTs",
                "x": x2,
                "y": y2,
                "text": text2,
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size2
                          }
            } 
    ]
    
    layout = {
                "title": "Most active CALLs and PUTs",
                "showlegend": True,
                "width": 1000,
                "height": 800,
                "xaxis": {
                            "title": "Scrip"
                         },
                "yaxis": {
                            "title": "Strike price",
                            "showline": True
                         }
    }

    plotargs = {"data": data, "layout":layout}
    return plotargs
