def form_plotargs(x, y, height, title):
    data = [
            {
                "x": x,
                "y": y,
                "type": "bar",
                "orientation": "h"
            }
        ] 
        
    layout = {
                "title": title,
                "width": 1000,
                "height": height,
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
