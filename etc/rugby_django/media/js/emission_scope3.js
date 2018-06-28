function hideAll()
{
    $('#calculo_terrestre').hide();
    $('#calculo_aereo').hide();
    $('#calcs_1').hide();
    $('#calcs_2').hide();
    $('#calcs_3').hide();
    $('#calcs_mock').hide();
    $('#relato_direto').hide();
    noValidateAllChildren('body');
}

function toogle_itens(gas)
{
    if( $("#"+gas+"_emission_factor_type").val() == 'Reporter')
    {
        var temp =  'Fator de emiss&atilde;o:'+
                    '<input name="'+gas+'_emission_factor" type="text" class="t80" minlength="1" maxlength="50" data="numeric" customdata=".," /><br /><br />'+
                    'Fonte de F.E:'+
                    '<input name="'+gas+'_emission_factor_source" type="text" class="t80" minlength="1" maxlength="50" data="numeric" customdata=".," />';

        $("#"+gas+"_calc_fields").html("");
        $("#"+gas+"_calc_fields").append(temp);
    }
    else
        $("#"+gas+"_calc_fields").html("");
}


function reloadEmissionFactorValues(data)
{
    dados = data.split(";")

    var dist = parseFloat( $('#distance').val() ) * parseFloat( dados[1] );

    if ( dados[0] == 1 && $('#co2_emission_factor_type').val() == 'Program' ) //co2
    {
        $('#co2_calc_fields').html("");
        $('#co2_calc_fields').html( '<span>' + dados[1] + '</span>' );
        $('[name=co2_quantity]').attr('value', dist );
        $('#co2_quantity').html( dist );
    }
    if ( dados[0] == 16 && $('#ch4_emission_factor_type').val() == 'Program' ) //ch4
    {
        $('#ch4_calc_fields').html("");
        $('#ch4_calc_fields').html( '<span>' + dados[1] + '</span>' );
        $('[name=ch4_quantity]').attr('value', dist );
        $('#ch4_quantity').html( dist );
    }
    if ( dados[0] == 20 && $('#n2o_emission_factor_type').val() == 'Program' ) //n2o
    {
        $('#n2o_calc_fields').html("");
        $('#n2o_calc_fields').html( '<span>' + dados[1] + '</span>' );
        $('[name=n2o_quantity]').attr('value', dist );
        $('#n2o_quantity').html( dist );
    }

}

function reloadEmissionFactorValues_Reporter(gas)
{
    var dist = parseFloat( $('#distance').val() );
    var fator = parseFloat( $('[name='+gas+'_emission_factor]').val() );
    
    $('[name='+gas+'_quantity]').attr('value', dist*fator );
    $('#'+gas+'_quantity').html( dist*fator );
}





function reloadEmissionFactorValues2(data)
{
    dados = data.split(";")

    var dist = parseFloat( $('[name=fuel_quantity]').val() ) * parseFloat( dados[1] );

    if ( dados[0] == 1 ) //co2
    {
        $('#co2_calc_fields').html("");
        $('#co2_calc_fields').html( '<span>' + dados[1] + '</span>' );
        $('[name=co2_quantity]').attr('value', dist );
        $('#co2_quantity').html( dist );
    }
    if ( dados[0] == 16 ) //ch4
    {
        $('#ch4_calc_fields').html("");
        $('#ch4_calc_fields').html( '<span>' + dados[1] + '</span>' );
        $('[name=ch4_quantity]').attr('value', dist );
        $('#ch4_quantity').html( dist );
    }
    if ( dados[0] == 20 ) //n2o
    {
        $('#n2o_calc_fields').html("");
        $('#n2o_calc_fields').html( '<span>' + dados[1] + '</span>' );
        $('[name=n2o_quantity]').attr('value', dist );
        $('#n2o_quantity').html( dist );
    }

}

function reloadEmissionFactorValues_Reporter2(gas)
{
    var dist = parseFloat( $('[name=fuel_quantity]').val() );
    var fator = parseFloat( $('[name='+gas+'_emission_factor]').val() );

    $('[name='+gas+'_quantity]').attr('value', dist*fator );
    $('#'+gas+'_quantity').html( dist*fator );
}






function reloadFuels(data)
{
    $("#fuel").html("");

    $('#fuel').append("<option value='-'>- Selecione -</option>");

    $.each(data, function(index, item)
    {
        $('#fuel').append("<option value='"+item.pk+"'>"+item.fields.name+"</option>");
    });

}














