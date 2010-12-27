var rutaBaseBuscador = '/neptuno/';
 
(function($)
{
	$.fn.buscador = function(sw,params,fFila,fFinal, fSalidaBuscador)
	{
		var lugar = $(this);
		
		var parametros = JSON.stringify(params).replace(/"/g,"'");
		$("head").append("<link>");
    	css = $("head").children(":last");
    	css.attr({
      		rel:  "stylesheet",
      		type: "text/css",
      		href: rutaBaseBuscador+"libjs/ender_buscador/estilos.css"
    	});
		
		
		lugar.load(rutaBaseBuscador+'libjs/ender_buscador/plantilla.htm',null,function()
		{
			lugar.find('.buscador').attr('url',sw);
			lugar.find('.buscador').attr('params',parametros);
			
			lugar.find('.buscador').data('fFila',fFila);
			lugar.find('.buscador').data('fFinal',fFinal);
			lugar.find('input').keyup(function(e) {if(e.keyCode == 13) {$(this).parent().lanzaBuscador();}});
			
			lugar.find('.botonBuscador').bind('clickea',$(this).lanzaBuscador);
			lugar.activarBoton('botonBuscador');


			
			if(typeof fSalidaBuscador=='function')
			{
				
				fSalidaBuscador(lugar);	
			}else if(typeof fSalidaBuscador=='string')
			{
				
				eval(fSalidaBuscador);
			}				
			
		});
		
	

	}

	$.fn.lanzaBuscador = function()
	{
		var lugar = $(this);
		lugar.parents('.buscador').desactivarBoton('botonBuscador');
		
		var url = $(this).parents('.buscador').attr('url');
		var fFila = $(this).parents('.buscador').data('fFila');
		var fFinalPrev = $(this).parents('.buscador').data('fFinal');
		
		var params = $(this).parents('.buscador').attr('params').replace(/'/g,"\"");
	 
		eval("var data =" + params);
		
		if(typeof fFinalPrev == 'function')
		{
			fFinal = function()
			{
				fFinalPrev();
				lugar.parents('.buscador').activarBoton('botonBuscador');	
			}
		}
		else
		{
			fFinal = fFinalPrev+";$(this).parents('.buscador').activarBoton('botonBuscador');";
		}
		

		
		data.busqueda = $(this).parents('.buscador').find('.textoBusqueda').val();
		
		$(this).parents('.buscador').find('.resultadosBuscador').html('').listaPaginada(url,data,fFila,fFinal);
		

	}
	
	$.fn.nuevoBotonBuscador = function(nombreBoton, textoBoton, funcionBoton)
	{
		
		$(this).find('.cajaBuscador').append('<div class="botonBuscador '+nombreBoton+'">'+textoBoton+'</div>');

		if(typeof(funcionBoton) == 'function')
		{
			$(this).find('.'+nombreBoton).unbind('clickea').bind('clickea',funcionBoton);
			$(this).activarBoton(nombreBoton);
		}
		else
		{
			$(this).find('.'+nombreBoton).unbind('clickea').bind('clickea',function(){eval(funcionBoton);});
			$(this).activarBoton(nombreBoton);
		}		
	}	

})(jQuery);
