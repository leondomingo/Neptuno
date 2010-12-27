/////////////////////////////////////////////////////////////////////////
//// Objeto Selector
/////////////////////////////////////////////////////////////////////////
(function($) 
{
	var propiedades;
	var acciones;
  	
  	$.fn.Selector=function(parametros) 
  	{
		
		$('*').css('cursor','wait');
		
		propiedades = $.extend({
			idSeleccionado: null,
			campos: null, 
			tabla: null,
			botonCrear: null,
			titulo: null,
			campofiltrado: null,
			valorfiltrado: null,
			campospordefecto: null,
			valorespordefecto: null,

			orderbyid:false,
			debug: false,
			contenedorMensajes:null,
			inicializadoDialogoBorrar:false,
			tipoEdicion:null,
			solo_lectura:false,
			acciones_ocultar:null,
			actions:null,
			resultsActions: null,
			maxResults:50,
			acciones_ocultar:null,
			modo: null,
			activaSeleccion:false, 
			pos: 0,
			webservice: null, /* Para especificar la llamada a otro s.w. distinto del de por defecto */		
			onReady:null,  /* Cuando el selector está totalmente cargado */
			onEdit: null, /* Se llama cuando está lista la edición de un nuevo registro */
			onCreate: null,  /* Se llama cuando está lista la creación de un nuevo registro */
			onReadyResults:null,
			onReadyCreate:null,
			extraparams: null /* Un array de parámetros extra a pasar al s.w.
						extraparams:[{nombre:'p1',valor:p1},...,{nombre:'pn',valor:pn}]
					*/
		}, parametros || {});
		
		var selector=$(this);
		var idSelector=$(this).attr("id");
		
		/***************************************************************
		 Procesamos los parámetros
		 **************************************************************/

		// Añadimos la acción por defecto de abrir registro
		var idAction=neptuno.addAction(neptuno.accionAbrir);
		if(propiedades.resultsActions!=null)
		{
			propiedades.resultsActions[propiedades.resultsActions.length]={label:'Abrir',clase:'abrirNuevaPestanya', idAction:idAction};
		}
		else
		{
			propiedades.resultsActions=[{label:'Abrir',clase:'abrirNuevaPestanya', idAction:idAction}];
		}
		
		// Inicializamos la consola
		selector.logconsola=new RegistroSapns();
		selector.logconsola.Debug=false;
		selector.logconsola.BloqueInicio="[Objeto Selector] ";
		selector.logconsola.IniciaTemporizador("ObjetoSelector");
		selector.logconsola.Debug=propiedades.debug;
		selector.logconsola.Log("Constructor del selector, idSeleccionado: "+propiedades.idSeleccionado+", tabla: "+propiedades.tabla+", campofiltrado: "+propiedades.campofiltrado+", valorfiltrado: "+propiedades.valorfiltrado);

		// Propiedades html
		selector.attr('idSeleccionado',propiedades.idSeleccionado);
		selector.attr('tabla',propiedades.tabla);	
		selector.attr('tipoEdicion',propiedades.tipoEdicion);
		selector.attr('campofiltrado',propiedades.campofiltrado);	
		selector.attr('valorfiltrado',propiedades.valorfiltrado);		
		selector.attr('campospordefecto',propiedades.campospordefecto);	
		selector.attr('valorespordefecto',propiedades.valorespordefecto);		
		
		selector.attr('debug',propiedades.debug);
		selector.attr('activaSeleccion',propiedades.activaSeleccion);
		
		neptuno.setAttrData(idSelector, 'selectorPrincipal', selector.hasClass('selectorPrincipal'))

		if(selector.attr('solo_lectura') )
		{
			propiedades.solo_lectura=selector.attr('solo_lectura');
		}
		
		propiedades.titulo=(selector.attr("titulo")!="" ? selector.attr("titulo") : propiedades.titulo);
		propiedades.modo=(selector.attr("modo")!="" ? selector.attr("modo") : propiedades.modo);
		
		if(neptuno &&  neptuno.getAttrData(idSelector, "selectorPrincipal") )
		{
			// Solo le hemos de aplicar el modo del hash si es el selector principal de la página
			var datosNavegacion=neptuno.obtenerDatosNavegacion();
			if(datosNavegacion.modo!='')
			{
				propiedades.modo=datosNavegacion.modo;
			}
		}
		
		if (selector.attr('idSeleccionado') == 'null') 
		{
			selector.attr('idSeleccionado','-1');
		}

		if(neptuno)
		{
		    // Guardamos los parámetros
		    neptuno.setAttrData(idSelector, "tabla", propiedades.tabla);
		    neptuno.setAttrData(idSelector, "titulo", propiedades.titulo);

		    neptuno.setAttrData(idSelector, "modo", (neptuno.getAttrData(idSelector, 'selectorPrincipal') ? propiedades.modo : ''));

		    neptuno.setAttrData(idSelector, "campofiltrado", propiedades.campofiltrado);
			neptuno.setAttrData(idSelector, "valorfiltrado", propiedades.valorfiltrado);
			neptuno.setAttrData(idSelector, "tipoEdicion", propiedades.tipoEdicion);
		    neptuno.setAttrData(idSelector, "campospordefecto", propiedades.campospordefecto);
			neptuno.setAttrData(idSelector, "valorespordefecto", propiedades.valorespordefecto);
			
			
		    
		    neptuno.setAttrData(idSelector, "maxResults", propiedades.maxResults);
		    neptuno.setAttrData(idSelector, "pos", propiedades.pos);
		    neptuno.setAttrData(idSelector, "numero_resultados", propiedades.numero_resultados);
		    neptuno.setAttrData(idSelector, "webservice", propiedades.webservice);
		    neptuno.setAttrData(idSelector, "onReadyResults", propiedades.onReadyResults);
		    neptuno.setAttrData(idSelector, "orderbyid", propiedades.orderbyid);
		    neptuno.setAttrData(idSelector, "campos", propiedades.campos);
		    neptuno.setAttrData(idSelector, "onEdit", propiedades.onEdit);
		    neptuno.setAttrData(idSelector, "onReadyCreate", propiedades.onReadyCreate);
		    neptuno.setAttrData(idSelector, "onCreate", propiedades.onCreate);
		    neptuno.setAttrData(idSelector, "acciones_ocultar", propiedades.acciones_ocultar);
		    neptuno.setAttrData(idSelector, "solo_lectura", propiedades.solo_lectura);
		    neptuno.setAttrData(idSelector, "botonCrear", propiedades.botonCrear);

		    // Parámetros de tipo objeto
		    neptuno.setAttrDataObject(idSelector, "resultsActions", propiedades.resultsActions);
		    neptuno.setAttrDataObject(idSelector, "extraparams", propiedades.extraparams);
		    neptuno.setAttrDataObject(idSelector, "actions", propiedades.actions);
		}

	var cajabusqueda=null;
	var cajaacciones=null;
	var cajaresultado=null;
	var cajatitulogrande=null;
	var cajaaccionactiva=null;
	$.ajax({
		url: "/neptuno/libjs/jquery_ender_selector/modulos/Selector.htm", 
		async :false,
		cache:false,
		success:
			function(respuesta)
			{
				load_css("/neptuno/libjs/jquery_ender_selector/modulos/Selector.css");
				
				// Modo full screen
				
				var fullScreenMode=(neptuno && neptuno.getAttrData(idSelector, "modo")=="full");
				
				if( fullScreenMode )
				{
					load_css("/neptuno/libjs/jquery_ender_selector/modulos/fullScreenMode.css");
				}
				
				selector.html(respuesta);	

				var usuarioNeptuno=neptuno.obtenerusuarioNeptuno();
				
				cajabusqueda=selector.find('.CajaBusqueda');
				cajaacciones=selector.find('.Seleccionado');
				cajaresultado=selector.find('.ResultadoBusqueda');
				cajatitulogrande=selector.find('.CajaTituloGrande');
				cajaaccionactiva=selector.find('.AccionActiva');
				
				if( fullScreenMode )
				{
					cajatitulogrande.html( neptuno.getAttrData(idSelector, 'titulo') );
				}

				selector.find('.navegacionResultados').fadeOut();
				
				// Le aplicamos el componente C1(caja de búsqueda)
				var searchactions=new Array();
				var searchAction=(  neptuno.getAttrData(idSelector, "solo_lectura") ? BuscarRegistroModoLista :  BuscarRegistro);
				
				var _searchaction=neptuno.addAction(searchAction);
				searchactions[0]={label:'buscar', _class:'BotonBuscar', idAction:_searchaction};

				if( neptuno.getAttrData(idSelector, "botonCrear") ) 
				{
					var onCreate=neptuno.getAttrData(idSelector, "onCreate");
					if(onCreate)
					{
						var _createaction=neptuno.addAction(onCreate);	
					}
					else
					{
						var _createaction=neptuno.addAction(CrearRegistro);	
					}

					searchactions[1]={label:'nuevo', _class:'BotonCrear', idAction: _createaction};
				}

				if( neptuno.getAttrData(idSelector, "modo")!="full" )
				{

					var titulo=neptuno.getAttrData(idSelector, "titulo" );
					cajabusqueda.searchbox({
						title: (titulo==null ?  selector.attr('titulo') : titulo),
						actions: searchactions,
						readonly: neptuno.getAttrData(idSelector, "solo_lectura"),
						control: selector
					});
					
				}
				
			   	

				cajaresultado.grid({idselector: selector.attr("id"),
						   actions: neptuno.getAttrDataObject(idSelector, "resultsActions")
						   });
		        
				if( neptuno.getAttrData(idSelector, "solo_lectura") )
				{
					// En el modo de solo lectura, ocultamos la caja de búsqueda
					cajabusqueda.ocultaBotonBusqueda();
				}
				else
				{
					cajabusqueda.activaFoco();									
				}
				$('*').css('cursor','');
				

				// FCambiado
				selector.find('.Dialogo').attr('id', 'Dialogo'+idSelector);
			} // success
		});  // ajax

		cajaresultado.fadeOut();
		cajaaccionactiva.fadeOut();		
		selector.AsignarRegistro(this.attr('idSeleccionado'));
	
		var campofiltrado=propiedades.campofiltrado;
		var valorfiltrado=propiedades.valorfiltrado;

		var campopordefecto=propiedades.campospordefecto;
		var valorpordefecto=propiedades.valorespordefecto;

	
		if ((campofiltrado != null) && (valorfiltrado != null)) 
		{
			selector.DevolverLista(campofiltrado, valorfiltrado, true);
		}
	
		this.logconsola.FinalizaTemporizador("ObjetoSelector");

		var onReady=neptuno.getAttrData(idSelector, "onReady")
		if( onReady!=null )
		{
			eval(onReady+"()");			
			$.ender.posicionaAccionActiva( $(this) );
		}
	$('*').css('cursor','');
	}; 

	if( $.fn.logconsola==null )
	{
		$.fn.logconsola=new RegistroSapns();
		$.fn.logconsola.BloqueInicio="[Selector] ";
	}
	
	/**
	 * Esta acción se invoca después de mostrar todos los resultados
	 * @function readyResults
	 */
	$.fn.readyResults=function(idselector)
	{
		var onReadyResults=neptuno.getAttrData(idselector, "onReadyResults");
		
		if(onReadyResults)
		{
			onReadyResults();
		}

		// Desactivamos la selección de registros
		var selector=$("#"+idselector);
		if( selector.attr('campofiltrado')!='' && selector.attr('campofiltrado')!='null' && propiedades.activaSeleccion != true)
		{
			selector.desactivaSeleccion();
			
			// TODO: No oculta correctamente este bloque por medio de
			// fadeOut o hide. Por ello elimino el borde.
			selector.find(".AccionActiva").css("border", "none");			
		}
		
		$.ender.posicionaAccionActiva( $("#"+idselector) );
	}; // readyResults
	
	/**
	 * @function MuestraMensaje
	 */
	$.fn.MuestraMensaje=function(msg)
	{
		if(neptuno && neptuno.cntMsgs)
		{
			neptuno.cntMsgs.Show(msg);
		}
	}; // MuestraMensaje
	
	/**
	 * @function MuestraMensajeError
	 */
	$.fn.MuestraMensajeError=function(data, msg)
	{
		if( neptuno && neptuno.cntMsgs )
		{
			neptuno.cntMsgs.ShowError(data, msg);
		}		
	}; // MuestraMensajeError
	
	/**
	 * @function asignarAcciones
	 */
	$.fn.asignarAcciones=function(bloque, datosAcciones)
	{
		var ndatosAcciones=datosAcciones.length;
	
		for(ACCIONi=0;ACCIONi<ndatosAcciones;ACCIONi++)
		{
			$(this).asignarAccion(bloque, datosAcciones[ACCIONi].clase, datosAcciones[ACCIONi].funcion);
		} // recorremos las acciones
		
		$(this).cargaAccionDefecto(bloque);
	}; // asignarAcciones
	
	/**
	* @function cargaAccionDefecto
	*/
	$.fn.cargaAccionDefecto=function(bloque)
	{
	 	var selector=$(this);
		var idSelector=selector.attr('id');
		
		if ( neptuno.getAttrData(idSelector, 'modo') == 'full') 
	 	{
			if (bloque.find('[accionPorDefecto] > a').attr('ejecutado') != 'true') 
			{
				bloque.find('[accionPorDefecto] > a').attr('ejecutado','true');
				$(this).Log("La acción por defecto es "+bloque.find('[accionPorDefecto] > a').html() );
				bloque.find('[accionPorDefecto] > a').trigger('click');
			}
		}
		else if(selector.attr('cargaacciones') == 'true' )
		{
			var datosNavegacion=neptuno.obtenerDatosNavegacion();
			var accion=datosNavegacion.accion;
			
			if(accion!=null)
			{
				bloque.find('.'+accion+' > a').trigger('click');
			}										
		}
	}; // cargaAccionDefecto
	
	/**
	 * Selector::asignarAccion
	 */
	$.fn.asignarAccion=function(bloque, clase, funcion)
	{
		var selector=$(this);
		var idSelector=selector.attr('id');
		
		bloque.find('.'+clase).unbind("click");
		bloque.find('.'+clase).bind("click", {selector: $(this)}, function a(event)
		{
			// Vaciamos los resultados de la búsqueda.
			selector.find(".exportarResultados").hide();
			selector.find(".ResultadoBusqueda").find(".resultados").html("");
			selector.find(".AccionActiva").focus();
			
			funcion(event);
		});
		
		var datosNavegacion=neptuno.obtenerDatosNavegacion();
		var hash='#'+idSelector+':'+datosNavegacion.id+':'+clase+':'+datosNavegacion.modo;
		
		bloque.find('.'+clase+' > a').attr("href", hash); 
	}; // asignarAccion
	

	/**
	 * Selector::$.fn.emptySelect
	 * Vacía un elemento de formulario de tipo select
	 */
	$.fn.emptySelect = function() {
		$(this).Log("emptySelect");
		return this.each(function(){
			if (this.tagName=='SELECT') this.options.length=0;
		});
	}; // emptySelect
	
	
	/**************************************************************************
	 * Selector::$.fn.BorrarRegistro
	 * Borra el registro seleccionado en la tabla del selector.
	 *************************************************************************/
	$.fn.BorrarRegistro = function(ocultaDialogo) 
	{
		$(this).Log("BorrarRegistro");
		selector = $(this);
	 	var idDialogo='#Dialogo'+$(this).attr('id');
	 	var usuarioNeptuno=neptuno.obtenerusuarioNeptuno();
	 	var tabla=selector.attr('tabla');
		
	 	$(idDialogo).html("¿Borrar este registro?");
	 	
	 	var idSelector=selector.attr('id');
	 	
		var _id		=$('#'+idSelector).attr('idSeleccionado');
		var _tabla	=$('#'+idSelector).attr('tabla');
		
	 	neptuno.inicializaDialogo(idDialogo, "Borrar registro");
	 	$(idDialogo).dialog('option', 'buttons',
	 	{
			"Cancelar": function()
			{
				// cerramos el diálogo
				$(this).dialog('close');
			},
		 	"Aceptar": function() 
			{ 
		
				$.ajax({ type:'POST',
				url:'/neptuno/sw/borrar.py',
				cache:false,
				data:{ idSelector: selector.attr('id'),
				       id_usuario:usuarioNeptuno.id, 
				       id_sesion:usuarioNeptuno.challenge,
				       id:_id,
				       tabla: _tabla																			       
				       },
				success:function(respuesta)	
				{																					
					
					$(idDialogo).dialog('close');																					
					endcursorEspera();
					eval("var resultado="+respuesta);
					
					if(resultado.codigo && resultado.texto)
					{
						// Se ha producido una excepción
						// http://bean.ender.es/mantis/view.php?id=4379						
						if(resultado.texto==_tabla)
						{
							neptuno.cntMsgs.ShowError(null, "No se puede borrar porque hace referencia a algún otro registro de esta tabla(código de error "+resultado.codigo+")" );
						}
						else
						{
							neptuno.cntMsgs.ShowError(null, "No se puede borrar el registro en la tabla "+_tabla+" porque hace referencia a algún elemento en la tabla "+resultado.texto+" (código de error "+resultado.codigo+")" );
						}
					}
					else
					{
					
						neptuno.cntMsgs.Show("Registro borrado en la tabla "+_tabla);
						selector.attr('idSeleccionado', -1)																					
						selector.find('.Seleccionado').html('');
						selector.find('.AccionActiva').html('');
						selector.AsignarRegistro(-1);
						selector.find(".Seleccionado").fadeOut();
																					
					}
					
				},
				error: function(resultado)
				{																					
					/**
					Si el registro tiene elementos asociados en otra tabla es posible que se genere un error
					Hemos de mostrar un mensaje descriptivo.
					 **/
					$(idDialogo).dialog('close');																					
					endcursorEspera();

					neptuno.cntMsgs.ShowError(resultado, "No se ha podido borrar el registro en la tabla "+_tabla+", error inesperado.");																																										
				}
				});	 														 
			}
		});
		
		if(!ocultaDialogo)
		{
			$(idDialogo).dialog('open');
		}

	}; // BorrarRegistro
		
	/**************************************************************************
	Selector::$.fn.getHTMLBotonGuardar
	Genera dinámicamente el HTML del botón de guardar para la pantalla de 
	edición de registro.
	 *************************************************************************/	
	var getHTMLBotonGuardar=function(idSelector)
	{
		var selector=$('#'+idSelector);
		var str="";		

		// Construimos la URL de los enlaces
		var hash="#";		
		var datosNavegacion=neptuno.obtenerDatosNavegacion();
		hash+=idSelector+":"+selector.attr('idseleccionado')+'::'+datosNavegacion.modo;
	
		str="<div class=\"CampoSelector\">"+
			"<div class=\"LabelSelector\">"+
			"<div class=\"LineaSelector\">"+
				"<a class=\"BotonGuardar\" href=\""+hash+"\">Guardar</a>"+
			"</div>"+
			"<div class=\"LineaSelector\">"+
				"<a class=\"BotonCancelar\" href=\""+hash+"\">Cancelar</a>"+
			"</div>"+
		"</div>";
		
		return str;
	}; // getHTMLBotonGuardar


	/**************************************************************************
	 * getHTMLCampo
	 * Genera dinámicamente el código de formulario HTML para un campo del registro 
	 * 
	 * - Titulo: label del campo
	 * - Nombre: nombre interno del campo
	 * - Valor: valor del campo
	 * - Tipo: cadena que identifica el tipo de registro
	 * - TablaRelacionada: cadena que identifica la tabla si se trata de un elemento 'select'
	 * o 'Selector'. 
	 * - UtilizarSelector: booleano que indica para un campo con tabla relacionada si hay que utilizar
	 * el select o el Selector.
	 * - Valores: En el caso de un elemento 'select' se le pasa el array de valores a rellenar.
	 *************************************************************************/
	var getHTMLCampo=function(campo, pos, idSelector, req)
	{
	  
    var Titulo= campo.etiqueta;
    var Nombre = campo.nombre;
    var Valor = campo.valor;
    var Tipo = campo.tipo;
    var TablaRelacionada = campo.tabla_relacionada;
    var UtilizarSelector = campo.utilizar_selector;
    var Valores = campo.valores;
    var solo_lectura = campo.solo_lectura;
    

		var _TEXT	="string";
		var _TEXTAREA	="text";
		var _DATE	="date";
		var _INTEGER 	="integer";
		var _REAL	="real";
		var _IMG	=4;
		var _BOOLEAN	="boolean";

		if(Valor=='undefined' || Valor==undefined)
		{
			Valor='';
		}
		
		var soloLectura='';
		if(solo_lectura)
		{
			soloLectura='disabled="true"';
		}
		
		var requerido=' requerido = "'+req+'"';
		
		
		var primerRegistro='';
		if(pos==1)
		{
			primerRegistro='primerRegistro';
		}
		
		switch(Tipo)
		{
			case _BOOLEAN:
			{
				if(Valor.toLowerCase()=='true')
				{
					Valor='Checked';					
				}
				else
				{
					Valor='';	
				}
				
				str=	"<div class=\"LabelSelector\"";
				if(req) str+=" style='font-weight:bold' ";
				str+=">"+Titulo+":</div>"+
						"<div class=\"LineaSelector\"><input type=\"checkbox\" "+soloLectura+"class=\"ValorCampo Boolean "+primerRegistro+"\" name=\""+Nombre+"\" tipo=\"boolean\" "+Valor+" /></div>";

				break;
			}
			case _REAL:
			{
				str=	"<div class=\"LabelSelector\">"+Titulo+":</div>"+
						"<div class=\"LineaSelector\"><input type=\"text\" "+soloLectura+"class=\"ValorCampo Texto "+primerRegistro+"\" name=\""+Nombre+"\" tipo=\"real\" value=\""+Valor+"\" /></div>";
				break;
			}
			default:
			case _TEXT:
			{
				str=	"<div class=\"LabelSelector\">"+Titulo+":</div>"+
						"<div class=\"LineaSelector\"><input "+soloLectura+requerido+" tipo=\"text\" type=\"text\" class=\"ValorCampo Texto "+primerRegistro+"\" name=\""+Nombre+"\" value=\""+Valor+"\" /></div>";					
				break;
			}
			case _TEXTAREA:
			{
				str=	"<div class=\"LabelSelector\">"+Titulo+":</div>"+
						"<div class=\"LineaSelector\"><textarea class=\"AreaTexto ValorCampo "+primerRegistro+"\" tipo=\"text\" name=\""+Nombre+"\" "+soloLectura+requerido+" >"+Valor+"</textarea></div>";
							
				break;
			}
			case _DATE:
			{
				var claseFecha=(solo_lectura? '' : 'Fecha');

				str=	"<div class=\"LabelSelector\">"+Titulo+":</div>"+
						"<div class=\"LineaSelector\"><input "+soloLectura+" tipo=\"date\" class=\""+claseFecha+" ValorCampo Texto "+primerRegistro+requerido+"\" type=\"text\" name=\""+Nombre+"\" value=\""+Valor+"\" /></div>";
		
				break;
			}
			case _IMG:
			{
				str=	"<div class=\"LabelSelector\">"+Titulo+":</div>"+
						"<div class=\"ValorSelector\">"+
						"<div><img src=\"/neptuno/sw/personalSW.py/foto?id="+Valor+"\"></img></div>"+
						"<form enctype=\"multipart/form-data\" method=\"post\" action=\"/neptuno/sw/personalSW.py/editar\" >"+
						"<input type=\"file\" name=\""+Nombre+"\" />"+
						"<input type=\"hidden\" name=\"id\" value=\""+Valor+"\" />"+
						"<input type=\"submit\" value=\"Guardar\" />"+
						"</form>"+
						"</div>";
				break;
			}
 			case _INTEGER :
			{ 
				if (TablaRelacionada != undefined) {
					if (UtilizarSelector == 'true') 
					{
						var propiedadSoloLectura=(solo_lectura? "solo_lectura=\"true\" " : "");

            str=  "<div class=\"LabelSelector\"";
            if(req) str+=" style='font-weight:bold' ";
            str+=">"+Titulo+":</div>";						

            var camposReferencia = JSON.stringify(campo.campos_referencia);
          
            str+="<div class=\"LineaSelector\">";
						str+="<div tipo='selectorEnder' class='selector ValorCampo' id='"+campo.nombre+"' titulo='"+campo.titulo+"' valor='"+campo.valor+"' tabla='"+TablaRelacionada+"'nombre='"+campo.nombre+"' camposReferencia='"+camposReferencia+"'></div>";
            str+="</div>";
						//str="<span name=\""+idSelector+"_"+Nombre+"\"><div class=\"LineaSelector\"><div class=\"ValorCampo Selector "+primerRegistro+"\" tipo=\"selector\" titulo=\""+Titulo+"\" campo=\""+Nombre+"\" idSeleccionado=\""+Valor+"\" tabla=\""+TablaRelacionada+"\" "+propiedadSoloLectura+" id=\""+idSelector+"_"+Nombre+"\" ocultaacciones=\"true\" ></div></span>";
					} 
					else 
					{
						// poner un select						
						if(solo_lectura)
						{
							soloLectura='disabled';
						}
						
						str=	"<div class=\"LabelSelector\"";
						if(req) str+=" style='font-weight:bold' ";
						str+=">"+Titulo+":</div>"+
								"<div class=\"LineaSelector\"><select "+soloLectura+" class=\"ValorCampo "+primerRegistro+"\" tipo=\"integer\" name=\""+Nombre+"\">";

						$(this).logconsola.MostrarObjeto(Valores);

						var NValores=Valores.length;

						if(req != true) str+="<option value=\"null\">ninguno</option>";

						for(var indiceValores=0;indiceValores<NValores;indiceValores++)
						{
							var NPropiedades=Valores[indiceValores].length;
							for(var indicePropiedades=0;indicePropiedades<NPropiedades;indicePropiedades++)
							{
								var _etiqueta	=Valores[indiceValores][indicePropiedades].etiqueta;
								var _nombre		=Valores[indiceValores][indicePropiedades].nombre;
								var _valor		=Valores[indiceValores][indicePropiedades].valor;

								switch(_nombre)
								{
									case "id":
									{
										 var valorFinal=_valor;
										 break;
									}
									case "nombre":
									{
										var etiquetaFinal=_valor;
										break;
									}
								} 
							} // Recorriendo las propiedades
							
							if(Valor==valorFinal)
							{
								str+="<option value=\""+valorFinal+"\" selected>"+etiquetaFinal+"</option>";
							}
							else
							{
								str+="<option value=\""+valorFinal+"\">"+etiquetaFinal+"</option>";
							}

						} // Recorriendo los objetos

						
						str+="</select>";
						
						// TODO: Habilitar la opción de añadir campo
						/*
						str+="<div class=\"addCampo Boton\">A&ntilde;adir campo</div>";
						str+="</div>";*/
					}
				}
				else 
				{
					str=	"<div class=\"LabelSelector\">"+Titulo+":</div>"+
							"<div class=\"LineaSelector\"><input type=\"text\" class=\"ValorCampo Texto "+primerRegistro+"\" name=\""+Nombre+"\" tipo=\"integer\" value=\""+Valor+"\" /></div>";					
				}
			}
			break;
		}
			
		str="<div class=\"CampoSelector\">"+str+"</div>";
		
		return str;			

	}; // getHTMLCampo

	/**
	 * @function desactivaSeleccion
	 */	
	$.fn.desactivaSeleccion=function()
	{
		
		$(this).find('.ColumnaSeleccionar').unbind('click');
		$(this).find('.ColumnaSeleccionar').css('text-decoration', 'None');
		$(this).find('.ColumnaSeleccionar').find('.Boton').removeClass('Boton');
	}; // desactivaSeleccion

	/**************************************************************************
		Selector::$.fn.DevolverLista
		  
		Hace que el selector muestre automáticamente el conjunto de resultados
		de una búsqueda en la tabla. 
		  
		- campofiltrado: campo de la tabla por el que filtramos
		- valorfiltrado: valor correspondiente 
	 *************************************************************************/	
	$.fn.DevolverLista = function(campofiltrado, valorfiltrado, actualizaAccionesResultados) 
	{
		$(this).find(".ResultadoBusqueda").find(".resultados").html('<img src="./images/loader.gif"></img>');
		
		
		$(this).Log("DevolverLista");
		var selector = $(this);

		var ResultadoBusqueda 	= selector.find('.ResultadoBusqueda:first');
		var nombretabla = selector.attr('tabla');
		var usuarioNeptuno=neptuno.obtenerusuarioNeptuno();
		
		var webservice=neptuno.getAttrData(selector.attr("id"), "webservice");
		var pos=parseInt(neptuno.getAttrData(selector.attr("id"), "pos"));
		var maxResults=neptuno.getAttrData(selector.attr("id"), "maxResults");
		var campos=neptuno.getAttrData(selector.attr("id"), "campos");
		var orderbyid=neptuno.getAttrData(selector.attr("id"), "orderbyid");

		// Procesamos los parámetros internos del selector
		orderbyid=(orderbyid ? 'True' : 'False');
		
		if(campos==null || campos=="")
		{
			// Mantenemos la compatibilidad con el sistema antiguo
			var campos='[["'+campofiltrado+'", "'+valorfiltrado+'" ]]';
		}
		
		if(webservice==null || webservice=="")
		{
			// Solo añadimos el parámetro que indica el número de resultados,
			// la primera vez.
			
			 
			var n_resultados=(pos==0? '?numero_resultados=true' : '');
			webservice='/neptuno/sw/buscar.py'+n_resultados;
		}
		else
		{
			// Solo añadimos el parámetro que indica el número de resultados,
			// la primera vez.
			
			if(pos==0)
			{
				//webservice += '&numero_resultados=true';
			}
			
		}

		// Hacemos la llamada
		$('*').css('cursor','wait');
		var campofiltrado = selector.attr('campofiltrado');
		if(campofiltrado != null)
		{
			var valorfiltrado = selector.attr('valorfiltrado');
			
			$.get(webservice,
			{
				campos:campos, 
				tabla: nombretabla, 
				id_usuario:usuarioNeptuno.id, 
				id_sesion:usuarioNeptuno.challenge,
				campofiltrado:campofiltrado,
				valorfiltrado:valorfiltrado,
				limite_resultados: maxResults,
				pos: pos,
				orderbyid:orderbyid
			},
			function(respuesta)
			{
				ProcesarResultadoBusqueda(selector, respuesta, (pos==0), actualizaAccionesResultados);
				$('*').css('cursor','');
			}); 
		
		}
		else
		{
			$.get(webservice,
			{
				campos:campos, 
				tabla: nombretabla, 
				id_usuario:usuarioNeptuno.id, 
				id_sesion:usuarioNeptuno.challenge,
				limite_resultados: maxResults,
				pos: pos,
				orderbyid:orderbyid
			},
			function(respuesta)
			{
				ProcesarResultadoBusqueda(selector, respuesta, (pos==0), actualizaAccionesResultados);
				$('*').css('cursor','');
			}); 
		}
	}; // DevolverLista


	/**************************************************************************
	 * Selector::$.fn.EditarRegistro 
	 *************************************************************************/	
	$.fn.EditarRegistro = function() 
	{
		var usuarioNeptuno=neptuno.obtenerusuarioNeptuno();
		var onEdit=neptuno.getAttrData($(this).attr("id"), "onEdit");
		
		
		
		$(this).Log("Editar registro");
		return this.each(function()
		{ 
			var a=randomString(5);
			var selector = $(this);
			var idSelector=selector.attr("id");
			
			selector.find('.AccionActiva').html('');

			var parametrosEdicion;

			propiedades.campospordefecto = neptuno.getAttrData(idSelector, "campospordefecto");
			propiedades.valorespordefecto = neptuno.getAttrData(idSelector, "valorespordefecto")
			if(propiedades.campospordefecto != null)
			{
				
				var param = "parametrosEdicion = {	tabla:selector.attr('tabla'),";
					param+= "id: selector.find('.AccionActiva').attr('idRegistro'),"; 
					param+=" id_usuario:usuarioNeptuno.id,"; 
					param+=" id_sesion:usuarioNeptuno.challenge,";
					for(var i = 0; i<propiedades.campospordefecto.length; i++)
					{
						param+= propiedades.campospordefecto[i]+":'"+propiedades.valorespordefecto[i]+"'";						
					}


					param+=" };";
				eval(param);
				
			}
			else
			{
				parametrosEdicion = {	tabla:selector.attr('tabla'),
					id: selector.find('.AccionActiva').attr('idRegistro'), 
					id_usuario:usuarioNeptuno.id, 
					id_sesion:usuarioNeptuno.challenge
				};
			}
			$.get('/neptuno/sw/datosRegistro.py?a='+a,
				parametrosEdicion,			
				function(respuesta)
				{					
					eval('var registro = '+respuesta);
					
					var ExisteAlgunoSoloLectura=false;
					
					selector.find('.AccionActiva').html('');
					selector.find('.AccionActiva').append(getHTMLBotonGuardar(idSelector));
					
					var nRegistro=registro.length;
					
					for(i=0;i<nRegistro;i++)
					{
						var campo=registro[i];
						if(campo.nombre!="id")
						{
							var html="";
							
							if(campo.solo_lectura)
							{
								ExisteAlgunoSoloLectura=true;
							}
							
							html+=getHTMLCampo(campo, i, idSelector, campo.requerido);
							selector.find('.AccionActiva').append(html);								
							selector.find('[requerido=true]').parent().siblings('.LabelSelector').css('font-weight','bold');
						}
					}
					
					if(ExisteAlgunoSoloLectura)
					{
						$(this).MuestraMensaje("No dispone de privilegios de escritura en algunos de los campos...");
					}

					// Inicializamos los campos de tipo selector
					selector.find('.AccionActiva').find('.selector').each(function()
					{	
						var idSeleccionado=$(this).attr('idSeleccionado');
						
						if (idSeleccionado == 'None')
						{
   							idSeleccionado = '-1';
						}
						
						var tabla=$(this).attr('tabla');
						var debug=$(this).attr('debug');
						console.log('a');
						var camposReferencia= JSON.parse($(this).attr('camposReferencia'));
						
						camposReferencia = camposReferencia.join('+')
						
						$(this).selectorEnder(
                                    {"valor":$(this).attr('titulo'), "id":$(this).attr('valor')},
                                    tabla,
                                    '',
                                    camposReferencia,
                                    neptuno.obtenerusuarioNeptuno()
                                    );
						
						
						/*$(this).Selector(
							{ idSeleccionado: idSeleccionado,
								tabla: tabla,
								debug: debug,
								botonCrear:true
							});*/						 
					});

					selector.find('.AccionActiva').append(getHTMLBotonGuardar());
					selector.find('.Fecha').datepicker(
					{
						dateFormat: 'dd/mm/yy', 
						firstDay: 1,
						dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
						dayNames: ['Domingo', 'Lunes', 'Martes', 'Mi&eacute;rcoles', 'Jueves', 'Viernes', 'S&aacute;bado'],
						monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],								
						yearRange: '1900:2050',
						changeMonth: true,
						changeYear: true,
						showOn: 'button'																		
					});

					selector.find('.BotonGuardar').unbind('click');
					selector.find('.BotonGuardar').bind('click',GuardarRegistro);
					selector.find('.BotonCancelar').unbind('click');
					selector.find('.BotonCancelar').bind('click',CancelarGuardarRegistro);
					
					// Acción para el botón de crear registro debajo de los selects
					selector.find('.addCampo').unbind('click');
					selector.find('.addCampo').bind('click', addCampo);
					
					// Por último asignamos el focus
					selector.find('.primerRegistro').focus();
					
					if(onEdit)
					{
						onEdit();
					}
					neptuno.posicionaAccionActiva( selector.find('.AccionActiva') );
				}
			);

			selector.find('.AccionActiva').fadeIn();
		})

	}; // EditarRegistro


	/**
	 * En el modo edición guarda el registro actual de la tabla. 
	 * @function $.fn.GuardarRegistro
	*/
	$.fn.GuardarRegistro = function()
	{
		if( $(this).hasClass('Selector') )
		{
			var selector=$(this);
		}
		else if( $(this).parent().hasClass('Selector') )
		{
			var selector=$(this).parent();			
		}

		var idRegistro=selector.find('.AccionActiva').attr("idregistro");
		var tabla=selector.attr("tabla");
	
		if (idRegistro != '-1') 
		{
			var objeto={"id": idRegistro};
		} 
		else 
		{ 
			var objeto = {};
		}
		
		var pos=0;
	
		var requeridos_vacios = '';
	
		selector.find(".ValorCampo").each( function(campo)
		{
      		
				jQuery(this).css('background-color','');
			
				if(jQuery(this).attr('requerido')=='true') 
				{
					if (jQuery(this).val() == '') 
					{
						jQuery(this).css('background-color', '#FFAAAA');
						if (requeridos_vacios == '') 
							requeridos_vacios = jQuery(this).parent().siblings('.LabelSelector').html();
						else 
							requeridos_vacios += ', ' + jQuery(this).parent().siblings('.LabelSelector').html();
					}
				}
				else
				{
					
				}
			//if ($(this).parent().parent().parent().parent().attr('id') == selector.attr('id')) 
      		//{
				var tipo	=$(this).attr('tipo');
				var valor	=$(this).attr('value');
				var valor_checkbox=new String($(this).attr('checked'));
				var valorDefinido= (valor!= '') && (valor!="None") && (valor!=undefined);
				
				switch( tipo )
				{
					case 'selectorEnder':
					{
		/*			  var valorSelector = $(this).attr('value');
					  if(valorSelector == undefined) valorSelector = -1;
					  objeto[$(this).attr('id')] = 1*valorSelector;*/
					  
            if( $(this).attr('idSeleccionado')<0)
            {
              // Selector vacío
              objeto[$(this).attr('id')] = 'null';
            }        
            else if (($(this).attr('idSeleccionado') > 0)  && ($(this).attr('idSeleccionado')!=undefined)) 
            {
              // Selector con id seleccionado
              objeto[$(this).attr('id')] = $(this).attr('idSeleccionado');
            }					  
					  
					  break;
					}
					case 'boolean':
					{
						if(valor_checkbox.toLowerCase()=='true')
						{
							objeto[$(this).attr('name')] = 'True';
						}
						else
						{
							objeto[$(this).attr('name')] = 'False';
						}
						
						break;
					}
					case 'real':
					{
						// El caso integer y real se tratan de forma similar, por eso
						// no hay un 'break'. Únicamente se sustituye la coma por el punto
						// si fuera necesario: http://bean.ender.es/mantis/view.php?id=4800
						var valorReal=$(this).attr('value');
						$(this).attr('value', $(this).attr('value').replace(',','.') );
					}
					case 'integer':
					{
						if( !valorDefinido )
						{
							objeto[$(this).attr('name')] = 0;						
						}
						else
						{
							objeto[$(this).attr('name')] = $(this).attr('value');						
						}
						
						break;
					}
					case 'date':
					case 'text':
					{
						if( !valorDefinido )
						{
							objeto[$(this).attr('name')] = 'null';		
						}
						else
						{
							objeto[$(this).attr('name')] = $(this).attr('value');
						}
						
						break;
					}
					case 'selector':
					{
						if( $(this).find('.busqueda').val()=='' || $(this).attr('idSeleccionado')=='-1')
						{
							// Selector vacío
							objeto[$(this).attr('campo')] = 'null';
						}				 
						else if (($(this).attr('idSeleccionado') != '') && ($(this).attr('campo') != '') && ($(this).attr('campo')!=undefined) && ($(this).attr('idSeleccionado')!='-1')) 
						{
							// Selector con id seleccionado
							objeto[$(this).attr('campo')] = $(this).attr('idSeleccionado');
						}
						
						break;
					}
				} // switch
			//} // Guardamos únicamente los campos del selector abierto

		});
		
		
		if(requeridos_vacios == '')
		{
			$(this).Log("Guardando registro..."+idRegistro+" => "+toString(objeto) );
			
			
			var usuarioNeptuno=neptuno.obtenerusuarioNeptuno();
			
			
			
			
			cursorEspera();
			
			$.ajax({ type:'POST',
				url:'/neptuno/sw/guardarRegistro.py',
				data:{
					datos:toString(objeto), 
					tabla:tabla,
					id_usuario:usuarioNeptuno.id, 
					id_sesion:usuarioNeptuno.challenge
				},
				cache:false,
				success:function(resultado)	
				{
					// Limpiamos los campos
					selector.find('.AccionActiva').html("");
					selector.find('.AccionActiva').fadeOut();
					endcursorEspera();
					
					selector.MuestraMensaje("Registro guardado");
					selector.Log("Registro guardado correctamente");
					
					if(idRegistro!=-1)
					{
						selector.AsignarRegistro(idRegistro);
					}
					else
					{
						eval('var cod_nuevoRegistro='+resultado);
	
						if(cod_nuevoRegistro>0)
						{
							var onReadyCreate=neptuno.getAttrData(selector.attr('id'), "onReadyCreate");
	
							if( onReadyCreate!=null )
							{
	
								onReadyCreate(cod_nuevoRegistro, objeto);
							}
							else
							{
								selector.AsignarRegistro(cod_nuevoRegistro);
							}
						}
					}
				},
				error: function(resultado)
				{
					endcursorEspera();
					selector.MuestraMensajeError(resultado, "Error guardando registro");
					selector.LlamadaIncorrecta(resultado);
				}
				});
			
		}
		else
		{
			//selector.Log
			$(this).MuestraMensaje("Los campos "+requeridos_vacios+" son requeridos" );
		}
		

	}; // GuardarRegistro


	/**************************************************************************
	 * Selector::$.fn.MostrarMensaje
	 *
	 * - texto: texto del mensaje a mostrar
	 *************************************************************************/
	 $.fn.MostrarMensaje=function(texto, titulo)
	 {
	 	if(titulo)
	 	{
	 		$(idDialogo).attr('title')=titulo;
	 	}

	 	var idDialogo='#Dialogo'+$(this).attr('id');
	 	$(idDialogo).html(texto);
	 	
	 	neptuno.inicializaDialogo(idDialogo, titulo);	 	
	 	$(idDialogo).dialog('option', 'buttons', 
	 	{ 
	 		"Aceptar": function() 
	 		{ 
	 			$(this).dialog("close"); 
	 		}
	 	});
	 	
	 	$(idDialogo).dialog('open');
	 }; // MostrarMensaje


	/**************************************************************************
	 * Selector::$.fn.Log
	 *
	 * - texto: texto del mensaje a mostrar
	 *************************************************************************/
	$.fn.Log=function(texto)
	{
		$(this).logconsola.Debug=false;
		$(this).logconsola.BloqueInicio="(#"+$(this).attr("id")+") ";
		$(this).logconsola.Log(texto);		
	}; // Log
	
	
	/**************************************************************************
	 * Selector::$.fn.LlamadaIncorrecta
	 *
	 * Función invocada desde la propiedad 'error' dentro de una llamada $.ajax.
	 * Se encarga de devolver un mensaje en función del código de error que se 
	 * ha generado.
	 *************************************************************************/
	$.fn.LlamadaIncorrecta = function(xhr)	
	{
		var CodigoErrorHTTP=parseInt(xhr.status);
		var TextoAMostrar='';

		$(this).Log("*** LlamadaIncorrecta, código de error "+CodigoErrorHTTP);
				
		switch(CodigoErrorHTTP)
		{
			case 403: // Forbidden
			{
				TextoAMostrar='Forbidden'
				break;
			}
			case 404: // Usuario no encontrado
			{
				TextoAMostrar='Service not found';
				break;
			}
			case 406:
			{
				TextoAMostrar='Not Acceptable';
				break;
			}
			case 409:
			{
				TextoAMostrar='El objeto ya existe en la base de datos';
				break;
			}
			default: // Error interno
			{
				TextoAMostrar='Internal server error';
				break;			
			}
		} // switch CodigoErrorHTTP
				
		$(this).MostrarMensaje(TextoAMostrar);

	}; // LlamadaIncorrecta

		
	/**************************************************************************
	 * Selector::$.fn.AsignarRegistro
	 *
	 * Asigna un registro al selector, muestra los detalles y las acciones asociadas
	 * a la tabla.
	 * 
	 * - idSeleccionado: recibe el identificador a asignar.
	 *************************************************************************/
	$.fn.AsignarRegistro = function(idSeleccionado)
	{

		var selector=$(this);		
		var usuarioNeptuno=neptuno.obtenerusuarioNeptuno();
		var datosNavegacion=neptuno.obtenerDatosNavegacion();
		var actionsbox=selector.find(".Seleccionado:first");
		var searchresults=selector.find('.ResultadoBusqueda:first');
		var cajabusqueda=selector.find(".CajaBusqueda:first");

		// datos de navegacion
		if(selector.attr('tabla')==datosNavegacion.clase)
		{	
			neptuno.setNavegacion(datosNavegacion.clase, idSeleccionado, datosNavegacion.accion, datosNavegacion.modo);
		}

		selector.Log('AsignarRegistro id: '+idSeleccionado);
		selector.logconsola.IniciaTemporizador("AsignarRegistro");
		
		// Para cargar los resultados siempre llama a buscar.py
		if(idSeleccionado != '-1' && idSeleccionado!='' && idSeleccionado!='undefined') 
		{
			selector.attr('idSeleccionado', idSeleccionado);
			
			// En estos campos almacenamos los parámetros para la creación de la caja de acciones
			var campos=[];
			var acciones='';
			var CAMPOi=0;

			// Obtenemos los valores a mostrar en la caja de acciones
			$.ajax({ type:'GET',
				data:
				{
					id:selector.attr('idSeleccionado'), 
					tabla:selector.attr('tabla'), 
					id_usuario:usuarioNeptuno.id, 
					id_sesion:usuarioNeptuno.challenge,
					limite_resultados:1
				},		
				async:false,
				cache:false,
				url:'/neptuno/sw/buscar.py',
				success:function(respuesta) 
				{	
					
					eval('var registro = '+respuesta);
					var ncampos=registro.numero_resultados;
					var PrimerValor="";
					var cabeceras = registro.columnas;

					for(var i=0;i<ncampos;i++)
					{
					
						var campoActual=registro.datos[i];
						for(var j = 0;j<campoActual.length;j++)
						{
						
							var clave = cabeceras[j];
							var valor = campoActual[j]
							if(clave!="id")
							{
								var campo={};
								campo.label=clave;
								campo.value=valor;
								campo.nohidden=false;
								campos[CAMPOi]=campo;							
								CAMPOi++;
								
								if(PrimerValor=="")
								{
									PrimerValor=campo.value;
								}
							}
						} 
					} // recorremos los valores
					
					
					cajabusqueda.find(".busqueda").val(PrimerValor);
					
					if(neptuno)
					{
						var acciones_ocultar=neptuno.getAttrData($(this).attr("id"), "acciones_ocultar");
					}
					
					// Obtenemos las acciones
					if( selector.attr('ocultaacciones')!='true' )
					{
						$.ajax({
							url: "./acciones/"+selector.attr('tabla')+".htm", 
							async:false,
							cache:false,
							type: "POST",
							success:function(acciones)
							{
								// Construimos la caja de acciones
								var fullScreen=(neptuno.getAttrData(selector.attr('id'), "modo")=="full");
								
								actionsbox.actionsbox(
								{
									htmlactions:acciones, 
									campos: campos,
									id: idSeleccionado,
									accionesocultar: acciones_ocultar,
									loadactions: (selector.attr('cargaacciones')=="true"),
									load: "CargaAcciones"+selector.attr('tabla'),
									showdetails: MostrarDetalles,
									fullScreen: fullScreen
								});
								
								
								primervalor=PrimerValor;								
								selector.attr('primervalor', primervalor);	
								selector.find('.navegacionResultados').fadeOut();							
							}
						});
					}
					
					/**********************************************
					* Nueva funcionalidad, permite añadir acciones
					* por parámetro.
					* Siguiendo la estructura de un objeto de acciones:
					*
					* actions[0...n]
					* actions[i].onAction 	=> función a ejecutar.
					* actions[i].label	=> etiqueta a mostrar.
					**********************************************/
					var acciones=neptuno.getAttrDataObject(selector.attr("id"), "actions");								
								
					if(acciones!=null)
					{
						var bloqueAcciones=actionsbox.find('.Acciones');
						var htmlAction='';
						var action=null;
						var nAcciones=acciones.length;
						
						for(ACCIONi=0;ACCIONi<nAcciones;ACCIONi++)
						{
							action=propiedades.actions[ACCIONi];
							htmlAction='<div class=\"Accion Action\"><a href=\"#\">'+action.label+'</a></div>';
							bloqueAcciones.append(htmlAction);
							
							bloqueAcciones.find('.Action').unbind();
							bloqueAcciones.find('.Action').bind('click', action.onAction);										
						} // Recorremos las acciones
					}							
				} // success
			});  // ajax
		}
		
		// Muestra el valor registro vacío, por ejemplo cuando se borra 
		// llamamos a esta función asignándole -1.
		if( idSeleccionado== -1 || idSeleccionado==null)
		{
			cajabusqueda.find(".busqueda").val("");
		}
		
		// Actualizamos los datos de navegación si estamos en el selector principal
		if( selector.hasClass('selectorPrincipal') )
		{
			var nav=neptuno.obtenerDatosNavegacion();
			neptuno.setNavegacion(nav.clase, idSeleccionado, '', '');
		}
		
		searchresults.fadeOut();
		selector.logconsola.FinalizaTemporizador("AsignarRegistro");
		
	}; // AsignarRegistro	
	
	
	/**************************************************************************
	 Selector::$.fn.addCampo
	**************************************************************************/	 
	$.fn.addCampo = function(tabla, labelCampo)
	{
	 	var idDialogo='#Dialogo'+$(this).attr('id');
	 	neptuno.inicializaDialogo(idDialogo, "Creaci&oacute;n de campos en la tabla "+tabla);
	 	
		$.ajax({
			url: "/neptuno/libjs/jquery_ender_selector/modulos/SelectorDefault.htm", 
			async : false,
			cache:false,
			success:
				function(respuesta)
				{
					$(idDialogo).html(respuesta);
					
					var datosNavegacion=neptuno.obtenerDatosNavegacion();
					var id=datosNavegacion.id;
			
					$('#selectorDefault').Selector(
						{ idSeleccionado: '-1',
							tabla: tabla,
							debug: true,
							titulo: labelCampo,
							contenedorMensajes:neptuno.cntMsgs,
							botonCrear:true							 
						 });							 
				}
			});

	 	$(idDialogo).dialog('option', 'buttons',
	 	{
			"Cancelar": function()
			{
				$(idDialogo).dialog('close');
			},
			"Aceptar": function() 
			{ 
				// Cargamos el contenido
				$(idDialogo).dialog('close');
			}
		});
		
		$(idDialogo).dialog('open');
		
	}; // addCampo

})(jQuery);


