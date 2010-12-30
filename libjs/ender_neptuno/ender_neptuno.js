/*******************************************************************************
* @author desarrollo@ender.es
* @module neptuno.ender
*******************************************************************************/

if(!console)
{
  var console = {};
  console.log = function(){};
}


/*******************************************************************************
* @class ControladorNeptuno
*******************************************************************************/
function ControladorNeptuno()
{
	/**
	 * Propiedades del objeto Con
rolador Neptuno
	 **/
	this.Debug=false;
	this.cntMsgs=new contenedorMensajes();
	this.logconsola=null;
	this.utilizarURLBase=false;
	this.URLBase=null;
	this.Data=[];
	this.Actions=[];

	/*
	 * Esta variable va a determinar si hemos de cargar todas las librerías
	 * de neptuno o no.
	 **/
	this.loaded=false;
	
	/**************************************************************************
	* TODO: Esta función solo está planteada
	*	http://url/index.htm#clase:id:accion:modo:fecha=21/11/2009,alumno=39
	* - Añade un nuevo parámetro hash
	* La parte a tener en cuenta es 'fecha=21/11/2009,alumno=39' allí pasamos los
	* parámetros separados por comas.
	*
	* @function addParametroHash
	* @param {String} nombre - Nombre del parámetro
	* @param {String} valor - Valor
	**************************************************************************/
	this.addparametroHash=function(nombre, valor) {};

	/**************************************************************************
	* TODO: Esta función solo está planteada
	* Devuelve el valor de un parámetro hash
	* @function getparametroHash
	* @see #this.addparametroHash
	* @param {String} nombre - Nombre del parámetro hash a devolver
	* @returns {String} valor - Valor del parámetro hash
	**************************************************************************/
	this.getparametroHash=function(nombre) {};

	/**************************************************************************
	*  Guarda una función en el array de acciones
	* @function addAction
	* @param {function} f
	* @returns {Integer} identificador
	**************************************************************************/
	this.addAction=function(f)
	{
		var nactions=this.Actions.length;
		neptuno.Actions[nactions]=f;
		return nactions;
	}; // addAction
	
	/**************************************************************************
	* Recupera una acción del array de acciones
	* @function getAction
	* @param {Integer} i
	* @returns {function} funcion
	**************************************************************************/
	this.getAction=function(i)
	{
		if(neptuno.Actions && neptuno.Actions[i])
		{
			return neptuno.Actions[i];
		}
		else
		{
			return null;
		}
	}; // getAction

	
	/**************************************************************************
	 * Guarda un objeto en memoria
	* @function setAttrDataObject
	* @param {String} idParent - identificador del elemento padre del objeto
	* @param {String} id - identificador del objeto
	**************************************************************************/
	this.setAttrDataObject=function(idParent, id, obj)
	{
		neptuno.setAttrData(idParent, id, $.toJSON(obj));
	}; // setAttrDataObject

	/**************************************************************************
	* - Recupera un objeto de memoria
	* @function getAttrDataObject
	* @param {String} idParent - identificador del elemento padre del objeto
	* @param {String} id -identificador del objeto
	**************************************************************************/
	this.getAttrDataObject=function(idParent, id)
	{
		var str=neptuno.getAttrData(idParent, id);

		var obj=$.evalJSON(str);
		return obj;		
	}; // getAttrDataObject

	/**************************************************************************
	* - Recupera una variable de memoria asociada a un objeto
	* @function getAttrData
	* @param {String} idParent - identificador del elemento padre de la variable
	* @param {String} id - identificador de la variable
	* @returns {String} valor
	**************************************************************************/
	this.getAttrData=function(idParent, id)
	{
		if(neptuno.Data[idParent] && neptuno.Data[idParent][id]!=null)
		{
			//atenea.logconsola.Log("getAttrData "+idParent+" => "+id+" = "+atenea.Data[idParent][id]);
			return neptuno.Data[idParent][id];
		}
		else
		{
			//atenea.logconsola.Log("getAttrData "+idParent+" => "+id+" = null");
			return null;
		}
	}; // getAttrData

	/**************************************************************************
	* - Guarda una variable en memoria asociada a un objeto
  	* @function setAttrData
	* @param {String} idParent - identificador del elemento padre de la variable
	* @param {String} id - identificador de la variable
	* @param {String} value - valor a almacenar
	**************************************************************************/
	this.setAttrData=function( idParent, id, value )
	{
		if(!this.Data[idParent])
		{
			this.Data[idParent]=[];
		}
		
		this.Data[idParent][id]=value;
	}; // setAttrData
	
	/**************************************************************************
	* - Pasa una cadena a formato título.
	* Sustituye los espacios por pasa a mayúsculas la primera letra
	* @function ConvierteTitulo 
	* @param {String} Titulo
	*************************************************************************/	
	this.ConvierteTitulo=function(Titulo)
	{
		Titulo=Titulo.replace(/_/, " ");
		Inicial=Titulo.substr(0,1);
		Titulo=Inicial.toUpperCase()+Titulo.substr(1, Titulo.length);
		return Titulo;
	}; // ConvierteTitulo

	/***********************************************************************
	 * - Construye un objeto Date a partir de las cadenas
	 * de fecha y hora.
	 * Si no se le pasa la hora le aplica por defecto las 00:00
	 * @function getDate
	 * @param {String} fecha - Fecha en formato dd/mm/aaaa
	 * @param {optional String} hora - Hora en formato hh:mm
	 * @returns {Date} fecha
	***********************************************************************/
	this.getDate=function(fecha, hora)
	{
		if(!hora)
		{
			hora="00:00";
		}

		var _tmpFecha	=fecha.split("/");
		var _tmpHora	=hora.split(":");
		var toReturn=new Date(_tmpFecha[2], (_tmpFecha[1]-1), _tmpFecha[0], _tmpHora[0], _tmpHora[1]);
		
		return toReturn;		
	}; // getDate

	/***********************************************************************
	* - Activa los mensajes de consola
	* @function activaConsola 
	***********************************************************************/	
	this.activaConsola=function()
	{
		this.logconsola=new RegistroSapns();
		this.logconsola.Debug=true;
		this.logconsola.BloqueInicio="[neptuno] ";
	}; // activaConsola

	/**************************************************************************
	 * Le aplica el objeto datepicker a un elemento pasado
	 * @function cargaDatePicker
	 * por parámetro.
	 * @param {Object} input
	 * @param {Function} onSelect - Función a activar en caso del evento onSelect
	**************************************************************************/	
	this.cargaDatePicker=function(input, onSelect)
	{
		input.datepicker(
		{
			dateFormat: 'dd/mm/yy', 
			firstDay: 1,
			dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
			dayNames: ['Domingo', 'Lunes', 'Martes', 'Mi&eacute;rcoles', 'Jueves', 'Viernes', 'S&aacute;bado'],
			monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],								
			yearRange: '1900:2050',
			changeMonth: true,
			changeYear: true,
			onSelect: onSelect,
			showOn: 'button'									
		});
	}; // cargaDatePicker

	/**************************************************************************
	* - Actualiza el texto de horas por semana en el planner
	* @function actualizaTextoDuracionPlanner 
	* TODO: No debería estar aquí.
	**************************************************************************/	
	this.actualizaTextoDuracionPlanner=function()
	{
		var minutosSemana=parseInt($("#Planner").attr('minutossemana'));
		var textoSemana=parseFloat(minutosSemana/60);
		
		$("#Planner").parent().find('.TextoInformacionHorario').html("Horas semanales: "+textoSemana);	
	}; // actualizaTextoDuracionPlanner

	/**************************************************************************
	* - Carga el weekplanner en la página actual
	* @function Cargahorario 
	**************************************************************************/	
	this.Cargahorario=function()
	{
		load_css("./acciones/personal/horario.css");
		
		$('#selectorFecha').unbind('keyup');
		$('#selectorFecha').bind('keyup', function()
		{
			if (jQuery('#selectorFecha').val().length > 6) 
			{
				if (isValidDate(jQuery('#selectorFecha').val(), 'DMY')) {
					/*	$('#Planner').seleccionaFecha($('#selectorFecha').val());
					 $('#Planner').ActualizaEventos(RecibeDatos);
		 			$('#selectorFecha').val("");*/
					$('#selectorFecha').css('background-color', '#FFF');
					$('.avisoFechaErronea').remove();
				}
				else {
					$('#selectorFecha').css('background-color', '#FF9999');
				}
			}
			else 
			{
				$('#selectorFecha').css('background-color', '#FFF');
				$('.avisoFechaErronea').remove();
			}
		}); 
		
		$('.CerrarHorario').unbind('click'); 
		$('.CerrarHorario').bind('click', function()
		{
			$('.AccionActiva').html('');							
		});		
		
		$('.IrA').unbind('click');
		$('.IrA').bind('click', function()
		{
			if (isValidDate(jQuery('#selectorFecha').val(), 'DMY')) {
				if ($('#selectorFecha').val() != "") {
					$('#Planner').seleccionaFecha($('#selectorFecha').val());
					$('#Planner').ActualizaEventos(RecibeDatos);
					$('#selectorFecha').val("");
				}
			}
			else
			{
				neptuno.cntMsgs.Show("Formato de fecha erroneo");
			}
		});

		
		$('#selectorFecha').bind('keypress', function(event)
		{
			if(event.keyCode == 13)
			{
				$('.IrA').click();	
				
			}	
			
		}	
		);	
		
		$('.IrHoy').unbind('click');
		$('.IrHoy').bind('click', function()
		{
			$('#Planner').irHoy();
			$('#selectorFecha').val("");
		});
		
		$('.Imprimir').unbind('click');
		$('.Imprimir').bind('click', neptuno.imprimirHorario);

		// Le ponemos la fecha de hoy
		var fechaHoy=new Date();
		$('#selectorFecha').val(fechaHoy._toString());
		
		neptuno.cargaDatePicker($('#selectorFecha'), function a(fecha)
		{
			$('#Planner').seleccionaFecha(fecha);
			$('#Planner').ActualizaEventos(RecibeDatos);			
		});

		$('#Planner').Planner(
		{ 	
			onRequestFun:RecibeDatos,
			onRequestEditEvent:RecibeDatosEvento,				
			onRequestCreateEvent:CrearEvento,
			cellWidth:100,
			cellHeight:40,
			controller: weekPlannerController,
			onRequestUpdated: neptuno.actualizaTextoDuracionPlanner,
			onReady: function a()
			{
				// Posicionamos sobre el planner
				neptuno.posicionaAccionActiva( $('#Planner').parent().parent() );
				neptuno.actualizaTextoDuracionPlanner();
			}
		});
			 
		

	} // CargaHorario						

	
	/**************************************************************************
	* Posiciona el foco en el bloque pasado por parámetro.
	* @function posicionaAccionActiva 
	* @param {Object} bloque
	**************************************************************************/	
	this.posicionaAccionActiva=function(bloque)
	{
		if(bloque)
		{
			var offsetAlto=bloque.offset().top;
			$('html,body').animate({scrollTop: offsetAlto}, 700);
		}
	};

	/**************************************************************************
	* Genera la página de impresión
	* @function imprimirHorario
	* @param {Event} event
	**************************************************************************/	
	this.imprimirHorario=function(event)
	{
		var selector=$(this).parent().parent().parent();
		var busqueda=selector.attr('busqueda');
		var tabla=selector.attr('tabla');
		var etiqueta=selector.attr('primervalor');
		var miHTML=selector.find(".AccionActiva").html();

		var tituloHorario="";

		// Construimos el título del horario
		switch(tabla)
		{
			case 'personal':
			{
				tituloHorario="Horario del profesor "+etiqueta;
				break;
			}
			case 'grupos':
			{
				tituloHorario="Horario del grupo "+etiqueta;
				break;
			}
		}
		
		// Cargamos la plantilla de impresión
		$.get('./templates/imprimirHorario.htm',{},
		function(plantillaImpresion)
		{
			var ventimp = window.open();
			ventimp.document.write( plantillaImpresion );			
			ventimp.document.write( miHTML );
			ventimp.document.close();
			
			// Modificamos la posición de los eventos
			/*
			$.each( $(ventimp.document).find(".Event"), function a()
			{
				$(this).css('width', '100');
				
				var old_left=parseInt($(this).css('left'));
				
				var offsetDia=$(this).attr('offsetdia');
				
				if(offsetDia==0)
				{
					// Es el domingo
					var n=6;
				}
				else
				{
					var n=offsetDia;
					n--;
				}
				
				var new_left=old_left+(30*n);
				$(this).css('left', new_left);
			});*/
			
			$(ventimp.document).find("#CabeceraImpresion").html(tituloHorario);			
		});			

	}; // imprimirHorario

	/**
	 * TODO: pensar otra manera de hacer esto.
	 * @function traducirTablaClase
	 **/
	this.traducirTablaClase=function(nombreTabla)
	{
		var toReturn='';
		
		switch(nombreTabla)
		{
			default:
			{
				toReturn=nombreTabla;
				break;
			}
			case 'alumnos_en_grupos':
			{
				toReturn='alumnos';
				break;
			}
		}
		
		return toReturn;
	};

	/**
	* Carga la acción de abrir registro en nueva pestaña.
	* @function accionAbrir 
	* @param {Event} event 
	**/	
	this.accionAbrir=function(event)
	{
		
		var id=$(this).parent().attr('idseleccionadobusqueda');
		
		var tabla=$(this).parent().parent().parent().parent().attr('tabla');
		
		
		var url=new String(window.location, tabla+id);

		// le quitamos #
		url=url.split("#");
		tabla=neptuno.traducirTablaClase(tabla);
		var tipoEdicion = $(this).parent().parent().parent().parent().attr('tipoEdicion');
		if(tipoEdicion != null && tipoEdicion != 'null' && tipoEdicion != '') tabla = tipoEdicion;
		
		// activamos el modo fullscreen para el contentLoader
		url=url[0];
		url=url+"#"+tabla+':'+id;
		url=url+"::full";
		
		var caption=$(this).html();
		var html="<a href='"+url+"' target='_blank'>"+caption+"</a>";
		
		window.open(url,tabla+id, "directories:no,location=no,menubar=no,status=no,toolbar=no,width=800, height=600, resizable=no,titlebar=no,scrollbars=yes");
				
	}; // accionAbrir


	/**************************************************************************
	* - Lanza la acción de fusionar desde el selector pasado por parámetro.
	* El registro que va a desaparecer será el que seleccionemos, no el
	* que tengamos seleccionado en selectorDestino.
	* @function accionFusionar
	* @param {Object} selectorDestino - Selector que contiene el registro que
	* queremos fusionar.
	* @param {Object} bloque - Bloque donde vamos a cargar el template de fusionar
	**************************************************************************/	
	this.accionFusionar=function(selectorDestino, bloque)
	{
		var tabla=selectorDestino.attr('tabla');
		var idDestino	=selectorDestino.attr('idseleccionado');
		
		neptuno.logconsola.Log("atenea::accionFusionar => "+tabla+" "+idDestino);
		
		// Cargamos los html y css correspondiente
		load_css("/neptuno/templates/fusionar/fusionar.css");
		$.get('/neptuno/templates/fusionar/fusionar.htm',
			{},
			function(respuesta)
			{
				bloque.html(respuesta);				
				
				var selectorOrigen=bloque.find('.Selector');
				selectorOrigen.attr('titulo', 'Registro que desaparece');
				
				selectorOrigen.Selector(
				{ 
					idSeleccionado: null,
					contenedorMensajes:neptuno.cntMsgs,									
					tabla: tabla
				});

				bloque.find(".BotonFusionar").unbind("click");
				bloque.find(".BotonFusionar").bind("click", function f()
				{
					var idOrigen		=selectorOrigen.attr('idseleccionado');
					var usuarioNeptuno	=neptuno.obtenerusuarioNeptuno();
					
					neptuno.logconsola.Log("atenea::accionFusionar => Fusionando en "+tabla+" destino="+idDestino+" origen="+idOrigen);
					
					if( idOrigen==-1 || idOrigen=="undefined" || idOrigen==null)
					{
						neptuno.cntMsgs.ShowError(null, "Ha de seleccionar un registro origen, en la tabla "+tabla+" para realizar la fusi&oacute;n.");
					}
					else if(idOrigen==idDestino)
					{
						neptuno.cntMsgs.ShowError(null, "No se puede realizar la operaci&oacute;n de fusi&oacute;n sobre el mismo registro de la tabla "+tabla+".");			
					}
					else
					{
						neptuno.inicializaDialogo(".ConfirmaFusion", "Confirmar operaci&oacute;n");
						$('.ConfirmaFusion').html("¿Est&aacute; seguro de que desea realizar la operaci&oacute;n de fusi&oacute;n entre los dos registros de la tabla "+tabla+"?");
						$('.ConfirmaFusion').dialog('option', 'buttons', 
						{ 
							"Cancelar": function() {$(".ConfirmaFusion").dialog("close");}, 
							"Aceptar": function() 
							{
								$(".ConfirmaFusion").dialog('close');
								neptuno.cntMsgs.Show("Comenzando fusi&oacute;n");
								
								cursorEspera();

								$.ajax({
									url: "/neptuno/sw/fusionarSW.py",
									data: {
											nombre_tabla: tabla,
											id_destino: idDestino,
											id_origen: idOrigen,
											id_usuario:usuarioNeptuno.id, 
											id_sesion:usuarioNeptuno.challenge
										}, 
									async : false,
									cache:false,
									success:
										function(respuesta)
										{
											endcursorEspera();
											neptuno.cntMsgs.Show("Operaci&oacute;n de fusi&oacute;n realizada correctamente.");
											
											// Repetimos la última búsqueda																																								
											var terminoBusqueda=selectorOrigen.attr('busqueda');
											selectorOrigen.find('.busqueda').val( terminoBusqueda );
											selectorOrigen.find('.BotonBuscar').trigger('click');
										},
									error:
										function(respuesta)
										{
											selectorOrigen.AsignarRegistro(-1);
											endcursorEspera();
											neptuno.cntMsgs.ShowError(respuesta, "Error fusionando registros en la tabla "+tabla+".");															
										}
								}); // ajax
							} // Aceptar
						}); // dialog
		
						$(".ConfirmaFusion").dialog('open');
						
					} // Los registros son correctos
					
				}); // bind
				
			}); // get		

	}; // accionFusionar

	/**
	* Genera un selector en modo lista, filtrando
	* por una tabla y campo relacionados. El valor lo recoge del selector desde
	* donde estemos cargando la acción.
	* 
	* @function accionTablaRelacionada
	* @param {Event} event
	* @param {String} tabla
	* @param {String} campofiltrado
	* @param {String} titulo - Titulo a mostrar en el selector en modo lista
	* @param {Object} resultsActions - Objeto conteniendo las acciones sobre los resultados
	*/	
	this.accionTablaRelacionada=function(event, tabla, campofiltrado, titulo, resultsActions,tipoEdicion)
	{
		$('*').css('cursor','wait');
		var selector = $(event.data.selector);
		$(event.data.selector).find('.AccionActiva').attr('idRegistro',$(event.data.selector).attr('idSeleccionado'));
		
  		var datosNavegacion=this.obtenerDatosNavegacion();
  		var nombreClase=datosNavegacion.clase;
  		var rnd=randomString(5);
		$.get('./acciones/'+nombreClase+'/'+tabla+'.htm?a=rnd'+rnd,
			{},
			function(respuesta)
			{
				selector.find('.AccionActiva').html(respuesta);	
				selector.find('.AccionActiva').find('.Selector').Selector({ 
								tabla: tabla,
								campofiltrado: campofiltrado,
								valorfiltrado: selector.attr('idSeleccionado'),
								tipoEdicion:tipoEdicion,
								titulo: titulo,
								debug: (selector.attr('debug')=='true'),
								solo_lectura: true,
								maxResults:20,
								resultsActions: resultsActions
							});

				selector.find('.AccionActiva').show();
				$('*').css('cursor','');

			});		
	}; // accionTablaRelacionada

	/**
	 * Lanza la acción de edición
	 * @function accionEditar 
	 * @param {Event} event
	*/	
	this.accionEditar=function(event)
	{
		$(event.data.selector).find('.AccionActiva').attr('idRegistro',$(event.data.selector).attr('idSeleccionado'));
  		$(event.data.selector).EditarRegistro();
	}; // accionEditar

	/**
	 * Lanza la acción de borrado
	 * @function accionBorrar
	 * @param {Event} event
	*/	
	this.accionBorrar=function(event)
	{
		var datosNavegacion=neptuno.obtenerDatosNavegacion();
		
		switch(datosNavegacion.modo)
		{
			default:
			case '':
			{
				var selector=$(event.data.selector);
				selector.BorrarRegistro();
				break;
			}
			case 'full':
			{
				// En modo pantalla completa no se permite borrar el registro seleccionado
				neptuno.cntMsgs.ShowError(null, 'En modo pantalla completa no se permite borrar el registro seleccionado');
				break;
			}
		}
	}; // accionBorrar


	/**************************************************************************
	* Le asigna valores a un select por medio de un array.
	*
	* Requiere que la lista de valores tenga el id en primer lugar y luego
	* como 'etiqueta' pone el siguiente campo que se le pase.
	*
	* @function actualizaValoresSelect -
	* @param {Object} select - select donde insertaremos valores
	* @param {Array} valores
	*	@... {Integer} id
	*	@... {String} nombre
	**************************************************************************/	
	this.actualizaValoresSelect=function(select, valores)
	{
		if(valores!=null)
		{
			var html='';
			var nvalores=valores.length;
			
			for(var REGISTROi=0;REGISTROi<nvalores;REGISTROi++)
			{				
				var registro=valores[REGISTROi];

				var id='';
				var nombre='';
				
				if( registro[0] && registro[1] )
				{
					for(var _id in registro[0] )
					{
						var idCampo=_id;
						eval('var id=registro[0].'+idCampo);
						break;
					}
					
					for(var _nombre in registro[1] )
					{
						var nombreCampo=_nombre;
						eval('var nombre=registro[1].'+nombreCampo);
						break;
					}
					
					html+='<option value=\"'+id+'\">'+nombre+'</option>';
				}

			} // recorremos los valores

			select.html(html);		
		}
	}; // actualizaValoresSelect

	/**************************************************************************
	* Genera la url para un s.w.
	* Si el objeto neptuno utiliza los s.w. base=> urlBase+nombre servicio
	* En caso contrario => "../../neptuno/libpy"+nombre servicio
	* TODO: No deberíamos utilizar ../../neptuno, si no que debería parametrizarse.
	* @function obtenUrl
	* @param {String} webservice
	* @returns {String} url
	**************************************************************************/	
	this.obtenUrl=function(webservice)
	{
		var toReturn=(this.utilizarURLBase ? this.URLBase+"/"+webservice : "../../neptuno/sw/"+webservice);
		
		return toReturn;		
	}; // obtenUrl

	/**
	* @function getValoresFiltrando
	* @param {String} tabla
	* @param {String} campos
	* @param {Function} onRequest - Se lanza cuando se reciben los resultados
	* @param {Function} onNoHayRegistros - Se lanza si no hay registros
	**/
	this.getValoresFiltrando=function(tabla, campos, onRequest, onNoHayRegistros)
	{
		var usuarioNeptuno=this.obtenerusuarioNeptuno();
		var objetoNeptuno=this;
		
		$.ajax({																												
			url: this.obtenUrl("buscar.py"), 
			data:
			{
				tabla: tabla,
				campos: campos,
				id_usuario:usuarioNeptuno.id, 
				id_sesion:usuarioNeptuno.challenge,
				pos:0,
				limite_resultados:1,
				pos:0,
				orderbyid:'True'
			}, 
			async : false,
			cache:false,
			error: function()
			{
				onRequest(null);
			},
			success:
			function(registros)
			{
				
				if(registros=="[]")
				{
					if(onNoHayRegistros)
					{
						onNoHayRegistros();
					}
					else
					{
						neptuno.cntMsgs.ShowError(null, "No se han podido encontrar registros en la tabla "+tabla+" filtrando por "+campo);						
					}
				}
				else
				{
					eval('var valores='+registros+';');
					onRequest(valores);
				}
			}
		});			
	}; // getValoresFiltrando
	

	/**************************************************************************
	 * Esta función se va a utilizar para obtener los valores de una tabla,
	 * generalmente de tablas pequeñas, como por ejemplo 'sexos'.
	 * De esta forma, se pueden obtener los valores para mostrar en un select.
	 * La función onRequest, se pasa por parámetro y recibirá los valores obtenidos.
	 *
	 * @function getValoresTabla
	 * @param {String} tabla
	 * @param {Function} onRequest
	 *************************************************************************/
	this.getValoresTabla=function(tabla, onRequest)
	{
		var usuarioNeptuno=this.obtenerusuarioNeptuno();
		var objetoNeptuno=this;

		$.ajax({																												
				url: this.obtenUrl("buscar.py"), 
				data:
				{
					tabla: tabla, 
					id_usuario:usuarioNeptuno.id, 
					id_sesion:usuarioNeptuno.challenge,
					busqueda: '*'
				}, 
				async : false,
				cache:false,
				error: function()
				{
					onRequest(null);
				},
				success:
				function(registros)
				{
				  	// esta función convierte los resultados de buscar.py del nuevo formato al formato raro que se usaba al principio
					// TO DO: Obviamente, cambiar todas las funciones que se usan esta salida de datos para que utilicen el formato nuevo
					// y dejar esto como una salida de datos normal sin convertir nada.
						
					eval('var valores='+registros+';');
					var columnas = valores.columnas;
					var datos = valores.datos;
					var registros = '';
					for(var i=0;i<datos.length;i++)
					{
						var registro='';
						for(var j=0;j<columnas.length;j++)
						{
							if(registro != '') registro += ', ';
							registro+='{"'+columnas[j]+'":"'+datos[i][j]+'"}';
						}						
						if(registros != '') registros += ', ';
						registros += '['+registro+']';
						
					}
					
					registros = '['+registros+']';
					
					eval('valores = '+registros); 
					
					onRequest(valores);
				}
		});			
		
	}; // getValoresTabla

	
	/**************************************************************************
	* Inicializa las propiedades estándar en un bloque
	* antes de aplicarle la función dialog.
	* @function inicializaDialogo
	* @see http://groups.google.com/group/jquery-ui/browse_thread/thread/3246dbd433e8df5f?pli=1
	* @param {String} idDialogo
	* @param {String} titulo
	* @param {Integer} ancho
	* @param {Integer} alto
	*************************************************************************/
	this.inicializaDialogo=function(idDialogo, titulo, ancho, alto)
	{
		//$(idDialogo).dialog('option', 'destroy');
		if(ancho <1) ancho = 300;
		if(alto < 1) alto = 300;
		if($(idDialogo).length == 0)
		{
			$('body').append('<div id="dialogoGenerico" class="Dialogo">lll</div>');
			idDialogo = "#dialogoGenerico";
		}
		//$(idDialogo).dialog('option', 'show', 'slide');
		var dialogo = $(idDialogo).dialog({autoOpen: false, resizable:true});
		dialogo.dialog('option', 'modal', false);
		dialogo.dialog('option', 'draggable', true);
		dialogo.dialog({closeOnEscape: true});
		//TODO: parece que no funciona correctamente, aplicando el estilo directamente
		dialogo.dialog('option', 'open', function a() 
		{
			// http://groups.google.com/group/jquery-ui/browse_thread/thread/3246dbd433e8df5f?pli=1
			// Para solucionar el conflicto con el datepicker
			// Lo implemento de momento mediante css en /tandem/interfaz/estilos.css
			//$("#ui-datepicker-div").css("z-index", $(this).parents(".ui-dialog").css("z-index")+1);
		});  
		if(titulo)
			dialogo.dialog('option', 'title', titulo);				
		if(ancho)
			dialogo.dialog('option', 'width', ancho);
		if(alto)
			dialogo.dialog('option', 'height', alto);
			
		return dialogo;
	}; // inicializaDialogo

	/**************************************************************************
	 * Muestra la información de la versión del sistema
	 * Neptuno. Para ello lee el fichero version.js dentro de la carpeta de interfaz.
	 * Dicho fichero se genera automáticamente por medio de los scripts de
	 * actualización.
  	 * @function infoVersion
	 *************************************************************************/
	this.infoVersion=function()
	{
		var urlInfo="./version.js";
		var objetoNeptuno=this;
		
		$.ajax({
				url: urlInfo, 
				async : false,
				cache:false,
				dataType:'json',
				success:
				function(version)
				{

					if(typeof(version)=='object')
					{
					
						if(version.info)
						{
							objetoNeptuno.cntMsgs.Show(version.info);
						}
					  
						if(version.debug)
						{
						  
							objetoNeptuno.activaConsola();
							objetoNeptuno.Debug=true;
							objetoNeptuno.logconsola.Log('Depuración activada');
						}
						
						if(version.ver)
						{
							$("#versionAtenea").html(version.ver);
						}
					}
					
				},
				error:
				function(a,err)
				{
					alert(err);
					// Si no se ha generado version.js, no pasa nada.
				}
		});
		
	}; // infoVersion

	/**************************************************************************
	*  TODO: Revisar la necesidad de esta función
	*  @function lanzaAccion
	*  @param {String} nombreAccion
	*************************************************************************/
	this.lanzaAccion=function(nombreAccion)
	{
		// var datosNavegacion=this.obtenerDatosNavegacion();
		// datos de navegacion
		//window.location.hash="#"+datosNavegacion.clase+"_"+datosNavegacion.id+"_"+nombreAccion;
	};

	/***********************************************************************
	* Redirecciona a un estado de la página.
	* TODO: Revisar la necesidad de esta función
	* @function Navega
	* @param {String} clase
	* @param {String} id
	* @param {String} accion
	* @param {String} modo
	**********************************************************************/
	this.Navega=function(clase, id, accion, modo)
	{
		this.setNavegacion(clase, id, accion, modo);
		window.open(window.location);
	}; // Navega

	/**************************************************************************
	* Actualiza la información de navegación del
	* hash de la página.
	* @function setNavegacion
	* @see https://docs.google.com/a/ender.es/Doc?docid=0AdmMl5H6gCAaZGYzaHc4amNfNDZkM3prcGdnZg&hl=es
	* @param {String} clase
	* @param {String} id
	* @param {String} accion
	* @param {String} modo
	*************************************************************************/
	this.setNavegacion=function(clase, id, accion, modo)
	{
		if(!modo)
		{
			var datosNavegacion=this.obtenerDatosNavegacion();
			modo=datosNavegacion.modo;
		}

		if(clase==null && id==null && accion==null)
		{
			window.location.hash='';	
		}
		else
		{
			clase	=(clase!=null ? clase : '');
			id	=(id!=null ? id : '');
			accion	=(accion!=null ? accion : '');
			modo	=(modo!=null ? modo : '');
			
			window.location.hash=clase+":"+id+":"+accion+":"+modo;
		}
	}; // setNavegacion

	/**************************************************************************
	 @function obtenerDatosNavegacion
	 @see https://docs.google.com/a/ender.es/Doc?docid=0AdmMl5H6gCAaZGYzaHc4amNfNDZkM3prcGdnZg&hl=es
	 @returns {Object} objetoDatos
	 @... {String} clase
	 @... {String} id
	 @... {String} accion
	 @... {String} modo
	 *************************************************************************/
	this.obtenerDatosNavegacion=function()
	{
		var urlNavegacion=new String(window.location.hash);
		var datosNavegacion=new String(urlNavegacion);
		datosNavegacion=datosNavegacion.split(":");
		
		var objetoDatos={};
		objetoDatos.id		=( datosNavegacion[1] ? datosNavegacion[1] : null );
		objetoDatos.accion	=( datosNavegacion[2] ? datosNavegacion[2] : null );
		objetoDatos.modo	=( datosNavegacion[3] ? datosNavegacion[3] : null );
		
		/*
		// Construimos los parámetros
		var paramsstr	=new String( datosNavegacion[4] ? datosNavegacion[4] : ""  ) ;
		objetoDatos.params=new Array();
		
		if(paramsstr!="")
		{
			var parametros=paramsstr.split(",");
			alert(parametros.length);
	
			for(var i=0;i<parametros.length;i++)
			{
				var parametroActualstr=new String( parametros[i] ? parametros[i] : null );
				var parametro=parametroActualstr.split("=");
				
				var nombre=(parametro[0] ? parametro[0] : null);
				var valor=( parametro[1] ? parametro[1] : "" );
				
				if(nombre)
				{
					objetoDatos.params[objetoDatos.params.length]={};
					
					alert(nombre+" "+valor+" "+objetoDatos.params[objetoDatos.params.length]);
					
					eval("objetoDatos.params[objetoDatos.params.length]."+nombre+"='"+valor+"';"); 
				}
			}			
			neptuno.logconsola.MostrarObjeto(objetoDatos.params);
		}
		*/
										       
		if(datosNavegacion[0])
		{
			var tmp=new String(datosNavegacion[0]);
			tmp=tmp.toLowerCase();
			
			// le quitamos #
			tmp=tmp.replace(/#/g , "");
			objetoDatos.clase=tmp;			
		}	
		else
		{
			objetoDatos.clase=null;
		}
		
		return objetoDatos;
	}; // obtenerDatosNavegacion

	
	/**************************************************************************
	 * Devuelve un objeto con información
	 * acerca del usuario logueado en el sistema(por medio de la cookie)
	 * @function obtenerusuarioNeptuno
	 * @returns {Object} usuario
	 * @... {Integer} id
	 * @... {String} challenge
	 *************************************************************************/
	this.obtenerusuarioNeptuno=function()
	{
		if( $.cookie('neptuno') )
		{
			eval('var usuario = '+$.cookie('neptuno'));
			return usuario;
		}
		else
		{
			return {id:-1, challenge:null};
		}
		
	}; // obtenerusuarioNeptuno


	/**************************************************************************
	 * Genera un alfabeto en castellano, incluyendo además los números.
	 * Se utiliza para los tests de prueba.
	 * TODO: Revisar si se puede poner en otro sitio
	 @function generaAlfabeto 
	 *************************************************************************/
	this.generaAlfabeto=function()
	{
		return "abcdefghijklmnñopqrstuvwxyzáéíóú0123456789";
	}; // generaAlfabeto

	/**************************************************************************
	 * Procesa los distintos casos de error en el login.
	 * @function loginIncorrecto
	 * @param {Object} xhr
	 * @param {String} msg
	 * @param {Exception} excep
	 *************************************************************************/
	this.loginIncorrecto=function(xhr,msg,excep)
	{
		var CodigoErrorHTTP=parseInt(xhr.status);
		var TextoAMostrar='';
	
		switch(CodigoErrorHTTP)
		{
			case 403: // Forbidden
			{
				TextoAMostrar='Contrase&ntilde;a incorrecta'
				break;
			}
			case 404: // Usuario no encontrado
			{
				TextoAMostrar='Nombre de usuario incorrecto';
				break;
			}
			case 406:
			{
				TextoAMostrar='Not Acceptable';
				break;
			}
			default: // Error interno
			{
				TextoAMostrar='Servicio no disponible...';
				break;			
			}
		} // switch CodigoErrorHTTP
		
		neptuno.cntMsgs.ShowError(null, TextoAMostrar);
		
	}; // loginIncorrecto


	/**************************************************************************
	* Destruye la cookies de sesión 'neptuno'
	* @function cerrarSesion
	* @param {Function} onClose
	*************************************************************************/
	this.cerrarSesion=function(onClose)
	{
		var usuario=this.obtenerusuarioNeptuno();
		var objetoNeptuno=this;		
		
		$.get(this.obtenUrl("checkuser.py/cerrarsesion"),
			  {id_usuario: usuario.id , id_sesion:usuario.challenge},
			  function(respuesta)
			  {		
				  eval("var res = "+respuesta);
				  if(res.resultado == true)				  
				  {
					objetoNeptuno.cntMsgs.Show("Sesi&oacute;n de "+usuario.nombre+" cerrada.");
					onClose();
				  }
				  else
				  {
					objetoNeptuno.cntMsgs.ShowError(null, "Error cerrando sesi&oacute;n");
				  }
			  }
		);
	
		$('.caja_login').remove();
		LoginYaDibujado=false;

	}; // cerrarSesion

	/**************************************************************************
	* Tests base del sistema
	* @function testsBase
	* test_carga
	* test_atenea
	* test_login
	*************************************************************************/
	this.testsBase=function(propiedades)
	{
		$.cookie('neptuno',null);

		///////////////////////////////////////////////////////////////////////
		// Test de carga de librerías
		///////////////////////////////////////////////////////////////////////
		module("test_carga");
		test("Test de carga de librer&iacute;as", function() 
		{
			neptuno.consola.Log("Iniciando test de carga de librerías");
			var nErrores=cargador.fails.length;
			var descripcion="";
   
			if(nErrores>0)
			{
				for(var ERRORi=0;ERRORi<nErrores;ERRORi++)
				{
					descripcion+=" "+cargador.fails[ERRORi];
				}
			}

			equals(0, nErrores, "Librerías no cargadas: "+descripcion );
		});

   
		///////////////////////////////////////////////////////////////////////
		// Test de carga del objeto Atenea
		///////////////////////////////////////////////////////////////////////
		module("test_neptuno");
		test("Test de carga del objeto Neptuno", function() 
		{
			ok( neptuno !== null) && (typeof( neptuno ) == 'object', "El objeto neptuno se encuentra definido.");
		});

		///////////////////////////////////////////////////////////////////////
		// Test del sistema de login
		///////////////////////////////////////////////////////////////////////
		
		var user='';
		var pass='';
		
		if(propiedades && typeof(propiedades)=='object')
		{
			user=propiedades.login;
			pass=propiedades.password;
		}
		else
		{
			user='admin';
			pass='admin';
		}
		
		module("test_login");   
		test("Test de login", function()
		{
			neptuno.consola.Log("Iniciando test de login");
			var usuarioNeptuno=neptuno.obtenerusuarioNeptuno();
			equals(usuarioNeptuno.id, -1, "El usuario no se encuentra registrado en el sistema");
			var bloque=$('#testDiv');
			stop();

			neptuno.checkLogin(user, pass,function f()
			{
				ok(true, "login admin correcto");
				start();
			},
			function g()
			{
				ok(false, "Login admin incorrecto");
				start();
			});
   
			usuarioNeptuno=neptuno.obtenerusuarioNeptuno();
   
			ok(usuarioNeptuno.id >= 0, "Identificador de usuario correcto: "+usuarioNeptuno.id);   
			ok(usuarioNeptuno.challenge != '', "challenge correcto: "+usuarioNeptuno.challenge);
   
		});

	}; // testsBase
	
	
	/**************************************************************************
	 * Comprueba el login del usuario.
	 * Si pasamos el parámetro remember como cierto, recuerda durante 15 días el login
	 * @function checkLogin
	 * @param {String} username
	 * @param {String} password
	 * @param {Function} onLogin
	 * @param {Boolean} remember
	 *************************************************************************/
	this.checkLogin=function(username, password, onLogin, remember, sw)
	{
		if(sw == '' || sw == null) sw = this.obtenUrl('checkuser.py/login');
		
		if(username && password)
		{
			var objetoNeptuno=this;
		
			$.ajax({
					url: sw, 
					data:{login:username, password:password}, 
					async : false,
					error:this.loginIncorrecto,
					cache:false,
					success:
					function(respuesta)
					{
						eval('var usuario='+respuesta);
						
						if(usuario.id>0 && usuario.challenge!='')
						{
							var options={};
							
							if(remember)
							{
								options = {path: '/', expires: 15};
							}
							
							objetoNeptuno.cntMsgs.Show("Usuario "+username+" registrado en el sistema.");
							$.cookie('neptuno', respuesta, options);
							usuarioNeptuno=usuario;
							onLogin();							
						}
					}
			});
		}
		else
		{
			this.cntMsgs.Show("Ha de introducir nombre de usuario y contrase&ntilde;a");
		}		
	}; // checkLogin
	
	
	/**************************************************************************
	 * Comprueba si el usuario se encuentra logueado en el sistema
	 * @function sessionOK
	 * @param {Function} requestOK
	 * @param {Function} requestERROR
	 *************************************************************************/
	this.sessionOK=function(requestOK, requestERROR)
	{
		if($.cookie('neptuno') == null)
		{
		  eval(requestERROR+'();');
		}
		else
		{
			eval('var usuario = '+$.cookie('neptuno'));

			$.get(this.obtenUrl('checkuser.py/compruebasesion'),
				  {id: usuario.id , challenge:usuario.challenge},
				  function(res)
				  {
					if(usuario.id>0)
					{
					  if(res=='True')
					  {
					  	eval(requestOK+'();');
					  }
					  else
					  {
						  $.cookie('neptuno',null);
						  eval(requestERROR+'();');
					  }
					}
					else
					{
					  eval(requestERROR+'();');
					}
				  });
		}
	}; // sessionOK
	
	/**************************************************************************
	 @function borrarUsuarioEnSelector
	 @param {Object} selector
	 @param {String} idDialogo
	 *************************************************************************/
	this.borrarUsuarioEnSelector=function(selector, idDialogo)
	{
		
		var idUsuario=selector.attr('idseleccionado');
		
		this.borrarUsuario(idUsuario, idDialogo, function a()
		{
		
			selector.BorrarRegistro(true);		
		});
		
	}; // borrarUsuarioEnSelector


	/**************************************************************************
	* Borra el usuario de identificador pasado por parámetro.
	* @function borrarUsuario
	* @param {Integer} idUsuario
	* @param {Integer} idDialogo
	* @param {Function} onAccept
	*************************************************************************/
	this.borrarUsuario=function(idUsuario, idDialogo, onAccept)
	{
	 	$(idDialogo).html("¿Borrar este usuario?");
	 	
	 	neptuno.inicializaDialogo(idDialogo, "Borrar usuario");
		
	 	$(idDialogo).dialog('option', 'buttons',
	 	{
			"Cancelar": function(){$(idDialogo).dialog('close');},
	 		"Aceptar": function() 
			{ 
				var usuarioNeptuno=neptuno.obtenerusuarioNeptuno();
				
				if(idUsuario==usuarioNeptuno.id)
				{
					neptuno.cntMsgs.ShowError(null, "No puede borrar su propia cuenta de usuario.");																	
				}
				else
				{
					// En primer lugar obtenemos el id de 'salt'
					neptuno.logconsola.Log("borrando el usuario de id "+idUsuario);

					// tabla, campos, onRequest, onNoHayRegistros
					// 'id_usuarios_id', idUsuario
					neptuno.getValoresFiltrando('salts', "[[\"id_usuarios_id\", \""+idUsuario+"\" ]]",  function a(usuarios)
					{
						for(i=0;i<usuarios[0].length;i++)
						{
							var idSalt=(usuarios[0][i].id!=null? usuarios[0][i].id : -1);
							if(idSalt!=-1)
								break;
						}
						
						var textoBorraUsuario="Borrado usuario";
						
						if(idSalt!=-1)
						{
							neptuno.logconsola.Log("borrando el registro de la tabla salts "+idSalt);
							
							neptuno.borrarRegistro(idSalt, 'salts', function b()
							{
								neptuno.cntMsgs.Show('Borrada cadena \'salt\'');

								neptuno.borrarRegistro(idUsuario, 'usuarios', function b()
								{
									neptuno.cntMsgs.Show(textoBorraUsuario);
									onAccept();
								}); 
							}); 
						}
						else
						{
							/**
								Si no tenía salt, borramos directamente.
							 **/
							neptuno.borrarRegistro(idUsuario, 'usuarios', function b()
							{
								neptuno.cntMsgs.Show(textoBorraUsuario);
								onAccept();
							}); 
						}
					});
		
					
				}
				
				$(idDialogo).dialog('close');
			}
		 });

		$(idDialogo).dialog('open');
		
	}; // borrarUsuario
	
	/**************************************************************************
	* Borra el registro de identificador pasado por parámetro, en la tabla seleccionada.
	* @function borrarRegistro
	* @param {Integer} idRegistro
	* @param {String} tabla
	* @param {Function} success
	* @param {Function} error
	*************************************************************************/
	this.borrarRegistro=function(idRegistro, tabla, success, error)
	{
		var usuarioNeptuno=this.obtenerusuarioNeptuno();
		var objetoNeptuno=this;
		
		if(!error)
		{
			var error=function(respuesta)
			{
				objetoNeptuno.cntMsgs.ShowError(respuesta, "Error borrando registro "+idRegistro+"en la tabla "+tabla);	
			}
		}
		
		$.ajax({
				url: this.obtenUrl("borrar.py"), 
				data:{
					tabla: tabla,
					id: idRegistro, 
					id_usuario:usuarioNeptuno.id, 
					id_sesion:usuarioNeptuno.challenge																		       
				}, 
				async : false,
				cache: false,
				error:error,
				success: success
		});
		
	}; // borrarRegistro
	
	
	/**************************************************************************
	 * Devuelve un registro de una tabla en forma de objeto.
	 * @function datosRegistro
	 * @param {String} tabla
	 * @param {Integer} id
	 * @param {Function} success
	 * @param {optional Boolean} sincrona
	 *************************************************************************/
	this.datosRegistro=function(tabla, id, success,sincrona)
	{
		// si el par�metro "sincrona" es true, funciona sincronamente y devuelve la respuesta.
		var usuarioNeptuno=this.obtenerusuarioNeptuno();
		var objetoNeptuno=this;
		resp = -1;
/*		if(sincrona == true)
		{
			success = function(respuesta)
			{
				resp = respuesta;
			}
		}
		else
		{
			sincrona = false;
		}*/ // No tiene sentido este bloque
		
		if(id && id!='')
		{
			$.ajax({																												
					url: this.obtenUrl("datosRegistro.py"), 
					data:
					{
						tabla: tabla,
						id: id,
						id_usuario:usuarioNeptuno.id,
						id_sesion: usuarioNeptuno.challenge
					}, 
					async : !sincrona,
					cache:false,
					success: success,
					error:
					function(respuesta)
					{
						objetoNeptuno.cntMsgs.ShowError(respuesta, "Error recibiendo el registro "+id+" en la tabla "+tabla);	
					}
			});			
		}	
		else
		{
			$.ajax({																												
					url: this.obtenUrl("datosRegistro.py"), 
					data:
					{
						tabla: tabla,
						id_usuario:usuarioNeptuno.id,
						id_sesion: usuarioNeptuno.challenge
					}, 
					async : !sincrona,
					cache:false,
					success: success,
					error:
					function(respuesta)
					{
						objetoNeptuno.cntMsgs.ShowError(respuesta, "Error recibiendo el registro "+id+" en la tabla "+tabla);	
					}
			});			
		}	
		
		return resp;

	}; // datosRegistro
	
	
	
	/**************************************************************************
	* Guarda un registro en la tabla a partir de un objeto.
	* @function guardarRegistro
	* @param {String} tabla
	* @param {Integer} id
	* @param {Object} objetoRegistro
	* @param {Function} success
	*************************************************************************/
	this.guardarRegistro=function(tabla, id, objetoRegistro, success)
	{
		var usuarioNeptuno=this.obtenerusuarioNeptuno();
		var objetoNeptuno=this;

		$.ajax({																												
				url: this.obtenUrl("guardarRegistro.py"), 
				data:{
					tabla: tabla,
					datos: toString(objetoRegistro),
					id: id,
					id_usuario:usuarioNeptuno.id,
					id_sesion: usuarioNeptuno.challenge
				}, 
				async : false,
				cache:false,
				success: success,
				error:
				function(respuesta)
				{
					objetoNeptuno.cntMsgs.ShowError(respuesta, "Error guardando registro "+idRegistro+"en la tabla "+tabla);	
				}
		});			
		
	}; // guardarRegistro

	/**************************************************************************
	* Las variables que contienen intros, los reciben en la forma '@ENTER',
	* deberá por tanto ser filtrado desde el otro lado.
	*  @function construirObjeto -
	* @param {String} respuesta
	* @returns {Object} objeto
	*************************************************************************/
	this.construirObjeto=function(respuesta)
	{
		var toReturn={};
		respuesta=respuesta.replace(/\\n/g , "@ENTER");
		
		eval("var datos="+respuesta);
		for(objeto in datos)
		{
			if( datos[objeto]["valor"] )
			{
				eval('toReturn.'+datos[objeto]["nombre"]+'=\"'+datos[objeto]["valor"]+'\";');								
			}
			else
			{
				eval('toReturn.'+datos[objeto]["nombre"]+'=null;');
			}
		}		
		
		return toReturn;
		
	}; // construirObjeto	
	
	
	/**************************************************************************
	* - Compara dos cadenas para ver si representan una contraseña
	* válida. Han de ser iguales, no vacías y de longitud superior
	* a 3 caracteres.
	* @function validaPasswords
	* @param {String} password1
	* @param {String} password2
	* @param {Function} onRequest
	*************************************************************************/
	this.validaPasswords=function(password1, password2, onRequest)
	{
		if(password1!=password2)
		{
			neptuno.cntMsgs.ShowError(null, 'Las contrase&ntilde;as no coinciden.');
		}
		else if(password1=='')
		{
			neptuno.cntMsgs.ShowError(null, 'No se admite la contrase&ntilde;a vac&iacute;a.');
		}
		else if(password1.length<4)
		{
			neptuno.cntMsgs.ShowError(null, 'No se admiten contrase&ntilde;as con una longitud inferior a 4 caracteres.');
		}
		else
		{
			onRequest();
		}
	}; // validaPasswords

	/***********************************************************************
	@function aplicaDatePicker
	@param {Object} bloque
	@param {Object} opciones
	@param {Function} fCambiaMes
	@param {Function} fSeleccionaFecha
	@param {Function} onReady
	**********************************************************************/
	this.aplicaDatePicker=function(bloque, opciones, fCambiaMes, fSeleccionaFecha, onReady)
	{
    
	    $date1=bloque.datePicker(opciones)
		.bind('dpMonthChanged',
			function(event, displayedMonth, displayedYear)
			{
			    if(fCambiaMes)
			    {
				fCambiaMes(displayedMonth, displayedYear);
			    }
			}
		)
		.bind('dateSelected',
			function(event, date, $td, status)
			{
			    if(fSeleccionaFecha)
			    {
				fSeleccionaFecha(date, $td, status);
			    }
			}
		)
		.bind('dpDisplayed', function()
		    {
			    onReady();
		    });
		    
	}; // aplicaDatePicker
	
	/**************************************************************************
	* Devuelve el valor correspondiente a una propiedad de un objeto devuelto por un s.w.
	* @function getVal
	* @param {String} respuesta
	* @param {String} nombre
	* @returns {String} valor
	*************************************************************************/
	this.getVal=function(respuesta, nombre)
	{
		if(typeof(respuesta)!='object')
		{
			var i=0;
			
			eval("var datos="+respuesta);
			
			for(objeto in datos)
			{
				if( datos[objeto]["nombre"]==nombre )
				{
					return datos[objeto]["valor"];
				}
			}
			
			return null;
		}		
		else 
		{
			var toReturn=null;
			var nrespuesta=respuesta.length;
			for(i=0;i<nrespuesta;i++)
			{
				eval("if(respuesta["+i+"]."+nombre+") toReturn=respuesta["+i+"]."+nombre+";");
			}
			
			return toReturn;
		}
		
	}; // getVal	
	
} // ControladorNeptuno

