var n_modulos = 13;
var maxIntentos=2;
var intentos=0;

/**************************************************************************
* Carga el núcleo de neptuno.
* @function initNeptuno
* @param {Function} onRequest
**************************************************************************/
function initNeptuno(onRequest)
{
	$.ajaxSetup({
	  type: "POST"
	});

	$.ajax({type: "GET",
                    url: "./lib/libs.js", 
                    dataType: "script",
                    async:false,
                    complete: function()
					{      
						if(typeof(CargaLibrerias)=="function")
						{
							CargaLibrerias();
							
							if(typeof(onRequest)=="function")
							{
								onRequest();
							}
						}
						else if(intentos<maxIntentos)
						{
							initNeptuno();
							intentos++;
						}
					}
		});
} // initNeptuno


/**************************************************************************
* @function load_css
* @param {String} url
* @param {String} media
*************************************************************************/    
function load_css(url, media) 
{
   var e = document.createElement("link");
   e.href = url;
   e.type = "text/css";
   e.rel = "stylesheet";
   
   e.media = (media? media: "screen");
   document.getElementsByTagName("head")[0].appendChild(e);
}
    

/**************************************************************************
* @function InicializaBarraProgreso
*************************************************************************/
function InicializaBarraProgreso()
{
	cursorEspera();
	$(".progressbar").progressbar( 'value' , 0 );	
	$('#barra_de_progreso').fadeIn('quick');	
	$('.progressbar').progressbar({ value: 0 });
} // InicializaBarraProgreso

var llamada=0;

/**************************************************************************
* @function cursorEspera
* @param {String} texto
*************************************************************************/
function cursorEspera(texto)
{
	if(!texto)
	{
		texto='Por favor, espere unos instantes...';
	}

	$.blockUI(
	{ css: { 
            border: 'none', 
            padding: '15px', 
            backgroundColor: '#000', 
            '-webkit-border-radius': '10px', 
            '-moz-border-radius': '10px', 
            opacity: '.5', 
            color: '#fff'             
        },
        message: texto        
	}); 
} // cursorEspera

/**************************************************************************
* @function endcursorEspera
*************************************************************************/
function endcursorEspera()
{
	$.unblockUI();
} // endcursorEspera

/**************************************************************************
* @function IncrementaBarraProgreso
* @param {Integer} valor
*************************************************************************/
function IncrementaBarraProgreso(valor)
{
	$(".progressbar").progressbar( 'value' , valor );
} // IncrementaBarraProgreso

/**************************************************************************
* @function CierraBarraProgreso
*************************************************************************/
function CierraBarraProgreso()
{
	$(".progressbar").progressbar( 'value' , 100 );	
	$('#barra_de_progreso').fadeOut('slow');	
	endcursorEspera();
} // CierraBarraProgreso


/**************************************************************************
* definición de la clase Cargador
* @function Cargador
* @param {Integer} n_modulos
*************************************************************************/
function Cargador(n_modulos)
{
	this.n_modulos=n_modulos;
	this.n=1;
	this.fails=new Array();


	// Inicializamos la barra de progreso
	InicializaBarraProgreso();

	this.IncrementaBarraProgreso=function()
	{
		var _progreso=(cargador.n/cargador.n_modulos)*100;
		IncrementaBarraProgreso(_progreso);
		cargador.n++;
	}; // Final de IncrementaBarraProgreso
	
	this.CargaCabecera=function(NombreCabecera, fIncrementa)
	{
		if(fIncrementa)
		{
			$.ajax(
			{
				async:false,
				type: "GET",
				cache:false,
				url: NombreCabecera, 
				dataType: "script", 
				success: fIncrementa
			});
		}
		else
		{	
			var loader=this;
			
			// Primero intenta cargar el fichero fichero.js.mymin.js
/*			$.ajax(
			{
				async:false,
				type: "GET",
				cache:false,
				url: NombreCabecera+".mymin.js", 
				dataType: "script", 
				success: function f() { loader.IncrementaBarraProgreso(); },
				error: function f() 
				{
					// Si no lo encuentra intenta cargar el original
					$.ajax(
					{
						async:false,
						type: "GET",
						cache:false,
						url: NombreCabecera, 
						dataType: "script", 
						success: function f() { loader.IncrementaBarraProgreso(); },
						error: function f() 
						{
							var n_fails=loader.fails.length;
							loader.fails[n_fails]=NombreCabecera;
						}
					});
				}
		   	});*/
			
					$.ajax(
					{
						async:false,
						type: "GET",
						cache:false,
						url: NombreCabecera, 
						dataType: "script", 
						success: function f() { loader.IncrementaBarraProgreso(); },
						error: function f() 
						{
							var n_fails=loader.fails.length;
							loader.fails[n_fails]=NombreCabecera;
						}
					});
			
		}
	}; // Final de CargaCabecera
		
} // Clase Cargador

// Creamos la instancia global del objeto Cargador
var cargador=new Cargador(n_modulos);

/**
 * @function CargaLibreriasNeptuno
 **/
function CargaLibreriasNeptuno(no_finalizar)
{
	if(window.neptuno===undefined)
	{
		$('#barra_de_progreso').fadeIn('quick');


		/**
			Librerías jquery_ender
		**/
		cargador.CargaCabecera("/neptuno/libjs/jquery_ender_base/jquery.ender.base.js");
		cargador.CargaCabecera("/neptuno/libjs/json2/json2.js");
		cargador.CargaCabecera("/neptuno/libjs/ender_neptuno/ender_neptuno.js");
		cargador.CargaCabecera("/neptuno/libjs/jquery_form/jquery.form.js");
		cargador.CargaCabecera("/neptuno/libjs/UtilidadesSapns/UtilidadesSapns.js");
		cargador.CargaCabecera("/neptuno/libjs/jquery_ender_selector/jquery_ender_selector_latest.js");

		cargador.CargaCabecera("/neptuno/libjs/jquery_ender_searchbox/jquery.ender.searchbox.js");
		cargador.CargaCabecera("/neptuno/libjs/jquery_ender_actionsbox/jquery.ender.actionsbox.js");
		cargador.CargaCabecera("/neptuno/libjs/jquery_ender_grid/jquery.ender.grid.js");
		cargador.CargaCabecera("/neptuno/libjs/jquery_ender_selector/jquery_ender_selector_latest.js");
		cargador.CargaCabecera("/neptuno/libjs/jquery_ender_contentLoader/jquery_ender_contentLoader_latest.js");
		if(!no_finalizar) finalizarCarga();
	
	} // neptuno.loaded
} // CargaLibreriasNeptuno

function finalizarCarga()
{
		$('#barra_de_progreso').fadeOut('slow');
		CierraBarraProgreso();
		neptuno.cntMsgs.Show("Carga del sistema completada");
		neptuno.loaded=true;
		neptuno.infoVersion();

}
