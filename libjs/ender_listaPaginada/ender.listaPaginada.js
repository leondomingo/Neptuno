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
  var metodos_listaPaginada =
  {
  	init:function(p)
  	{
      
      if($(this).attr('listaInicializada')!= "true")
      {
        
        if(p.sw)
        { 
           var sw = p.sw;
        }
        else
        {
           var sw = '/neptuno/sw/buscar.py';
        }

        if(p.sw_borrar)
        {
          var sw_borrar= p.sw_borrar;
        }
        else
        {
          var sw_borrar = "/neptuno/sw/borrar.py";
        }

        if(p.sw_guardar)
        {
          var sw_guardar= p.sw_guardar;
        }
        else
        {
          var sw_guardar = '/neptuno/sw/guardarRegistro.py';
        }        

        if(p.sw_datosRegistro)
        {
          var sw_datosRegistro= p.sw_datosRegistro;
        }
        else
        {
          var sw_datosRegistro = '/neptuno/sw/datosRegistro.py/raw';
        }     

        var params = p.params;
        var fFila = p.fFila;
        var fFinal = p.fFinal;
        $(this).data("params",params);
        $(this).data("sw",sw);
        $(this).data("sw_borrar",sw_borrar);
        $(this).data("sw_guardar",sw_guardar);
        $(this).data("sw_datosRegistro",sw_datosRegistro);
        $(this).data('fFila',fFila);
        $(this).data('fFinal',fFinal);
        $(this).data('borrable',p.borrable);
        $(this).data('editable',p.editable);
        $(this).data('campos',p.params.camposEdicion);
        //$(this).data('fEdicionCampos',p.params.fEdicionCampos);

        $(this).attr('listaPaginada',true);
    	  $(this).attr('listaInicializada',true);
    		var lugar = $(this);
    		var parametros = JSON.stringify(params).replace(/"/g,"'");
    
    		lugar.html('');
    		lugar.append('<div class="listaPaginada" url="'+sw+'" params="'+parametros+'"></div>');
    		lugar.children('.listaPaginada').data('fFila',fFila);
    		lugar.children('.listaPaginada').data('fFinal',fFinal);
    		
    		lugar.append('<div class="imagen_carga"><img src="'+imagen_carga+'" /><div>Procesando ...</div></div>');
             
        $(this).listaPaginada('cargar');
   
    	}
  		else
  		{
  		  $(this).listaPaginada('cargar');
  		}
  	},
  	cargar:function()
  	{
  	  
  	  var sw = $(this).data("sw");
  	  var params = $(this).data("params");
  	  var fFinal = $(this).data("fFinal");
  	  var fFila = $(this).data("fFila");
  	  var borrable = $(this).data("borrable");
  	  var editable = $(this).data("editable");
  	  var lugar = $(this);

      if(borrable)
      {
        if(typeof(fFinal)=="function")
        {
          var fFinalOriginal = fFinal;
          fFinal = function()
          {
            fFinalOriginal(lugar);
            lugar.listaPaginada('botonBorrar');
          }
        }  
        else
        {
          fFinal = function()
          {
            lugar.listaPaginada('botonBorrar');
          }
        }
      }
      if(editable)
      {
          var fFinalOriginalEditar = fFinal;
          fFinal = function()
          {
            fFinalOriginalEditar(lugar);
            lugar.find('.fila').not('.cabecera').find('.celda').not('.boton').bind('click',function(){$(this).listaPaginada('editarRegistro')})
          }
        
      }      
  	  
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
        
  	},  	
  	botonBorrar:function()
  	{
  	  var lugar = $(this);
  	  $(this).find('.fila').not('.cabecera').append('<div class="celda boton borrar">borrar</div>');
  	  $(this).find('.fila').find('.boton.borrar').bind('click',function(){$(this).listaPaginada("borrarRegistro");});
  	},
  	borrarRegistro:function()
  	{
  	   var lugar = $(this).parents('[listaPaginada]');
  	   var idObjeto = $(this).parents('.fila').attr('idObjeto');
       var params = lugar.data('params');
       var sw_borrar = lugar.data('sw_borrar');
       var datos = {}
       datos.tabla = params.tabla;
       datos.id_usuario = params.id_usuario;
       datos.id_sesion = params.id_sesion;
       datos.id = idObjeto;
       $('.confirmarBorrar').remove();
       $('body').append('<div class="confirmarBorrar">¿Está seguro de que desea borrar el registro?</div>');
       $('.confirmarBorrar').dialog();
       $('.confirmarBorrar').dialog('option','buttons',
        {
          "Cancelar":function(){$('.confirmarBorrar').dialog('close');},
          "Borrar":function()
          {
            $.ajax(
            {
              url:sw_borrar,
              dataType:'json',
              data:datos,
              success:function(){lugar.listaPaginada('carga');}
            }
            );
            $('.confirmarBorrar').dialog('close'); 
          }
        });
                	   
  	},
    nuevoRegistro:function()
    {

      var ventana=$(document).find('.nuevoCampoListaPaginada');
      if(ventana.lenght>0)
      {
        ventana.html('');
      }
      else
      {
        $(this).append('<div class="nuevoCampoListaPaginada"></div>');
        var ventana=$(this).find('.nuevoCampoListaPaginada');
      }

      var campos = $(this).data('campos');

      var lista = $(this);

      campos.push({"nombre":"id","texto":"","valor":"null"});
      $(this).data('campos',campos);
      
      $(this).find('form.nuevoCampoListaPaginada').data('padre',$(this));
      
      for(var i=0;i<campos.length;i++)
      {
        var html = '<div class="campo  ';
        if(campos[i].texto==null || campos[i].texto=='') html += ' oculto ';
        if(campos[i].requerido == true) html += ' requerido ';
        html += '"';
        html += '>';
        html += '<div class="titulo">'+campos[i].texto+'</div>';
        html += '<div class="valor">';

        html += '<input id="'+campos[i].nombre+'" name="'+campos[i].nombre+'" value="'+campos[i].valor+'" "';
        if(campos[i].requerido == true) html+= " requerido=true ";
        html += '></input>';
        html += "</div>";
        html +='</div>';
        ventana.append(html);      
      }
      if($().wTooptip != undefined) ventana.find('.requerido .titulo').wTooltip({content:"Campo requerido", appendTip:ventana});
      ventana.find('#id_sesion, #id_usuario').hide();
      ventana.find('nuevoCampoListaPaginada').bind('submit',$(this).listaPaginada.enviarRegistro)
      ventana.dialog({ width: 600, title:"Evaluaciones" });
      ventana.dialog('option','buttons',
        {
          "Cancelar":function(){ventana.dialog('close');},
          "Guardar":function(){
                                $(this).data('ventana',ventana);
                                $(this).data('padre',lista);
                                $(this).listaPaginada('enviarRegistro');
                              }
        }
      );
      ventana.dialog('open');
      if(lista.data('fEdicionCampos')) lista.data('fEdicionCampos')();
       
      return ventana;
    },
    editarRegistro:function()
    {
      var padre = $(this).parents('[listaPaginada]');
      var params = padre.data('params');
      var idObjeto = $(this).parents('.fila').attr('idObjeto');
      $.ajax(
        {
          url:padre.data('sw_datosRegistro'),
          dataType:'json',
          data:
          {
            id_usuario:params.id_usuario,
            id_sesion:params.id_sesion,
            tabla:params.tabla,
            id:idObjeto
          },
          success:function(res)
          {
            var ventana = padre.listaPaginada('nuevoRegistro');
            for(campo in res)
            {
              ventana.find('#'+campo).val(res[campo]);
            }
          }
        }
      )
      
    },
    enviarRegistro:function ()
    {
      
      
      var lista = $(this).data('padre');
      var ventana = $(this).data('ventana');
         
      var campos = ventana.find('[id]').not('#id_usuario,#id_sesion,#tabla');
      var requeridos = ventana.find('[requerido="true"]');
      var errores = false;
      $('[requerido="true"]').each(function()
                                   {
                                      if($(this).val() =='')
                                      {
                                          $(this).css('background-color','#FAA'); 
                                          errores = true;
                                      }
                                   });
      if(!errores)
      {
        var data = {};
        data.id_usuario = ventana.find('#id_usuario').val();
        data.id_sesion = ventana.find('#id_sesion').val();
        data.tabla = ventana.find('#tabla').val();
  
        data.datos = "{";
        
        for(var i=0;i<campos.length;i++)
        {
          if($(campos[i]).val()!="null")
          {
            if(i>0) data.datos +=', '
            data.datos += '"'+$(campos[i]).attr('id')+'" : "'+$(campos[i]).val()+'"';
          }
        };
        data.datos += "}";      
        
  
        var sw_guardar = lista.data('sw_guardar');  
  
  
  
        ventana.dialog('close');
  
        $.ajax(
          {
            url:sw_guardar,
            method:'POST',
            dataType:'json',
            data:data,
            success:function()
            {
              lista.listaPaginada('cargar');
            },
          
          }
        );
      }
      else
      {
        alert('Rellene todos los campos indicados, por favor');
      }
    
    }
  
  }

  $.fn.listaPaginada = function( method ) 
  {
    if ( metodos_listaPaginada[method] ) 
    {

      return metodos_listaPaginada[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
      
    } 
    else  
    {
      
      // Si se le pasan los parámetros independientes, en vez de en un objeto
      // los convertimos al objeto correspondiente.
      // Se incluye este código para asegurar la compatibilidad con las 
      // primeras versiones del componente.
      if(arguments.length > 1)
      {
        var argumentos =
        {
          sw:arguments[0],
          params:arguments[1],
          fFila:arguments[2],
          fFinal:arguments[3],
          borrable:arguments[4],
          editable:arguments[5]          
        }
        arguments = [argumentos];
      } 
      // fin del arreglo de compatibilidad //
      
      return metodos_listaPaginada.init.apply( this, arguments );  
      
    } 
        
  
  };









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



