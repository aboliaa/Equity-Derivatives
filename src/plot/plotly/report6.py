def form_plotargs(x, y):
    data = [
            {
                "name": "CALLs",
                "x": x,
                "y": y,
                "text": text,
                "mode": "markers"
            }        
    ]
    
    layout = {}

    plotargs = {"data": data, "layout":layout}
    return plotargs
