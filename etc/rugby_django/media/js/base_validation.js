function hide(label)
{
    $('[name='+label+']').qtip('hide');
}


function initValidation()
{
    //limita a quantidade de caracteres nos campos
    //e quais caracteres podem ser inseridos
    $('input:text').each(function()
    {
        if( $(this).attr('data') == 'alphanumeric' )
            if( $(this).attr('customdata') && $(this).attr('customdata').length > 0 )
                $(this).alphanumeric({allow:$(this).attr('customdata')});
            else
                $(this).alphanumeric();


        if( $(this).attr('data') == 'alpha' )
            if( $(this).attr('customdata') && $(this).attr('customdata').length > 0 )
                $(this).alpha({allow:$(this).attr('customdata')});
            else
                $(this).alpha();


        if( $(this).attr('data') == 'numeric' )
            if( $(this).attr('customdata') && $(this).attr('customdata').length > 0 )
                $(this).numeric({allow:$(this).attr('customdata')});
            else
                $(this).numeric();


        var length = parseInt( $(this).attr('maxlength') );


        //cria a funcao de aviso associada ao elemento
        $(this).qtip(
        {
            position:
            {
                corner:
                {
                    target: 'topLeft',
                    tooltip: 'bottomLeft'
                }
            },
            content: "Maximo de "+length+" caracteres!",
            show: {when: false},
            hide: {when: false},
            style:
            {
                name: 'cream',
                tip: 'bottomLeft',
                border:
                {
                    width: 1,
                    radius: 12,
                    color:'#F49105'
                },
                color: '#fff',
                background: '#F49105'
            }
        });


        //faz a verificacao do limite de caracteres
        $(this).keydown(function()
        {
            //se ultrapassou o limite exibe uma mensagem avisando e
            //some com ela depois de 2000 ms
            if( $(this).val().length > length-1 )
            {
                $(this).attr('value', $(this).val().substring(0, length) );
                var name = $(this).attr('name');
                $(this).qtip('show').ready(function()
                {
                    setTimeout( hide, 2000, name );
                });
            }
        });

    });
}



function clearErrors()
{
    //apaga as mensagens de erro
    $('.destaque_validation').each(function()
    {
        $(this).qtip('hide').qtip('destroy');
        $(this).removeClass('destaque_validation');
        $(this).css({'border':'none'});
    });
}



function noValidateChildren(selectorFather, selectorChildren)
{
    $(selectorFather).find(selectorChildren).each(function()
    {
        $(this).attr('novalidate', true);
    });
}

function noValidateAllChildren(selectorFather)
{
    noValidateChildren(selectorFather, 'input');
    noValidateChildren(selectorFather, 'textarea');
    noValidateChildren(selectorFather, 'select');
}




function ValidateChildren(selectorFather, selectorChildren)
{
    $(selectorFather).find(selectorChildren).each(function()
    {
        $(this).removeAttr('novalidate');
    });
}


function ValidateAllChildren(selectorFather)
{
    ValidateChildren(selectorFather, 'input');
    ValidateChildren(selectorFather, 'textarea');
    ValidateChildren(selectorFather, 'select');
}




$('document').ready(function()
{

    initValidation();



    $('form').submit(function()
    {
        var ok = true;
        var i = 0, cont = 0;
        var names = Array();
        var messages = Array();


        clearErrors();


        //verifica se todos os campos do tipo texto possuem
        //o tamanho minimo especificado em minlength
        $('input:text').each(function()
        {
            if( $(this).attr('novalidate') && $(this).attr('novalidate').length > 0 )
                return true; //continue

            //alert( $(this).attr('name') );


            var leng = $(this).val().length;
            var aux = parseInt( $(this).attr('minlength') );
            
            min = ( isNaN(aux) ) ? 0 : aux;

            
            if( leng < min )
            {
                messages[cont] = "Minimo de "+min+" caracteres!";
                names[cont] = $(this).attr('name');
                cont++;
                ok = false;
            }

        });



        //verifica a situacao de todos os select box
        $('select').each(function()
        {
            if( $(this).attr('novalidate') && $(this).attr('novalidate').length > 0 )
                return true; //continue

            if( $(this).val() == '-' )
            {
                messages[cont] = "Escolha alguma opcao!";
                names[cont] = $(this).attr('name');
                cont++;
                ok = false;
            }
        });


        //verifica a situacao de todos os select box
        $('textarea').each(function()
        {
            if( $(this).attr('novalidate') && $(this).attr('novalidate').length > 0 )
                return true; //continue

            $(this).removeClass('destaque_validation');
            

            var aux = parseInt( $(this).attr('minlength') );
            var min = ( isNaN(aux) ) ? 0 : aux;


            if( $(this).val().length < min )
            {
                messages[cont] = "Digite ao menos "+min+" caracteres";
                names[cont] = $(this).attr('name');
                cont++;
                ok = false;
            }
        });




        var targ = 'rightMiddle';
        var tool = 'leftMiddle';
        //exibe as mensagens pedindo correcao nos campos
        for(i=0;i<cont;i++)
        {
            //posiciona o balao de aviso conforme o valor de tip
            if( $('[name='+names[i]+']').attr('tip') == 'left' )
            {
                tool = 'rightMiddle';
                targ = 'leftMiddle';
            }
            else
            {
                tool = 'leftMiddle';
                targ = 'rightMiddle';
            }
            if( $('[name='+names[i]+']').attr('tip') == 'bottomMiddle')
            {
                tool = 'topMiddle';
                targ = 'bottomMiddle';
            }


            $('[name='+names[i]+']').addClass('destaque_validation');
            $('[name='+names[i]+']').css({'border':'solid 1px red'});


            //cria a funcao de aviso associada ao elemento
            $('[name='+names[i]+']').qtip(
            {
                position:
                {
                    corner:
                    {
                        target: targ,
                        tooltip: tool
                    }
                },
                content: messages[i],
                show: {when: false},
                hide: {when: false},
                style:
                {
                    name: 'cream',
                    tip: tool,
                    border:
                    {
                        width: 1,
                        radius: 2,
                        color:'#F49105'
                    },
                    color: '#fff',
                    background: '#F49105'
                }
            }).qtip('show');
        }

        //alert(ok);
        return ok;
    });



});