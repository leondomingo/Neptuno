/**
 * A continuación definimos las clases(pestañas) a mostrar
 **/
var ClasesMain={"nombres":["clientes","cursos","grupos", "alumnos","personal", "usuarios", "aulas", "centros", "informes", "explorar", "labs"]};

var n_modulos = 16;
var cargador=new Cargador(n_modulos);

// Estas variables globales nos van a permitir guardar las últimas fechas que el usuario
// ha seleccionado.
var objUltimaFechaDesde=null;
var objUltimaFechaHasta=null; 

// Variable global con el timeout
var _timeout=8000;

/**
 * @function CargaLibrerias
 **/
function CargaLibrerias()
{
  CargaLibreriasNeptuno(true);

  // Controlador estandar del horario
  cargador.CargaCabecera("../../neptuno/libjs/ender_listaJSON/ender.listaJSON.js");
  cargador.CargaCabecera("../../neptuno/libjs/ender_listaPaginada/ender.listaPaginada.js");
  cargador.CargaCabecera("../../neptuno/libjs/ender_buscador/ender.buscador.js");
  
  cargador.CargaCabecera("./lib/ender/selector/ender.selector.js");
  cargador.CargaCabecera("./lib/ender/alumnosEnGrupos/ender.alumnosEnGrupos.js");
  cargador.CargaCabecera("./lib/ender/nivelesDeAlumnos/ender.nivelesDeAlumnos.js");
  
  cargador.CargaCabecera("./lib/jquery_ender_weekplanner/jquery_ender_weekplanner.js");
  cargador.CargaCabecera("./lib/jquery_ender_weekplanner/defaultWeekPlannerController.js");
  cargador.CargaCabecera("./lib/cookies/jquery.cookie.js");
  cargador.CargaCabecera("./lib/jquery_ender_lista/jquery.ender.lista.js");
  cargador.CargaCabecera("./lib/jquery_ender_lista_desplegable/jquery.ender.lista.desplegable.js");
  cargador.CargaCabecera("./lib/jquery_ender_lista_desplegable_formas_de_pago/jquery.ender.lista.desplegable.formas_de_pago.js");
  cargador.CargaCabecera("./lib/jquery_ender_lista_recibos/jquery.ender.lista.recibos.js");
  cargador.CargaCabecera("./lib/jquery_json/jquery.json-2.2.min.js");
  cargador.CargaCabecera("./lib/jquery_download/jquery.download.js");
  cargador.CargaCabecera("./lib/jquery_uri/jquery_uri_latest.js");
  /**
    Otras librerías
   **/
  
  cargador.CargaCabecera("./lib/jquery_selectboxes/jquery.selectboxes.min.js");
  cargador.CargaCabecera("./lib/jquery_fileupload/ajaxfileupload.js");
  cargador.CargaCabecera("./lib/selectToUISlider/js/selectToUISlider.jQuery.js");
  cargador.CargaCabecera("./lib/jquery_rangoFecha/jquery_rangoFecha.js");
  cargador.CargaCabecera("./lib/jquery_datepicker_multimonth/date.js");
  cargador.CargaCabecera("./lib/jquery_datepicker_multimonth/jquery.datePicker.js");
  cargador.CargaCabecera("./lib/jquery_wtooltip/wtooltip.min.js");
  //cargador.CargaCabecera("./lib/jquery.contextmenu/jqcontextmenu.js");


  

  finalizarCarga();
} // CargaLibrerias

/**
 * @function conectorTandem
 **/
