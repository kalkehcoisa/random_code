var total_geral = 0;

function ativaManual(manual)
{
    var gases = Array('co2', 'ch4', 'n2o', 'hfc', 'pfc', 'sf6');
    var i = 0;

    manual = !manual;

    for(i=0;i<6;i++)
    {
        $('#man_'+gases[i]+'_scope1').attr('disabled', manual);
        $('#man_'+gases[i]+'_scope3').attr('disabled', manual);

        $('#man_'+gases[i]+'_scope1').attr('value', '');
        $('#man_'+gases[i]+'_scope2').attr('value', '');
        $('#man_'+gases[i]+'_scope3').attr('value', '');
        $('#man_'+gases[i]+'_biomass').attr('value', '');
    }

    $('#man_co2_scope2').attr('disabled', manual);
    $('#man_ch4_scope2').attr('disabled', manual);
    $('#man_n2o_scope2').attr('disabled', manual);

    $('#man_hfc_scope2').attr('disabled', true);
    $('#man_pfc_scope2').attr('disabled', true);
    $('#man_sf6_scope2').attr('disabled', true);


    $('#man_co2_biomass').attr('disabled', manual);

    $('#man_ch4_biomass').attr('disabled', true);
    $('#man_n2o_biomass').attr('disabled', true);
    $('#man_hfc_biomass').attr('disabled', true);
    $('#man_pfc_biomass').attr('disabled', true);
    $('#man_sf6_biomass').attr('disabled', true);


    $('#man_hfc_scope2').attr('novalidate', true);
    $('#man_pfc_scope2').attr('novalidate', true);
    $('#man_sf6_scope2').attr('novalidate', true);
    $('#man_ch4_biomass').attr('novalidate', true);
    $('#man_n2o_biomass').attr('novalidate', true);
    $('#man_hfc_biomass').attr('novalidate', true);
    $('#man_pfc_biomass').attr('novalidate', true);
    $('#man_sf6_biomass').attr('novalidate', true);


    if( !manual )
        $('#buttons_send_data').show();
    else
        $('#buttons_send_data').hide();


}





function autoUpdateEmissionValues(data)
{
    ativaManual(false);

    //recebe os dados e quebra em tres vetores, cada um
    //referente a um dos escopos
    var emissions = data.split("#");
    var emi = Array();

    emi[0] = emissions[0].split(';');
    emi[1] = emissions[1].split(';');
    emi[2] = emissions[2].split(';');


    //exibe os valores na celulas da tabela para calculo automatico
    var i = 0;
    var j = 0;
    var totais = Array(0, 0, 0);

    for(i=0;i<3;i++)
    {
        $("#co2_scope"+(i+1)).html( emi[i][0]+'' );
        $("#ch4_scope"+(i+1)).html( emi[i][1]+'' );
        $("#n2o_scope"+(i+1)).html( emi[i][2]+'' );
        $("#hfc_scope"+(i+1)).html( emi[i][3]+'' );
        $("#pfc_scope"+(i+1)).html( emi[i][4]+'' );
        $("#sf6_scope"+(i+1)).html( emi[i][5]+'' );

        for(j=0;j<6;j++)
            totais[i] += parseFloat( emi[i][j] );
    }

    //exibe os valores da soma de cada coluna
    $("#tot_scope1").html( totais[0]+'' );
    $("#tot_scope2").html( totais[1]+'' );
    $("#tot_scope3").html( totais[2]+'' );

    $('#tot_escopo1_2').html( totais[0]+totais[1]+'' );
    $('#tot_escopo_geral').html( totais[0]+totais[1]+totais[2]+'' );
    total_geral = totais[0]+totais[1]+totais[2];
}



function autoUpdateEmissionValuesSector(data)
{
    var emissions = data.split(";");

    $('#static_emissions').html( emissions[0]+'' );
    $('#movel_emissions').html( emissions[1]+'' );
    $('#process_emissions').html( emissions[2]+'' );
    $('#fugitive_emissions').html( emissions[3]+'' );
    //$('#rural_emissions').html( emissions[4]+'' );

    var total = 0;
    total += parseFloat( emissions[0] );
    total += parseFloat( emissions[1] );
    total += parseFloat( emissions[2] );
    total += parseFloat( emissions[3] );
    //total += parseFloat( emissions[4] );

    $('#total_emissions').html( total+'' );

    /*
    if( total != total_geral )
    {
        $('#erro_warning').html( 'Erro nos calculos! Os valores totais diferem!' );
        $('#erro_warning').css({'color': 'red', 'font-weight': 'bold'});
        $('#erro_warning').show();

        $('#tot_escopo_geral').css({'color': 'red', 'font-weight': 'bold'});
        $('#total_emissions').css({'color': 'red', 'font-weight': 'bold'});
    }
    */

}




function cleanAuto()
{
    var i = 0;
    var j = 0;
    var totais = Array(0, 0, 0);
    var vazio = '<input type="text" value="" class="summary_item_tab" disabled />';


    for(i=0;i<3;i++)
    {
        $("#co2_scope"+(i+1)).html( vazio );
        $("#ch4_scope"+(i+1)).html( vazio );
        $("#n2o_scope"+(i+1)).html( vazio );
        $("#hfc_scope"+(i+1)).html( vazio );
        $("#pfc_scope"+(i+1)).html( vazio );
        $("#sf6_scope"+(i+1)).html( vazio );
    }

    $("#tot_scope1").html( vazio );
    $("#tot_scope2").html( vazio );
    $("#tot_scope3").html( vazio );

    $('#tot_escopo1_2').html( vazio );
    $('#tot_escopo_geral').html( vazio );


    $('#static_emissions').html( vazio );
    $('#movel_emissions').html( vazio );
    $('#process_emissions').html( vazio );
    $('#fugitive_emissions').html( vazio );
    $('#rural_emissions').html( vazio );
    $('#total_emissions').html( vazio );
}



function autoCalcs(data)
{
    autoUpdateEmissionValues(data);
    $.post("/factors/summary_calc_emissions_sector", { 'emission_report': $('#emission_report_id').val() }, autoUpdateEmissionValuesSector );
}



$('document').ready(function()
{
    ativaManual(false);
    cleanAuto();
    $('#erro_warning').hide();
    $('#buttons_send_data').hide();


    $('#calc_automatico').click(function()
    {
        clearErrors();
        $.post("/factors/summary_calc_emissions", { 'emission_report': $('#emission_report_id').val() }, autoCalcs );
    });

    $('#calc_manual').click(function()
    {
        clearErrors();
        cleanAuto();
        ativaManual(true);
    });


});
