	{% load staticfiles %}

	var paper;
	var colors = {'CCR':'#E71D36','D':'#2EC4B6','E':'#2EC4B6', 'I':'#2EC4B6', 'HL': '#BF55EC', 'SEL': '#FDE3A7'}
	var typesData = {};

	{% for link_type in link_types %}
		typesData['{{link_type.id}}'] = {
							'type' : '{{link_type.type|escapejs}}',
							'logic' : '{{link_type.logic|escapejs}}',
							'inverse' : '{{link_type.inverse|escapejs}}',
							'source': {
							{% if link_type.arrows > 1 %}
								fill: '{{link_type.strokeColor|escapejs}}',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							{% endif %}
							} ,
							'target': {
							{% if link_type.arrows > 0 %}
								fill: '{{link_type.strokeColor|escapejs}}',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							{% endif %}
							},
							'connection': {
								stroke: '{{link_type.strokeColor|escapejs}}',
								'stroke-width': {{link_type.strokeWidth}}
							}
						} ;
	{% endfor %}

	//On va stocker tous les ronds la-dedans, pour gérer leurs positions
	var circles = [];
	var syls = [];

	//Correspondances id
	propIdCorrespondance = {};
	linkIdCorrespondance = {};
	circleIdCorrespondance = {};
	authorList = {};

	//Ini graph
    var graph = new joint.dia.Graph;

	var selectedElement = '';

	//Variables pour le paper
	var graphScale = 1;
	var originX = {% if graph %} {{graph.originx}} {% else %}0{% endif %};
	var originY = {% if graph %} {{graph.originy}} {% else %}0{% endif %};
	var sensibility = 20;

	var dragger;
	var selectedCells = [];

	//Créer une proposition
	function addProp(id_prop, text, autorname) {

		heightPrediction = 30 + text.length;
		if (heightPrediction < 100) {
			heightPrediction = 100;
		}

		var wraptext = joint.util.breakText(text, {
			width: 145,
			height: heightPrediction,
			attrs: {
				'text-anchor': 'middle'
			}
		});

		joint.shapes.basic.twoTextRect = joint.shapes.basic.Generic.extend({

			markup: '<g class="rotatable">'
						+'<g class="scalable">'
							+'<rect/>'
						+'</g>'
						+'<text class = "word1"></text>'
						+'<text class = "word2"></text>'
						+'<image/>'
					+'</g>',

			defaults: joint.util.deepSupplement({

				type: 'basic.twoTextRect',
				attrs: {
					rect: {
						fill: 'rgb(55,55,55)',
						stroke: 'white',
						'stroke-width': 0,
						'follow-scale': true,
						width: 200,
						height: heightPrediction
					},

					'.word2': {
						'font-size': 15,
						'font-weight': 'bold',
						fill: 'white',
						'text-anchor':'end',
						transform: "translate(165,"+(heightPrediction-18)+")"
					},
					'.word1': {
						'ref': 'rect',
						'font-size': 15,
						'text-anchor':'middle',
						transform: "translate(95,20)" ,
						fill: 'white',
						'dy': 100
					},
					'image': {
						'ref-x': 2,
						'ref-y': 2,
						 ref: 'rect',
						 width: 50,
						 height: 30
					}
				},
				size: { width: 200, height: heightPrediction },
				id_prop : id_prop,
				text : text,
				autorname: autorname,
			}, joint.shapes.basic.Generic.prototype.defaults)
		});

		var el = new joint.shapes.basic.twoTextRect({
			attrs: {
	//			image: { 'xlink:href': "{% static 'gdpcore/speechicon.png' %}" }
			}
		});
		el.attr('.word1/text', wraptext);
		el.attr('.word2/text', autorname);
		el.attr('./display', '');

		graph.addCell(el);

		console.log('prop added to graph - id_prop: '+id_prop+' id: '+el.id)

		return(el)
	}

	//ajouter une vidéo youtube
	function addYoutube(id_prop, text, ytid, ytbeginning, ytend) {

		var wraptext = joint.util.breakText(text, {
			width: 145,
			height: 90,
			attrs: {
				'text-anchor': 'middle'
			}
		});

		joint.shapes.basic.youtubeVideo = joint.shapes.basic.Generic.extend({

			markup: '<g class="rotatable">'
						+'<g class="scalable">'+
							'<rect/>'
						+'</g>'
						+'<image/>'
						+'<text/>'
					+'</g>',

			defaults: joint.util.deepSupplement({

				type: 'basic.youtubeVideo',
				size: { width: 200, height: 100 },
				attrs: {
					'rect': { fill: '#EEEEEE', stroke: '', width: 200, height: 100 },
					'text': { 'font-size': 14, text: '', 'ref-x': .5, 'ref-y': .5, ref: 'rect', 'y-alignment': 'middle', 'x-alignment': 'middle', fill: 'black' },
					'image': { 'ref-x': 2, 'ref-y': 2, ref: 'rect', width: 50, height: 30 }
				},
				id_prop : id_prop,
				ytid : ytid,
				ytbeginning : ytbeginning,
				ytend : ytend,
				text: text

			}, joint.shapes.basic.Generic.prototype.defaults)
		});


		var el = new joint.shapes.basic.youtubeVideo({
			position: { x: 0, y: 0 },
			size: { width: 200, height: 100 },
			attrs: {
				text: { text: wraptext },
				image: { 'xlink:href': "{% static 'gdpcore/yticon.png' %}" }
			}
		});
		graph.addCell(el);

		el.attr('./display', 'none');
		graph.addCell(el);

		return el;

	}

	//Ajouter un syllogisme
	function addSyllogism(id_prop) {
		joint.shapes.basic.syllogism = joint.shapes.basic.Generic.extend({

			markup: '<g class="rotatable">'
						+'<g class="scalable">'
							+'<rect/>'
						+'</g>'
						+'<text/>'
					+'</g>',

			defaults: joint.util.deepSupplement({

				type: 'basic.syllogism',
				size: { width: 30, height: 30 },
				attrs: {
					'rect': { fill: '#EEEEEE', stroke: 1, width: 30, height: 30 },
					'text': { 'font-size': 14, text: '&', 'ref-x': .5, 'ref-y': .5, ref: 'rect', 'y-alignment': 'middle', 'x-alignment': 'middle', fill: 'black' }
				},
				id_prop : id_prop,
				text: '&'

			}, joint.shapes.basic.Generic.prototype.defaults)
		});
		var el = new joint.shapes.basic.syllogism();
		el.attr('./display', 'none');
		graph.addCell(el);

		syls.push(el);

		return el
	};

	//Creation d'un lien (avec bonne visibilité)
	function addLink(id_link, id_left_prop, id_right_prop, type_id, autorname){

		updateCorrespondances();

		logic =  '<div>'+graph.getCell(propIdCorrespondance[id_left_prop]).get('text')+'</div>'
				+'<div>'+typesData[type_id]['logic']+'</div>'
				+'<div>'+graph.getCell(propIdCorrespondance[id_right_prop]).get('text')+'</div>'

/*		joint.shapes.improvedLink = joint.dia.Link.extend({
			labelMarkup: '<g class="label"><rect /><text /></g>'
		});

		var impLi = new joint.shapes.improvedLink({
			source: { id: propIdCorrespondance[id_left_prop] },
			target: { id: propIdCorrespondance[id_right_prop] },
			attrs: {},
			id_link: id_link,
			type_id : type_id,
			link_autorname: autorname,
			logic: logic,
			labels : [
			{ position: 0.5, attrs: { text: { text: 'impli', 'font-size': 12 } } }
			]
		});
		graph.addCell(impLi) ; */

		var li = new joint.dia.Link({
			source: { id: propIdCorrespondance[id_left_prop] },
			target: { id: propIdCorrespondance[id_right_prop] },
			attrs: {},
			id_link: id_link,
			type_id : type_id,
			link_autorname: autorname,
			logic: logic,
			labels: [{
				position: 0.5,
				attrs: {
					text: {
//						text: typesData[type_id]['type']+' ('+autorname+')',
						text: typesData[type_id]['type'],
						fill: '#f6f6f6',
						'font-family': 'sans-serif'
					},
					rect: {
						stroke: '#7c68fc',
						'stroke-width': 20,
						rx: 5,
						ry: 5
					}
				}
			}]

//			labels : [
//			{ position: 0.5, attrs: { text: { text: typesData[type_id]['type']+' ('+autorname+')', 'font-size': 12 } } }
//			]
		});

		li.attr({
			'.connection': typesData[type_id]['connection'],
			'.marker-source': typesData[type_id]['source'],
			'.marker-target': typesData[type_id]['target']
		});

		li.label(0, { attrs: { rect: { stroke: typesData[type_id]['connection']['stroke'] } } } );

		li.attr('./display', 'none');

		graph.addCell(li) ;
		linkVisu(li);

		console.log('link added to graph - id_link: '+id_link+' id: '+li.id)

		if (typesData[type_id]['type'] != 'syllogisme') {
//			addCircToLink(li);
		}

		return li
	}

	//Pour ajouter un rond à un lien  (pour pouvoir pointer dessus)
	function addCircToLink(link){
		source_position = link.getSourceElement().get('position');
		target_position = link.getTargetElement().get('position');
		var middle_position = {};
		middle_position['x'] = (source_position['x']+target_position['x'])/2+80;
		middle_position['y'] = (source_position['y']+target_position['y'])/2+30;

		var el = new joint.shapes.fsa.State({
				position: { x: middle_position['x'], y: middle_position['y'] },
				size: { width: 40, height: 40 },
				attrs: {
					text : { text: '', fill: '', 'font-weight': 'normal' },
					'circle': {
						fill: '',
						stroke: '#000000',
						'stroke-width': 0.1
					}
				},
				link_id: link.get('id_link')
			});
		el.attr('./display', link.attr('./display'));
		graph.addCell(el);
		el.toBack();
		circles.push(el);
		return el
	};

	//Creation d'une implication (avec bonne visibilité)
	function addImp(id_imp, id_imp_link, id_imp_prop, autorname ) {
		var lo = new joint.dia.Link({
			source: { id: circleIdCorrespondance[id_imp_link] },
			target: { id: propIdCorrespondance[id_imp_prop] },
			attrs: {},
			id_implication: id_imp,
			labels : [
			{ position: 0.5, attrs: { text: { text: 'Implication ('+autorname+')', 'font-size': 12 } } }
			]
		});

		lo.attr({
			'.connection': typesData[1]['connection'],
			'.marker-source': typesData[1]['source'],
			'.marker-target': typesData[1]['target']
		});
		lo.attr('./display', 'none');
		graph.addCell(lo) ;
		linkVisu(lo);

		console.log('imp added to graph - id_imp: '+id_imp+' id: '+lo.id);

		return lo
	}

	//MAJ des correspondances
	function updateCorrespondances(){

		all_elems = graph.getElements();
		propIdCorrespondance = {};
		circleIdCorrespondance = {};
		all_elems.forEach(function(entry) {
			propIdCorrespondance[entry.get('id_prop')] = entry.id;
			circleIdCorrespondance[entry.get('link_id')] = entry.id;
		});

		all_links = graph.getLinks();
		linkIdCorrespondance = {};
		all_links.forEach(function(entry) {
			linkIdCorrespondance[entry.get('id_link')] = entry.id;
		});

	}

	//MAJ de la visibilité d'un lien et du cercle
	function linkVisu(link) {
			if( graph.getCell(link.get('source')['id']).attr('./display') == ''
			  && graph.getCell(link.get('target')['id']).attr('./display') == '' ) {
					link.attr('./display', '');
			} else {
					link.attr('./display', 'none');
			}

		updateCorrespondances()

		if (circ = graph.getCell( circleIdCorrespondance[link.get('id_link')] )) {
			circ.attr('./display', link.attr('./display'));
		}


	}

	//MAJ des visiiblités des liens entourant une cell
	function aroundCellVisu(cell) {

		links = graph.getConnectedLinks(cell);
		links.forEach(function(li) {
			linkVisu(li);
		});
	};

	//MAJ de con_display
	function updateConDisplay(cell) {
		$("#cons_display").html('');
		updateCorrespondances();

		links = graph.getConnectedLinks(cell, {inbound: true});
		links.forEach(function(entry){
			voisin = entry.getSourceElement();

			if (entry.attr('./display') == 'none') {
				$("#cons_display").append(
					"<div class='con'> "
						+"<span id='"+voisin.get('id_prop')+"' class='glyphicon glyphicon-plus-sign' aria-hidden='true'></span> "
						+typesData[entry.get('type_id')]['inverse']+' '
						+voisin.get('text')
					+'</div>');
			};
		});

		links = graph.getConnectedLinks(cell, {outbound: true});
		links.forEach(function(entry){
			voisin = entry.getTargetElement();


			if (entry.attr('./display') == 'none') {
				$("#cons_display").append(
					"<div class='con'> "
						+"<span id='"+voisin.get('id_prop')+"' class='glyphicon glyphicon-plus-sign' aria-hidden='true'></span> "
						+typesData[entry.get('type_id')]['type']+' '
						+voisin.get('text')+' ('+entry.get('link_autorname')+')'
					+'</div>');
			};


		});
	};

	//Ajouter des props depuis un Json envoyé par le serveur
	function fromJsonAddProp( entry ) {
		if (entry['model']=='gdpcore.proposition'){
			if (entry['fields']['nature'] == 'Diagnostic') {
				elem = addProp(
							entry['pk'],
							entry['fields']['text'],
							authorList[entry['fields']['autor']]
						);

			} else if (entry['fields']['nature'] == 'YT'){
				elem = addYoutube(
							entry['pk'],
							entry['fields']['text'],
							entry['fields']['ytid'],
							entry['fields']['ytbeginning'],
							entry['fields']['ytend']

						);

			} else if (entry['fields']['nature'] == 'SY'){
				elem = addSyllogism(
							entry['pk']
						);

			} else {
				elem = '';
			}
			return elem;
		} else {
			return null
		}

	};

	//Ajouter des links depuis un Jsons envoyé par le serveur
	function fromJsonAddLink( entry ) {
		if (entry['model']=='gdpcore.link'){
			li = addLink(
					entry['pk'],
					entry['fields']['left_prop'],
					entry['fields']['right_prop'],
					entry['fields']['type'],
					authorList[entry['fields']['autor']]
					);
			return li
		} else {
			return null;
		}
	};

	function addPaper(holder){

		holder = $('#'+holder);
		paper = new joint.dia.Paper({
			el: holder,
			width: 1000,
			height: 500,
			model: graph,
			gridSize: 1,
			interactive: function(cellView) {
				if (cellView.model instanceof joint.dia.Link) {
					// Disable the default vertex add functionality on pointerdown.
					return { vertexAdd: false };
				}
			return true;
			}
		});
		paper.setOrigin(originX, originY);

		return paper;
	};

	//Doesn't work with the player... better use setDrag()
	function setGridZoom(paper, holder, gridOrNot) {
		holder = $('#'+holder);
			//NAV PAPER
		//Initial Parameters
		var gridsize = 1;
		var currentScale = 1;

		//Get the div that will hold the graph
		var targetElement= holder[0];

		//Bonus function use (see below) - create dotted grid
		setGrid(paper, gridsize*15, '#808080');

		//Setup  svgpan and zoom, with handlers that set the grid sizing on zoom and pan
		//Handlers not needed if you don't want the dotted grid
		panAndZoom = svgPanZoom(targetElement.childNodes[0],
		{
			viewportSelector: targetElement.childNodes[0].childNodes[0],
			fit: false,
			zoomScaleSensitivity: 0.4,
			panEnabled: false,
			onZoom: function(scale){
				currentScale = scale;
				setGrid(paper, gridsize*15*currentScale, '#808080');
			},
			beforePan: function(oldpan, newpan){
				setGrid(paper, gridsize*15*currentScale, '#808080', newpan);
			}
		});

		//Enable pan when a blank area is click (held) on
		paper.on('blank:pointerdown', function (evt, x, y) {
			panAndZoom.enablePan();
			//console.log(x + ' ' + y);
		});

		//Disable pan when the mouse button is released
		paper.on('cell:pointerup blank:pointerup', function(cellView, event) {
		  panAndZoom.disablePan();
		});

		//BONUS function - will add a css background of a dotted grid that will scale reasonably
		//well with zooming and panning.
		function setGrid(paper, size, color, offset) {
			if(gridOrNot != 0) {
				// Set grid size on the JointJS paper object (joint.dia.Paper instance)
				paper.options.gridsize = gridsize;
				// Draw a grid into the HTML 5 canvas and convert it to a data URI image
				var canvas = $('<canvas/>', { width: size, height: size });
				canvas[0].width = size;
				canvas[0].height = size;
				var context = canvas[0].getContext('2d');
				context.beginPath();
				context.rect(1, 1, 1, 1);
				context.fillStyle = color || '#AAAAAA';
				context.fill();
				// Finally, set the grid background image of the paper container element.
				var gridBackgroundImage = canvas[0].toDataURL('image/png');
				$(paper.el.childNodes[0]).css('background-image', 'url("' + gridBackgroundImage + '")');
				if(typeof(offset) != 'undefined'){
					$(paper.el.childNodes[0]).css('background-position', offset.x + 'px ' + offset.y + 'px');
				}
			}
		}
	}

	function setDrag(){

		paper.on('blank:pointerdown',
		function(event, x, y) {
				dragStartPosition = { x: x, y: y};
			}
		);

		paper.on('cell:pointerup blank:pointerup', function(cellView, x, y) {
			delete dragStartPosition;
		});

		dragger = $("#myholder")
			.mousemove(function(event) {
				if (typeof dragStartPosition !== 'undefined')
					paper.setOrigin(
						event.offsetX - dragStartPosition.x,
						event.offsetY - dragStartPosition.y);
			});

	}
	//DOESN'T WORK : SOLUTION TO BE FOUND...
	function unsetDrag(){
		paper.off('blank:pointerdown');
	}
	//Firstload : if fed directly with props and links
	function firstLoad(holder) {

		holder = $('#'+holder);
//		$("#actionProp").hide();
//		$("#actionLink").hide();

		//Chargement des props (toutes invisibles)
		{% for prop in props%}
			{% if prop.nature == 'Diagnostic' %}
				addProp(
					{{prop.id}},
					'{{prop.text|escapejs}}',
					'{{prop.autor.username|escapejs}}'
				);
			{% endif %}

			{% if prop.nature == 'YT' %}
				addYoutube(
					{{prop.id}},
					'{{prop.text|escapejs}}',
					'{{prop.ytid}}',
					'{{prop.videoBeginning}}',
					'{{prop.videoEnd}}'
				);
			{% endif %}

			{% if prop.nature == 'SY' %}
				addSyllogism(
					{{prop.id}}
				);
			{% endif %}
		{% endfor %}

		updateCorrespondances()

		//Chargement des attributs
		{% for key, value in attributes.items %}

			cell = graph.getCell(propIdCorrespondance[{{key}}]);
			cell.translate({{value.x}},{{value.y}});
			cell.attr('./display', '');


		{% endfor %}

		//Chargement des liens classiques
		{% for link in links%}

			li = addLink(
				{{link.id}},
				{{link.left_prop.id}},
				{{link.right_prop.id}},
				{{link.type}},
				'{{link.autor.username|escapejs}}'
				);


		{% endfor %}

		updateCorrespondances()

		//Chargement des implications
		{% for implication in implications%}
			imp = addImp(
				'imp{{implication.id}}',
				{{implication.link.id}},
				{{implication.proposition.id}},
				'{{implication.autor.username|escapejs}}'
				);
		{% endfor %}

		updateCorrespondances();
	};

	//Firstload, if fed with showparts..
	function firstLoadFromShowparts() {
		//Chargement des props (toutes invisibles)
		{% for showpart in showparts%}
			{% if showpart.proposition %}
				{% if showpart.proposition.nature == 'Diagnostic' %}
					el = addProp(
						{{showpart.proposition.id}},
						'{{showpart.proposition.text|escapejs}}',
						'{{showpart.proposition.autor.username|escapejs}}'
					);
					el.attr('./display', '');
					el.translate( {{showpart.x}} , {{showpart.y}} );

					el.on('change:position', function(event) {

						$("#partsMenu tr[prop="+event.get('id_prop')+"] .propX").html( event.get('position')['x'] )
						$("#partsMenu tr[prop="+event.get('id_prop')+"] .propY").html( event.get('position')['y'] )

					})

				{% endif %}

				{% if showpart.proposition.nature == 'YT' %}
					el = addYoutube(
						{{showpart.proposition.id}},
						'{{showpart.proposition.text|escapejs}}',
						'{{showpart.proposition.ytid}}',
						'{{showpart.proposition.videoBeginning}}',
						'{{showpart.proposition.videoEnd}}'
					);
					el.attr('./display', '');
					el.translate( {{showpart.x}} , {{showpart.y}} );

					el.on('change:position', function(event) {

						$("#partsMenu tr[prop="+event.get('id_prop')+"] .propX").html( event.get('position')['x'] )
						$("#partsMenu tr[prop="+event.get('id_prop')+"] .propY").html( event.get('position')['y'] )

					})


				{% endif %}

				{% if showpart.proposition.nature == 'SY' %}
					addSyllogism(
						{{showpart.proposition.id}}
					);
				{% endif %}
			{% endif %}
		{% endfor %}

		updateCorrespondances()

		//Chargement des liens classiques
		{% for showpart in showparts%}
			{% if showpart.link %}
				li = addLink(
					{{showpart.link.id}},
					{{showpart.link.left_prop.id}},
					{{showpart.link.right_prop.id}},
					{{showpart.link.type}},
					'{{showpart.link.autor.username|escapejs}}'
					);
			{% endif %}
		{% endfor %}

		{% for link in links %}
			li = addLink(
				{{link.id}},
				{{link.left_prop.id}},
				{{link.right_prop.id}},
				{{link.type}},
				'{{link.autor.username|escapejs}}'
			);
			li.attr('./display','');

		{% endfor %}

		updateCorrespondances()

		//Chargement des implications
		{% for implication in implications%}
			imp = addImp(
				'imp{{implication.id}}',
				{{implication.link.id}},
				{{implication.proposition.id}},
				'{{implication.autor.username|escapejs}}'
				);
		{% endfor %}
		updateCorrespondances();
	};

	var counter;
	var audioplayer = document.querySelector('#audioplayer');

	if(audioplayer){
		audioplayer.volume=0.15;
	}

	$("#stop").hide();
	$("#ytshow").hide();
	var currentX=0;
	var currentY=0;
	var selectedElement='';
	var selectedCounter=1;
	var selectedAudioTime = 0;
	var counter = 1;

	var timeOut;
	var moveTimeOut;
	var videoTimeOut;

	var allCells = graph.getCells();

	function readshow() {

		console.log('currentTime : '+audioplayer.currentTime);

		//audioplayer.play();
		currentX=0;
		currentY=0;

		updateCorrespondances();

		allCells = graph.getCells();
		allCells.forEach(function(entry) {
			entry.attr('./display','none');
		});

		var i = 0;

		$("#partsMenu tr").each(function() {
			if (i<counter && i != 0){
				propId = $(this).find(".propId").text();
				cell = graph.getCell( propIdCorrespondance[ propId ])
				cell.attr('./display','');
				aroundCellVisu(cell);
			}
			i = i+1;

		});

		readpart();
	}

	function stopshow() {

		console.log('fin du show');
		audioplayer.pause();
		paper.setOrigin(0,0);
		counter = 1;

		clearTimeout(timeOut);
		clearTimeout(moveTimeOut);
		clearTimeout(videoTimeOut);

	//	$("#ytshow").hide();
		if (typeof player !== 'undefined'){
			player.stopVideo();
		}



	}

	function readpart(){

		//Si on n'est pas au bout, on va lire...
		if ( $("#partsMenu #showpart"+(counter)+" .order").html() ) {

			console.log('readpart starting... counter = '+counter)

			//Afficher la proposition
			if ( $("#partsMenu #showpart"+(counter)+" .propId").html() ) {
				elem = graph.getCell( propIdCorrespondance[ $("#partsMenu #showpart"+(counter)+" .propId").html() ] );
				elem.attr('./display','');
				aroundCellVisu(elem);
			}

			//Lancer l'audio
			audioplayer.setAttribute('src', "{{MEDIA_URL}}/media/"+$("#partsMenu #showpart"+(counter)+" .audioex").text());
			audioplayer.play();

			
			
			audioplayer.addEventListener("loadedmetadata", function(_event) {
				//var duration = audioElement.duration;
				$("#durationIndic").html(audioplayer.duration);
				
			});
			
			
			//console.log($("#partsMenu #showpart"+(counter)+" .audioex").text());

			//Afficher le texte
			$("#textDisplay").text( $("#partsMenu #showpart"+(counter)+" .text input").val() )

			//Changer le focus
			midX = $(window).width() / 2 - 100;
			midY = $(window).height() / 2 - 50;

			currentX = currentX;
			nextX = -$("#partsMenu #showpart"+(counter)+" .propX").html() + midX - 100;
			stepX = (nextX - currentX) / 100;

			currentY = currentY;
			nextY = -$("#partsMenu #showpart"+(counter)+" .propY").html() + midY - 50;
			stepY = (nextY - currentY) / 100;

			var i = 1;                     //  set your counter to 1


			function myLoop () {           //  create a loop function
			   moveTimeOut = setTimeout(function () {    //  call a 3s setTimeout when the loop is called
				  currentX = currentX + stepX;
				  currentY = currentY + stepY;
				  paper.setOrigin( currentX, currentY);
				  i++;                     //  increment the counter
				  if (i < 101) {            //  if the counter < 10, call the loop function
					 myLoop();             //  ..  again which will trigger another
				  }                        //  ..  setTimeout()
			   }, 10)
			}

			myLoop();

			function startVideo(elem) {
				$("#ytshow").show();
				player.loadVideoById({
					'videoId': elem.get('ytid'),
					'startSeconds': elem.get('ytbeginning'),
					'endSeconds': elem.get('ytend'),
					'suggestedQuality': 'large'
				});
			}

			elem = graph.getCell( propIdCorrespondance[ $("#partsMenu #showpart"+(counter)+" .propId").html() ]);

			if (elem.get('type') == 'basic.youtubeVideo') {

/*				videoTimeOut = setTimeout(function () {
					startVideo( elem )
				}, 1100);
*/			}

//				$("#showpart"+counter).css('background-color','grey');
//				$("#showpart"+(counter-1)).css('background-color','black');


			//Attendre, et lancer le prochain readpart
			timeOut = setTimeout(readpart, $("#partsMenu #showpart"+(counter)+" .duration input").val() * 1000);
			counter = counter +1

		}
		else {
			stopshow();
			initCta()
		}
	}

	var selectTime = 1200;
	var selectTimeNext = 2000;

	function selectHandlerAnim(type, elemId){

		$('.'+type+'Img').removeClass('animated bounceInLeft');
		$('.'+type+'Text').removeClass('animated bounceInRight');

		$('.'+type+'Img').not("#"+type+elemId).addClass('animated bounceOutLeft');
		$('.'+type+'Text').not("#"+type+elemId+"Text").addClass('animated bounceOutRight');

		setTimeout("$('#"+type+elemId+"').addClass('animated bounceOutLeft');",selectTime);
		setTimeout("$('#"+type+elemId+"Text').addClass('animated bounceOutRight');",selectTime);

	}

	function initAnim(isItFirst){
		counter = 1;
		console.log('initAnim');
		unsetDrag();
		allCells = graph.getCells();
		allCells.forEach(function(entry) {
			paper.findViewByModel(entry).unhighlight();
			entry.attr('./display','none');
		});

		$(".anim").show();
		$('.cta, .cta2').hide();
		$("#blackUnivok").show();
		$("#stopAnim").hide();

		$('#myholder').removeClass('animated bounceInLeft');
		$('#callToAction').removeClass('animated bounceOutRight');

		$('#callToAction').removeClass('fullscreen');
		$('#myholder').addClass('fullscreen');

		console.log(isItFirst);

		if (isItFirst != false){
			console.log('azeazeazeaz')
			$('#myholder').removeClass('animated bounceOutRight');
			$('#myholder').addClass('animated bounceInLeft');
		}

		paper.setDimensions($('#myholder').width(), $('#myholder').height());

		$("#playAnim, #soundPicture, #soundText").removeClass('animated bounceOutRight');
		$("#playAnim, #soundPicture, #soundText").addClass('animated bounceInLeft');

		$( "body" ).one("click", "#playAnim", function(event) {
			$("#playAnim, #soundPicture, #soundText").removeClass('animated bounceInLeft');
			$("#playAnim, #soundPicture, #soundText").addClass('animated bounceOutRight');
			setTimeout(readshow,2000);
		});

		$( "body" ).one("click", "#closeCross", function(event) {
			stopshow();
			initCta();
		});

	}

	function initCta(){
		console.log('initCta');
		$(".anim, .cta2").hide();
		$(".cta").show();
		$("#blackUnivok").show();

		$('#myholder').removeClass('fullscreen');
		$('#callToAction').addClass('fullscreen');

		$('.ctaImg').removeClass('bounceOutLeft');
		$('.ctaText').removeClass('bounceOutRight');

		$('.ctaImg').addClass('animated bounceInLeft');
		$('.ctaText').addClass('animated bounceInRight');


		$( "body" ).one("click", "#ctaOk", function(event) {
			selectHandlerAnim('cta','Ok');
			sayThanks('A bientôt, et merci !','#2ecc71');
			setTimeout(
				"$('#callToAction').removeClass('animated bounceInLeft');"
				+"$('#callToAction').addClass('animated bounceOutRight');"
				,4000);
			setTimeout(initPage,5000)
			setTimeout(
				"$('#callToAction').show();"
				+"$('#starter').removeClass('animated bounceOutLeft');"
				+"$('#starter').addClass('animated bounceInRight');"
				,6000)
		});

		$( "body" ).one("click", "#ctaNok", function(event) {
			selectHandlerAnim('cta','Nok');
			setTimeout(initCtaQuestion, selectTimeNext);
		});

		$( "body" ).one("click", "#ctaAgain", function(event) {
			selectHandlerAnim('cta','Again');
			setTimeout(function() {
				initAnim(false);
			}, selectTimeNext);
		});

		$( "body" ).one("click", "#ctaGraph", function(event) {
			selectHandlerAnim('cta','Graph');
			setTimeout(initGraph, selectTimeNext);
		});

	}

	function initCtaQuestion(){

		console.log('initCtaQuestion');
		$(".anim, cta2").hide();
		$(".ctaQue").show();
		$("#blackUnivok").show();

		$('#myholder').removeClass('fullscreen');
		$('#callToAction').addClass('fullscreen');

		$('.ctaQueImg').removeClass('bounceOutLeft');
		$('.ctaQueText').removeClass('bounceOutRight');

		$('.ctaQueImg').addClass('animated bounceInLeft');
		$('.ctaQueText').addClass('animated bounceInRight');


		$( "body" ).one("click", "#ctaQueAccurate", function(event) {
			selectHandlerAnim('ctaQue','Accurate');
			setTimeout(initGraph, selectTimeNext);
			setTimeout(initAccurate, selectTimeNext);
		});

		$( "body" ).one("click", "#ctaQueGeneral", function(event) {
			selectHandlerAnim('ctaQue','General');
			setTimeout(initGeneralForm, selectTimeNext);
		});

		$( "body" ).one("click", "#ctaQueBack", function(event) {
			selectHandlerAnim('ctaQue','Back');
			setTimeout(initCta, selectTimeNext);
		});

	}

	function initGeneralForm(){

		$('#ctaForm').removeClass('animated bounceOutRight');
		$('#ctaForm').show();
		$('#ctaForm').addClass('animated bounceInLeft');
	}

	function initAccurate(){

		selectedCells = [];
		allCells.forEach(function(entry) {
			paper.findViewByModel(entry).unhighlight();
			entry.attr('./display','');
		});
		$("#ctaQueAccurateSelection,#ctaQueAccurateInput").val('');
		
		setPossibleSelection();
		setTimeout("$('#ctaQueAccurateInstruction').show();$('#ctaQueAccurateInstruction').addClass('animated bounceInUp');",1000);

		$( "body" ).one("click", "#ctaQueAccurateClick", function(event) {

			$(".ctaInput").removeClass('animated bounceInRight');
			$(".ctaInput").addClass('animated bounceOutRight');
			sayThanks('Votre question a été enregistrée, merci', '#2ecc71');
			selectedCells = [];
			initAccurate();
//			unsetPossibleSelection();

		});
	}
	
	function initAccurateForm(selectedCells){

		console.log('initAccurateForm');
		$(".anim, cta2").hide();
		$(".cta").hide();
		$("#callToAction").show();
		$("#blackUnivok").show();

		$('#myholder').removeClass('fullscreen');
		$('#callToAction').addClass('fullscreen');

		console.log(selectedCells);
		selectedCells.forEach(function(entry) {

			cell = graph.getCell(entry)
			stri =
			"<div class = 'accurateText'>"+cell.get('autorname')+' '+cell.get('text')+'</div>'
			+"<textarea class='form-control' rows='3' placeholder='Votre remarque...'></textarea>"

			$("#ctaQueAccurateContainer").append(stri);
		});


	}

	function initPage(){

		$('#myholder').removeClass('animated bounceInLeft');
		$('#callToAction').removeClass('animated bounceOutRight');
		$('.anim, .cta, .cta2, .ctaQue, #blackUnivok').hide();
		$('#myholder').removeClass('fullscreen');
		$('#callToAction').removeClass('fullscreen');

		$( "body" ).one("click", '#starter', function(event) {
			$("#starter").removeClass('animated bounceInRight');
			$("#starter").addClass('animated bounceOutLeft');
			setTimeout(function() {
				//initAnim(true);
				initCta();
			},1500);
		});
	}

	function sayThanks(text, color){
		$('#ctaMerci').text(text);
		$('#ctaMerci').css('color',color);

		$('#ctaMerci').removeClass('animated bounceOutRight');

		setTimeout("$('#ctaMerci').show();$('#ctaMerci').addClass('animated bounceInLeft');", 1000);
		setTimeout("$('#ctaMerci').addClass('animated bounceOutRight');", 4000);
//		setTimeout(initPage, 4000);
	}

	function initGraph(){
		console.log('initGraph');

		setDrag();
		unsetPossibleSelection();
		allCells = graph.getCells();
		allCells.forEach(function(entry) {
			paper.findViewByModel(entry).unhighlight();
			entry.attr('./display','');
		});

		$(".anim").show();
		$('.cta, .cta2').hide();
		$("#blackUnivok").show();
		$("#stopAnim,#playAnim,#soundPicture,#soundText").hide();

		$('#myholder').removeClass('animated bounceInLeft');
		$('#callToAction').removeClass('animated bounceOutRight');

		$('#callToAction').removeClass('fullscreen');
		$('#myholder').addClass('fullscreen');
		paper.setDimensions($('#myholder').width(), $('#myholder').height());

		$(window).resize(function(){
			paper.setDimensions($('#myholder').width(), $('#myholder').height());
		})
		//setGridZoom(paper, 'myholder', 0);
		$( "body" ).one("click", "#closeCross", function(event) {
			initCta();
		});

	}

	function setPossibleSelection(){
		selectedCells=[];
		paper.on('cell:pointerclick', function(cellView,evt, x, y) {
			
			console.log(selectedCells);
			
			if ($.inArray(cellView.model.id,selectedCells) == -1){
				selectedCells.push(cellView.model.id);
				cellView.highlight();			
						
			} else {
				console.log('already in selectedCells');
				selectedCells.splice( $.inArray(cellView.model.id, selectedCells), 1 );
				cellView.unhighlight();
			}

			if (selectedCells.length == 0){
				$(".ctaInput").removeClass('animated bounceInRight');
				$(".ctaInput").addClass('animated bounceOutRight');
			} else {
				$(".ctaInput").show();
				$(".ctaInput").removeClass('animated bounceOutRight');
				$(".ctaInput").addClass('animated bounceInRight');
			}

			$("#ctaQueAccurateSelection").val('');
			selectedCells.forEach(function(entry) {
				newAuthor = graph.getCell(entry).get('autorname');
				newText = graph.getCell(entry).get('text');
				$("#ctaQueAccurateSelection").val( $("#ctaQueAccurateSelection").val()+'\n'+newAuthor+' : '+newText  );
			});
		});
	}

	function unsetPossibleSelection(){
		paper.off('cell:pointerclick')
	}

	function setReadAudio(){


	}

	function quickSaveShow(){
		
		var bigjson = [];

		$("#partsMenu tr").each(function() {
		
			if ($(this).find("td").eq(0).html() != '#') {
					
				item = {
					'order': $(this).find("td").eq(0).html(),
					'propId': $(this).find("td").eq(1).html(),
					'propX': $(this).find("td").eq(4).html(),
					'propY': $(this).find("td").eq(5).html(),
					'text': $(this).find("input").eq(0).val(),
					'duration': $(this).find("input").eq(1).val()
				}
				
				bigjson.push(item);
			}
		});
		
		bigstring = JSON.stringify({ 'things': bigjson });
			
		$.ajax( {
			type: "POST",
			url: '/gdpcore/ajax_showsave/',
			data: { 
					showId: {{show.pk}},
					data: bigstring,
					csrfmiddlewaretoken: '{{ csrf_token }}'
			},
			success: function( data ) {		
				
				console.log(data);
			}
		});
				
	}
	
	$( document ).ready(function() {
		paper = addPaper('myholder');
		firstLoadFromShowparts('myholder');
		initPage();

		$( "body" ).on("click", "#stopAnim", function(event) {
			stopshow();
		});

		$( "body" ).on("click", "#submitQuestion", function(event) {

			$('#ctaForm').removeClass('animated bounceInLeft');
			$('#ctaForm').addClass('animated bounceOutRight');
			sayThanks('Votre demande a été prise en compte. Merci !','#3498db');
			setTimeout(initCta, 5000);

		});

	});
