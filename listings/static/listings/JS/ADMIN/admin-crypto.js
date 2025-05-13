(function($) {
    "use strict"
    
	var dzChartlist = function(){
        var screenWidth = $(window).width();
     
         
        var peityLine = function(){
            $(".peity-line").peity("line", {
                fill: ["rgba(234, 73, 137, .0)"], 
                stroke: '#EB8153', 
                strokeWidth: '4', 
                width: "280",
                height: "50"
            });
        }
            return {
                init:function(){
                },
                
                
                load:function(){			
                    peityLine();			
                },
                
                resize:function(){
                }
            }
    
        }();
            
        jQuery(window).on('load',function(){
            setTimeout(function(){
                dzChartlist.load();
            }, 1000); 
            
        });
    
        jQuery(window).on('resize',function(){
            
            
        });     
    
        // 
        var table = $('#example3, #example4, #example5').DataTable({
            language: {
                paginate: {
                    next: '<p style = "color:black"> \>\></p>',
                    previous: '<p style = "color:black"> \<\<</p>' 
                }
            }
        });
        $('#example tbody').on('click', 'tr', function () {
            var data = table.row( this ).data();
        });

})(jQuery);