// Instanciamos el objeto neptuno
var neptuno=new ControladorNeptuno();

/*******************************************************************************
@class contenedorMensajes
*******************************************************************************/
function contenedorMensajes()
{
	this.activo=true;

	/***********************************************************************
	* Muestra un mensaje por medio de jGrowl
	* @function Show
	* @param {String} msg
	***********************************************************************/
	this.Show=function(msg)
	{
		var fecha=new Date();
		var textoFecha=fecha._toString()+" "+fecha._toHours();
		msg=textoFecha+"<br/>"+msg;

		if(this.activo)
		{
			$.jGrowl(msg, {theme: 'GrowlSimple', life:8000});
		}
	}; // Show
	
	/***********************************************************************
	* Lanza un mensaje de error por medio de jGrowl
	* @function ShowError
	* @param {String} data
	* @param {String} msg
	***********************************************************************/
	this.ShowError=function(data, msg)
	{
		if(this.activo)
		{
			this.GrowlError(data, msg);
		}
	}; // ShowError


	/***********************************************************************
	* Recupera la parte más util de un mensaje de error del mod-python
	* @function Show
	* @param {String} msg
	* @returns {String} str
	***********************************************************************/
	this.getModPythonErrorText=function(msg)
	{
		var datos=new String(msg.responseText);
		var arrayMsg=datos.split("MODULE CACHE DETAILS");
		// Queremos la parte que va antes del texto anterior
		arrayMsg=new String(arrayMsg[0]);
		
		// Mostramos los últimos 200 caracteres
		arrayMsg=arrayMsg.substr(arrayMsg.length-200,200);
		 
		return arrayMsg;	 
	}; // getModPythonErrorText

	/***********************************************************************
	* Muestra un mensaje de error
	* @function Show
	* @param {String} respuesta
	* @param {String} msg
	***********************************************************************/
	this.GrowlError=function(respuesta, msg)
	{
		var fecha=new Date();
		var textoFecha=fecha._toString()+" "+fecha._toHours();
		msg=textoFecha+"<br/>"+msg;
		
		if(respuesta!=null)
		{
			msg+="<br/><br/>..."+this.getModPythonErrorText(respuesta)+"...";
		}

		if(this.activo)
		{		
			$.jGrowl(msg, {theme: 'GrowlError', sticky: true});
		}
	}; // GrowlError 

}; // contenedorMensajes


