const reservacion = {
    empleado = '',
    sala = '',
    horaInicio = '',
    HoraFin = ''
}

const admin = {
    idAdmin = '',
    password = ''
}

document.addEventListener('DOMContentLoaded', function(){
    iniciarApp();
});


function iniciarApp(){
    //solicitar un lugar
    empleadoReservacion();
    salaReservacion();
    horaInicio();
    horaFin();
    fecha();
    desabilitarFechaAnterior();

    //login
    loginIDAdmin();
    loginPassword();
}

function loginIDAdmin(){
    const adminInput = document.querySelector('#ID_admin');
    adminInput.addEventListener('input', e => {
        const IDAdmin = e.target.value.trim();

        if(IDAdmin === '' || IDAdmin.length < 5){
            mostrarAlerta('ID de admin  no valido');
        } else{
            const alerta = document.querySelector('.alerta');
            if(alerta){
                alerta.remove();
            }
            admin.idAdmin = IDAdmin;
        }
    });
}

function loginPassword(){
    const adminPassword = document.querySelector('#password');
    adminPassword.addEventListener('input', e => {
        const passwordAdmin = e.target.value.trim();

        if(passwordAdmin === '' || passwordAdmin < 5){
            mostrarAlerta('Contraseña no valida', 'error');
        } else{
            const alerta = document.querySelector('.alerta');
            if(alerta){
                alerta.remove();
            }

            admin.password = passwordAdmin;
        }
    });
}

function empleadoReservacion(){
    const empleadoInput = document.querySelector('#ID_empleado');

    empleadoInput.addEventListener('input', e => {

        const IdEmpleado = e.target.value.trim();

        //Validacion del Id de empleado
        if(IdEmpleado === '' || IdEmpleado.length < 5){
            mostrarAlerta('ID sala no valido', 'error');
        } else{
            const alerta = document.querySelector('.alerta');
            if(alerta){
                alerta.remove();
            }

            reservacion.empleado = IdEmpleado;
        }
    });
}

function salaReservacion(){
    const salaInput = document.querySelector('#ID_espacio');

    salaInput.addEventListener('input', e =>{
        const IdSala = e.target.value.trim();

        if(IdSala === '' || IdSala.length < 5){
            mostrarAlerta('ID de sala no valido', 'error');
        } else{
            const alerta = document.querySelector('.alerta');
            if(alerta){
                alerta.remove();
            }
            reservacion.sala = IdSala;
        }
    });
}

function horaInicio(){
    const inputHoraInicio = document.querySelector('#hora_inicio');
    inputHoraInicio.addEventListener('input', e =>{
        const horaInicio = e.target.value;
        const hora1 = horaInicio.split(':');

        if(hora1[0] < 10 || hora1[0] > 18){
            mostrarAlerta('Hora de inicio no valida', 'error');
            setTimeout(() => {
                inputHoraInicio.value = '';
            }, 3000);
        } else{
            reservacion.horaInicio = horaInicio;
        }
    });
}

function horaFin(){
    const inputHoraFin = document.querySelector('#hora_final');
    inputHoraFin.addEventListener('input', e => {
        const horaFin = e.target.value;
        const hora2 = horaFin.split(':');

        if(hora2[0] < 10 || hora2[0] > 16){
            mostrarAlerta('Hora de finalizacion no valida', 'error');
            setTimeout(() => {
                inputHoraFin.value = '';
            }, 3000);
        } else{
            reservacion.horaFin = horaFin;
        }
    });
}

function fecha(){
    const fechaInput = document.querySelector('#fecha');
    fechaInput.addEventListener('input', e => {
        const dia = new Date(e.target.value).getUTCDay();

        if([0,6].includes(dia)){
            e.preventDefault();
            fechaInput.value = '';
            mostrarAlerta('Escogiste un dia no valido, sabado y domingo no validos', 'error');
        } else{
            reservacion.fecha = fechaInput.value;
        }
    });
}

function desabilitarFechaAnterior(){
    const fechaAnterior = document.querySelector('#fecha');

    const fechaActual = new Date();
    const año = fechaActual.getFullYear();
    const mes = fechaActual.getMonth() + 1;
    const dia = fechaActual.getDay() + 1;

    const fechaDesabilitar = `${año}-0${mes}-${dia}`;

    fechaAnterior.min = fechaDesabilitar;
}

function mostrarAlerta(mensaje, tipo){
    //Si ya existe alerta previa no crear otra

    const alertaPrevia = document.querySelector('.alerta');
    if(alertaPrevia){
        return;
    }

    const alerta = document.createElement('DIV');
    alerta.textContent = mensaje;
    alerta.classList.add('alerta');

    if(tipo === 'error'){
        alerta.classList.add('error');
    }

    //insertar al formulario
    const formulario = document.querySelector('.formulario');
    formulario.appendChild(alerta);

    //alerta desaparece 3 segundos despues

    setTimeout(() => {
        alerta.remove();
    }, 3000);
}