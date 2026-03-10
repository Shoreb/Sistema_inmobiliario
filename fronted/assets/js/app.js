const API_URL = "https://sistemainmobiliario-production.up.railway.app";

/* LOGIN */
async function loginUser(e){

    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API_URL}/auth/login`,{
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ email,password })
    });

    const data = await res.json();

    console.log(data);

    if(res.ok){

        localStorage.setItem("token", data.access_token);

        window.location.replace("/dashboard.html");

    }else{

        alert("Credenciales incorrectas");

    }
}
document.addEventListener("DOMContentLoaded", function () {

    const togglePassword = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("password");

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener("click", function () {

            const type = passwordInput.type === "password" ? "text" : "password";
            passwordInput.type = type;

            this.classList.toggle("fa-eye");
            this.classList.toggle("fa-eye-slash");
        });
    }

});

/* REGISTER */
async function registerUser(event) {

    event.preventDefault()

    const name = document.getElementById("nombre").value
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value

    const data = {
    name: name,
    email: email,
    password: password
}
    try {

        const response = await fetch(`${API_URL}/auth/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })

        const result = await response.json()

        if (response.ok) {

            alert("Usuario registrado correctamente")

            window.location.href = "dashboard.html"

        } else {

            alert(result.detail || "Error al registrar")

        }

    } catch (error) {

        console.error(error)
        alert("Error conectando con el servidor")

    }

}

/* LOTES */
async function cargarLotes(){
    const res = await fetch(`${API_URL}/lotes`);
    const lotes = await res.json();

    const tabla = document.getElementById("tablaLotes");
    tabla.innerHTML="";

    lotes.forEach(lote=>{
        tabla.innerHTML+=`
        <tr>
            <td>${lote.area} m²</td>
            <td>${lote.ubicacion}</td>
            <td>$${lote.valor}</td>
            <td class="status-${lote.estado.toLowerCase()}">${lote.estado}</td>
            <td><button onclick="showToast('Compra simulada')">Comprar</button></td>
        </tr>
        `;
    });
}

/* FILTRO */
function filtrarLotes(){
    const filtro=document.getElementById("filtroEstado").value;
    const filas=document.querySelectorAll("#tablaLotes tr");

    filas.forEach(f=>{
        const estado=f.children[3].innerText;
        f.style.display=(!filtro||estado===filtro)?"":"none";
    });
}

/* TOAST */
function showToast(msg){
    const toast=document.createElement("div");
    toast.className="toast";
    toast.innerText=msg;
    document.body.appendChild(toast);

    setTimeout(()=>toast.remove(),3000);
}

function logout(){
    localStorage.removeItem("token");
    window.location.href="login.html";
}