$('document').ready(function()
{
    hideAll();
    $('#relato_direto').show();
    ValidateAllChildren('#relato_direto');
    $('#option_tab').removeAttr('novalidate');




    $('#auto_air_calc').click(function()
    {
        clearErrors();
        hideAll();
        ValidateAllChildren('#calculo_aereo');
        ValidateAllChildren('#calcs_1');
        ValidateAllChildren('#calcs_2');
        ValidateAllChildren('#calcs_3');
        $('#option_tab').removeAttr('novalidate');


        $('#option_tab').attr('value', 'air');
        $('#calculo_aereo').show();
        $('#calcs_1').show();
        $('#calcs_2').show();
        $('#calcs_3').show();


        $('#co2_emission_factor_type option:eq(0)').attr('selected', 'selected');
        $('#ch4_emission_factor_type option:eq(0)').attr('selected', 'selected');
        $('#n2o_emission_factor_type option:eq(0)').attr('selected', 'selected');
        $.post("/factors/recover_factor_value", {'fuel': '1', 'sector': '2', 'gas': '1'}, reloadEmissionFactorValues );
        $.post("/factors/recover_factor_value", {'fuel': '1', 'sector': '2', 'gas': '16'}, reloadEmissionFactorValues );
        $.post("/factors/recover_factor_value", {'fuel': '1', 'sector': '2', 'gas': '20'}, reloadEmissionFactorValues );


        $("#co2_emission_factor_type").change( function()
        {
            toogle_itens('co2');
            if( $(this).val() == 'Reporter')
                $('[name=co2_emission_factor]').blur( function(){ reloadEmissionFactorValues_Reporter('co2') });
            else
                $.post("/factors/recover_factor_value", {'fuel': '1', 'sector': '2', 'gas': '1'}, reloadEmissionFactorValues );
        });
        $("#ch4_emission_factor_type").change( function()
        {
            toogle_itens('ch4');
            if( $(this).val() == 'Reporter')
                $('[name=ch4_emission_factor]').blur( function(){ reloadEmissionFactorValues_Reporter('ch4') });
            else
                $.post("/factors/recover_factor_value", {'fuel': '1', 'sector': '2', 'gas': '16'}, reloadEmissionFactorValues );
        });
        $("#n2o_emission_factor_type").change( function()
        {
            toogle_itens('n2o');
            if( $(this).val() == 'Reporter')
                $('[name=n2o_emission_factor]').blur( function(){ reloadEmissionFactorValues_Reporter('n2o') });
            else
                $.post("/factors/recover_factor_value", {'fuel': '1', 'sector': '2', 'gas': '20'}, reloadEmissionFactorValues );
        });


        $('[name=distance]').blur( function()
        {
            if( $("#co2_emission_factor_type").val() == 'Reporter')
                $('[name=co2_emission_factor]').blur( function(){ reloadEmissionFactorValues_Reporter('co2') });
            else
                $.post("/factors/recover_factor_value", {'fuel': '1', 'sector': '2', 'gas': '1'}, reloadEmissionFactorValues );

            if( $("#ch4_emission_factor_type").val() == 'Reporter')
                $('[name=ch4_emission_factor]').blur( function(){ reloadEmissionFactorValues_Reporter('ch4') });
            else
                $.post("/factors/recover_factor_value", {'fuel': '1', 'sector': '2', 'gas': '16'}, reloadEmissionFactorValues );

            if( $("#n2o_emission_factor_type").val() == 'Reporter')
                $('[name=n2o_emission_factor]').blur( function(){ reloadEmissionFactorValues_Reporter('n2o') });
            else
                $.post("/factors/recover_factor_value", {'fuel': '1', 'sector': '2', 'gas': '20'}, reloadEmissionFactorValues );
        });

    });









    $('#auto_land_calc').click(function()
    {
        clearErrors();
        hideAll();
        ValidateAllChildren('#calculo_terrestre');
        ValidateAllChildren('#calcs_1');
        ValidateAllChildren('#calcs_mock');
        $('#option_tab').removeAttr('novalidate');


        $('#option_tab').attr('value', 'land');
        $('#calculo_terrestre').show();
        $('#calcs_1').show();
        $('#calcs_mock').show();


        $('#co2_emission_factor_type option:eq(0)').attr('selected', 'selected');

        $.ajax({
            url: "/factors/recover_fuels",
            dataType: 'json',
            data: {'emission_type': 'S'},
            type: 'POST',
            success: reloadFuels
         });



        $("#co2_emission_factor_type").change( function()
        {
            toogle_itens('co2');
            if( $("#co2_emission_factor_type").val() == 'Reporter')
                $('[name=co2_emission_factor]').blur( function(){ reloadEmissionFactorValues_Reporter2('co2') });
            else
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel').val(), 'sector': '2', 'gas': '1'}, reloadEmissionFactorValues2 );
        });

        $('[name=fuel_quantity]').blur(function()
        {
            if( $('#co2_emission_factor_type option:selected').val() == 'Program'  )
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel').val(), 'sector': '2', 'gas': '1'}, reloadEmissionFactorValues2 );
            else
                reloadEmissionFactorValues_Reporter2('co2');
        });

        $('#fuel').change(function()
        {
            if( $('#co2_emission_factor_type option:selected').val() == 'Program'  )
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel').val(), 'sector': '2', 'gas': '1'}, reloadEmissionFactorValues2 );
            else
                reloadEmissionFactorValues_Reporter2('co2');
        });



    });

    
    $('#manual').click(function()
    {
        clearErrors();
        hideAll();
        ValidateAllChildren('#relato_direto');
        $('#option_tab').removeAttr('novalidate');


        $('#option_tab').attr('value', 'manual');
        $('#relato_direto').show();
    });



});
