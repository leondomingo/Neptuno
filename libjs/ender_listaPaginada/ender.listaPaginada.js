$("head").append("<link>");
css = $("head").children(":last");
css.attr({
		rel:  "stylesheet",
		type: "text/css",
		href: "/neptuno/libjs/ender_listaPaginada/estilos.css"
});



(function($)
{
	var imagen_carga = '/neptuno/libjs/ender_listaPaginada/load.gif';
	var imagen_next = '/neptuno/libjs/ender_listaPaginada/next.png';
	var imagen_previous = '/neptuno/libjs/ender_listaPaginada/previous.png';
	
	$.fn.listaPaginada = function(sw, params, fFila, fFinal)
	{
		var lugar = $(this);
		var parametros = JSON.stringify(params).replace(/"/g,"'");

		lugar.html('');
		lugar.append('<div class="listaPaginada" url="'+sw+'" params="'+parametros+'"></div>');
		lugar.children('.listaPaginada').data('fFila',fFila);
		lugar.children('.listaPaginada').data('fFinal',fFinal);
		
		lugar.append('<div class="imagen_carga"><img src="'+imagen_carga+'" /><div>Procesando ...</div></div>');
          
		$.ajax(
		{
			url:sw,
			data:params,
			async: true,
			type: "POST",
			cache: false,
			dataType: "json",
			success:function(res)
			{
				 
		
				lugar.find('.listaPaginada').html('<div class="exportar" onclick="$(this).exportarCSVListaPaginada()">exportar</div><div class="paginacion"></div>');
				
				lugar.find('.listaPaginada').eq(0).listaJSON(res,fFila,fFinal);
				lugar.find('.listaPaginada').append('<div class="numero_resultados">Número de resultados: '+res.numero_resultados+'</div>');
				
				if(res.numero_resultados > params.limite_resultados)
				{
					var n_pagina = (params.pos/params.limite_resultados)+1;
					var total_paginas = ((res.numero_resultados / params.limite_resultados)|0)+1;
					
					lugar.find('.listaPaginada').find('.paginacion').append('<div class="texto_paginas">Página </div>');
					if(n_pagina > 1)
					{
						lugar.find('.listaPaginada').find('.paginacion').append('<div class="boton_anterior"  onclick="$(this).anteriorPagina();"><img src="'+imagen_previous+'"/></div>');						
					}
					lugar.find('.listaPaginada').find('.paginacion').append('<div class="n_pagina">'+n_pagina+'</div>');
						
					if(n_pagina < total_paginas)
					{
						lugar.find('.listaPaginada').find('.paginacion').append('<div class="boton_siguiente" onclick="$(this).siguientePagina();"><img src="'+imagen_next+'"/></div>');	
					}
					
					
					lugar.find('.listaPaginada').find('.paginacion').append('<div class="texto_paginas">de '+total_paginas+'</div>');					
					

					//lugar.find('.listaPaginada').find('.paginacion').html(n_paginas);
				}
				

							
			},
			complete:function()
			{
				lugar.find('.imagen_carga').slideUp();
			},
			error: function(XMLHttpRequest, textStatus, errorThrown)
			{
				lugar.find('.listaPaginada').append('<div class="mensaje_error">No se ha podido realizar la carga de la lista</div>');
				lugar.find('.listaPaginada').append('<div class="mensaje_error">URL:'+sw+'</div>');
				lugar.find('.listaPaginada').append('<div class="mensaje_error">Parametros:'+JSON.stringify(params)+'</div>');
				lugar.find('.listaPaginada').append('<div class="mensaje_error">Mensaje:'+textStatus+' // '+XMLHttpRequest.status+'</div>');
			}
			
			
			
		}
		);
		
	}


	$.fn.eliminarElementoListaPaginada = function(id)
	{
		$(this).eliminarFila(id);

		var texto = $(this).find('.listaPaginada').find('.numero_resultados').html().split(':');

		$(this).find('.listaPaginada').find('.numero_resultados').html('Número de resultados: '+((1*texto[1])-1));
		
		
		
		
	}

	$.fn.exportarCSVListaPaginada = function()
	{
		var url = $(this).parents('.listaPaginada').attr('url');
		eval("var data = "+$(this).parents('.listaPaginada').attr('params').replace(/'/g,"\""));
		data.generar_csv = true;
		var campos = '';
		if(data.campos != undefined)
		{
			campos = (data.campos);
			data.campos = undefined;
		}
			
		var param_str  = jsonToGet(data);
		url += '?'+param_str;
		if(campos != '')
		{
			url +='&campos='+campos;
		}
		
		var newWindow = window.open(url, '_blank');
	}
	
	$.fn.ordenCabeceras = function()
	{
		if($(this).hasClass('listaPaginada'))
			var lugar = $(this)
		else
			var lugar = $(this).find('.listaPaginada').parent();
			
		lugar.find('.cabecera').bind('click',$(this).ordena);
	}
	
	$.fn.ordena = function(e)
	{
		
		var parametro = $(e.target).attr('id_columna');
		var url = $(this).parents('.listaPaginada').attr('url');
		var fFila = $(this).parents('.listaPaginada').data('fFila');
		var fFinal = $(this).parents('.listaPaginada').data('fFinal');
		var params = $(this).parents('.listaPaginada').attr('params').replace(/'/g,"\"");
		
		eval("var data =" + params);
		
		var lugar = $(this).parents('.listaPaginada').parent();
		
		if(data.busqueda != null)
		{
			data.busqueda += '+'+parametro.split(' ').join('').toLowerCase();
		}
		else
		{
			data.busqueda = '+'+parametro.split(' ').join('').toLowerCase();
		}
			
		$(this).parents('.listaPaginada').remove();
				
		
		
		lugar.listaPaginada(url,data,fFila,fFinal);		
		
	}
	
	$.fn.anteriorPagina = function()
	{
		var url = $(this).parents('.listaPaginada').attr('url');
		var fFila = $(this).parents('.listaPaginada').data('fFila');
		var fFinal = $(this).parents('.listaPaginada').data('fFinal');
		var params = $(this).parents('.listaPaginada').attr('params').replace(/'/g,"\"");
		
		eval("var data =" + params);
		
		var lugar = $(this).parents('.listaPaginada').parent();
		
		$(this).parents('.listaPaginada').remove();
		
		data.pos = (1*data.pos)-(1*data.limite_resultados);
		
		if(data.pos<0) data.pos = 0;
		
		lugar.listaPaginada(url,data,fFila,fFinal);		
		
	}


	
	$.fn.siguientePagina = function()
	{
		var url = $(this).parents('.listaPaginada').attr('url');
		var fFila = $(this).parents('.listaPaginada').data('fFila');
		var fFinal = $(this).parents('.listaPaginada').data('fFinal');
		var params = $(this).parents('.listaPaginada').attr('params').replace(/'/g,"\"");
		
		eval("var data =" + params);
			
		var lugar = $(this).parents('.listaPaginada').parent();
		
		$(this).parents('.listaPaginada').remove();
		
		data.pos = (1*data.limite_resultados)+(1*data.pos);			
		if(data.pos>=data.numero_resultados) data.pos = 0;	
		
		lugar.listaPaginada(url,data,fFila,fFinal);		
		
	}
	

	
})(jQuery);

function jsonToGet(json)
{
	var str_get = JSON.stringify(json).replace(/,/g,"&").replace(/ /g,"").replace(/:/g,"=").replace(/{/g,'').replace(/}/g,'').replace(/"/g,'').replace('(','').replace(')','');
	return str_get;
}
