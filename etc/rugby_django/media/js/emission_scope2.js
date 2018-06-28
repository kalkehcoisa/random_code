function toogleValidation()
{
    var aux = $("input:radio[name=forma_calculo]:checked").val();
    var i = 1;

    if( aux == 'Anual' )
    {
        $('#anual').removeAttr('novalidate');

        for(i=1;i<=12;i++)
            $('#mes_'+i).attr('novalidate', true);
    }
    else
    {
        $('#anual').attr('novalidate', true);

        for(i=1;i<=12;i++)
            $('#mes_'+i).removeAttr('novalidate');
    }

}


function toogleFactor()
{
    var aux = $("input:radio[name=methodology]:checked").val();

    if( aux == 'Report' )
    {
        $('[name=custom_methodology]').removeAttr('novalidate');
        $('[name=justificative]').removeAttr('novalidate');
    }
    else
    {
        $('[name=custom_methodology]').attr('novalidate', true);
        $('[name=justificative]').attr('novalidate', true);
    }
}



function calculaEmissao()
{
    var aux = $("input:radio[name=forma_calculo]:checked").val();

    if( aux == 'Anual' )
    {
        aux = parseFloat( $('#anual').val() );
    }
    else
    {
        var i = 1;
        aux = 0;
        for(i=1;i<=12;i++)
            aux += parseFloat( $('#mes_'+i).val() );

        $('[name=fuel_mensal]').attr('value', aux);
    }

    if( $("input:radio[name=methodology]:checked").val() == 'Program' )
        aux *= 2;
    else
        aux *= parseFloat( $("input[name=custom_methodology]").val() );

    $('[name=co2_emission]').attr('value', aux );
}



function toogleUnidade()
{
    if( $("input[name='methodology']:checked").val() == 'Report' )
        $('#proprio_unit').html('tCO2e/MWh');
    else
        $('#proprio_unit').html('');
}















$('document').ready(function()
{
    toogleFactor();
    $('#eletric_2').hide();
    $('#bought_steam_1').hide();


    $('#emission_font option:eq(0)').attr('selected', 'selected');


    $('#eletric_2').find(':radio').change( calculaEmissao ).click( calculaEmissao );

    $('[name=forma_calculo]').click( toogleValidation );

    $('#anual').click(function()
    {
        $('#anual_radio').attr('checked', 'true');
        toogleValidation();
    });

    $('#met_rep').click(function()
    {
        $('#met_rep').attr('checked', 'true');
        toogleUnidade();
        calculaEmissao();

    }).change( toogleUnidade );

    $('#met_pro').click(function()
    {
        $('#met_pro').attr('checked', 'true');
        toogleUnidade();
        calculaEmissao();
        $('#fonte_do_fator').hide();

    }).change( toogleUnidade ).blur( calculaEmissao );
    $('#met_rep').click(function()
    {
        $('#met_rep').attr('checked', 'true');
        toogleUnidade();
        calculaEmissao();
        $('#fonte_do_fator').show();

    }).change( toogleUnidade ).blur( calculaEmissao );



    var i = 1;
    for(i=1;i<=12;i++)
    {
        $('#mes_'+i).attr('value', 0);
        $('#mes_'+i).click(function()
        {
            $('#mensal_radio').attr('checked', 'true');
            calculaEmissao();
            toogleValidation();
        });
    }

    $("#met_pro").attr("checked", true);
    $("#met_false").attr("checked", false);

    $('input').blur( calculaEmissao ).click( calculaEmissao );




    //$.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '1'}, reloadEmissionFactorValues );
    $('[name=methodology]').click( toogleFactor );







    function reloadFuels(data)
    {
        $("#unidades").html("");
        $("#fuel").html("");

        $('#fuel').append("<option value='-'>- Selecione -</option>");

        $.each(data, function(index, item)
        {
            $('#fuel').append("<option value='"+item.pk+"'>"+item.fields.name+"</option>");
            $('#unidades').append("<input type='hidden' id='unity_"+item.pk+"' value='"+item.fields.unity+"' />");
        });

    }


    jQuery('#co2_emission_factor_type option:eq(0)').attr('selected', 'selected');

    function calculaEmissaoCo2()
    {
        //parseFloat( $('#eficiency').val() )
        var aux = parseFloat( $('#quantity_fuel').val() );

        if( $("#co2_emission_factor_type").val() == 'Reporter')
            aux *= $('[name=co2_emission_factor]').val();
        else
            aux *= $('[name=co2_factor]').val();
        

        $('#co2_quantity').html("");
        $('#co2_quantity').html(aux);
        $('[name=co2_quantity]').attr('value', aux);
    }


    function reloadEmissionFactorValues(data)
    {
        dados = data.split(";")

        if ( dados[0] == 1 ) //co2
        {
            if( $("#co2_emission_factor_type").val() == 'Program')
            {
                $('#co2_calc_fields').html("");
                $('#co2_calc_fields').html( '<span>' + dados[1] + '</span>' );
            }
            $('[name=co2_factor]').attr('value', dados[1]);
            calculaEmissaoCo2();
        }
    }








    noValidateAllChildren('body');


    $('#emission_font').change(function()
    {
        clearErrors();
        noValidateAllChildren('body');


        //selecione
        if( $('#emission_font').val() == '-')
        {
            $('#eletric_2').hide();
            $('#bought_steam_1').hide();

            $('[name=aux_val]').attr('value', '-');
        }


        //energia eletrica
        if( $('#emission_font').val() == 'EP')
        {
            ValidateAllChildren('#eletric_2');
            toogleValidation();

            $('#eletric_2').show();
            $('#bought_steam_1').hide();

            $('[name=justificative]').attr('novalidate', true);
            $('[name=aux_val]').attr('value', 'EP');
        }


        //compra de vapor
        if( $('#emission_font').val() == 'BS')
        {
            ValidateAllChildren('#bought_steam_1');


            $('#anual').attr('novalidate', true);

            $('#eletric_2').hide();
            $('#bought_steam_1').show();


            $('[name=aux_val]').attr('value', 'BS');

            $.ajax({
                url: "/factors/recover_fuels",
                dataType: 'json',
                data: {'emission_type': 'S'},
                type: 'POST',
                success: reloadFuels
             });


             $('#quantity_fuel').blur( calculaEmissaoCo2 );

             $('#fuel').change(function()
             {
                 $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': '2', 'gas': '1'}, reloadEmissionFactorValues );
                 calculaEmissaoCo2();
             });

            $("#co2_emission_factor_type").change(function()
            {
                if( $("#co2_emission_factor_type").val() == 'Reporter')
                {
                    var temp =  'Fator de emiss&atilde;o:'+
                                '<input name="co2_emission_factor" type="text" class="t80" minlength="1" maxlength="50" data="numeric" customdata=".," /><br /><br />'+
                                'Fonte de F.E:'+
                                '<input name="co2_emission_factor_source" type="text" class="t80" minlength="1" maxlength="50" data="numeric" customdata=".," />';

                    $("#co2_calc_fields").html("");
                    $("#co2_calc_fields").append(temp);
                    $('[name=co2_emission_factor]').blur(function()
                    {
                        calculaEmissaoCo2();
                    });
                }
                else
                {
                    $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': '2', 'gas': '1'}, reloadEmissionFactorValues );
                }

            });

        }

    });



});
