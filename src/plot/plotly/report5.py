def form_plotargs(x, y, height, title):
    data = [
            {
                "x": x,
                "y": y,
                "type": "bar",
                "hoverinfo": "x+y",
                "orientation": "h"
            }
        ] 
        
    layout = {
                "title": title,
                "width": 1200,
                "height": height,
                "margin": {
                            "autoexpand": True,
                            "l": 120
                          },
                "xaxis": {
                            "showline": True,
                            "title": "Open Interest"
                         },
                "yaxis": {
                            "showline": True,
                            "title": "Scrip"
                         }

             }   

    if any(x):
        isempty = 0
    else:
        isempty = 1

    plotargs = {"data": data, "layout": layout, "empty": isempty}
    return plotargs