/********************
 * Comprueba si una fecha tiene un formato válido
 * $param {String} dateStr - Fecha a comprobar
 * $param {String} format - Formato de la fecha (DMY o MDY)
 */
function isValidDate(dateStr, format) 
{
   if (format == null) { format = "DMY"; }
   format = format.toUpperCase();
   if (format.length != 3) { format = "DMY"; }
   if ( (format.indexOf("M") == -1) || (format.indexOf("D") == -1) || 
      (format.indexOf("Y") == -1) ) { format = "DMY"; }
   if (format.substring(0, 1) == "Y") { // If the year is first
      var reg1 = /^\d{2}(\-|\/|\.)\d{1,2}\1\d{1,2}$/
      var reg2 = /^\d{4}(\-|\/|\.)\d{1,2}\1\d{1,2}$/
   } else if (format.substring(1, 2) == "Y") { // If the year is second
      var reg1 = /^\d{1,2}(\-|\/|\.)\d{2}\1\d{1,2}$/
      var reg2 = /^\d{1,2}(\-|\/|\.)\d{4}\1\d{1,2}$/
   } else { // The year must be third
      var reg1 = /^\d{1,2}(\-|\/|\.)\d{1,2}\1\d{2}$/
      var reg2 = /^\d{1,2}(\-|\/|\.)\d{1,2}\1\d{4}$/
   }
   // If it doesn't conform to the right format (with either a 2 digit year or 4 digit year), fail
   if ( (reg1.test(dateStr) == false) && (reg2.test(dateStr) == false) ) { return false; }
   var parts = dateStr.split(RegExp.$1); // Split into 3 parts based on what the divider was
   // Check to see if the 3 parts end up making a valid date
   if (format.substring(0, 1) == "M") { var mm = parts[0]; } else 
      if (format.substring(1, 2) == "M") { var mm = parts[1]; } else { var mm = parts[2]; }
   if (format.substring(0, 1) == "D") { var dd = parts[0]; } else 
      if (format.substring(1, 2) == "D") { var dd = parts[1]; } else { var dd = parts[2]; }
   if (format.substring(0, 1) == "Y") { var yy = parts[0]; } else 
      if (format.substring(1, 2) == "Y") { var yy = parts[1]; } else { var yy = parts[2]; }
   if (parseFloat(yy) <= 50) { yy = (parseFloat(yy) + 2000).toString(); }
   if (parseFloat(yy) <= 99) { yy = (parseFloat(yy) + 1900).toString(); }
   var dt = new Date(parseFloat(yy), parseFloat(mm)-1, parseFloat(dd), 0, 0, 0, 0);
   if (parseFloat(dd) != dt.getDate()) { return false; }
   if (parseFloat(mm)-1 != dt.getMonth()) { return false; }
   return true;
}

