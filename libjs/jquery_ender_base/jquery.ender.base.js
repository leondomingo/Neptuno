/******************************************************************************
* @author desarrollo@ender.es
* @module ender.base
*******************************************************************************/

/*******************************************************************************
@function $.ender
*******************************************************************************/
jQuery.ender=
{
	/**
		@function compruebaEscape
		@param {Event} event - evento desde donde se lanza la acción keyup
		@return {Boolean} escape - a cierto si pulsa intro
	 **/
	compruebaEscape: function(event)
	{
		if(event.keyCode!=undefined && event.keyCode!='undefined' && event.keyCode!=13)
		{
			return true;
		}
		
		return false;
	}, // compruebaEscape

	/**
		@function posicionaAccionActiva
		@param {Object} bloque - bloque div jquery donde se quiere posicionar el foco
	 **/
	posicionaAccionActiva: function(bloque)
	{
		if(bloque)
		{
			var offsetAlto=bloque.offset().top;
			$('html,body').animate({scrollTop: offsetAlto}, 700);
		}
	}, // posicionaAccionActiva

	/**
		@function getPosition
		@return {Object}
		@... {Number} x - posición x
		@... {Number} y - posición y
	 **/
	getPosition: function(e)
	{
	
	    e = e || window.event;
	
	    var cursor = {x:0, y:0};
	
	    if (e.pageX || e.pageY) {
	
		cursor.x = e.pageX;
	
		cursor.y = e.pageY;
	
	    }
	    else
	    {
		cursor.x = e.clientX +
	
		    (document.documentElement.scrollLeft ||
	
		    document.body.scrollLeft) -
	
		    document.documentElement.clientLeft;
	
		cursor.y = e.clientY +
	
		    (document.documentElement.scrollTop ||
	
		    document.body.scrollTop) -
	
		    document.documentElement.clientTop;
	
	    }
	
	    return cursor;
	} // getPosition

}; // jquery.ender.base

/**************************************************************************
	@function $.fn.loadSelect
	Añade elementos a un select a partir de un array de opciones.
	@param {Array} optionsDataArray - Array de opciones
*************************************************************************/
$.fn.loadSelect = function(optionsDataArray) {
	$(this).Log("loadSelect");
	return this.emptySelect().each(function()
	{
		if (this.tagName=='SELECT')
		{
			var selectElement = this;
			$.each(optionsDataArray,function(index,optionData)
			{
				var option = new Option(optionData.nombre,optionData.id);
				
				if ($.browser.msie)
				{
					selectElement.add(option);
				}
				else
				{
					selectElement.add(option,null);
				}
			}); // each
		}
	});
}; // loadSelect


/*//////////////////////////////////////////////////////////////////////////////
	Extensiones 'prototype' para el objeto Date
	@module ender.base.date
//////////////////////////////////////////////////////////////////////////////*/

/**
	@function getWeek
	@returns {Array} fechas - fecha de inicio y de fin de la semana
	@... {Date} fechainicio - fecha de inicio del mes
	@... {Date} fechafin - fecha de fin del mes
 **/
Date.prototype.getWeek= function(start)
{
	var tmp=new Date(this.getFullYear(), this.getMonth(), this.getDate());

	tmp.setDate(tmp.getDate()-tmp.getDay()+1);
	var startday=new Date(tmp);
	
	tmp.setDate(tmp.getDate()+6);
	var endday=new Date(tmp);
	
	return [startday, endday];
}; // getWeek

/**
	@function _getFinalMonthDate
	@returns {Date} fechafinal - fecha del último día del mes
 **/
Date.prototype._getFinalMonthDate=function()
{
	var tmp=new Date(this.getFullYear(), this.getMonth(), 1);
	tmp.setMonth( tmp.getMonth() +1);
	tmp.setDate(tmp.getDate()-1);
	return tmp;	
}; // _getFinalMonthDate

/**
	@function _toString
	@returns {String} cadenafecha - Fecha en formato dd/mm/aaaa
 **/
Date.prototype._toString= function()
{
	return this.getDate()+"/"+parseInt(this.getMonth()+1)+"/"+this.getFullYear();
}; // _toString

/**
	@function _toUSString
	@returns {String} fecha - Fecha en formato USA mm/dd/aaaa
 **/
Date.prototype._toUSString= function()
{
	return parseInt(this.getMonth()+1)+"/"+this.getDate()+"/"+this.getFullYear();
}; // _toUSString

/**
	@function _toPostgre
	@returns {String} fecha - Fecha en formato postgresql yyyy-mm-dd
 **/
Date.prototype._toPostgre= function()
{
	return this.getFullYear()+"-"+parseInt(this.getMonth()+1)+"-"+this.getDate();
}; // _toPostgre


/**
	@function _toZeroString
	@returns {String} fecha - Fecha en formato obligatorio de dos dígitos dd-mm-aaaa
 **/
Date.prototype._toZeroString= function()
{
	var dia=this.getDate();
	var mes=parseInt(this.getMonth()+1);
	
	if(dia<10)
	{
		dia="0"+dia;
	}
	
	if(mes<10)
	{
		mes="0"+mes;
	}

	return dia+"/"+mes+"/"+this.getFullYear();
}; // _toZeroString

/**
	@function _toHours
	@returns {String} hora - Hora actual en formato hh:mm
 **/
