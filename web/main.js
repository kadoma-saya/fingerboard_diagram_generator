function set_diagram(){
    let thead = document.getElementById("diagram_thead");
    let tbody = document.getElementById("diagram_tbody");
    let strs = parseInt(document.getElementById('strings').value);
    let frs = parseInt(document.getElementById('frets').value);
    let s;
    let f;
    let thead_html;
    let tbody_html;

    thead_html='';
    thead_html += '<tr>';
    thead_html += '<th class="text-center">x</th>';
    thead_html += '<th class="text-center">o</th>';
    for(f = 1; f <= frs; f++){
        thead_html += '<th class="text-center">'+f+'</th>';
    }
    thead_html += '</tr>';
    thead.innerHTML = thead_html;

    tbody_html='';
    for(s = 1; s <= strs; s++){
        tbody_html += '<tr>';
        tbody_html += '<td><input class="dgmopchk form-control" type="checkbox" value="'+s+'s-x"></td>';
        tbody_html += '<td><input class="dgmopchk form-control" type="checkbox" value="'+s+'s-o"></td>';
        for(f = 1; f <= frs; f++){
            tbody_html += '<td><input class="dgmclchk form-control" type="checkbox" value="'+s+'s-'+f+'f"></td>';
        }
        tbody_html += '</tr>';
    }
    tbody_html += '<tr><td></td><td></td>';
    for(f = 1; f <= frs; f++){
        tbody_html += '<td><input class="dgmfninput form-control" type="number" id="'+f+'f" min="1" value="'+f+'"></td>';
    }
    tbody_html += '</tr>';
    tbody.innerHTML = tbody_html;
  
  
}

function get_open_positions(){
    let dgmopchks = document.querySelectorAll(".dgmopchk");
    let selecteddgmopchks = [];
    selecteddgmopchks.splice(0);
    dgmopchks.forEach(chk => {
        if(chk.checked) {
            selecteddgmopchks.push(chk.value)
        }
    });
    return selecteddgmopchks.join(',');
}

function get_close_positions(){
    let dgmclchks = document.querySelectorAll(".dgmclchk");
    let selecteddgmclchks = [];
    selecteddgmclchks.splice(0);
    dgmclchks.forEach(chk => {
        if(chk.checked) {
            selecteddgmclchks.push(chk.value)
        }
    });
    return selecteddgmclchks.join(',');
}

function get_fret_nums(){
    let dgmfninputs = document.querySelectorAll(".dgmfninput");
    let dgmfninputvals = [];
    dgmfninputvals.splice(0);
    dgmfninputs.forEach(input => {
        if(input.value!="") {
            dgmfninputvals.push(input.id + input.value)
        }
    });
    return dgmfninputvals.join(',');
}

async function generate_svg() {
    await eel.generate_svg(
          document.getElementById('filename').value
        , parseInt(document.getElementById('strings').value)
        , parseInt(document.getElementById('frets').value)
        , get_open_positions()
        , get_close_positions()
        , get_fret_nums()
    )();
}
eel.expose(set_image);
function set_image(svgbase64) {
    document.getElementById("img").src = 'data:image/svg+xml;base64,' + svgbase64;
}

set_diagram();
