$(document).ready(function()
{
    //posiciona a construcao na posicao escolhida se possivel
    var posicionaConstrucao = function( elemento, topo, esquerda )
    {
        var pieces = elemento.find('img');
        var comprimento = Math.sqrt( pieces.length )

        
        //variavel para verificar se e possivel posicionar o elemento na 
        //posicao em que o usuario deseja
        var teste_posiciona = false;
        
        //verifica se e possivel posicionar a construcao onde o usaurio deseja
        var obj, i=0, j=0;
        for(i=0;i<comprimento;i++)
        {
            for(j=0;j<comprimento;j++)
            {
                teste_posiciona = $('.my_city tr').eq( topo + i ).children().eq( esquerda + j ).children().length > 0;
                if( teste_posiciona ) break;
            }
            if( teste_posiciona ) break;
        }

        //posiciona o elemento caso nao haja nenhum conflito de posicao
        if( !teste_posiciona )
        {
            for(i=0;i<comprimento;i++)
            {
                for(j=0;j<comprimento;j++)
                {
                    obj = $('.selectedBuilding').filter('[counter="'+(i*comprimento+j+1)+'"]');
                    $('.my_city tr').eq( topo + i ).children().eq( esquerda + j ).append( obj );
                }
            }

            elemento.empty().remove();
            return true;
        }
        else
        {
            elemento.empty().remove();
            return false;
        }
        
    }
    
    
    
    $('.construcao').mouseenter(function()
    {
        //variavel para armazenar o objeto flutuante que sera usado para 
        //o drag n drop
        var container = '<div id="'+$(this).attr('name')+'_container">';

        //armazena as pecas da construcao
        var pieces = $('img[name^='+$(this).attr('name')+']');
        var line_length = Math.sqrt(pieces.length);

        //remove as marcacoes e marca a construcao atual como a construcao sendo manipulada
        $('.selectedBuilding').removeClass('selectedBuilding');
        $('img[name^='+$(this).attr('name')+']').addClass('selectedBuilding');


        //monta o codigo da construcao flutuante
        $.each( pieces, function(i, obj)
        {
            if( i % line_length == 0 ) container += '<ul class="inlineblock">';
            container += '<li>' + $(this).parent().html() + '</li>';
            if( i % line_length == line_length - 1 ) container += '</ul>';
        });
        container += '</div>';
        $( document.body ).append( container );

        
        //armazena a peca da esquerda de cima da construcao
        var top_left = pieces.filter('[counter="1"]');
        var self = $('#'+$(this).attr('name')+'_container');

        //define a posicao do novo elemento para cobrir a construcao atual
        self.css(
        {
            position: 'absolute',
            top: top_left.position().top, //position retorna a posicao relativa ao pai
            left: top_left.position().left, //position retorna a posicao relativa ao pai
            opacity: 0.5,
            'z-index': 100,
            position: 'absolute'
        }).addClass('temp_clone');
        self.find('img').removeAttr('class').addClass('construcao_floater');



        
        self.drag("start", function( ev, dd )//este ocorre ao clicar e arrastar
        {
            var $cont = $('table.my_city'); //pega a tabela principal para os limites do drag n drop
            
            //define os limites para o drag n drop
            dd.limit = $cont.offset();
            dd.limit.bottom = dd.limit.top + $cont.outerHeight() - $( this ).outerHeight();
            dd.limit.right = dd.limit.left + $cont.outerWidth() - $( this ).outerWidth();

            return $( this ).clone()
                    .css({"opacity": 0.5, 'z-index': 100, 'position': 'absolute'} )
                    .appendTo( document.body );

        }).drag(function( ev, dd )//este evento ocorre durante o drag em si
        {
            //define os limites para o drag n drop
            var top = dd.limit.top + Math.round( Math.min( dd.limit.bottom, Math.max( dd.limit.top, dd.offsetY ) ) / 50 ) * 50;
            var left = dd.limit.left +  Math.round( Math.min( dd.limit.right, Math.max( dd.limit.left, dd.offsetX ) ) / 50 ) * 50;

            $( dd.proxy ).css({ top: top, left: left });
        })
        .drag("end", function( ev, dd ) //este evento ocorre ao realizar o "drop"
        {
            //define os limites para o drag n drop
            var top = Math.round( Math.min( dd.limit.bottom, Math.max( dd.limit.top, dd.offsetY ) ) / 50 ) * 50;
            var left = Math.round( Math.min( dd.limit.right, Math.max( dd.limit.left, dd.offsetX ) ) / 50 ) * 50;

            $( this ).animate({ top: top, left: left }, 420 );
            $( dd.proxy ).remove();
            
            //posiciona a construcao na posicao escolhida se possivel
            posicionaConstrucao( $(this), top/50, left/50 );
            
            //remove as marcacoes
            $('.selectedBuilding').removeClass('selectedBuilding');
        });

    }).mouseout(function()
    {
        $(this).unbind('drag');
    });


    var hoverInterval;
    var moveUp = function()
    {
        $.scrollTo('-=10px', 50, {axis: 'y'});
    }
    var moveDown = function()
    {
        $.scrollTo('+=10px', 50, {axis: 'y'});
    }
    
    $(".button_move_up").hover(function()
    {
        // call doStuff every 100 milliseconds
        hoverInterval = setInterval(moveUp, 50);
    },
    function()
    {
        // stop calling doStuff
        clearInterval(hoverInterval);
    });
    $(".button_move_down").hover(function()
    {
        // call doStuff every 100 milliseconds
        hoverInterval = setInterval(moveDown, 50);
    },
    function()
    {
        // stop calling doStuff
        clearInterval(hoverInterval);
    });
});