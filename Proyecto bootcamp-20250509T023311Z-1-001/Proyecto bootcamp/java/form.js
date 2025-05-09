document.addEventListener("DOMContentLoaded", function()    {
    let tabla=document.getElementById("ctabla")
    fetch("http://127.0.0.1:5000/hidro")
    .then(respuesta => respuesta.json())
    .then(datos => {

        let datoscol= []
        for (let i=0; i<datos.length;i++)    {
            if (datos[i].Entity=="Colombia")    {
                datoscol.push(datos[i])
                console.log(datoscol)
            }
        }
        for (let n=0; n<datoscol.length;n++)    {
            let año= datoscol[n]["Year"];
            let porcentaje=datoscol[n]["Hydro (% equivalent primary energy)"]

            tabla.innerHTML+=
            `<tr>
            <td>${año}</td>
            <td>${porcentaje.toFixed(2)}</td>
           </tr>`
        }



  })
})