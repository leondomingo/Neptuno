(function($)
{
	var settings=null;

	/**
		showNavigation
	 **/
	$.fn.showNavigation=function()
	{
		$(this).find('.navegacionResultados:first').fadeIn();
		actualizaTextoResultados();
	};
	
	/**
		appendRow
	 **/
	$.fn.appendRow=function(fila, i, campofiltrado, cabeceras)
	{
		
		var htmlResultado=getHTMLResultado(fila, i, campofiltrado, neptuno.getAttrDataObject($(this).attr("id"), "actions"),cabeceras);
		$(this).find(".resultados:first").append(htmlResultado);
	}; // appendRow
	
	/**
		@function loadData
		@param {Object} data
		@param {Integer} pos
		@param {Integer} maxResults
		@param {Boolean} cuentaResultados
		@param {String} campofiltrado
		@param {Function} onReady
	 **/
	$.fn.loadData=function(data, pos, maxResults, cuentaResultados, campofiltrado, onReady)
	{
		neptuno.logconsola.Log("pos="+pos+" maxResults="+maxResults);
		var labelExportarResultados=$(this).find(".exportarResultados");
		$(this).find(".resultados:first").html("");
		labelExportarResultados.fadeOut();

		var NPersonal = data.datos.length;
//		var numeroResultadosReales=(cuentaResultados ? NPersonal-1 : NPersonal);

		var numeroResultadosReales=NPersonal;
		
		$(this).find(".navegacionResultados:first").fadeIn();
		

		if(maxResults > 20)
		{
			$(this).find('.navegacionResultados:first').fadeOut();
		}
		
		if(pos==0 || pos==null)
		{
			$(this).find('.navegacionResultados').find('.anterior').fadeOut();
		}


		if(numeroResultadosReales > 0)
		{
			labelExportarResultados.fadeIn();

			var FilaResultado = $(this).find('.FilaResultado');
			// var FINAL=(cuentaResultados?NPersonal-1:NPersonal);
			var FINAL = NPersonal;
			
			$(this).appendRow(data.columnas, 0, campofiltrado,data.columnas);
			
			for(var i=0;i<FINAL;i++) 
			{
					
/*				var registro=data[i];
				var fila={};
			
				for(var indice in registro)
				{
					var propiedad=registro[indice];
					
					for(var IndicePropiedad in propiedad)
					{
						fila[IndicePropiedad]=propiedad[IndicePropiedad];	
					}
					
				} // recorremos el resultado
				*/
				
				var fila={};
				var fila = data.datos[i];
/*				for(var j=0; j< data.columnas.lenght;j++)
				{
				
					fila[j] = registro[j];
				}*/
							
				$(this).appendRow(fila, i+1, campofiltrado,data.columnas);
	
			} // Mostrando los resultados de la búsqueda
			
			var resultsActions=neptuno.getAttrDataObject($(this).attr("id"), "actions");			
			if(resultsActions!=null)
			{
				var bloqueResultAction=null;
				var nResultsActions=resultsActions.length;
				
				for(var ACCIONi=0;ACCIONi<nResultsActions;ACCIONi++)
				{
					var resultAction=resultsActions[ACCIONi];
					
					bloqueResultAction=$(this).find('.'+resultAction.clase);
					
					// TODO: Resolver el problema del target:_blank
					bloqueResultAction.unbind();
					var f=neptuno.getAction(resultAction.idAction);
					
					bloqueResultAction.bind('click', f );
				} // recorremos las acciones de resultados
			
			}					
	
			$(this).find('.ColumnaSeleccionar').unbind('click');
			$(this).find('.ColumnaSeleccionar').bind('click',SeleccionarRegistro);			
			$(this).fadeIn();
			
			var nResultados=0;
			if(cuentaResultados)
			{
				var nResultados=data.numero_resultados;
			}
			
			// TODO: Solo mostramos la navegación de resultados si hay más de una página.
	//			if( nResultados > selector.getPropiedad('maxResults') )
	//			{
					//$(this).showNavigation();
	//			}
	
			$(this).find('.exportarResultados').unbind();
			$(this).find('.exportarResultados').bind('click', exportarResultados);

			var idSelector=$(this).parent().attr('id');

			// Asignamos los eventos de anterior y siguiente
			$(this).find('.anterior').unbind();
			$(this).find('.anterior').bind('click', function()
			{
				cambiaPosicion(idSelector, false);
			});

			$(this).find('.siguiente').unbind();
			$(this).find('.siguiente').bind('click', function()
			{
				cambiaPosicion(idSelector, true);
			});

		}
		else
		{
			labelExportarResultados.hide();
			$(this).find('.enlacesNavegacion').fadeOut();
		}

		if(onReady)
		{
			var idselector=neptuno.getAttrData($(this).attr("id"), "idselector");
			onReady(idselector);
		}
	};
	
	/**
            grid
         **/
  $.fn.grid=function(callerSettings)
	{
		/**
			settings
		**/
		settings=$.extend(
		{
			actions: null,
			idselector: null
		}, callerSettings || {});
		
    console.log('1');
		var grid=$(this);

	        grid.attr("id", settings.idselector+"_Grid");
		var idGrid=$(this).attr("id");

		neptuno.logconsola.Log(idGrid);
		neptuno.logconsola.MostrarObjeto(settings.actions);

		if(neptuno)
		{
		    // Guardamos los parámetros
		    neptuno.setAttrDataObject(idGrid, "actions", settings.actions);
		    neptuno.setAttrData(idGrid, "idselector", settings.idselector);
		}
		
		$.ajax({
			url: "/neptuno/libjs/jquery_ender_grid/html/grid.htm", 
			async : false,
			success:function(respuesta)
			{  
				load_css("/neptuno/libjs/jquery_ender_grid/css/grid.css");
				grid.html(respuesta);				
			}
                    });
        }; // $.fn.grid

	/**************************************************************************
	 * Actualiza el texto de la navegación de resultados.
	 * @function calculaResultadosMostrados
	 *************************************************************************/
	$.fn.calculaResultadosMostrados=function(idSelector)
	{

		var pos=parseInt(neptuno.getAttrData(idSelector, "pos"));
		var maxResults=parseInt(neptuno.getAttrData(idSelector, "maxResults"));
		var numero_resultados=parseInt(neptuno.getAttrData(idSelector, "numero_resultados"));


		



		neptuno.logconsola.Log(pos+" "+maxResults+" "+numero_resultados);

		if((pos+maxResults) > numero_resultados)
		{
			var quitarResultados=(pos+maxResults)-numero_resultados;

			if(quitarResultados>0)
			{
				resultadosMostrados=maxResults-quitarResultados;
			}
			else
			{
				resultadosMostrados=maxResults;
			}

		}
		else
		{
			resultadosMostrados=maxResults;
		}

		return parseInt(resultadosMostrados);
	}; // calculaResultadosMostrados

	/**************************************************************************
	 * actualizaTextoResultados
	 * Actualiza el texto de la navegación de resultados.
	 *************************************************************************/	
	$.fn.actualizaTextoResultados=function()
	{
		var selector=$(this).parent();

		if(!selector.hasClass('Selector') )
		{
			selector=$(this).parent().parent();
			var grid=selector.find(".ResultadoBusqueda");

			var resultadosMostrados=grid.calculaResultadosMostrados(selector.attr('id'));
			var bloqueTextoResultados=grid.find('.navegacionResultados').find('.textoResultados');
		}
		else
		{
			var resultadosMostrados=$(this).calculaResultadosMostrados(selector.attr('id'));
			var bloqueTextoResultados=$(this).find('.navegacionResultados').find('.textoResultados');
		}

		var pos=parseInt( neptuno.getAttrData(selector.attr('id'), 'pos') );
		var numero_resultados=parseInt( neptuno.getAttrData(selector.attr('id'), "numero_resultados") );

		var inicio=parseInt(pos+1);
		var _final=pos+resultadosMostrados;
		var total=numero_resultados;
			
		bloqueTextoResultados.html("Resultados "+inicio+" a "+_final+" de "+total);
		bloqueTextoResultados.show();

		if(pos==0 && (pos+resultadosMostrados)>=numero_resultados )
		{
			selector.find(".siguiente").hide();
		}

		if(numero_resultados==0)
		{
			bloqueTextoResultados.hide();
		}
			
	} // $.fn.actualizaTextoResultados

	
	/**************************************************************************
	 * getHTMLResultado
	 * Genera dinámicamente el HTML de un resultado de búsqueda.
	 * 
	 * campofiltrado: booleano que indica cual es el campo por el que filtramos
	 * la búsqueda y que no se ha de mostrar.
	 *************************************************************************/	
	var getHTMLResultado=function(objeto, pos, campofiltrado, acciones, cabeceras)
	{		
		var str="";
		
		if (pos == 0) {
			str += "<div class=\"FilaCabeceraResultado\">";
			//for(prop in objeto)
			
			for (var i = 0; i < objeto.length; i++) {
				//if ((prop!="id") && (prop!=campofiltrado))
				if (cabeceras[i] != "id" && cabeceras[i] != campofiltrado) {
					//str+="<div class=\"CabeceraResultado "+toIndice(prop)+"\">"+prop+"</div>";
					str += "<div class=\"CabeceraResultado " + cabeceras[i] + "\">" + objeto[i] + "</div>";
				}
				 
					
			}
			str += "</div>";
		}
		else {
		
			var columna_id = cabeceras.indexOf("id");
			str += "<div class=\"FilaResultado\" idSeleccionadoBusqueda=\"" + objeto[columna_id] + "\">";
			
			var posicionActual = 0;
			var SeleccionadoImpreso = false;
			
			//for (val in objeto)
			for (var i = 0; i < objeto.length; i++) {
				var val = objeto[i];
				if ((cabeceras[i] != "id") && (cabeceras[i] != campofiltrado)) {
					var textoClase = toIndice(val);
					
					if (!SeleccionadoImpreso) {
						if (val == '') {
							val = 'seleccionar';
						}
						
						texto = "<span class=\"Boton\">" + val + "</span>";
						str += "<div class=\"ColumnaResultado ColumnaSeleccionar " + textoClase + "\">" + texto + "</div>";
						SeleccionadoImpreso = true;
					}
					else {
						texto = val;
						str += "<div class=\"ColumnaResultado " + textoClase + "\">" + texto + "</div>";
					}
				}
				
				posicionActual++;
			}
		}		
		/**********************************************************************
			Nueva característica, el parámetro resultsActions, va a permitir
			añadir al selector, enlaces con acciones en los resultados.
		**********************************************************************/
		if(acciones!=null && pos!=0)
		{
			var nActions=acciones.length;
			
			for(ACCIONi=0;ACCIONi<nActions;ACCIONi++)
			{
				var accion=acciones[ACCIONi];
				var etiqueta=accion.label;
				var clase=accion.clase;
				
				str+="<div class=\"Boton ColumnaResultado ColumnaAccion "+clase+"\">"+etiqueta+"</div>";
			} // recorremos las acciones de resultados
		} 
		
		str+="</div>";
	
		return str;
	} // getHTMLResultado


	/**************************************************************************
	 * toIndice
	 *************************************************************************/
	var toIndice=function(texto)
	{
		// Reemplazamos las comillas
		var textoIndice=new String(texto);
		textoIndice=textoIndice.replace(/\"/g, "\'");		
		textoIndice=textoIndice.replace(/á/g, "a");		
		textoIndice=textoIndice.replace(/é/g, "e");		
		textoIndice=textoIndice.replace(/í/g, "i");		
		textoIndice=textoIndice.replace(/ó/g, "o");		
		textoIndice=textoIndice.replace(/ú/g, "u");		
		textoIndice=textoIndice.replace(/ /g, "_");
		textoIndice=textoIndice.toLowerCase();
		textoIndice="col_"+textoIndice;		
		
		return textoIndice;
	} // toIndice


}) (jQuery);