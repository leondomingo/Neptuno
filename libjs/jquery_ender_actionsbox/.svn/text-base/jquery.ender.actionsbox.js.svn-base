(function($)
{
	var settings=null;
	var PrimerValor="";

	$.fn.getPrimerValor=function()
	{
		return $(this).attr('primervalor');
	}
	     
	$.fn.actionsbox=function(callerSettings)
	{
		/**
			settings
		**/
		settings=$.extend(
		{			
			campos: []/*[{label:'search', value:'', nohidden:false}]*/,
			htmlactions: '',
			id: -1, 
			onReady: null,
			accionesocultar: null,
			loadactions: false,
			load: null,
			showdetails: null,
			fullScreen: false
		}, callerSettings || {});
		
		var actionsbox=$(this);
		var selector=actionsbox.parent();
	        actionsbox.attr("id", selector.attr("id")+"_ActionsBox");
		
		if(neptuno)
		{
		    // Guardamos los parámetros
		    neptuno.setAttrDataObject($(this).attr('id'), "campos", settings.campos);
		}
		
		$.ajax({
			url: "/neptuno/libjs/jquery_ender_actionsbox/html/actionsbox.htm", 
			async : true,
			success:function(respuesta)
			{  
				actionsbox.html(respuesta);
		                load_css("/neptuno/libjs/jquery_ender_actionsbox/css/actionsbox.css");
				
				if(settings.fullScreen)
				{
			                load_css("/neptuno/libjs/jquery_ender_actionsbox/css/fullScreenMode.css");
					
					// Hemos de reposicionar la accion activa
					var accionActiva=selector.find(".AccionActiva");
					var accionActivaFullScreen=actionsbox.find(".AccionActivaFullScreen");
					
					accionActiva.remove();
					accionActivaFullScreen.addClass("AccionActiva");
				}

				neptuno.logconsola.Log("constructor searchbox::"+actionsbox.parent().attr('id') );

				// Insertamos las acciones
				actionsbox.find('.Acciones').html(settings.htmlactions);
				
				// Por defecto muestra los detalles
				actionsbox.find('.LineaOcultableSeleccionado').fadeIn();
				actionsbox.find('.Detalles').html("ocultar detalles");
				actionsbox.find('.Detalles').attr("oculto", "false");								

				actionsbox.fadeIn();
				
				var pos=0;
				var str="";
				var ncampos=settings.campos.length;
				
				for(LABELi=0;LABELi<ncampos;LABELi++)
				{
					var campoActual=settings.campos[LABELi];
					
					var campo={};
					campo.nombre=campoActual.label;
					campo.valor=campoActual.value;
					
					if(PrimerValor=="")
					{
						PrimerValor=campo.valor;
					}
					
					var seleccionado=(pos==0);
					
					str+=getHTMLDetalle(campo, seleccionado);
					pos++;
				}
				
				actionsbox.attr('primervalor', PrimerValor);
				
				var detalles=actionsbox.find('.DetallesRegistro');
				detalles.find('.LineaSeleccionado').html('');
				detalles.prepend(str);
				
				actionsbox.fadeIn();
				actionsbox.attr('tmpidseleccionado', settings.id);
				
				if( settings.loadactions)
				{
					// Cargamos las acciones
					eval( settings.load+"();");
					
					if( settings.accionesocultar )
					{
						var nAccionesOcultar=settings.accionesocultar.length;
						for(ACCIONi=0;ACCIONi<nAccionesOcultar;ACCIONi++)
						{
							for(ACCIONi=0;ACCIONi<respuesta.length;ACCIONi++)
							{
								var bloqueAccion=bloqueAcciones.find("."+settings.accionesocultar[ACCIONi]);
								bloqueAccion.unbind('click');
								bloqueAccion.fadeOut();
							} // Recorriendo las acciones no permitidas
						}
					}
				}

				//alert(settings.showdetails);

				if(settings.showdetails)
				{
					actionsbox.find('.Detalles').unbind();
					actionsbox.find('.Detalles').bind('click', settings.showdetails);
				}
				
				// Llamamos a la función una vez que el componente está cargado
				if(settings.onReady)
				{
					settings.onReady();
				}
			}
		});
	};


 	/**************************************************************************
	 * actionsbox::getHTMLDetalle
	 * Genera dinámicamente el HTML de un detalle del registro.
	 * 
	 * seleccionado: booleano indicando si el detalle es ocultable o no.
	 *************************************************************************/	
	var getHTMLDetalle=function(objeto, seleccionado)
	{
		// No mostramos el detalle si no tiene valor
		if(objeto.valor=="")
		{
			return "";
		}
		
		var str="";
		var CadenaClaseOcultable="";
		
		if(!seleccionado)
		{
			CadenaClaseOcultable=" LineaOcultableSeleccionado";
		}
	
		str="<div class=\"LineaSeleccionado"+CadenaClaseOcultable+"\">";
		str+="<div class=\"LabelSeleccionado\">"+objeto.nombre+":</div>";
		str+="<div class=\"CampoSeleccionado\">"+objeto.valor+"</div>";
		str+="</div>";

		return str;		
	}; // getHTMLDetalle

 
 }) (jQuery);
