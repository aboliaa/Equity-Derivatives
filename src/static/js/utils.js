function plot(input_data){
    return jQuery.ajax({                                                                   
                url: '/getdata/',                                                    
                type: 'GET',       
                data: input_data,
                dataType: 'json',                                                  
                async: false,
    });
}