//////////////////////////////////////////////////////////////////////////
//// Funciones externas para utilizar con bind
//////////////////////////////////////////////////////////////////////////


/**************************************************************************
 * addCampo
 *************************************************************************/
function addCampo()
{
	var idCampo		=$(this).parent().find('.ValorCampo').attr('name');
	// hemos de obtener 'sexos' a partir de 'id_sexos_sexo'
	var tabla=idCampo.split("_");
	tabla=tabla[1];
	
	var labelCampo	=$(this).parent().parent().find('.LabelSelector').html();
	// Le hemos de quitar ':' a la etiqueta
	labelCampo=labelCampo.replace(/:/, "");
	
	$(this).parent().parent().parent().parent().Log("addCampo");
	$(this).parent().parent().parent().parent().addCampo(tabla, labelCampo);		
} // GuardarRegistro


/**************************************************************************
 * GuardarRegistro
 *************************************************************************/
function GuardarRegistro()
{
	$(this).parent().parent().parent().parent().parent().GuardarRegistro();	
} // GuardarRegistro
	
	
/**************************************************************************
 * @function CancelarGuardarRegistro
 *************************************************************************/
function CancelarGuardarRegistro()
{
	$(this).parent().parent().parent().parent().parent().find('.AccionActiva').fadeOut();
	$(this).parent().parent().parent().parent().parent().find('.AccionActiva').html('');
} // CancelarGuardarRegistro


