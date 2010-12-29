(function($)
{
  
  /**** Parametros *****
  
  · sw: Servicio web del que recoge los elementos a mostrar en el desplegable, 
      usando el formato de salida columnas / datos de buscar.py
  
  · SWparams: el objeto "data" que se le pasa a este SW
  
  · campoIdentificador: nombre de la columna que se usará para identificar 
                        cada elemento
                          
  · nombre: Nombre del selector que se va a crear (id & name)
  
  · clase: Clase que se le aplica a este selector
  
  · valores: array de objetos de tipo {id, nombre} con los elementos a insertar 
             en el select
  
  */
  
  
  
  
  
  var metodos_enderCombo = 
  {
    init:function(params)
    {
          if(params.sw!=null)
          {
            $(this).enderCombo('initSW',params);
          }
          else
          {
            $(this).enderCombo('initJson',params);
          }
    },
    initSW:function(params)
    {
          if(params.campoIdentificador != null && params.campoIdentificador != undefined && params.campoIdentificador != '')
          {
            params.campoIdentificador = 'Nombre';
          }
          
          var elem = $(this);
          
          $.ajax(
          {
            url:params.sw,
            dataType:'json',
            data: params.SWparams,
            success:function(res)
            {
               var posId = res.columnas.indexOf('id');
               var posNombre = res.columnas.indexOf(params.campoIdentificador);
               params.valores = [];
               for(var i=0;i<res.datos.length;i++)
               {
                 params.valores.push({id:res.datos[i][posId], nombre:res.datos[i][posNombre]});
               }
               
               elem.enderCombo('initJson',params);
               
            }  
          } 
          );      
    },    
    initJson:function(params)
    {
          params = $(this).enderCombo('checkParams',params);
          
          if(!$(this).is('select'))
          {
            $(this).append('<select id="'+params.nombre+'" name="'+params.nombre+'" class="'+params.clase+'"></select>');
            var selector = $(this).children('select[id="'+params.nombre+'"]');            
          }
          else
          {
            $(this).attr('id',params.nombre);
            $(this).attr('name',params.nombre);
            $(this).attr('class',params.clase);
            var selector = $(this);            
          }
          
          for(var i = 0;i< params.valores.length; i++)
          {
            var html = '<option value ="' + params.valores[i].id + '">'+params.valores[i].nombre + '</option>';
            selector.append(html);
          }  
          
          selector.find('option[value="'+params.id+'"]').attr('selected','true');

    },
    checkParams:function(params)
    {
      if(params.nombre == null || params.nombre == undefined || params.nombre == '')
      {
        params.nombre = 'selectorEnder'
      }
      if(params.clase == null || params.clase == undefined || params.clase == '')
      {
        params.clase = 'selectorEnder'
      }      

      return params;
    }
    
  }  

  
  
  $.fn.enderCombo = function( method ) 
  {
    if ( metodos_enderCombo[method] ) 
    {
      return metodos_enderCombo[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
    } 
    else  
    {
      return metodos_enderCombo.init.apply( this, arguments );  
    } 
        
  
  };

  
  
  
})(jQuery);
