(function($) {
	
	var propiedades;
	var nombreprimeraClase='';

  	$.fn.ContentLoader = function(parametros) {
  
		propiedades = $.extend({
			idSeleccionado: null
		}, parametros || {});
		
		this.bloqueEnlaces=$(this).find('.EnlaceClases');
		this.bloqueEnlaces.html('');
		
		var usuarioNeptuno=neptuno.obtenerusuarioNeptuno();
		var datosNavegacion=neptuno.obtenerDatosNavegacion();

		this.fullScreen=(datosNavegacion.modo=="full" ? true : false);
		listaClasesProhibidas=null;		
		
		if(!this.fullScreen)
		{
							// Permitimos no pasar el nombre de las claves, esto garantiza compatibilidad con

							// versiones anteriores del sistema.
              var primeraClase = true;
              
							for(var i=0;i<ClasesMain.nombres.length;i++)
							{
							  var clave =i;
								if(primeraClase)
								{
									primeraClase=false;
									nombreprimeraClase=ClasesMain.nombres[clave];
								}
								
								var nombreClase=ClasesMain.nombres[clave];
								var HTMLEnlace=$(this).getHTMLClase(nombreClase);
								
								this.bloqueEnlaces.append(HTMLEnlace);
								
								// Enlazamos 
								this.bloqueEnlaces.find("."+nombreClase+"").unbind('click');
								this.bloqueEnlaces.find("."+nombreClase+"").bind('click', CargarAccionClase);	
							}


		}
		else
		{
			// Segundo modo sistema
			load_css("./css/fullScreenMode.css");
		}
		
	}; 
	
	/**
		cargaAccionClase
	 */
	$.fn.cargaAccionClase=function(nombreclase)
	{
		$(this).CargaAccionClase(nombreclase);
		$('.EnlaceClase').removeClass('tabSeleccionado');
		$('.'+nombreclase).addClass('tabSeleccionado');
	}; // cargaAccionClase

	/**************************************************************************
	 * ContentLoader::$.fn.getHTMLClase
	 *************************************************************************/	
	$.fn.getHTMLClase=function(NombreClase, LabelClase)
	{
		
		if(!LabelClase)
		{
			var LabelClase=NombreClase;
		}
		
		var str="";
		var CadenaClaseOcultable="";
		
		str	="<div class=\"LineaClase\">";
		str+="<div class=\"EnlaceClase "+NombreClase+"\" NombreClase=\""+NombreClase+"\" ><div class=\"TextoEnlaceClase\">"+LabelClase;
		// chorradilla ... quitar si molesta :)
//		if(NombreClase == 'labs') str+= "<img src=\"./images/labs_icon.png\" style=\"height: 23px; position: absolute;\"/>";
		// fchorradilla
		str+="</div></div>";
		str	+="</div>";

		return str;		
	}; // getHTMLClase

		
	/**************************************************************************
	 * ContentLoader::CargaAccionClase
	 *************************************************************************/	
	$.fn.CargaAccionClase=function(NombreClase)
	{
		//InicializaBarraProgreso();
    
		var selector=$(this);
		var bloqueAccion=$(this).find('.AccionClase');
		bloqueAccion.fadeOut();
		//bloqueAccion.hide();
		
		$.ajax({
			url: "./clases/"+NombreClase+"/"+NombreClase+".htm", 
			async : false,
			cache:false,
			success:
				function(respuesta)
				{
					
					var datosNavegacion=neptuno.obtenerDatosNavegacion();

            //					neptuno.logconsola.Clear();
//					neptuno.logconsola.Log("*** Clase "+NombreClase+" ***");
					
					bloqueAccion.html(respuesta);

					// Si hay un selector hemos de añadirle la clase de 'selectorPrincipal'
					$('.Selector:first').addClass('selectorPrincipal');

					if(datosNavegacion.clase!='' && NombreClase!=datosNavegacion.clase)
					{
						// Si cambiamos de clase, el id anterior ya no tiene sentido
						// tampoco la acción...
						datosNavegacion.id=-1;
						datosNavegacion.accion='';
						datosNavegacion.modo='';
					}
					
					neptuno.setNavegacion(NombreClase, datosNavegacion.id, datosNavegacion.accion, datosNavegacion.modo);						

					eval("Carga"+NombreClase+"();");
					bloqueAccion.fadeIn(); 
					//CierraBarraProgreso();
				},
			error:
				function(respuesta)
				{
					CierraBarraProgreso();
					neptuno.cntMsgs.ShowError(respuesta, "Error cargando acciones de "+NombreClase);
					
					// Cargamos por defecto la acción de personal
					$(selector).CargaAccionClase("personal");
				}
			}); 
		
		
	}; // getHTMLClase
  
  
})(jQuery);

/**************************************************************************
* CargarAccionClase
*************************************************************************/	
function CargarAccionClase()
{
	var idBloque=$(this).parent().parent().parent().attr('id');
	var NombreClase=$(this).attr('NombreClase');
	$('.EnlaceClase').removeClass('tabSeleccionado');
	$(this).addClass('tabSeleccionado');
	$("#"+idBloque).CargaAccionClase(NombreClase);
} // CargarAccionClase
