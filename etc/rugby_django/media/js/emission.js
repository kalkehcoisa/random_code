
function addOption(elementselector, value, label)
{
    $(elementselector).append("<option value='"+value+"'>"+label+"</option>");
}

function reloadEmissionTypes(data)
{
    emissions = data.split(";")

    $("#co2_emission_factor_type").html("");
    $("#ch4_emission_factor_type").html("");
    $("#n2o_emission_factor_type").html("");

    if (emissions[0] == 1)
        addOption("#co2_emission_factor_type", "Program", "Fator do Programa");
    if (emissions[1] == 1)
        addOption("#co2_emission_factor_type", "Reporter", "Fator do Próprio");
    if (emissions[2] == 1)
        addOption("#ch4_emission_factor_type", "Program", "Fator do Programa");
    if (emissions[3] == 1)
        addOption("#ch4_emission_factor_type", "Reporter", "Fator do Próprio");
    if (emissions[4] == 1)
        addOption("#n2o_emission_factor_type", "Program", "Fator do Programa");
    if (emissions[5] == 1)
        addOption("#n2o_emission_factor_type", "Reporter", "Fator do Próprio");

}




function reloadSectors(data)
{
    $("#sector").html("");
    $.each(data, function(index, item)
    {
        addOption("#sector", item.pk, item.fields.name);
    });
}


function reloadFuels(data)
{
    $("#unidades").html("");
    $("#fuel").html("");

    addOption("#fuel", '-', '- Selecione -');

    $.each(data, function(index, item)
    {
        addOption("#fuel", item.pk, item.fields.name);
        $('#unidades').append("<input type='hidden' id='unity_"+item.pk+"' value='"+item.fields.unity+"' />");
    });

}





function toogle_itens(gas)
{
    if( $("#"+gas+"_emission_factor_type").val() == 'Reporter')
    {
        var temp =  'Fator de emiss&atilde;o:<br/>'+
                    '<input name="'+gas+'_emission_factor" type="text" class="t80" minlength="1" maxlength="100" data="numeric" customdata=".," />'+
                    '<span id="unidade_p_'+gas+'"></span><br /><br />'+
                    'Fonte de F.E:<br/>'+
                    '<input name="'+gas+'_emission_factor_source" type="text" class="t80" minlength="1" maxlength="100" data="alphanumeric" />';

        $("#"+gas+"_calc_fields").html("");
        $("#"+gas+"_calc_fields").append(temp);
        $("#unidade_"+gas).html("");
        $('#unidade_p_'+gas).html( " t/" + $( '#unity_'+$('#fuel :selected').val() ).val() );
    }
    else
    {
        $("#"+gas+"_calc_fields").html("");
        $("#unidade_"+gas).html( " t/" + $( '#unity_'+$('#fuel :selected').val() ).val() );
    }
}


function reloadEmissionFactorValues(data)
{
    dados = data.split(";")

    var dist = parseFloat( $('[name=fuel_quantity]').val() ) * parseFloat( dados[1] );


    if ( dados[0] == 1 && $("#co2_emission_factor_type").val() == 'Program' ) //co2
    {
        $('#co2_calc_fields').html("");
        $('#co2_calc_fields').html( '<span>' + dados[1] + '</span>' );
        $('[name=co2_quantity]').attr('value', dist );
        $('#co2_quantity').html( dist );
    }
    if ( dados[0] == 16 && $("#ch4_emission_factor_type").val() == 'Program' ) //ch4
    {
        $('#ch4_calc_fields').html("");
        $('#ch4_calc_fields').html( '<span>' + dados[1] + '</span>' );
        $('[name=ch4_quantity]').attr('value', dist );
        $('#ch4_quantity').html( dist );
    }
    if ( dados[0] == 20 && $("#n2o_emission_factor_type").val() == 'Program' ) //n2o
    {
        $('#n2o_calc_fields').html("");
        $('#n2o_calc_fields').html( '<span>' + dados[1] + '</span>' );
        $('[name=n2o_quantity]').attr('value', dist );
        $('#n2o_quantity').html( dist );
    }

}


function clearEmissionFactorValues()
{
    $('#co2_calc_fields').html("");
    $('[name=co2_quantity]').attr('value', 0 );
    $('#co2_quantity').html( 0.0 );

    $('#ch4_calc_fields').html("");
    $('[name=ch4_quantity]').attr('value', 0 );
    $('#ch4_quantity').html( 0.0 );

    $('#n2o_calc_fields').html("");
    $('[name=n2o_quantity]').attr('value', 0 );
    $('#n2o_quantity').html( 0.0 );
}


function reloadEmissionFactorValues_Reporter(gas)
{
    var dist = parseFloat( $('[name=fuel_quantity]').val() );
    var fator = parseFloat( $('[name='+gas+'_emission_factor]').val() );

    $('[name='+gas+'_quantity]').attr('value', dist*fator );
    $('#'+gas+'_quantity').html( dist*fator );
}








