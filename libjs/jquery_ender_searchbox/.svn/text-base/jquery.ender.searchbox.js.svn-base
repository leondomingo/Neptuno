(function($)
 {
    var settings;
    
   /**
      ocultaBusqueda
    **/
   $.fn.ocultaBusqueda=function()
   {
      var searchbox=$(this);
      searchbox.find(".busqueda").hide();
      searchbox.find(".Boton").hide();
   }; // ocultaBusqueda

   /**
      ocultaBotonBusqueda
    **/
   $.fn.ocultaBotonBusqueda=function()
   {
      var searchbox=$(this);
      searchbox.find(".Boton").hide();
   }; // ocultaBusqueda


    $.fn.searchbox=function(callerSettings)
    {      
        /**
            settings
        **/
        settings=$.extend(
        {
            title:'searchbox',
            actions: [{label:'search', idAction:null, _class: ''}],
            readonly: false,
	    control: null
        }, callerSettings || {});
        
        var searchbox=$(this);
        var selector=searchbox.parent();
        var idSearchbox=selector.attr("id")+"_CajaBusqueda";
        
        searchbox.attr("id", idSearchbox);
        
        if(neptuno)
        {
            // Guardamos los parámetros            
            neptuno.setAttrData(idSearchbox, "title", settings.title);
            neptuno.setAttrDataObject(idSearchbox, "actions", settings.actions);
        }
	        
	$.ajax({
		url: "/neptuno/libjs/jquery_ender_searchbox/html/searchbox.htm", 
		async:false,
		cache:false,
		success:function(respuesta)
                {                            
                    load_css("/neptuno/libjs/jquery_ender_searchbox/css/searchbox.css");
                    searchbox.html(respuesta);
                    
                    var searchinput=searchbox.find('.busqueda:first');
                    var title=neptuno.getAttrData(searchbox.attr("id"), "title");
                    
                    searchbox.find('.TituloSelector').html(title);
                    
                    // modo solo lectura
                    if(settings.readonly)
                    {
                        searchinput.attr("readonly", true);                        
                    }
                    
                    // dibujamos los botones
                    var NActions=settings.actions.length;
                    for(var BOTONi=0;BOTONi<NActions;BOTONi++)
                    {
                        var botonActual=settings.actions[BOTONi];
                        var html=getHTMLButton(botonActual.label, botonActual._class);
                        searchbox.append(html);
                        
                        // Asignamos el bind correspondiente
                        var boton=searchbox.find('.'+botonActual._class+":first");
                        
                        if(boton)
                        {
                            boton.unbind();
                            boton.bind('click', neptuno.getAction(botonActual.idAction));
			    //boton.attr('href', '#'+$('#'+this.identificador).attr('id') );
                        }
                        
                    } // Recorremos los botones con acciones                    

                     searchinput.unbind();
                     searchinput.bind('keyup', function f(event)
                     {
			// Le asignamos el primer evento, si pulsamos la tecla ENTER
                        if( $.ender.compruebaEscape(event) )
                        {
                           return true;
                        }
   
                        // Lanza la primera acción
                        if(NActions>0)
                        {
                           if(neptuno)
                           {
                               var actions=neptuno.getAttrDataObject(idSearchbox, "actions");
                               var idAction=actions[0].idAction;  
                               var onRequest=neptuno.getAction(idAction);
                               onRequest(event, false, selector);
                           }
                        }
                        
                        return true;
                     });
                     
                     
        }
        ,error: function(){}
	});
        
        return this;
    }; // $.fn.searchbox

      $.fn.activaFoco=function()
      {
              $(this).find('.busqueda').focus();
      };

      /**
          getHTMLButton
      **/
      var getHTMLButton=function(label, _class)
      {
              return "<span class=\"Boton "+_class+"\">"+label+"</span>";
      } // getHTMLButton
    
 }) (jQuery);
