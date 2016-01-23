def form_plotargs(x, y):
    data = [
            {
                "x": x,
                "y": y,
                "mode": "markers"
                # "marker": {
                            # "color": ["rgb(93, 164, 214)", 
                                      # "rgb(255, 144, 14)",
                                      # "rgb(44, 160, 101)", 
                                      # "rgb(255, 65, 54)"],
                            # "opacity": [1, 0.8, 0.6, 0.4],
                            # "size": [40, 60, 80, 100]
                          # }
            }
        ] 
        
    layout = {
              "showlegend": False,
                "height": 600,
                  "width": 600}   

    plotargs = {"data": data, "layout": layout}
    print plotargs
    return plotargs
