def form_plotargs(x1, y1, text1, x2, y2, text2, title, tickval, ticktext):
    data = [
            {
                "name": "CALLs",
                "x": x1,
                "y": y1,
                "text": text1,
                "hoverinfo": "x+text",
                "type": "bar"
            },
            {
                "name": "PUTs",
                "x": x2,
                "y": y2,
                "text": text2,
                "hoverinfo": "x+text",
                "type": "bar"
            } 
    ]
    
    layout = {
                "title": title,
                "width": 1200,
                "height": 550,
                "showlegend": True,
                "xaxis": {
                            "title": "Scrip",
                            "ticktext": ticktext,
                            "tickvals": tickval
                         },
                "yaxis": {
                            "title": "Contracts",
                            "showline": True
                         }
    }
    
    isempty = 0

    plotargs = {"data": data, "layout": layout, "empty": isempty}
    return plotargs

def form_plotargs1(x1, y1, text1, size1, x2, y2, text2, size2, title):
    data = [
            {
                "name": "CALLs",
                "x": x1,
                "y": y1,
                "text": text1,
                "hoverinfo": "x+y",
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size1,
                            "symbol": "circle"
                          }
            },
            {
                "name": "PUTs",
                "x": x2,
                "y": y2,
                "text": text2,
                "hoverinfo": "x+y",
                "mode": "markers",
                "marker": {
                            "sizemode": "area",
                            "size": size2,
                            "symbol": "cross"
                          }
            } 
    ]
    
    layout = {
                "title": title,
                "width": 1200,
                "height": 550,
                "showlegend": True,
                "xaxis": {
                            "title": "Scrip"
                         },
                "yaxis": {
                            "title": "Strike Price",
                            "showline": True
                         }
    }
    
    isempty = 0

    plotargs = {"data": data, "layout": layout, "empty": isempty}
    return plotargs
