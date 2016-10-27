	{% load staticfiles %}

	var paper;
	var colors = {'CCR':'#E71D36','D':'#2EC4B6','E':'#2EC4B6', 'I':'#2EC4B6', 'HL': '#BF55EC', 'SEL': '#FDE3A7'}
	var typesData = {};

		typesData['1'] = {
							'type' : 'donc',
							'logic' : '... donc ...',
							'inverse' : 'car',
							'source': {
							
							} ,
							'target': {
							
								fill: '#2ecc71',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							
							},
							'connection': {
								stroke: '#2ecc71',
								'stroke-width': 4
							}
						} ;
	
		typesData['2'] = {
							'type' : 'car',
							'logic' : '... car ...',
							'inverse' : 'donc',
							'source': {
							
							} ,
							'target': {
							
								fill: '#2EC4B6',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							
							},
							'connection': {
								stroke: '#2EC4B6',
								'stroke-width': 4
							}
						} ;
	
		typesData['3'] = {
							'type' : 'concurrence',
							'logic' : '... est incompatible avec ...',
							'inverse' : 'concurrence',
							'source': {
							
								fill: '#EF4030',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							
							} ,
							'target': {
							
								fill: '#EF4030',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							
							},
							'connection': {
								stroke: '#EF4030',
								'stroke-width': 4
							}
						} ;
	
		typesData['4'] = {
							'type' : 'exemple',
							'logic' : '... est illustré par ...',
							'inverse' : 'théorie',
							'source': {
							
							} ,
							'target': {
							
								fill: '#2EC4B6',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							
							},
							'connection': {
								stroke: '#2EC4B6',
								'stroke-width': 4
							}
						} ;
	
		typesData['5'] = {
							'type' : 'théorie',
							'logic' : '... illustre que ...',
							'inverse' : 'exemple',
							'source': {
							
							} ,
							'target': {
							
								fill: '#2EC4B6',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							
							},
							'connection': {
								stroke: '#2EC4B6',
								'stroke-width': 4
							}
						} ;
	
		typesData['6'] = {
							'type' : 'contre\u002Dexemple',
							'logic' : '... est invalidé par le fait que ..',
							'inverse' : 'contre\u002Dthéorie',
							'source': {
							
							} ,
							'target': {
							
								fill: '#96281B',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							
							},
							'connection': {
								stroke: '#96281B',
								'stroke-width': 4
							}
						} ;
	
		typesData['7'] = {
							'type' : 'contre\u002Dthéorie',
							'logic' : '... est un élément qui rend impossible que ...',
							'inverse' : 'contre\u002Dexemple',
							'source': {
							
							} ,
							'target': {
							
								fill: '#96281B',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							
							},
							'connection': {
								stroke: '#96281B',
								'stroke-width': 4
							}
						} ;
	
		typesData['8'] = {
							'type' : 'complément',
							'logic' : '... traite du même sujet, et n\u0027est pas incompatible avec ...',
							'inverse' : 'complément',
							'source': {
							
								fill: '#4ECDC4',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							
							} ,
							'target': {
							
								fill: '#4ECDC4',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'
							
							},
							'connection': {
								stroke: '#4ECDC4',
								'stroke-width': 4
							}
						} ;
	
		typesData['9'] = {
							'type' : 'syllogisme',
							'logic' : 'syllogisme',
							'inverse' : 'syllogisme',
							'source': {
							
							} ,
							'target': {
							
							},
							'connection': {
								stroke: '#2EC4B6',
								'stroke-width': 4
							}
						} ;    
  
		typesData['10'] = {
							'type' : 'cependant',
							'logic' : 'cependant',
							'inverse' : 'cependant',
							'source': {
							
							} ,
							'target': {
								fill: 'rgba(243, 156, 18,1.0)',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'							
							},
							'connection': {
								stroke: 'rgba(243, 156, 18,1.0)',
								'stroke-width': 4
							}
						} ;  
                        
		typesData['11'] = {
							'type' : 'précision',
							'logic' : 'précision',
							'inverse' : 'précision',
							'source': {
							
							} ,
							'target': {
								fill: 'rgba(155, 89, 182,1.0)',
								stroke: 'none',
								d: 'M 10 0 L 0 5 L 10 10 z'							
							},
							'connection': {
								stroke: 'rgba(155, 89, 182,1.0)',
								'stroke-width': 4
							}
						} ;                          
                        
                        
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
	function addProp(id_prop, text, autorname, sentences, audio, authorPicture) {

		if (typeof sentences === 'undefined') { optionalArg = 'default'; }
		if (typeof audio === 'undefined') { optionalArg = 'default'; }
		if (typeof authorPicture === 'undefined') { optionalArg = 'default'; }

	
        if (typeof sentences !== 'undefined'){
            if (sentences.length==0){
                sentences = "Pas de citation.."
            }
        }
        
		heightPrediction = 30 + text.length;
		if (heightPrediction < 100) {
			heightPrediction = 100;
		}

		var wraptext = joint.util.breakText(text, {
			width: 145,
			height: 3000,
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
				sentences: sentences,
				audio: audio,
				authorPicture: authorPicture,
                showpartId: 'default',
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

    //Creation de liens pour sentenceBuilder
	function addLinkBuilder(id_link, id_left_prop, id_right_prop, type_id, autorname){

		updateCorrespondances();

		var li = new joint.dia.Link({
			source: { id: propIdCorrespondance[id_left_prop] },
			target: { id: propIdCorrespondance[id_right_prop] },
			attrs: {},
			id_link: id_link,
			type_id : type_id,
			link_autorname: autorname,
			labels: [{
				position: 0.5,
				attrs: {
					text: {
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

		});

		li.attr({
			'.connection': typesData[type_id]['connection'],
			'.marker-source': typesData[type_id]['source'],
			'.marker-target': typesData[type_id]['target']
		});

		li.label(0, { attrs: { rect: { stroke: typesData[type_id]['connection']['stroke'] } } } );

		li.attr('./display', '');

		graph.addCell(li) ;

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

	function addPaperBuilder(holder){

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
					return { vertexAdd: true };
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
						'{{showpart.proposition.autor.username|escapejs}}',
						"{% for sentence in showpart.proposition.sentences %}{{sentence.speaker.name}} : {{sentence|escapejs}}<br /><br />{% endfor %}",
						"{{showpart.audio}}",
						"{{showpart.proposition.autor.userprofile.picture}}"
						
					);
					el.attr('./display', '');
					el.translate( {{showpart.x}} , {{showpart.y}} );
                    
                    el.set('showpartId', {% if showpart.pk %}{{showpart.pk}}{% else %}''{% endif %});

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
        sizeAllRect();
	};

	var counter = 1;
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

	var timeOut;
	var moveTimeOut;
	var videoTimeOut;
    var clockInterval;
    
    var clockGoing = 0;
    var messageShowTimeout;
    var messageHideTimeout;
    
	var allCells = graph.getCells();

    function updateClock() {
                
        minutes = Math.floor(clockGoing/60)
        seconds = clockGoing - minutes*60
        seconds = ('0' + seconds).slice(-2)
        
        $("#clockGoing").text(minutes+":"+seconds);   

        clockGoing = clockGoing + 1;            
    }
    
	function readshow() {

        $('#playAnim').hide();
        $('#prevAnim').show();
    
        //Display pause
        $("#stopAnim").show();
        $("#stopAnim").off();
        $("#stopAnim").on('click', function(){
            
            pauseshow();
            
        });
    
		//start the clock
        clockGoing = 0;
        clockInterval = setInterval(updateClock, 1000);
        
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
        clearInterval(clockInterval);
        
		if (typeof player !== 'undefined'){
			player.stopVideo();
		}



	}

    function pauseshow(){
        console.log('pause du show');
		audioplayer.pause();
        
        counter = counter - 1;

		clearTimeout(timeOut);
		clearTimeout(moveTimeOut);
		clearTimeout(videoTimeOut);
        clearInterval(clockInterval);
        
		if (typeof player !== 'undefined'){
			player.stopVideo();
		} 

        $('#stopAnim').hide();
        $('#playAnim').show();
        $('#playAnim').off();
        $('#playAnim').on("click", function() {
            
            readshow();
            
        });
    }
  
    function previouspart(){        
        pauseshow();
        counter = counter - 1;
        if (counter<1) {
            counter = 1;           
        }
        readshow();               
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
			

			//Afficher le texte
			$("#textDisplay").text( $("#partsMenu #showpart"+(counter)+" .text input").val() )

			//Changer le focus
			//midX = $(window).width() / 2 - 100;
			//midY = $(window).height() / 2 - 50;

            midX = $("#myholder").width() / 2 - 100;
            midY = $("#myholder").height() / 2 - 100;
            
			currentX = currentX;
			nextX = -$("#partsMenu #showpart"+(counter)+" .propX").html() + midX;
			stepX = (nextX - currentX) / 100;

			currentY = currentY;
			nextY = -$("#partsMenu #showpart"+(counter)+" .propY").html() + midY;
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
			//initCta()
            initCtaNew()
		}
	}

    function clockHandler(){
        
        var start = new Date;
        
        start = 0;
        
        setInterval(function() {
            $('#timer').text(Math.round((new Date - start) / 1000, 0) + " Seconds"); 
        }, 1000);
        
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
        
        var id = window.setTimeout(function() {}, 0);

        while (id--) {
            window.clearTimeout(id); // will do nothing if no timeout with id is present
        }
               
		counter = 1;
        clockGoing = 0;
        updateClock();
        
		console.log('initAnim');
		unsetDrag();
        
		allCells = graph.getCells();
		allCells.forEach(function(entry) {
			paper.findViewByModel(entry).unhighlight();
			entry.attr('./display','none');
            questionsUnhightlighter(entry);
            detailsUnhighlighter(entry);
            paper.findViewByModel(entry).options.interactive = false;
		});

		$(".anim").show();
		$('.cta, .cta2').hide();
		$("#blackUnivok").show();
		$("#stopAnim, #prevAnim").hide();

        $("#closeCross").removeClass('openPan');
        
		$('#myholder').removeClass('animated bounceInLeft');
		$('#callToAction').removeClass('animated bounceOutRight');

		$('#callToAction').removeClass('fullscreen');
		$('#myholder').addClass('fullscreen');


		if (isItFirst != false){
			$('#myholder').removeClass('animated bounceOutRight');
			$('#myholder').addClass('animated bounceInLeft');
		}

		paper.setDimensions($('#myholder').width(), $('#myholder').height());
		$(window).resize(function(){
			paper.setDimensions($('#myholder').width(), $('#myholder').height());
		})
        
		$("#soundPicture, #soundText").removeClass('animated bounceOutRight');
		$("#soundPicture, #soundText").addClass('animated bounceInLeft');

        var fkq = function(){
			$("#soundPicture, #soundText").removeClass('animated bounceInLeft');
			$("#soundPicture, #soundText").addClass('animated bounceOutRight');
			to_aa = setTimeout(readshow,2000);                     
        };
        
        
        $( "#playAnim" ).off();
        $( "#playAnim" ).one("click", fkq);

        var fpw = function(){
			stopshow();
			//initCta();   
            initCtaNew()            
        }
        
        $( "#prevAnim" ).off();
        $( "#prevAnim" ).on('click', function(){
            
            previouspart();
            
        });
        

        $( "#closeCross" ).off();
        $( "#closeCross" ).on("click", fpw);        
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


        var fui = function(){
			selectHandlerAnim('cta','Ok');
			sayThanks('A bientôt, et merci !','#2ecc71',40);
			to_bb = setTimeout(
				"$('#callToAction').removeClass('animated bounceInLeft');"
				+"$('#callToAction').addClass('animated bounceOutRight');"
				,4000);
			to_cc = setTimeout(initPage,5000)
			to_dd = setTimeout(
				"$('#callToAction').show();"
				+"$('#starter').removeClass('animated bounceOutLeft');"
				+"$('#starter').addClass('animated bounceInRight');"
				,6000)
            setTimeout(function(){
                $("#starter").removeClass('animated bounceInRight');
            }, 7000)
        };
        

       
        $( "#ctaOk" ).off();
        $( "#ctaOk" ).on("click", fui);        
        

        var fxo = function(){
 			selectHandlerAnim('cta','Nok');
            to_ee = setTimeout(function(){
                initGraph();
                setQuestions();
                $("#ctaQueAccurateBackground,#closeCross").addClass('openPan');
            },selectTimeNext);                      
        };
        
        
        $( "#ctaNok" ).off();
        $( "#ctaNok" ).on("click", fxo); 
        
        var frj= function(){
			selectHandlerAnim('cta','Again');
			to_ff = setTimeout(function() {
				initAnim(false);
			}, selectTimeNext);       
                                  
        }
        
        
        $( "#ctaAgain" ).off();
        $( "#ctaAgain" ).on("click", frj);     

        var fhj = function(){
			selectHandlerAnim('cta','Graph');
			to_gg = setTimeout(function() {
                initGraph();                
                $("#detailsBackground").addClass('openPan');
            },selectTimeNext);                      
        };
        
        
        $( "#ctaGraph" ).off();
        $( "#ctaGraph" ).on("click", fhj);
        
	}

	function initCtaNew(){
		console.log('initCtaNew');
		$(".anim, .cta2").hide();
		$(".cta").show();
		$("#blackUnivok").show();

		$('#myholder').removeClass('fullscreen');
		$('#callToAction').addClass('fullscreen');

		$('.ctaImg').removeClass('bounceOutLeft');
		$('.ctaText').removeClass('bounceOutRight');

		$('.ctaImg').addClass('animated bounceInLeft');
		$('.ctaText').addClass('animated bounceInRight');


      
        

        var fxo = function(){
 			selectHandlerAnim('cta','Nok');
            to_ee = setTimeout(function(){
                window.location.href = "/reviewSimple/{{event.show2.pk}}";                
            },selectTimeNext);                      
        };
        
        
        $( "#ctaNok" ).off();
        $( "#ctaNok" ).on("click", fxo); 
        
        var frj= function(){
			selectHandlerAnim('cta','Again');
			to_ff = setTimeout(function() {
				initAnim(false);
			}, selectTimeNext);       
                                  
        }      
        
        $( "#ctaAgain" ).off();
        $( "#ctaAgain" ).on("click", frj);     

        
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

        var fgo = function(){
			selectHandlerAnim('ctaQue','Accurate');
			to_az = setTimeout(initGraph, selectTimeNext);
			to_xy = setTimeout(setQuestions, selectTimeNext+100);            
        };
        
        $( "#ctaQueAccurate" ).off();
        $( "#ctaQueAccurate" ).on("click", fgo);        
        
        var ffo = function(){
 			selectHandlerAnim('ctaQue','General');
			to_eoi = setTimeout(initGeneralForm, selectTimeNext);                     
        };
        

        $( "#ctaQueGeneral" ).off();
        $( "#ctaQueGeneral" ).on("click", ffo);        
        var faw = function(){
			selectHandlerAnim('ctaQue','Back');
			to_aza = setTimeout(initCta, selectTimeNext);        
        };
        

        $( "#ctaQueBack" ).off();
        $( "#ctaQueBack" ).on("click", faw);
	}

/*	function initGeneralForm(){

		$('#ctaForm').removeClass('animated bounceOutRight');
		$('#ctaForm').show();
		$('#ctaForm').addClass('animated bounceInLeft');
        
		$( "body" ).one("click", "#submitQuestion", function(event) {

			$('#ctaForm').removeClass('animated bounceInLeft');
			$('#ctaForm').addClass('animated bounceOutRight');
			sayThanks('Votre demande a été prise en compte. Merci !','#3498db',40);
			to_zpe = setTimeout(initCta, 5000);

		});        
	} */
	
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
       
        //$("#starter").addClass('hvr-skew-forward');
        
       
       var fop = function(){
            
            $("#starter").removeClass('hvr-skew-forward');
			$("#starter").removeClass('animated bounceInRight');
			$("#starter").addClass('animated bounceOutLeft');
			to_oza = setTimeout(function() {
				initAnim(true);
				//initCta();
                //initGraph();
			},1500);                     
        };
        
        $( "#starter" ).off();
        $( "#starter" ).on("click", fop);        
	}

	function sayThanks(text, color, fontSize){
		$('#ctaMerci').text(text);
		$('#ctaMerci').css('color',color);
        $('#ctaMerci').css('font-size', fontSize);
        
		$('#ctaMerci').removeClass('animated bounceOutRight bounceInLeft');

		to_zaiei = setTimeout("$('#ctaMerci').show();$('#ctaMerci').addClass('animated bounceInLeft');", 1000);
		to_zaje = setTimeout("$('#ctaMerci').addClass('animated bounceOutRight');", 4000);
//		setTimeout(initPage, 4000);
	}

	function initGraph(){
		console.log('initGraph');

        

		$(".anim, .graphElems").show();
		$('.cta, .cta2').hide();
		$("#blackUnivok").show();
        
        $("#ctaQueAccurateBackground, #openQuestions,.ctaInput,.graphElems").show();
		
        $("#stopAnim,#playAnim,#soundPicture,#soundText,#animClock").hide();

		$('#myholder').removeClass('animated bounceInLeft');
		$('#callToAction').removeClass('animated bounceOutRight');

		$('#callToAction').removeClass('fullscreen');
		$('#myholder').addClass('fullscreen');
		paper.setDimensions($('#myholder').width(), $('#myholder').height());
        paper.setOrigin( -1*{{showparts.0.x}} + $('#myholder').width()/2 - 100 , -1*{{showparts.0.y}} + $('#myholder').height()/2 -50);
        
        $("#ctaQueAccurateBackground, #detailsBackground").show();
        $("#ctaQueAccurateBackground").removeClass('closePan');   
        $("#detailsBackground").removeClass('closePan');        
        
		$(window).resize(function(){
			paper.setDimensions($('#myholder').width(), $('#myholder').height());
		})
		
        
        setDrag();
		unsetAll();
		allCells = graph.getCells();
		allCells.forEach(function(entry) {
            questionsUnhightlighter(entry);
            detailsUnhighlighter(entry);
			entry.attr('./display','');
            if(entry.get('type') == 'basic.twoTextRect') {
                paper.findViewByModel(entry).options.interactive = true;
            }
		});
        
        unsetDetails();
        unsetQuestions();  
        setDetails();

        $( "#closeCross" ).off();
        $( "#closeCross" ).on("click", initCta);          

	
    
        $(':checkbox').change(function() {
             
            unsetAll();
            if( $('#questionsCb > label > input').is(':checked') ) {            
               console.log('jçreaz');
               setQuestions();
            } else {
                unsetQuestions();
            }
           
            if( $('#detailsCb > label > input').is(':checked') ) {
                console.log('azeazezae');
                setDetails();
            } else {
                unsetDetails();
            }
        }); 
        
        var fob = function(){
            $("#ctaQueAccurateBackground, #closeCross").toggleClass('openPan');  
            if ($( "#ctaQueAccurateBackground" ).hasClass( "openPan" )){
                setQuestions();
            } else {
                unsetQuestions();
            }             
        };
        
 /*     $( "body" ).off("click", "#openQuestions", fob);
        $( "body" ).on("click", "#openQuestions", fob);*/
         $( "#openQuestions" ).off();
         $( "#openQuestions" ).on("click", fob);

        var fow = function(){
            $("#detailsBackground").toggleClass('openPan');          
        };
        
         $( "#openDetails" ).off();
         $( "#openDetails" ).on("click", fow);       
   
	}

    function initGraphList(){
        console.log('initGraphList');
        
        $('#myholder').show();
        $('myholder').removeClass();
        $('myholder').addClass('shrinked');
        $('#listMainContainer').show();
        $("#questionContainer").addClass('down');   
        
		allCells.forEach(function(entry) {
            questionsUnhightlighter(entry);
            detailsUnhighlighter(entry);
			entry.attr('./display','');
            if(entry.get('type') == 'basic.twoTextRect') {
                paper.findViewByModel(entry).options.interactive = true;
            }
		});

        var fob = function(){
            $("#questionContainer").toggleClass('down');  
            if ($( "#questionContainer" ).hasClass( "down" )){
                 unsetQuestionsList();
            } else {
                 setQuestionsList();
            }             
        };
        
        $( "#questionOpener" ).off();
        $( "#questionOpener" ).on("click", fob);

        
        
    }
       
    function questionsHighlighter(model){
        if( model.get('type') == 'basic.twoTextRect'){
            //model.attr('rect/fill', 'rgba(46, 204, 113,1.0)');
            model.attr('rect/fill', 'rgb(52, 73, 94)');
            //rgb(52, 73, 94)
        }
    }
    
    function questionsUnhightlighter(model){
        if( model.get('type') == 'basic.twoTextRect'){
            model.attr('rect/fill', 'rgb(55,55,55)');      
        }
    }
    
    function detailsHighlighter(model){
        if( model.get('type') == 'basic.twoTextRect'){
            model.attr('rect/stroke-width', 5);
            model.attr('rect/stroke', 'rgba(52, 152, 219,1.0)');
        }
    }
    
    function detailsUnhighlighter(model){
        if( model.get('type') == 'basic.twoTextRect'){
            model.attr('rect/stroke-width', 0);  
        }
    }
          
    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i = 0; i <ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length,c.length);
            }
        }
        return "";
    } 
    
	function setQuestions(){
        console.log('setQuestions...');
        
        $(".ctaInput").removeClass("animated bounceOutRight");
        $(".ctaInput").show();
        $(".ctaInput2").hide();
        $("#ctaQueAccurateAjaxMessage").hide();
        
        $("#ctaQueAccurateSelection").html(
            "Double-cliquez sur la/les proposition(s) concernée(s) par votre question"
            +"<img id='simpleClick' src='{% static 'gdpcore/doubleClick.png' %}'>"
            );
        
    

        
        $("#ctaQueAccurateName").val( getCookie('name') );
        $("#ctaQueAccuratePhone").val( getCookie('phone') );
        $("#ctaQueAccurateEmail").val( getCookie('email') );
        
		selectedCells=[];
        
        $('#questionsCb > label > input').prop('checked', true);
        
        paper.off('cell:pointerclick');
		paper.on('cell:pointerclick', function(cellView,evt, x, y) {
			
			if ($.inArray(cellView.model.id,selectedCells) == -1){
				selectedCells.push(cellView.model.id);
				//cellView.highlight();
                questionsHighlighter(cellView.model);
						
			} else {
				console.log('already in selectedCells');
				selectedCells.splice( $.inArray(cellView.model.id, selectedCells), 1 );
				//cellView.unhighlight();
                questionsUnhightlighter(cellView.model);
			}


			$("#ctaQueAccurateSelection").html('');
            
            if(selectedCells.length == 0) {
                $("#ctaQueAccurateSelection").html(
                    "Double-Cliquez sur la/les proposition(s) concernée(s) par votre question"
                    +"<img id='simpleClick' src='{% static 'gdpcore/doubleClick.png' %}'>"
                );
            } else {
                selectedCells.forEach(function(entry) {
                    newAuthor = graph.getCell(entry).get('autorname');
                    newText = graph.getCell(entry).get('text');
                    $("#ctaQueAccurateSelection").html( $("#ctaQueAccurateSelection").html()+'<br />'+newAuthor+' : '+newText  );
                });
            }
		});
 
        var foa = function(){
            
            if (selectedCells.length != 0) {
            
                if ($("#ctaQueAccurateInput").val().length == 0){
                    
                    $('#ctaQueAccurateInput').removeClass('animated shake').addClass('animated shake').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                        $(this).removeClass('animated shake');
                    });
                   

                    $( "#ctaQueAccurateClick" ).off();
                    $( "#ctaQueAccurateClick" ).on("click", foa);                     
                    
                } else {            
                    var showpartsIds = [];
                    selectedCells.forEach(function(entry) {
                        showpartsIds.push(graph.getCell(entry).get('showpartId'));
                    });

                    $("#ctaQueAccurateSelection, #ctaQueAccurateInput").removeClass('animated bounceInRight shake');
                    $("#ctaQueAccurateSelection, #ctaQueAccurateInput").addClass('animated bounceOutRight');

                    $("#ctaQueAccurateClick").removeClass('animated flip');
                    $("#ctaQueAccurateClick").addClass('animated flip');
                              
                    setTimeout(function () { 
                        $("#ctaQueAccurateSelection, #ctaQueAccurateInput").hide();
                        $(".ctaInput2").show();
                        $(".ctaInput2").removeClass('animated bounceOutRight');
                        $(".ctaInput2").addClass('animated bounceInRight');                
                    }, 500)
                    
                    paper.off('cell:pointerclick');
                   
                    var fmm = function(){
                        
                        $('.ctaInput2').removeClass('animated bounceInRight');
                        
                        if ( $("#ctaQueAccurateName").val().length == 0 ) {
                        
                            console.log('àe');
                            $('#ctaQueAccurateName').removeClass('animated shake').addClass('animated shake').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                                $(this).removeClass('animated shake');
                            });
                   
                            $( "#ctaQueAccurateClick" ).off();
                            $( "#ctaQueAccurateClick" ).one("click", fmm);
                        
                        } else if ( $("#ctaQueAccurateEmail").val().length == 0 ) {
                            
                             $('#ctaQueAccurateEmail').removeClass('animated shake').addClass('animated shake').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                                $(this).removeClass('animated shake');
                            });
                   
                            $( "#ctaQueAccurateClick" ).off();
                            $( "#ctaQueAccurateClick" ).one("click", fmm);                           
                            
                        } else {
                     
                            textVal = $("#ctaQueAccurateInput").val();
                            emailVal = $('#ctaQueAccurateEmail').val();
                            nameVal = $('#ctaQueAccurateName').val();
                            phoneVal =  $('#ctaQueAccuratePhone').val();
                        
                            $.ajax( {
                                type: "POST",
                                url: '/ajax_newquestion/',
                                data: { 
                                        text: textVal,
                                        'showpartIds[]': showpartsIds,
                                        email: emailVal,
                                        name: nameVal,
                                        phone: phoneVal,
                                        event: {% if event.id %}{{event.id}}{%else%}1{%endif%},
                                        csrfmiddlewaretoken: '{{ csrf_token }}'
                                },
                                beforeSend: function() {
                                    $("#ctaQueAccurateClick").removeClass('animated flip');
                                    $("#ctaQueAccurateClick").removeClass('animated rotateIn');
                                    $("#ctaQueAccurateClick").addClass('animated rotateIn');
                                    
                                    $(".ctaInput2").removeClass('animated bounceInRight');
                                    $(".ctaInput2").addClass('animated bounceOutRight');
                                    
                                },
                                success: function( data ) {
                                    $("#ctaQueAccurateClick").removeClass('animated rotateIn');
         
                                     $("#ctaQueAccurateInput, .ctaInput2").hide();
         
                                    $("#ctaQueAccurateAjaxMessage").css('color','white');
                                    $("#ctaQueAccurateAjaxMessage").show();
                                    $("#ctaQueAccurateAjaxMessage").removeClass('animated','bounceOutRight');
                                    $("#ctaQueAccurateAjaxMessage").addClass('animated','bounceInRight');
                                    $("#ctaQueAccurateAjaxMessage").text("Votre question a bien été enregistrée. Nous revenons vers vous très prochainement !")
         
                                    //$(".ctaInput, .ctaInput2").removeClass('animated bounceInRight');
                                    //$(".ctaInput, .ctaInput2").addClass('animated bounceOutRight');
                            
                                    document.cookie = "email="+emailVal+"; expires=Fri, 31 Dec 9999 23:59:59 GMT";
                                    document.cookie = "name="+nameVal+"; expires=Fri, 31 Dec 9999 23:59:59 GMT";
                                    document.cookie = "phone="+phoneVal+"; expires=Fri, 31 Dec 9999 23:59:59 GMT";
                                                  
                                        
                                    $("#blackUnivok").addClass('animated bounceOutRight');
                                    setTimeout(function () {    
                                        $("#blackUnivok").attr("src", "{% static 'gdpcore/merci.png' %}");
                                    }, 500)
                                    setTimeout(function () { 
                                        $("#blackUnivok").removeClass('animated bounceOutRight');
                                        $("#blackUnivok").addClass('animated bounceInRight');
                                    }, 1000)
                                    setTimeout(function () { 
                                        $("#blackUnivok").removeClass('animated bounceInRight');
                                        $("#blackUnivok").addClass('animated bounceOutRight');                               
                                    }, 5000)
                                    setTimeout(function () { 
                                         $("#blackUnivok").attr("src", "{% static 'univok/univokText.png' %}");                              
                                    }, 5500)
                                    setTimeout(function () { 
                                        $("#blackUnivok").removeClass('animated bounceOutRight');
                                        $("#blackUnivok").addClass('animated bounceInRight');
                                    }, 6000) 


                                    setTimeout(function () { 
                                        unsetQuestions();
                                        setQuestions();                              
                                    }, 6000);
                                             
                                },
                                error: function(data){
                                    $("#ctaQueAccurateAjaxMessage").css('color','red');
                                    $("#ctaQueAccurateAjaxMessage").show();
                                    $("#ctaQueAccurateAjaxMessage").removeClass('animated','bounceOutRight');
                                    $("#ctaQueAccurateAjaxMessage").addClass('animated','bounceInRight');
                                    $("#ctaQueAccurateAjaxMessage").text("Une erreur a eu lieu. Merci de vérifier votre connexion internet et de ré-essayer. Si le problème persiste, copier/coller votre question et envoyer un mail à bonjour@univok.fr")
                                    
                                    $("#ctaQueAccurateInput").removeClass('animated bounceOutRight');
                                    $("#ctaQueAccurateInput").show();
                                    
                                    $( "#ctaQueAccurateClick" ).off();
                                    $( "#ctaQueAccurateClick" ).one("click", fmm); 
                                }
                            });                   
                        }    
                    }
                   
                    $( "#ctaQueAccurateClick" ).off();
                    $( "#ctaQueAccurateClick" ).one("click", fmm);
                }
                            
            } else {
                console.log('&')
                $('#ctaQueAccurateSelection').removeClass('animated shake').addClass('animated shake').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                    $(this).removeClass('animated shake');
                });
               
                $( "#ctaQueAccurateClick" ).off();
                $( "#ctaQueAccurateClick" ).on("click", foa);                 
            }
        }
		
        $( "#ctaQueAccurateClick" ).off();
        $( "#ctaQueAccurateClick" ).on("click", foa);

	}

    function setQuestionsList(){
        console.log('setQuestionsList');
        
        $(".questionFirstStep").removeClass("animated bounceOutRight");
        $(".questionFirstStep").show();
        $(".questionSecondStep").hide();
        $("#ctaQueAccurateAjaxMessage").hide();
        
        $("#ctaQueAccurateSelection").html(
            "Double-Cliquez sur la/les proposition(s) concernée(s) par votre question"
            +"<img id='simpleClick' src='{% static 'gdpcore/doubleClick.png' %}'>"
            );        
        selectedCells=[];
        
        $("#ctaQueAccurateName").val( getCookie('name') );
        $("#ctaQueAccuratePhone").val( getCookie('phone') );
        $("#ctaQueAccurateEmail").val( getCookie('email') );        
 
        function clickOnPropEventHandler(model){
			
            if ($.inArray(model.id,selectedCells) == -1){
				selectedCells.push(model.id);
                questionsHighlighter(model);						
			} else {
				console.log('already in selectedCells');
				selectedCells.splice( $.inArray(model.id, selectedCells), 1 );
				//cellView.unhighlight();
                questionsUnhightlighter(model);
			}
            
			$("#ctaQueAccurateSelection").html('');
            
            if(selectedCells.length == 0) {
                $("#ctaQueAccurateSelection").html(
                    "Double-Cliquez sur la/les proposition(s) concernée(s) par votre question"
                    +"<img id='simpleClick' src='{% static 'gdpcore/doubleClick.png' %}'>"
                );
            } else {
                selectedCells.forEach(function(entry) {
                    newAuthor = graph.getCell(entry).get('autorname');
                    newText = graph.getCell(entry).get('text');
                    $("#ctaQueAccurateSelection").html( $("#ctaQueAccurateSelection").html()+'<br />'+newAuthor+' : '+newText  );
                });
            }            
            $("#listFinalTable tr").filter( function(){
                return $(this).find('.propId').eq(0).text() == model.get('id_prop') 
            }).find('.propText').eq(0).toggleClass('dblClicked');
            
           
        
        }
 
        paper.off('cell:pointerdblclick');
		paper.on('cell:pointerdblclick', function(cellView,evt, x, y) {
			
            console.log('daidui');
            clickOnPropEventHandler(cellView.model);
            
/*			if ($.inArray(cellView.model.id,selectedCells) == -1){
				selectedCells.push(cellView.model.id);
                questionsHighlighter(cellView.model);						
			} else {
				console.log('already in selectedCells');
				selectedCells.splice( $.inArray(cellView.model.id, selectedCells), 1 );
				//cellView.unhighlight();
                questionsUnhightlighter(cellView.model);
			}
            
			$("#ctaQueAccurateSelection").html('');
            
            if(selectedCells.length == 0) {
                $("#ctaQueAccurateSelection").html(
                    "Cliquez sur la/les proposition(s) concernée(s) par votre question"
                    +"<img id='simpleClick' src='{% static 'gdpcore/simpleClick.png' %}'>"
                );
            } else {
                selectedCells.forEach(function(entry) {
                    newAuthor = graph.getCell(entry).get('autorname');
                    newText = graph.getCell(entry).get('text');
                    $("#ctaQueAccurateSelection").html( $("#ctaQueAccurateSelection").html()+'<br />'+newAuthor+' : '+newText  );
                });
            } */
		});        

        $("#listFinalTable").off();
        $("#listFinalTable").on('dblclick',function(event){
            if ($(event.target).hasClass('propText')){
               
               
                idProp = $(event.target).parent().find('.propId').eq(0).text();
                console.log(propIdCorrespondance[idProp]);           
                cell = graph.getCell( propIdCorrespondance[idProp] );
                
                clickOnPropEventHandler(cell);
            };
            
        });
        
   
        
        var foa = function(){
            
            if (selectedCells.length != 0) {
            
                if ($("#ctaQueAccurateInput").val().length == 0){
                    
                    $('#ctaQueAccurateInput').removeClass('animated shake').addClass('animated shake').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                        $(this).removeClass('animated shake');
                    });
                   

                    $( "#ctaQueAccurateClick" ).off();
                    $( "#ctaQueAccurateClick" ).on("click", foa);                     
                    
                } else {            
                    var showpartsIds = [];
                    selectedCells.forEach(function(entry) {
                        showpartsIds.push(graph.getCell(entry).get('showpartId'));
                    });

                    $("#ctaQueAccurateSelection, #ctaQueAccurateInput").removeClass('animated bounceInRight shake');
                    $("#ctaQueAccurateSelection, #ctaQueAccurateInput").addClass('animated bounceOutRight');

                    $("#ctaQueAccurateClick").removeClass('animated flip');
                    $("#ctaQueAccurateClick").addClass('animated flip');
                              
                    setTimeout(function () { 
                        $("#ctaQueAccurateSelection, #ctaQueAccurateInput").hide();
                        $(".questionSecondStep").show();
                        $(".questionSecondStep").removeClass('animated bounceOutRight');
                        $(".questionSecondStep").addClass('animated bounceInRight');                
                    }, 500)
                    
                    paper.off('cell:pointerclick');
                   
                    var fmm = function(){
                        
                        $('.questionSecondStep').removeClass('animated bounceInRight');
                        
                        if ( $("#ctaQueAccurateName").val().length == 0 ) {
                        
                            console.log('àe');
                            $('#ctaQueAccurateName').removeClass('animated shake').addClass('animated shake').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                                $(this).removeClass('animated shake');
                            });
                   
                            $( "#ctaQueAccurateClick" ).off();
                            $( "#ctaQueAccurateClick" ).one("click", fmm);
                        
                        } else if ( $("#ctaQueAccurateEmail").val().length == 0 ) {
                            
                             $('#ctaQueAccurateEmail').removeClass('animated shake').addClass('animated shake').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                                $(this).removeClass('animated shake');
                            });
                   
                            $( "#ctaQueAccurateClick" ).off();
                            $( "#ctaQueAccurateClick" ).one("click", fmm);                           
                            
                        } else {
                     
                            textVal = $("#ctaQueAccurateInput").val();
                            emailVal = $('#ctaQueAccurateEmail').val();
                            nameVal = $('#ctaQueAccurateName').val();
                            phoneVal =  $('#ctaQueAccuratePhone').val();
                        
                            $.ajax( {
                                type: "POST",
                                url: '/ajax_newquestion/',
                                data: { 
                                        text: textVal,
                                        'showpartIds[]': showpartsIds,
                                        email: emailVal,
                                        name: nameVal,
                                        phone: phoneVal,
                                        event: {% if event.id %}{{event.id}}{%else%}1{%endif%},
                                        csrfmiddlewaretoken: '{{ csrf_token }}'
                                },
                                beforeSend: function() {
                                    $("#ctaQueAccurateClick").removeClass('animated flip');
                                    $("#ctaQueAccurateClick").removeClass('animated rotateIn');
                                    $("#ctaQueAccurateClick").addClass('animated rotateIn');
                                    
                                    $(".questionSecondStep").removeClass('animated bounceInRight');
                                    $(".questionSecondStep").addClass('animated bounceOutRight');
                                    
                                },
                                success: function( data ) {
                                    $("#ctaQueAccurateClick").removeClass('animated rotateIn');        
                                    $("#ctaQueAccurateInput").addClass('animated bounceOutRight');        
                                    $("#ctaQueAccurateAjaxMessage").css('color','white');
                                    
                                    $("#ctaQueAccurateAjaxMessage").removeClass('animated','bounceOutRight');
                                    $("#ctaQueAccurateAjaxMessage").show();
                                    $("#ctaQueAccurateAjaxMessage").addClass('animated','bounceInRight');
                                    $("#ctaQueAccurateAjaxMessage").text("Votre question a bien été enregistrée. Nous revenons vers vous très prochainement !")
         
                            
                                    document.cookie = "email="+emailVal+"; expires=Fri, 31 Dec 9999 23:59:59 GMT";
                                    document.cookie = "name="+nameVal+"; expires=Fri, 31 Dec 9999 23:59:59 GMT";
                                    document.cookie = "phone="+phoneVal+"; expires=Fri, 31 Dec 9999 23:59:59 GMT";
                                                  
                                        
/*                                    $("#blackUnivok").addClass('animated bounceOutRight');
                                    setTimeout(function () {    
                                        $("#blackUnivok").attr("src", "{% static 'gdpcore/merci.png' %}");
                                    }, 500)
                                    setTimeout(function () { 
                                        $("#blackUnivok").removeClass('animated bounceOutRight');
                                        $("#blackUnivok").addClass('animated bounceInRight');
                                    }, 1000)
                                    setTimeout(function () { 
                                        $("#blackUnivok").removeClass('animated bounceInRight');
                                        $("#blackUnivok").addClass('animated bounceOutRight');                               
                                    }, 5000)
                                    setTimeout(function () { 
                                         $("#blackUnivok").attr("src", "{% static 'univok/univokText.png' %}");                              
                                    }, 5500)
                                    setTimeout(function () { 
                                        $("#blackUnivok").removeClass('animated bounceOutRight');
                                        $("#blackUnivok").addClass('animated bounceInRight');
                                    }, 6000) */


                                    setTimeout(function () { 
                                        unsetQuestionsList();
                                        setQuestionsList();                              
                                    }, 6000);
                                             
                                },
                                error: function(data){
                                    $("#ctaQueAccurateAjaxMessage").css('color','red');
                                    $("#ctaQueAccurateAjaxMessage").show();
                                    $("#ctaQueAccurateAjaxMessage").removeClass('animated','bounceOutRight');
                                    $("#ctaQueAccurateAjaxMessage").addClass('animated','bounceInRight');
                                    $("#ctaQueAccurateAjaxMessage").text("Une erreur a eu lieu. Merci de vérifier votre connexion internet et de ré-essayer. Si le problème persiste, copier/coller votre question et envoyer un mail à bonjour@univok.fr")
                                    
                                    $("#ctaQueAccurateInput").removeClass('animated bounceOutRight');
                                    $("#ctaQueAccurateInput").show();
                                    
                                    $( "#ctaQueAccurateClick" ).off();
                                    $( "#ctaQueAccurateClick" ).one("click", fmm); 
                                }
                            });                   
                        }    
                    }
                   
                    $( "#ctaQueAccurateClick" ).off();
                    $( "#ctaQueAccurateClick" ).one("click", fmm);
                }
                            
            } else {
                console.log('&')
                $('#ctaQueAccurateSelection').removeClass('animated shake').addClass('animated shake').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                    $(this).removeClass('animated shake');
                });
               
                $( "#ctaQueAccurateClick" ).off();
                $( "#ctaQueAccurateClick" ).on("click", foa);                 
            }
        }
		
        $( "#ctaQueAccurateClick" ).off();
        $( "#ctaQueAccurateClick" ).on("click", foa);
        
    }
    
    function unsetQuestions(){
        
        console.log('unsetQuestions..');
        selectedCells=[];
        
        $("#ctaQueAccurateClick").removeClass('animated flip');      
        $(".ctaInput, .ctaInput2").removeClass('animated bounceInRight');
//        $(".ctaInput, .ctaInput2").addClass('animated bounceOutRight');        
        $("#ctaQueAccurateInput, .ctaInput2").val('');
        $("#ctaQueAccurateSelection").html('');
		allCells = graph.getCells();
		allCells.forEach(function(entry) {
			//paper.findViewByModel(entry).unhighlight();
            questionsUnhightlighter(entry);
		});
 
        clearTimeout(messageShowTimeout);
        clearTimeout(messageHideTimeout);
 
        $('#ctaQueAccurateInstruction').removeClass('animated bounceInUp'); 
        $('#ctaQueAccurateInstruction').addClass('animated bounceOutDown');

        $('#questionsCb > label > input').prop('checked', false);
        
        paper.off('cell:pointerclick');
    }

    function unsetQuestionsList(){
        
        console.log('unsetQuestionsList..');
        selectedCells=[];
        
        $("#ctaQueAccurateClick").removeClass('animated flip');      
        $(".questionFirstStep, .questionSecondStep").removeClass('animated bounceInRight');   
        $("#ctaQueAccurateInput, .questionSecondStep").val('');
        $("#ctaQueAccurateSelection").html('');
		allCells = graph.getCells();
		allCells.forEach(function(entry) {
            questionsUnhightlighter(entry);
		});
        
        $('.dblClicked').removeClass('dblClicked');
 
        clearTimeout(messageShowTimeout);
        clearTimeout(messageHideTimeout);
 
        $('#ctaQueAccurateInstruction').removeClass('animated bounceInUp'); 
        $('#ctaQueAccurateInstruction').addClass('animated bounceOutDown');
 
        paper.off('cell:pointerdblclick');
        $("#listFinalTable").off();
    }
    
    function setDetails(){	
        console.log("setDetails");
        $("#detailsSentences, #detailsPicture").show();
        $('#detailsCb > label > input').prop('checked', true);
        
        $("#detailsPicture").show();
        $("#detailsSentences").html("Double-cliquez sur une proposition pour avoir des détails...");
        $("#detailsPicture").attr('src', "{% static 'gdpcore/doubleClick.png' %}");
        
        paper.on('blank:pointerdblclick', function(cellView,evt, x, y) {

			allCells = graph.getCells();
			allCells.forEach(function(entry) {
				//paper.findViewByModel(entry).unhighlight();
                detailsUnhighlighter(entry);
			});  
            $("#detailsSentences").html("Double-cliquez sur une proposition pour avoir des détails...");
            $("#detailsPicture").attr('src', "{% static 'gdpcore/doubleClick.png' %}");
        });
        
        paper.off('cell:pointerdblclick');
        paper.on('cell:pointerdblclick', function(cellView,evt, x, y) {
			
			//On entoure et desentour			
			allCells = graph.getCells();
			allCells.forEach(function(entry) {
				//paper.findViewByModel(entry).unhighlight();
                detailsUnhighlighter(entry);
			});
			detailsHighlighter(cellView.model);
			
			//On ajoute les citations
			text = cellView.model.get("sentences");			
			$("#detailsSentences").html(text);
            
            //On montre l'image
            $("#detailsPicture").show()
            $("#detailsPicture").attr('src', "{{MEDIA_URL}}/media/"+cellView.model.get("authorPicture"));

			//On lit l'audio
			audioplayer.setAttribute('src', "{{MEDIA_URL}}/media/"+cellView.model.get("audio"));
			audioplayer.play();			
			
		});	        
    }
    
    function unsetDetails(){
        allCells = graph.getCells();
        allCells.forEach(function(entry) {
            //paper.findViewByModel(entry).unhighlight();
            detailsUnhighlighter(entry);
        }); 

        $("#detailsSentences").html('');
        $("#detailsPicture").attr('src', "");
        $("#detailsSentences, #detailsPicture").hide();
        
        audioplayer.setAttribute('src', "");
        audioplayer.pause();

        $('#detailsCb > label > input').prop('checked', false);
    }
    
	function unsetAll(){
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
					showId: {% if show.pk %}{{show.pk}}{% else %}0{% endif %},
					data: bigstring,
					csrfmiddlewaretoken: '{{ csrf_token }}'
			},
			success: function( data ) {		
				
				console.log(data);
			}
		});
				
	}
	
    function themeHighlighter(){
        var themes = {};
        themes[0] = {'color': ''}
        themes[1] = {'color': 'yellow'}
        themes[2] = {'color': 'orange'}
        themes[3] = {'color': 'blue'}
        themes[4] = {'color': 'green'}  
        themes[5] = {'color': 'purple'}    
        themes[6] = {'color': 'brown'}
        themes[7] = {'color': 'pink'}   
        var i = 0;

        updateCorrespondances();
        //On sélectionne chaque theme, et pour chacun...
        $('#listThemeSelect option').each(function(key, value){
         
            //On selectionne les bonnes lignes..
           goodRows = $('#listPropsTable tr').filter(function () {
                return $(this).find(".theme").eq(0).text() == $(value).text()
            });
                 
            //et pour chaque ligne, on va changer le highlight de la cell
            goodRows.each(function(key2, val2){
            
                //L'id du model sur paper...
                id = propIdCorrespondance[ $(val2).find('.propId').eq(0).text()  ];
                   
                //Et on change la cell..
                cell = graph.getCell(id);
                cell.attr('rect/stroke-width', 3);
                cell.attr('rect/stroke', themes[i]['color']);
            });       
        i=i+1;    
        });
      
    }     
 
    function sizeAllRect(){
        
        console.log('sizeAllRect');
        
		allCells = graph.getElements();
		allCells.forEach(function(entry) {
            
            word1 = $('g').filter( function(){        
                return $(this).attr('model-id') == entry.id
            }).eq(0).find('.word1').eq(0);            
       
        
            console.log('word1' + word1);
            
            if(typeof(word1.get(0)) != 'undefined') {
                heightValue = word1.get(0).getBBox().height;       
                console.log(heightValue);            
                entry.attr('rect/height', heightValue + 50);            
                entry.attr('.word2/transform','translate(165,'+(heightValue+30)+')');   
            }
        });
    }
 
/*	$( document ).ready(function() {
		paper = addPaper('myholder');
		firstLoadFromShowparts('myholder');
		initPage(); 

		$( "body" ).on("click", "#stopAnim", function(event) {
			stopshow();
		});
	});
*/