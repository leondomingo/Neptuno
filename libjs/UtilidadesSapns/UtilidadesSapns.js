/**
* @class RegistroSapns
**/
function RegistroSapns()
{
	this.Debug=false;
	this.Simple=0;
	this.Info=1;
	this.Warning=2;
	this.Error=3;
	this.BloqueInicio="[logSapns] ";

	/**
	 * @function Firebug
	 **/
	this.Firebug=function()
	{
		if( window.console && window.console.firebug )
		{
			return true;
		}
		else
		{
			return false;
		}
	}; // Firebug


	/**
	 * @function Log
	 * @param {String} texto
	 * @param {Integer} nivel - sus valores pueden ser los siguientes:
	 *
	 * logSapns.Simple 	- 0 - console.error => mensaje con el icono de error
	 * logSapns.Info 		- 1 - console.warn => mensaje con el icono de exclamación
	 * logSapns.Warning 	- 2 - console.info => mensaje con el icono de información
	 * logSapns.Error 		- 3 - console.debug => mensaje sin icono
	**/
	this.Log=function(texto, nivel)
	{
		if( this.Firebug() && this.Debug )
		{
			if(!nivel)
			{
				nivel=0;
			}
			
			texto=this.GetBloqueInicio()+texto;
			
			switch(nivel)
			{
				case 0:
				{
					console.debug(texto);
					break;
				}
				case 1:
				{
					console.info(texto);
					break;
				}
				case 2:
				{
					console.warn(texto);
					break;
				}
				case 3:
				{
					console.error(texto);
					break;
				}
			}
		}
	}; // Log
	
	/**
	* @function MostrarObjeto
	* @param {Object} objeto
	**/
	this.MostrarObjeto=function(objeto)
	{
		if( this.Firebug() && this.Debug )
		{
			console.dir(objeto);
		}		
	}; // MostrarObjeto


	/**
	* @function IniciaTemporizador
	* @param {Integer} id
	**/
	this.IniciaTemporizador=function(id)
	{
		if(this.Firebug() && this.Debug)
		{
			id=this.GetBloqueInicio()+id;
			console.time(id);
		}
	}; // IniciaTemporizador
	
	/**
	* @function FinalizaTemporizador
	* @param {Integer} id
	**/
	this.FinalizaTemporizador=function(id)
	{
		if(this.Firebug() && this.Debug)
		{
			id=this.GetBloqueInicio()+id;
			console.timeEnd(id);
		}
	}; // FinalizaTemporizador
	
	
	/**
	* @function MostrarXML
	* @param {} nodoXML
	**/
	this.MostrarXML=function(nodoXML)
	{
		if(this.Firebug() && this.Debug )
		{
			console.dirxml(nodoXML);
		}
	}; // MostrarXML
	
	/**
	* @function GetBloqueInicio
	**/
	this.GetBloqueInicio=function()
	{
		return this.BloqueInicio;
	}; // GetBloqueInicio
	
	/**
	* @param {String} Titulo
	**/
	this.IniciarGrupoMensajes=function(Titulo)
	{
		if(this.Firebug() && this.Debug )
		{
			Titulo=this.GetBloqueInicio()+Titulo;
			console.group(Titulo);
		}
	}; // Titulo
	
	/**
	* @function CerrarGrupoMensajes
	**/
	this.CerrarGrupoMensajes=function()
	{
		if(this.Firebug() && this.Debug )
		{
			console.groupEnd();
		}
	}; // CerrarGrupoMensajes
	
	/**
	* @function Trace
	**/
	this.Trace=function()
	{
		if(this.Firebug() && this.Debug)
		{
			console.trace();
		} 
	}; // Trace
	
	/**
	 * @function Clear
	 **/
	this.Clear=function()
	{
		if(this.Firebug() && this.Debug)
		{
			
		}
	};

	/**
	 * @function CargaInfoDebug
	 **/
	this.CargaInfoDebug=function()
	{
		$.ajax({async:false,
				type: "GET",
				cache:"false",
				url: "/neptuno/sw/checkdebug.py", 
				success: logSapns.RecibidaInfoDebug	
			   });
	};

	/**
	 * @function RecibidaInfoDebug
	 * @param {String} var_json
	 **/
	this.RecibidaInfoDebug=function(var_json)
	{
		var respuesta = eval("("+var_json+")");
								
		if( typeof(respuesta)=='object' )
		{
			var debug=(respuesta.Debug.Activo=='True');
			logSapns.Debug=debug;									
		}
	}; // RecibidaInfoDebug
} // RegistroSapns

/**
 * @function NumeroAleatorio
 * @param {Integer} inferior
 * @param {Integer} superior
 **/
function NumeroAleatorio(inferior,superior)
{
	numPosibilidades = superior - inferior
	aleat = Math.random() * numPosibilidades
	aleat = Math.floor(aleat)
	return parseInt(inferior) + aleat
} // NumeroAleatorio

/**
* @function LlamadaIncorrecta
* @param {XMLHttpRequest} xhr
* @param {String} msg
* @param {Exception} excep
**/
function LlamadaIncorrecta(xhr,msg,excep)
{
	var CodigoErrorHTTP=parseInt(xhr.status);
	var TextoAMostrar='';

	switch(CodigoErrorHTTP)
	{
		case 403: // Forbidden
		{
			TextoAMostrar='Forbidden'
			break;
		}
		case 404: // Usuario no encontrado
		{
			TextoAMostrar='Service not found';
			break;
		}
		case 406:
		{
			TextoAMostrar='Not Acceptable';
			break;
		}
		default: // Error interno
		{
			TextoAMostrar='Internal server error';
			break;			
		}
	} // switch CodigoErrorHTTP
	
	$.prompt(TextoAMostrar);
} // Final de LLamadaIncorrecta

(function($)
{

  $.fn.soloNumeros = function(enlazar)
  {
    var valor=  $(this).val();
    valor = valor.replace(/[^0-9.,-]/g, "");
    if((valor[valor.length-1] == '.')||(valor[valor.length-1] == ',')) valor += '0';
    if((valor[0]=='.')||(valor[0]==',')) valor = '0'+valor;
    if(valor=='') valor = 0;
    valor = valor.replace(',','.');
    $(this).val(valor);
    
    if(enlazar)
    {
      $(this).bind('change',$(this).soloNumeros);  
    }
    
    return $(this).val();
  }
  

  $.fn.soloFecha = function(enlazar)
  {
    var valor=  $(this).val();
    valor = valor.replace(/[^0-9-/]/g, "");
    if((valor[valor.length-1] == '.')||(valor[valor.length-1] == ',')) valor += '0';
    if((valor[0]=='.')||(valor[0]==',')) valor = '0'+valor;
    if(valor=='') valor = "01/01/1900";
    
    valor = valor.replace(/,/g,'-');
    
    valor = valor.replace(/\//g,'-');
    
    var valor_dividido = valor.split('-');
    
    var anyo = valor_dividido[2].replace(/[^0-9]/g, "").substring(0,4);
    if(anyo.length < 4) anyo += '0000';
    valor = valor_dividido[0].replace(/[^0-9]/g, "")+'/'+valor_dividido[1].replace(/[^0-9]/g, "")+'/'+anyo;
    
    
    
    $(this).val(valor);
    
    if(enlazar)
    {
    
      $(this).bind('change',$(this).soloFecha);
      
    }
    
    
    return $(this).val();
    
  }  
  
  
  
})(jQuery);


$('.numerico').live('bind',$(this).soloNumeros);

// Creamos la instancia global de RegistroSapns
var logSapns=new RegistroSapns();