function conectorTandem()
{
  /**************************************************************************
   * Saca un alumno del grupo desde la fecha que el
  usuario seleccione.
  * @function quitarAlumno
  * @param {Object} obj - Objeto contenedor
  * @param {Object} objParams
  * @param {Boolean} actualizaAlumnosGrupo
  * @param {Function} onReady
  **************************************************************************/
  this.compruebaDatosGrupo=function(obj, objParams)
  {
    
    
    if($('#datosGrupo').length >0)
    {
      
    }
    else
    {
      var id = $('#Grupos').attr('idseleccionado');
      
      neptuno.datosRegistro('grupos', id, function asignaDatosGrupo(resp)
      {
          
          $('body').append('<input type="hidden" id="datosGrupo"></input>');
          
          $('#datosGrupo').val(resp);
          
          
                      
      },true);  
    }
  }
  
  this.quitarAlumno=function(obj, objParams, actualizaAlumnosGrupo, onReady)
  {
    var idGrupo=parseInt(objParams.idgrupo);
    var idAlumno=parseInt(objParams.idalumno);

    if(idGrupo==-1)
    {
      idGrupo=obj.parent().attr('idseleccionadobusqueda');
    }

    if(idAlumno==-1)
    {
      idAlumno=obj.parent().attr('idseleccionadobusqueda');
    }

    neptuno.inicializaDialogo('#dialogoPreguntaFecha', 'Quitar desde', 420, 150);

    $.get('./acciones/grupos/modulos/preguntaFecha.htm',{},function(respuesta)
    {
      $('#dialogoPreguntaFecha').html(respuesta);
      $('#dialogoPreguntaFecha').find(".TextoSeleccion").html("Fecha desde la que se quita del grupo:");

      neptuno.cargaDatePicker($('#dialogoPreguntaFecha').find(".seleccionaFecha"));
      compruebaDatosGrupo();
      var respuesta = $('#datosGrupo').val();
      var grupo=neptuno.construirObjeto(respuesta);

      // Guardamos la última fecha desde seleccionada
      if( objUltimaFechaDesde!=null )
      {
        var objFechaDesde=objUltimaFechaDesde;
      }
      else
      {
        var objFechaActual=new Date();
        var objFechaDesde=objFechaActual;
      }

      $('#dialogoPreguntaFecha').find(".seleccionaFecha").val(objFechaDesde._toString());
      $('#dialogoPreguntaFecha').dialog('option', 'buttons',
      {
        "Cancelar":function()
        {
          $(this).dialog("close");
          neptuno.logconsola.Log("Cancelar diálogo de conflicto.");
        },
        "Aceptar":function()
        {
          $("#dialogoPreguntaFecha").dialog("close");
          cursorEspera();

          var fecha_desde=$('#dialogoPreguntaFecha').find(".seleccionaFecha").val();
          objUltimaFechaDesde=getDateObject(fecha_desde);

          neptuno.logconsola.Log("Quitando el alumno "+idAlumno+" del grupo "+idGrupo+" desde la fecha "+fecha_desde);

          var fechaFinGrupo=getDateObject(grupo.fechafin);
          var fechaInicioGrupo=getDateObject(grupo.fechainicio);

          if(objUltimaFechaDesde>fechaFinGrupo)
          {
            endcursorEspera();
            alert('No se puede quitar alumno del grupo ya que la fecha seleccionada es posterior a la fecha de fin del grupo.')
          }
          else if(objUltimaFechaDesde<fechaInicioGrupo)
          {
            endcursorEspera();
            alert('No se puede quitar alumno del grupo ya que la fecha seleccionada es anterior a la fecha de inicio del grupo.')
          }
          else
          {

            var usuarioNeptuno=neptuno.obtenerusuarioNeptuno();
            $.ajax({
              url: "./scripts/gruposSW.py/sacar_alumno",
              async:false,
              cache:false,
              data:
              {
                id_alumno:idAlumno,
                id_grupo:idGrupo,
                fecha_desde:fecha_desde,
                id_usuario:usuarioNeptuno.id,
                id_sesion:usuarioNeptuno.challenge
              },
              success:function(respuesta)
              {
                endcursorEspera();
                eval('var success='+respuesta+';');
                neptuno.cntMsgs.Show("Alumno eliminado del grupo correctamente.");

                if(actualizaAlumnosGrupo)
                {
                  actualizaAlumnosEnGrupo();
                  //actualizaAlumnosDisponibles(idGrupo);
                }
                else
                {
                  onReady();
                }
              },
              error:function a(respuesta)
              {
                endcursorEspera();
                neptuno.cntMsgs.ShowError(respuesta, "Error quitando alumno del grupo.");
                //alert('Problema en la conexión, por favor vuelva a intentar quitar el alumno.');
              }
            }); // ajax
          }
        } // Aceptar
      }); // Dialogo

      $('#dialogoPreguntaFecha').dialog('open');

      

    }); // get

  } // quitarAlumno


  /**********************************************************************
   * Carga el template de hojas de asistencias
   * @function hojaDeAsistencia
   * @param {Object} bloqueAcciones - bloque donde se van a cargar
   * @param {Object} params -
   *  params.idProfesor
   *  params.idCliente
   *  params.idCurso
  ***********************************************************************/
  this.hojaDeAsistencia=function(bloqueAcciones, params)
  {
    // idProfesor, idGrupo, idCliente
    // TODO: Esto se va a cambiar proximamente
    var idProfesor=(params.idProfesor ? params.idProfesor : '');
    var idGrupo=(params.idGrupo ? params.idGrupo : '');
    var idCliente=(params.idCliente ? params.idCliente : '');
    var idCurso=(params.idCurso ? params.idCurso : '');
    neptuno.logconsola.Log("hojaDeAsistencia::"+idProfesor+' '+idGrupo+' '+idCliente+' '+idCurso);

    $.ajax({
      url: "./templates/hoja_de_asistencia.htm", 
      async : false,
      cache:false,
      success:
        function(respuesta)
        {
          bloqueAcciones.html(respuesta);
          lanza(idProfesor, idGrupo, idCliente, idCurso);
          bloqueAcciones.fadeIn();
        },
      error:
        function(respuesta)
        {
          neptuno.cntMsgs.ShowError(respuesta, "Error lanzando hoja de asistencia");                              
        }
    }); // ajax   
    
  }; // hojaDeAsistencia
  
  /**
  * @function calendario
  **/
  this.calendario=function(bloqueAcciones, idCurso, idGrupo, fechainicio, fechafin)
  {
    neptuno.logconsola.Log("calendario::"+idCurso+' '+idGrupo+' '+fechainicio+' '+fechafin);

    $.ajax({
      url: "./templates/calendario.htm", 
      async : false,
      cache:false,
      success:
        function(respuesta)
        {
          bloqueAcciones.html(respuesta);
          lanzaCalendario(idCurso, idGrupo, fechainicio, fechafin);
          bloqueAcciones.fadeIn();
        },
      error:
        function(respuesta)
        {
          neptuno.cntMsgs.ShowError(respuesta, "Error lanzando calendario");                              
        }
    });
    
  }; // calendario

} // conectorTandem

// Creamos la instancia del conector tandem
var tandem=new conectorTandem();
