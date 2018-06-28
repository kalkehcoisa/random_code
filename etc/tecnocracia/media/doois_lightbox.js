/*******************************************************************************
 jquery.doois.lightbox
 Copyleft (c) 2011. Jayme Tosi Neto - .doois.
 Email: jayme@doois.com.br
 Site: http://www.doois.com.br
 ******************************************************************************/

/*
 * Name: jquery.doois.lightbox
 * Version: 0.1
 */



$.fn.extend({

    my_scrollbar: function()
    {
        $.settings =
        {
            MEDIA_URL: window.my_settings.MEDIA_URL+'js/my_scrollbar',
        }

        $(this).each(function(i, elem)
        {
            $(elem).my_create_object( $(elem) );
        });

        return $(this);
    },

    my_mousemove: function(ev)
    {
        var $gp = $('.my_scrolled_elem.active');
        
        var move = ev.pageY - parseFloat($gp.attr('reft')) - $gp.find('.my_scroller').height()/2;
        var real_move = 0;


        if( move > 0 && move < parseFloat($gp.attr('refd')) ) //normal movement
           real_move = move;
        else
        { //on extremes
           if( move <= 0 )
               real_move = 0;
           if( move > parseFloat( $gp.attr('refd')) )
               real_move = parseFloat( $gp.attr('refd') );
        }
        $gp.find('.my_scroller').css({'top': real_move+'px'});
        $gp.find('.my_scrolled_content').css('margin-top','-'+(parseFloat($gp.attr('scroll_prop'))*real_move)+'px');
    }
    
});
