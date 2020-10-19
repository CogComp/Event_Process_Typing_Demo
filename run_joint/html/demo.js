var demo_examples = {
	"Study": "read papers @ attend conferences @ go to seminars @ write a thesis"
	,
	"Garden": "dig a hole @ put some seeds @ fill the soil @ water the soil"
	,
	"Crime": "make explosive materials @ obtain a container @ obtain shrapnel @ install a trigger"
	,
	"Transport": "print out the forms @ go to the dmv @ pay the fee @ take photos @ take the vision test @ take the permit test @ take the road test"
	,
	"Decoration": "clean windows @ buy plants @ paint walls  @ hang pictures @ carpet floors @ reorganize furniture"
	,
	"Health": "get a referral @ verify the specialist's qualifications @ ask questions @ assess whether treatment is working"
	,
	"Makeup": "position yourself @ trim your eyebrows @ use the eyebrow pencil"
}

function clearResult() {
	// $("#result").html( "" );	
	$("#working").hide();
	$("#result").hide();
}

function showWorking() {
	$("#working").show();
	$("#result").hide();
	$("#intention").html( "?" );
    for (i = 0; i < 5; i++) {
        $("#as"+i).html( "?" );
		$("#at"+i).html( "?" );
		$("#ot"+i).html( "?" );
        $("#os"+i).html( "?" );
	}

}

function showResult() {
	$("#working").hide();
	$("#result").show();
}

function fillExamplesSelectField() {
    selectField = document.getElementById("examples");
	textField = document.getElementById("text");
    for (var key in demo_examples) {
        if (demo_examples.hasOwnProperty(key)) {           
            var opt = document.createElement("option");
            opt.value=key;
            opt.innerHTML = key;
            selectField.appendChild(opt);
        }
    }    
	selectField.value = "Study";
    textField = document.getElementById("text");
	textField.value = demo_examples[selectField.value];
	// fillExampleSelectField(selectField.value)
	// $("#result").html( "" );
	clearResult();
}

async function postData(url = '', data = {}, pfunction) {
	  fetch(url, {
		      method: 'POST',
		      cache: 'no-cache',
		      headers: { 'Content-Type': 'application/json' },
		      body: JSON.stringify(data) 
		    }).then(resp => resp.json())
	    .then(json => {
			        pfunction(json);
			    });
}

function outputResult(json) {
	// alert("outputs results here");
	// alert(json["verb"][0]+" "+json["argument"][0]);
	for (i = 0; i < 5; i++) {
		a = ""+json["verb"][i]; a = a.split(",");
		o = ""+json["argument"][i]; o = o.split(",");
		if (i==0) {
			$("#intention").html( a[0]+" "+o[0] );
		}
		$("#as"+i).html( (1 - a[1]).toString().substring(0,5) );
		$("#at"+i).html( a[0] );
		$("#ot"+i).html( o[0] );
		$("#os"+i).html( (1 - o[1]).toString().substring(0,5) );
	}
	showResult();
}

function runDemo() {
	// alert('Demo runs here...');
	var data = {"sequence": document.getElementById("text").value};
	url="./annotate";
	postData(url, data, outputResult);
}

function newExampleSelect() {
    exampleSelectField = document.getElementById("examples");
    example = exampleSelectField.value;
    textField = document.getElementById("text");
    textField.value = demo_examples[example];
    // $("#result").html( "" );
	clearResult();
}



function formSubmit() {
	// $("#result").html( "" );
    showWorking();
	runDemo();
	return false;
}

