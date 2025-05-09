document.addEventListener("DOMContentLoaded", function(){

    document.addEventListener("submit", function()  {

        event.preventDefault()
        let consumo= document.getElementById("consumo").value
        let nombre= document.getElementById("nombre").value
        console.log(consumo)
        let Hidro2023= 0.8893

        let proporcionHidro= consumo*Hidro2023

         let caja= document.getElementById("resultado")
         caja.innerHTML= "La proporción de energía renobable hidroeléctrica consumida por  "+ nombre+" es de : " + proporcionHidro.toFixed(2) + " kWh."
        document.getElementById("re").style.display = "flex"
        document.getElementById("imgr").style.display = "block";


    })

})