/**************************************************************************
 * Devuelve la cadena json correspondiente a un objeto.
 * @function toString
 * @param {Object} objeto
 *************************************************************************/
function toString(objeto)
{
  texto = '{';
	for (propiedad in objeto)
	{	
    if (texto != '{') {
     texto += ',';
    }
		// Reemplazamos las comillas
		var CadenaValor=new String(objeto[propiedad]);
		CadenaValor = CadenaValor.replace(/\\/g, '\\\\');
		CadenaValor = CadenaValor.replace(/\"/g, '\\"');
		CadenaValor = CadenaValor.replace(/\n/g, '\\n');
		CadenaValor = CadenaValor.replace(/\t/g, '\\t');		
		CadenaValor = CadenaValor.replace(/\//g, '\\/');				
		
		// TODO: Revisar(tipos)
		if(CadenaValor=='null')
		{
			texto += '"'+propiedad+'": null';
		}
		else
		{
			texto += '"'+propiedad+'": "'+CadenaValor+'"';
		}
	}
  texto += '}';
  return texto;
} // toString


/**************************************************************************
 * MostrarDetalles
 * 
 * Muestra u oculta los detalles del registro seleccionado.
 *************************************************************************/
function MostrarDetalles() 
{
	seleccionado = $(this).parent().parent();
	seleccionado.Log("Llamada externa a MostrarDetalles, oculto="+ seleccionado.find('.Detalles').attr('oculto') );
	
	if( !seleccionado.find('.Detalles').attr('oculto') || seleccionado.find('.Detalles').attr('oculto')=='true') 
	{
		// Los detalles están ocultos
		seleccionado.find('.Detalles').html("ocultar detalles");
		seleccionado.find('.LineaOcultableSeleccionado').fadeIn();
		seleccionado.find('.Acciones').fadeIn();
		seleccionado.find('.Detalles').attr('oculto','false');
	}
	else
	{
		// Estamos mostrando los detalles
		seleccionado.find('.Detalles').html("mostrar detalles");
		seleccionado.find('.LineaOcultableSeleccionado').fadeOut();
		seleccionado.find('.Acciones').fadeOut();
		seleccionado.find('.Detalles').attr('oculto','true');
	} 

} // MostrarDetalles