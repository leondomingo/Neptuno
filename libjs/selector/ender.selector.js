var rutaBaseSelector ='/neptuno/libjs/selector/';
var rutaCompletaSelector = '/neptuno/libjs/selector/'; 
var rutaBaseSelectorSW = '/neptuno/sw';


/*
 * Ejemplo de invocación:
 * 
 * $('.cliente > .campo').selectorEnder({"valor":"Pepito", "id":res.cliente},'clientes','','cliente',usuario(),tamañoBuscador);
 */


(function($)
{
  
  $.fn.selectorTablaEnder = function(tabla,campo) // facilita la inicialización de un selector vacío sobre una tabla
  {
    /* Construye un selector vacio enlazado con una tabla*/
    $(this).selectorEnder({},tabla,'',campo,neptuno.obtenerusuarioNeptuno(),null);
  }
  
  $.fn.selectorEnder = function(seleccionado, tabla,filtro, campoIdentificador, usuario, fBuscador, fSeleccion)
  {
    
    /* esta función sólo sirve para conservar la compatibilidad con el formato anterior de llamadas */
    
    var params =
      {
        seleccionado:seleccionado,
        tabla:tabla,
        filtro:filtro,
        campoIdentificador:campoIdentificador,
        usuario:usuario,
        fBuscador: fBuscador,
        fSeleccion: fSeleccion
        
      }  
      $(this).selectEnder(params);
  }
  
  $.fn.selectEnder = function( method ) 
  {
    if ( metodos_selector[method] ) 
    {
      return metodos_selector[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
    } 
    return metodos_selector.init.apply( this, arguments );  
  };

  var metodos_selector =
  {
    init:function(params)
    { 
      /* parametros */
      /* seleccionado: Objeto que indica el registro seleccionado al inicializar, con formato {id: id_objeto, valor: texto a mostar}*/
      var seleccionado = params.seleccionado;
      
      /* tabla: tabla de la que se recogen los datos en la BDD */
      var tabla = params.tabla;
      
      /* filtro: campo y valor por el que se filtra la búsqueda*/
      var filtro = params.filtro;
      
      /* campoIdentificador: Campo de la tabla del que se recoge el texto a mostrar una vez seleccionado un registro.
      Puede contener varios campos separados por '+' */
      var campoIdentificador = params.campoIdentificador;
      if(campoIdentificador == null || campoIdentificador == '') campoIdentificador = 'id';
      
      /* usuario: objeto con los datos del usuario (id y challenge) */
      var usuario = params.usuario;
      
      /* fBuscador: función que se ejecuta cuando se completa una llamada al buscador */
      var fBuscador = params.fBuscador;
      
      /* fSeleccion: función que se ejecuta cuando se realiza una selección */
      var fSeleccion = params.fSeleccion;
      
      /* sw: url del servicio web que accede a la base de datos*/
      var sw = params.sw;
      
      /* extraParams: parametros adicionales que pudiera necesitar el sw */    
      var extraParams = params.extraParams;
      
      /* fparametros*/
      
      
      if(tabla != '' && tabla != null)
      {
        if(sw == null || sw == '') sw = rutaBaseSelectorSW+'/buscar.py';
        
        $(this).addClass('selectorEnder');
        $(this).load(rutaCompletaSelector+'/plantilla.htm',null,function()
        {
          $("head").append("<link>");
          css = $("head").children(":last");
          css.attr({
              rel:  "stylesheet",
              type: "text/css",
              href: rutaCompletaSelector+'/estilos.css'
          });      
          
       
          var params = 
          {
            busqueda: "",
            id_usuario: usuario.id,
            id_sesion: usuario.challenge,
            campos: filtro,
            limite_resultados: 10,
            n_resultados: true,
            pos: 0,
            tabla: tabla
          };
          
          
          for(var nombrePropiedad in extraParams) 
          {
              eval("params."+nombrePropiedad+" = '"+extraParams[nombrePropiedad]+"'");
          }
          
          
          
          if(seleccionado != null && seleccionado.id>0)
          {
            $(this).attr('value',seleccionado.id);
            $(this).attr('idSeleccionado',seleccionado.id);
            $(this).find('.elementoSeleccionado').html(seleccionado.valor);  
          }
          else
          {
            $(this).attr('value',null);
            $(this).attr('idSeleccionado',null);
          }
          
          $(this).find('.elementoSeleccionado').after('<div class="botonVaciar"><img src="'+rutaCompletaSelector+'/vaciar.png"></img></div>');
          $(this).find('.botonVaciar').bind('click', $(this).vaciarSelectorEnder);
          $(this).bind('mouseover',function(){$(this).find('.botonVaciar').css('opacity','1')});
          $(this).bind('mouseout',function(){$(this).find('.botonVaciar').css('opacity','0.3')});
          $(this).attr('campoIdentificador',campoIdentificador);
          $(this).find('.elementoSeleccionado').click(despliegaBuscadorSelector);    
          $(this).data('fSeleccion',fSeleccion);
          var selector = $(this);
          $(this).find('.zonaBuscador').buscador(sw,params,null, function(){botonesSelector(selector);if(fBuscador!=null) fBuscador();selector.find('.resultados').ajustarAnchoCeldas()});
          $(this).trigger('cargado');
          $(this).attr('inicializado',true);
        });
        
      }
      
    },
    'selecciona':function(id,valor)
    {

    
      if($(this).find('.elementoSeleccionado').length > 0)
      {   // si se hace esta llamada cuando el selector ya está creado, se hace la asignación
        
        $(this).find('.elementoSeleccionado').html(valor);
        $(this).val(id);
        $(this).attr('idSeleccionado',id);
        $(this).change();    
      }
      else
      { // sino espera a que el método init lance el trigger "cargado" y la hace entonces     
        $(this).one('cargado',function()
        {
          $(this).find('.elementoSeleccionado').html(valor);
          $(this).val(id);
          $(this).attr('idSeleccionado',id);
          $(this).change();    
          
        })
      }

    }
  }
    
  $.fn.vaciarSelectorEnder = function()
  {
    $(this).parents('.selectorEnder').attr('value',null);
    $(this).parents('.selectorEnder').attr('idSeleccionado',null);
    $(this).parents('.selectorEnder').find('.elementoSeleccionado').html('');
  }
  
  $.fn.minimizaBuscador = function()
  {
    $(this).parents('.buscador').fadeOut();
  }  
  
  
})(jQuery);



function botonesSelector(selector)
{
    
    $(selector).find('.zonaBuscador').find('.fila').not('.cabecera').find('.celda').unbind('click').click(seleccionarRegistro);
    $(selector).find('.zonaBuscador').ordenCabeceras();
}

function seleccionarRegistro()
{
  var id = $(this).parent().attr('idObjeto');
  var campos =$(this).parents('.selectorEnder').attr('campoIdentificador').split(","); 
  var texto = '';
  for(var i = 0; i<campos.length;i++)
  {
    if(texto!='') texto += '.';
    texto += $(this).parents('.resultados').find('.fila[idObjeto="'+id+'"]').find('.celda[id_columna="'+campos[i]+'"]').html();  
  }
  
  $(this).parents('.selectorEnder').find('.elementoSeleccionado').html(texto);
  $(this).parents('.selectorEnder').attr('value',id);
  $(this).parents('.selectorEnder').attr('idSeleccionado',id);

  if($(this).parents('.selectorEnder').data('fSeleccion') != null) $(this).parents('.selectorEnder').data('fSeleccion')();

  $(this).parents('.selectorEnder').change();
  $(this).parents('.buscador').slideUp(1000).fadeOut(1000);
  
  
}

function despliegaBuscadorSelector()
{
   $(this).parents('.selectorEnder').find('.buscador').fadeIn(500).slideDown(1500);
   if($(this).parents('.selectorEnder').find('.zonaBuscador').find('.cajaBuscador').find('.botonMinimizar').length == 0)
   {
     $(this).parents('.selectorEnder').find('.zonaBuscador').find('.cajaBuscador').append('<div class="botonMinimizar"><img src="'+rutaCompletaSelector+'/min.png"></img></div>');
     $(this).parents('.selectorEnder').find('.zonaBuscador').find('.cajaBuscador').find('.botonMinimizar').click($(this).minimizaBuscador);
     
   }

}




