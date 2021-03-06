
{% load staticfiles %}
	
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
	authorList[{{user.id}}] = '{{user.username|escapejs}}'

	//Ini graph
    var graph = new joint.dia.Graph;
	
	var selectedElement = '';
	
	//Variables pour le paper
	var graphScale = 1;
	var originX = {{graph.originx}};
	var originY = {{graph.originy}};
	var sensibility = 20;	
	

	$( "#ytcontainer" ).draggable();
	//Créer une proposition
	function addProp(id_prop, text, autorname) {

		var wraptext = joint.util.breakText(text, {
			width: 145,
			height: 90,
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
						fill: '#EEEEEE', 
						stroke: 'white', 
						'stroke-width': 4, 
						'follow-scale': true, 
						width: 150, 
						height: 80
					},

					'.word2': { 
						'font-size': 15,
						'font-weight': 'bold',
						fill: 'black', 
						'text-anchor':'end',
						transform: "translate(165,82)" 
					},
					'.word1': { 
						'ref': 'rect',
						'font-size': 15,
						'text-anchor':'middle',
						transform: "translate(95,20)" ,
						fill: 'black',
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
				size: { width: 200, height: 100 },
				id_prop : id_prop,
				text : text
			}, joint.shapes.basic.Generic.prototype.defaults)
		});

		var el = new joint.shapes.basic.twoTextRect({
			attrs: {}
		});
		el.attr('.word1/text', wraptext);
		el.attr('.word2/text', autorname);
		el.attr('./display', 'none');	
	
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
			labels : [
			{ position: 0.5, attrs: { text: { text: typesData[type_id]['type']+' ('+autorname+')', 'font-size': 12 } } }
			]
		});

		li.attr({
			'.connection': typesData[type_id]['connection'],
			'.marker-source': typesData[type_id]['source'],
			'.marker-target': typesData[type_id]['target']
		});	

		li.attr('./display', 'none');
		
		graph.addCell(li) ;
		linkVisu(li);		
		
		console.log('link added to graph - id_link: '+id_link+' id: '+li.id)
		
		if (typesData[type_id]['type'] != 'syllogisme') {
			addCircToLink(li);
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
		
	//Firstload : main
	function firstLoad() {
	
		//Ini paper
		var paper = new joint.dia.Paper({
			el: $('#myholder'),
			width: 100/100*$(window).width(),
			height: $(window).height(),
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
	
		$("#actionProp").hide();
		$("#actionLink").hide();
	
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
		
