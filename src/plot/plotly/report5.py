def form_plotargs(x, y):
    data = [
            {
                "x": x,
                "y": y,
                "type": "bar",
                "orientation": "h"
            }
        ] 
        
    layout = {
                "title": "High/Low Open interest",
                "width": 1000,
                "margin": {
                            "autoexpand": True,
                            "l": 120
                          },
                "xaxis": {
                            "showline": True,
                            "title": "Open interest"
                         },
                "yaxis": {
                            "showline": True,
                            "title": "Scrip"
                         }

             }   

    plotargs = {"data": data, "layout": layout}
    print plotargs
    return plotargs
