var edicionPorDefecto = '/neptuno/sw/datosRegistro.py';

(function($)
{
	$.fn.listaJSON = function(paramJson, fFila, fFinal)
	{
		$("head").append("<link>");
    	css = $("head").children(":last");
    	css.attr({
      		rel:  "stylesheet",
      		type: "text/css",
      		href: "/neptuno/libjs/ender_listaJSON/estilos.css"
    	});

		var cabecera = paramJson.columnas;
		var datos = paramJson.datos;
		var claseFila ='';
		
		
		$(this).hide();
		$(this).append('<div class="resultados"></div>');
		
		$(this).nuevaFila(cabecera,cabecera, 'cabecera',null);
		
		
		for(var i=0;i<datos.length;i++)
		{
			$(this).nuevaFila(datos[i],cabecera,claseFila,fFila);
		}

		if(typeof fFinal=='function')
		{
			fFinal();	
		}else if(typeof fFinal=='string')
		{
			eval(fFinal);
		}		
		
		$(this).slideDown();
		
	}
	
	$.fn.ajustarAltoFilas = function(alto, excluir_cabeceras, color)
	{
		if(color == '' || color == null) color = '#dde';
		if (excluir_cabeceras) 
		{
			$(this).find('.fila').not('.cabecera, .cabecera .div').height(alto);
			$(this).find('.fila .celda').not('.cabecera, .cabecera .div').height(alto-8);
		}
		else 
		{
			$(this).find('.fila').height(alto);
			$(this).find('.fila .celda').height(alto-8);
		}
			

	}
	
	
	$.fn.ajustarAnchoCeldas = function(n_elementos)
	{
	  if(n_elementos == null || n_elementos == undefined || n_elementos < 1)
	  {
	    n_elementos = $(this).find('.cabecera').find('.celda').length;
	  }
	  var ancho_celda = ((100 / (n_elementos))|0)-1;
    $(this).find(".celda").css('width',ancho_celda+'%');
	}
	
	$.fn.nuevaFila = function(fila, columnas,claseFila,fFila)
	{
		if(!claseFila || claseFila=="undefined") claseFila='';
		
		var n_columnas= fila.length;
		
		var columna_id = columnas.indexOf('id');
		
		var html = "<div class=\"fila "+claseFila+"";
		if(claseFila != 'noHover') html += " filaHover";		
		html+= "\" idObjeto='"+fila[columna_id]+"' alt='"+fila[columna_id]+"'";
		html+=">";
	
		
		
		for(var j = 0; j< n_columnas; j++)
		{
			if(j!=columna_id)
			{
				html += "<div class=\"celda";
				if(claseFila != 'noHover') html += " celdaHover";
				html += "\" id_columna=\""+columnas[j]+"\"";
				html += ">"+fila[j]+"</div>";
			}						
		}
		
		html+="</div>";

		$(this).find(".resultados").append(html);
		
		if(typeof fFila=='function')
		{
			fFila();	
		}else if(typeof fFila=='string')
		{
			eval(fFila);
		}

	}


	$.fn.eliminarFila = function(id)
	{
		$(this).find('.fila[idObjeto="'+id+'"]').slideUp().remove();
	}
	
	$.fn.nuevoBoton = function(nombreBoton, textoBoton, funcionBoton, id_fila)
	{
		if (id_fila > 0) 
		{
			$(this).find('.fila[idObjeto="' + id_fila + '"]').not('.cabecera').append('<div class="boton_fila ' + nombreBoton + '">' + textoBoton + '</div>');
		}
		else
		{
			$(this).find('.fila').not('.cabecera').append('<div class="boton_fila ' + nombreBoton + '">' + textoBoton + '</div>');
		} 
			
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
	
	$.fn.desactivarBoton = function(nombreBoton)
	{
		
		$(this).find('.'+nombreBoton).unbind('click');
	}

	$.fn.activarBoton = function(nombreBoton)
	{
		$(this).find('.'+nombreBoton).unbind('click');
		$(this).find('.'+nombreBoton).bind('click',function(){$(this).trigger('clickea');});
	}



	
	
	

})(jQuery);


// parche para que indexOf funcione en la mierda del IE
if(!Array.indexOf){
    Array.prototype.indexOf = function(obj){
        for(var i=0; i<this.length; i++){
            if(this[i]==obj){
                return i;
            }
        }
        return -1;
    }
}