/********************
 * Guarda los datos de una variable en el dom, en $('#nombrevariable')
 * $param {String} nombre - nombre de la variable
 * $param {String} datos - datos en formato string
 */

function guardaDOM(nombre, datos)
{
	if($('#'+nombre).length > 0) $('#'+nombre).val(datos);
	else $('body').append('<input type="hidden" id="'+nombre+'" value="'+datos+'"></input>');
}


function continuar(texto, fSalida)
{
	if(texto =='' || texto == 'undefined' || texto == null) texto = "¿Continuar?";
	$('body').append('<div class="ventanaConfirmar">'+texto+'</diV>');
	$('.ventanaConfirmar').dialog(
									{ modal:true,
									  buttons: 
									  {
										  	"Cancelar": function(){
										  		$(this).dialog('close');
										  		$('.ventanaConfirmar').remove();
										  		
										  	}, // Cancelar
											"Aceptar": function(){
												$(this).dialog('close');
												$('.ventanaConfirmar').remove();
												fSalida();
											} // Aceptar
										}
						         	}        
            					 ); // Dialogo		

}


function getCampos(tabla)
{
  var usuarioNeptuno = neptuno.obtenerusuarioNeptuno();
  var campos = [];
  $.ajax(
  {
      url:'/neptuno/sw/datosRegistro.py',
      dataType:'json',
      async:false,
      data:
      {
        id_usuario:usuarioNeptuno.id,
        id_sesion:usuarioNeptuno.challenge,
        tabla:tabla,
        id:-1
      },
      success:function(res)
      {
        campos = res; 
        for(var i=0;i<campos.length;i++){if(!campos[i].valor) campos[i].valor=''};
        campos.push({ nombre: "id_usuario", etiqueta: "", valor: usuarioNeptuno.id, requerido:true});
        campos.push({ nombre: "id_sesion", etiqueta:"", valor: usuarioNeptuno.challenge, requerido:true});
        campos.push({ nombre: "tabla", etiqueta:"", valor: tabla, requerido:true});
        return campos;          
      }
      
  }
  );
  
  return campos;
}