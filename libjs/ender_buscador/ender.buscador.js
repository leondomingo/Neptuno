var rutaBaseBuscador = '/neptuno/';
 
(function($)
{
	$.fn.buscador = function(sw,params,fFila,fFinal, fSalidaBuscador)
	{
		var lugar = $(this);
		
		console.log('********++');
		console.log(params.fEdicionCampos);
		
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
			lugar.find('.buscador').data('params',params);
			lugar.find('.buscador').data('fFila',fFila);
			lugar.find('.buscador').data('fFinal',fFinal);
			lugar.find('input').keyup(function(e) {if(e.keyCode == 13) {$(this).parent().lanzaBuscador();}});
			
			lugar.find('.botonBuscador.buscar').bind('clickea',$(this).lanzaBuscador);
			lugar.activarBoton('botonBuscador.buscar');


			
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
		lugar.parents('.buscador').desactivarBoton('botonBuscador.buscar');
		
		var url = $(this).parents('.buscador').attr('url');
		var fFila = $(this).parents('.buscador').data('fFila');
		var fFinalPrev = $(this).parents('.buscador').data('fFinal');
		
		var params = $(this).parents('.buscador').attr('params').replace(/'/g,"\"");
    	 
		eval("var data =" + params);
		
		params = $(this).parents('.buscador').data('params');
		console.log('+++++++');
		console.log(params.fEdicionCampos);
		
		
		if(typeof fFinalPrev == 'function')
		{
			var fFinal = function(lug)
			{
				fFinalPrev();
				if(lug) lugar = lug;
				lugar.parents('.buscador').activarBoton('botonBuscador.buscar');	
			}
		}
		else
		{
			var fFinal = function(lug)
			{

			   if(lug) lugar = lug;
			   lugar.parents('.buscador').activarBoton('botonBuscador.buscar'); 
			}
		}
		

		
		data.busqueda = $(this).parents('.buscador').find('.textoBusqueda').val();
		
		$(this).parents('.buscador').find('.resultadosBuscador').listaPaginada(url,data,fFila,fFinal,true,true);
		$(this).parents('.buscador').find('.resultadosBuscador').data('fEdicionCampos',params.fEdicionCampos);
    console.log("entrando en lanzaBuscador");
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