$('document').ready(function()
{
    jQuery('#emission_type option:eq(0)').attr('selected', 'selected');
    $('#sector_wrapper').hide();
    $('#buttons_wrapper').hide();



    $('#fuel').change(function()
    {
        var aux = $( '#unity_'+jQuery('#fuel').val() ).val();
        clearEmissionFactorValues();


        $('#unidade').html("");
        $('#unidade').html( aux );

        $('#unidade_co2').html( "" );
        $('#unidade_ch4').html( "" );
        $('#unidade_n2o').html( "" );
        $('#unidade_co2').html( "t/" + aux );
        $('#unidade_ch4').html( "t/" + aux);
        $('#unidade_n2o').html( "t/" + aux );


        $('#co2_emission_factor_type option:eq(0)').attr('selected', 'selected');
        $('#ch4_emission_factor_type option:eq(0)').attr('selected', 'selected');
        $('#n2o_emission_factor_type option:eq(0)').attr('selected', 'selected');
        $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '1'}, reloadEmissionFactorValues );
        $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '16'}, reloadEmissionFactorValues );
        $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '20'}, reloadEmissionFactorValues );


        $("#co2_emission_factor_type").change( function()
        {
            toogle_itens('co2');

            if( $(this).val() == 'Reporter')
                $('[name=co2_emission_factor]').blur( function(){ reloadEmissionFactorValues_Reporter('co2') });
            else
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '1'}, reloadEmissionFactorValues );

        });
        $("#ch4_emission_factor_type").change( function()
        {
            toogle_itens('ch4');
            if( $("#ch4_emission_factor_type").val() == 'Reporter')
                $('[name=ch4_emission_factor]').blur( function(){ reloadEmissionFactorValues_Reporter('ch4') });
            else
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '16'}, reloadEmissionFactorValues );
        });
        $("#n2o_emission_factor_type").change( function()
        {
            toogle_itens('n2o');
            if( $("#n2o_emission_factor_type").val() == 'Reporter')
                $('[name=n2o_emission_factor]').blur( function(){ reloadEmissionFactorValues_Reporter('n2o') });
            else
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '20'}, reloadEmissionFactorValues );
        });


        $('[name=fuel_quantity]').keyup(function()
        {
            if( $('#co2_emission_factor_type option:selected').val() == 'Program'  )
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '1'}, reloadEmissionFactorValues );
            else
                reloadEmissionFactorValues_Reporter('co2');

            if( $('#ch4_emission_factor_type option:selected').val() == 'Program'  )
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '16'}, reloadEmissionFactorValues );
            else
                reloadEmissionFactorValues_Reporter('ch4');

            if( $('#n2o_emission_factor_type option:selected').val() == 'Program'  )
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '20'}, reloadEmissionFactorValues );
            else
                reloadEmissionFactorValues_Reporter('n2o');
        });
    });




    $("#emission_type").change(function()
    {
        clearErrors();
        clearEmissionFactorValues();

        if( $(this).val() == '-' )
            $('#buttons_wrapper').hide();
        else
        {
            $('#buttons_wrapper').show();

            if( $(this).val() == 'S' )
                $('#sector_wrapper').show();
            else
                $('#sector_wrapper').hide();
        }



        $.post("/factors/recover_factor_types", {'emission_type': $(this).val()}, reloadEmissionTypes );

        $.ajax({
            url: "/factors/recover_sectors",
            dataType: 'json',
            data: {'emission_type': $(this).val()},
            type: 'POST',
            success: reloadSectors
         });

        $.ajax({
            url: "/factors/recover_fuels",
            dataType: 'json',
            data: {'emission_type': $(this).val()},
            type: 'POST',
            success: reloadFuels
         });





        $('#co2_emission_factor_type').change(function()
        {
            if( $('#co2_emission_factor_type option:selected').val() == 'Program'  )
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '1'}, reloadEmissionFactorValues );
        });
        $('#ch4_emission_factor_type').change(function()
        {
            if( $('#ch4_emission_factor_type option:selected').val() == 'Program'  )
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '16'}, reloadEmissionFactorValues );
        });
        $('#n2o_emission_factor_type').change(function()
        {
            if( $('#n2o_emission_factor_type option:selected').val() == 'Program'  )
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '20'}, reloadEmissionFactorValues );
        });


        $("#sector").change(function()
        {
            if( $('#co2_emission_factor_type option:selected').val() == 'Program'  )
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '1'}, reloadEmissionFactorValues );
            else
                reloadEmissionFactorValues_Reporter('co2');

            if( $('#ch4_emission_factor_type option:selected').val() == 'Program'  )
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '16'}, reloadEmissionFactorValues );
            else
                reloadEmissionFactorValues_Reporter('ch4');

            if( $('#n2o_emission_factor_type option:selected').val() == 'Program'  )
                $.post("/factors/recover_factor_value", {'fuel': $('#fuel option:selected').val(), 'sector': $('#sector option:selected').val(), 'gas': '20'}, reloadEmissionFactorValues );
            else
                reloadEmissionFactorValues_Reporter('n2o');
        });




    });


});