Date.prototype._toHours= function()
{
	var hora=this.getHours();
	var minutos=this.getMinutes();
	
	if(hora<10)
	{
		hora="0"+hora;
	}
	
	if(minutos<10)
	{
		minutos="0"+minutos;
	}
	
	return hora+":"+minutos;
}; // _toHours


/*//////////////////////////////////////////////////////////////////////////////
	Otras utilidades
	@module ender.base.utils
//////////////////////////////////////////////////////////////////////////////*/


/******************************************************************************
	@function getDateObject
	Construye un objeto Date a partir de las cadenas de fecha y hora
	
	@param {String} fecha - Fecha en formato dd/mm/yyyy
	@param {String} hora - Hora en formato hh:mm
	
	@returns {Date} fecha - Objeto fecha 
******************************************************************************/
function getDateObject(fecha, hora)
{
	if(!hora)
	{
		var hora="00:00";
	}
	
	fecha=fecha.replace(/-/g,"/");
	
	var _tmpFecha	=fecha.split("/");
	var _tmpHora	=hora.split(":");
	var toReturn=new Date(_tmpFecha[2], (_tmpFecha[1]-1), _tmpFecha[0], _tmpHora[0], _tmpHora[1]);
	
	return toReturn;			
} // getDateObject


/******************************************************************************
	@function randomString
	Genera una cadena aleatoria de una longitud específica

	@param {optional Integer} length - Por defecto 8
	@returns {String} cadena - Cadena aleatoria
******************************************************************************/
function randomString(length) 
{
	var string_length=(length? length : 8);
	var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";

	var randomstring = '';
	for (var i=0; i<string_length; i++) 
	{
		var rnum = Math.floor(Math.random() * chars.length);
		randomstring += chars.substring(rnum,rnum+1);
	}
	
	return randomstring;
} // randomString


/******************************************************************************
	@function utf8_encode
	Codifica desde iso-8859-1 a utf-8
	@param {String} string - cadena codificada en ISO-8859-1
	@returns {String} cadena - Cadena codificada en utf8
******************************************************************************/
function utf8_encode(string) 
{
	string = string.replace(/\r\n/g,"\n");
	var utftext = "";

	for (var n = 0; n < string.length; n++) {

		var c = string.charCodeAt(n);

		if (c < 128) {
			utftext += String.fromCharCode(c);
		}
		else if((c > 127) && (c < 2048)) {
			utftext += String.fromCharCode((c >> 6) | 192);
			utftext += String.fromCharCode((c & 63) | 128);
		}
		else {
			utftext += String.fromCharCode((c >> 12) | 224);
			utftext += String.fromCharCode(((c >> 6) & 63) | 128);
			utftext += String.fromCharCode((c & 63) | 128);
		}

	}

	return utftext;
} // utf8_encode

/******************************************************************************
	@function utf8_decode
	Codifica desde UTF-8 a ISO-8859-1
	@see http://phpjs.org/functions/utf8_decode
	@version 903.3016
	@param {String} str_data - cadena codificada en UTF-8
	@returns {String} cadena - cadena decodificada en ISO-8859-1
******************************************************************************/
function utf8_decode ( str_data )
{
    var tmp_arr = [], i = 0, ac = 0, c1 = 0, c2 = 0, c3 = 0;
    
    str_data += '';
    
    while ( i < str_data.length ) {
        c1 = str_data.charCodeAt(i);
        if (c1 < 128) {
            tmp_arr[ac++] = String.fromCharCode(c1);
            i++;
        } else if ((c1 > 191) && (c1 < 224)) {
            c2 = str_data.charCodeAt(i+1);
            tmp_arr[ac++] = String.fromCharCode(((c1 & 31) << 6) | (c2 & 63));
            i += 2;
        } else {
            c2 = str_data.charCodeAt(i+1);
            c3 = str_data.charCodeAt(i+2);
            tmp_arr[ac++] = String.fromCharCode(((c1 & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
            i += 3;
        }
    }

    return tmp_arr.join('');
} // utf8_decode

/******************************************************************************
	@function in_array
	Devuelve cierto si localiza un valor en el array.

		example 1: in_array('van', ['Kevin', 'van', 'Zonneveld']);
		returns 1: true
		example 2: in_array('vlado', {0: 'Kevin', vlado: 'van', 1: 'Zonneveld'});
		returns 2: false
		example 3: in_array(1, ['1', '2', '3']);
		returns 3: true
		example 3: in_array(1, ['1', '2', '3'], false);
		returns 3: true
		example 4: in_array(1, ['1', '2', '3'], true);
		returns 4: false
		
	@see http://phpjs.org/functions/in_array
	@version 905.3120
	@param {String} needle - Elemento a buscar
	@param {Array} haystack - Array donde buscamos
	@param {optional Boolean} argStrict - por defecto a false
	@returns {Boolean} encuentra_valor - Cierto si localiza el valor en el array
******************************************************************************/
function in_array(needle, haystack, argStrict) 
{
    var key = '', strict = !!argStrict;

    if (strict) {
        for (key in haystack) {
            if (haystack[key] === needle) {
                return true;
            }
        }
    } else {
        for (key in haystack) {
            if (haystack[key] == needle) {
                return true;
            }
        }
    }

    return false;
} // in_array