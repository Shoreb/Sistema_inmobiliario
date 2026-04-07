// ================================================================
// CONFIGURACIÓN GLOBAL
// ================================================================
const API_URL = "https://sistemainmobiliario-production-a013.up.railway.app";

// ================================================================
// UTILIDADES JWT — leer el payload del token sin librerías
// ================================================================
function parseJwt(token) {
  try {
    const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
    const json = decodeURIComponent(
      atob(base64)
        .split("")
        .map(c => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    return JSON.parse(json);
  } catch {
    return null;
  }
}

function getUsuarioActual() {
  const raw = localStorage.getItem("user");
  if (!raw) return null;
  try { return JSON.parse(raw); } catch { return null; }
}

function getToken() {
  return localStorage.getItem("token") || null;
}

function isTokenValido() {
  const token = getToken();
  if (!token) return false;
  const payload = parseJwt(token);
  if (!payload) return false;
  // Verificar expiración
  if (payload.exp && Date.now() / 1000 > payload.exp) {
    logout();
    return false;
  }
  return true;
}

// ================================================================
// GUARDS — proteger páginas según rol
// Llama a este guard al inicio de cada página protegida
// ================================================================
function requireAuth() {
  if (!isTokenValido()) {
    window.location.replace("login.html");
    return false;
  }
  return true;
}

function requireAdmin() {
  if (!requireAuth()) return false;
  const user = getUsuarioActual();
  if (!user || user.role !== "admin") {
    // Es cliente, redirigir a su portal
    window.location.replace("cliente.html");
    return false;
  }
  return true;
}

function requireCliente() {
  if (!requireAuth()) return false;
  const user = getUsuarioActual();
  if (!user || user.role !== "cliente") {
    // Es admin, redirigir a su panel
    window.location.replace("dashboard.html");
    return false;
  }
  return true;
}

// ================================================================
// LOGIN
// ================================================================
async function loginUser(e) {
  e.preventDefault();

  const email    = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const btnLogin = document.getElementById("btnLogin");

  if (btnLogin) {
    btnLogin.disabled    = true;
    btnLogin.textContent = "Ingresando...";
  }

  try {
    const res = await fetch(`${API_URL}/auth/login`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (res.ok) {
      // Guardar token Y datos del usuario
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user",  JSON.stringify(data.user));

      // Redirigir según rol
      if (data.user.role === "admin") {
        window.location.replace("dashboard.html");
      } else {
        window.location.replace("cliente.html");
      }
    } else {
      mostrarError("errorLogin", data.detail || "Credenciales incorrectas");
    }
  } catch {
    mostrarError("errorLogin", "No se pudo conectar con el servidor. Intenta de nuevo.");
  } finally {
    if (btnLogin) {
      btnLogin.disabled    = false;
      btnLogin.textContent = "Iniciar Sesión";
    }
  }
}

// ================================================================
// REGISTER
// ================================================================
async function registerUser(event) {
  event.preventDefault();

  const name             = document.getElementById("nombre").value.trim();
  const last_name        = document.getElementById("apellido").value.trim();
  const email            = document.getElementById("email").value.trim();
  const tel              = document.getElementById("telefono").value.trim();
  const password         = document.getElementById("password").value;
  const confirm_password = document.getElementById("confirm").value;

  // Validaciones en el cliente
  if (password !== confirm_password) {
    mostrarError("errorRegister", "Las contraseñas no coinciden");
    return;
  }
  if (password.length < 8) {
    mostrarError("errorRegister", "La contraseña debe tener al menos 8 caracteres");
    return;
  }

  const btnReg = document.getElementById("btnRegister");
  if (btnReg) {
    btnReg.disabled    = true;
    btnReg.textContent = "Registrando...";
  }

  try {
    const response = await fetch(`${API_URL}/auth/register`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ name, last_name, email, tel, password, confirm_password }),
    });

    const result = await response.json();

    if (response.ok) {
      showToast("¡Cuenta creada correctamente! Iniciando sesión...");
      // Loguear automáticamente después del registro
      await loginSilencioso(email, password);
    } else {
      mostrarError("errorRegister", result.detail || "Error al registrar");
    }
  } catch {
    mostrarError("errorRegister", "Error conectando con el servidor");
  } finally {
    if (btnReg) {
      btnReg.disabled    = false;
      btnReg.textContent = "Crear Cuenta";
    }
  }
}

// Login silencioso después del registro
async function loginSilencioso(email, password) {
  try {
    const res = await fetch(`${API_URL}/auth/login`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user",  JSON.stringify(data.user));
      // Los clientes registrados siempre van a cliente.html
      window.location.replace("cliente.html");
    }
  } catch {
    // Si falla el login automático, mandar al login manual
    window.location.replace("login.html");
  }
}

// ================================================================
// LOGOUT
// ================================================================
function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  window.location.replace("login.html");
}

// ================================================================
// CARGAR NOMBRE DEL USUARIO EN LA UI
// Busca elementos con id="userName", "adminName", "clienteName"
// y los rellena con los datos guardados
// ================================================================
function cargarNombreUsuario() {
  const user = getUsuarioActual();
  if (!user) return;

  const nombre    = user.name || "Usuario";
  const iniciales = nombre.charAt(0).toUpperCase() + (user.last_name ? user.last_name.charAt(0).toUpperCase() : "");

  // Rellenar donde exista en el HTML
  const ids = ["userName", "adminName", "clienteName", "userFullName"];
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = nombre;
  });

  const avatarIds = ["userAvatar", "adminAvatar", "clienteAvatar"];
  avatarIds.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = iniciales;
  });

  const roleIds = ["userRole", "adminRole"];
  roleIds.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = user.role === "admin" ? "Administrador" : "Cliente";
  });
}

// ================================================================
// LOTES — cargar desde la API real
// ================================================================
async function cargarLotes() {
  const tabla = document.getElementById("tablaLotes");
  if (!tabla) return;

  try {
    const token = getToken();
    const res = await fetch(`${API_URL}/lots`, {
      headers: token ? { "Authorization": `Bearer ${token}` } : {}
    });

    if (!res.ok) throw new Error("Error al cargar lotes");

    const lotes = await res.json();

    if (!lotes.length) {
      tabla.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:32px;color:#888">No hay lotes registrados</td></tr>`;
      return;
    }

    tabla.innerHTML = lotes.map(lote => `
      <tr>
        <td>${lote.area} m²</td>
        <td>${lote.location}</td>
        <td>$${Number(lote.price).toLocaleString("es-CO")}</td>
        <td><span class="badge-estado badge-${lote.status}">${lote.status}</span></td>
        <td><button class="btn-accion" onclick="mostrarDetalleLote(${lote.id})">Ver detalle</button></td>
      </tr>
    `).join("");
  } catch (err) {
    console.error(err);
    if (tabla) tabla.innerHTML = `<tr><td colspan="5" style="text-align:center;color:red">Error al cargar lotes</td></tr>`;
  }
}

// ================================================================
// PAGOS — cargar historial
// ================================================================
async function cargarPagos() {
  const tabla = document.getElementById("tablaPagos");
  if (!tabla) return;

  try {
    const token = getToken();
    const res = await fetch(`${API_URL}/payments`, {
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (!res.ok) throw new Error();

    const pagos = await res.json();

    if (!pagos.length) {
      tabla.innerHTML = `<tr><td colspan="4" style="text-align:center;padding:32px;color:#888">Sin pagos registrados</td></tr>`;
      return;
    }

    tabla.innerHTML = pagos.map(p => `
      <tr>
        <td>${new Date(p.payment_date).toLocaleDateString("es-CO")}</td>
        <td>Compra #${p.purchase_id}</td>
        <td>$${Number(p.amount).toLocaleString("es-CO")}</td>
        <td><button onclick="showToast('Comprobante descargando...')">Descargar</button></td>
      </tr>
    `).join("");
  } catch {
    if (tabla) tabla.innerHTML = `<tr><td colspan="4" style="color:red;text-align:center">Error al cargar pagos</td></tr>`;
  }
}

// ================================================================
// PQRS — enviar solicitud real a la API
// ================================================================
async function enviarPQRS(e) {
  e.preventDefault();

  const user = getUsuarioActual();
  if (!user) { logout(); return; }

  const tipo    = document.getElementById("tipoPQRS").value;
  const mensaje = document.getElementById("mensajePQRS").value.trim();

  if (!tipo || !mensaje) {
    showToast("Por favor completa todos los campos");
    return;
  }

  try {
    const token = getToken();
    const res = await fetch(`${API_URL}/pqrs`, {
      method:  "POST",
      headers: {
        "Content-Type":  "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ user_id: user.id, type: tipo, message: mensaje })
    });

    if (res.ok) {
      showToast("✅ Solicitud enviada correctamente");
      document.getElementById("tipoPQRS").value    = "";
      document.getElementById("mensajePQRS").value = "";
      cargarMisPQRS();
    } else {
      showToast("❌ Error al enviar la solicitud");
    }
  } catch {
    showToast("❌ Error de conexión");
  }
}

async function cargarMisPQRS() {
  const tabla = document.getElementById("tablaPQRS");
  if (!tabla) return;

  try {
    const token = getToken();
    const res = await fetch(`${API_URL}/pqrs`, {
      headers: { "Authorization": `Bearer ${token}` }
    });

    const lista = await res.json();
    const user  = getUsuarioActual();

    // Filtrar solo las del usuario actual
    const misPqrs = lista.filter(p => p.user_id === user?.id);

    if (!misPqrs.length) {
      tabla.innerHTML = `<tr><td colspan="3" style="text-align:center;padding:24px;color:#888">No tienes solicitudes</td></tr>`;
      return;
    }

    tabla.innerHTML = misPqrs.map(p => `
      <tr>
        <td>${new Date(p.created_at).toLocaleDateString("es-CO")}</td>
        <td>${p.type}</td>
        <td><span class="badge-estado badge-${p.status}">${p.status}</span></td>
      </tr>
    `).join("");
  } catch {
    if (tabla) tabla.innerHTML = `<tr><td colspan="3" style="color:red">Error al cargar PQRS</td></tr>`;
  }
}

// ================================================================
// FILTRO DE LOTES
// ================================================================
function filtrarLotes() {
  const filtro = document.getElementById("filtroEstado")?.value;
  const filas  = document.querySelectorAll("#tablaLotes tr");
  filas.forEach(f => {
    const estado = f.children[3]?.innerText || "";
    f.style.display = (!filtro || estado.includes(filtro)) ? "" : "none";
  });
}

// ================================================================
// TOAST — notificación visual
// ================================================================
function showToast(msg) {
  // Buscar toast existente
  let toast = document.getElementById("globalToast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "globalToast";
    toast.style.cssText = `
      position:fixed; bottom:28px; left:50%; transform:translateX(-50%) translateY(80px);
      background:#1a3a2a; color:#fff; padding:14px 28px; border-radius:10px;
      font-size:0.92rem; font-weight:500; z-index:9999;
      box-shadow:0 8px 32px rgba(0,0,0,0.22);
      transition:transform 0.35s cubic-bezier(.34,1.56,.64,1), opacity 0.3s;
      opacity:0; pointer-events:none;
    `;
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  requestAnimationFrame(() => {
    toast.style.transform  = "translateX(-50%) translateY(0)";
    toast.style.opacity    = "1";
  });
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => {
    toast.style.transform = "translateX(-50%) translateY(80px)";
    toast.style.opacity   = "0";
  }, 3200);
}

// ================================================================
// HELPER — mostrar mensaje de error en formularios
// ================================================================
function mostrarError(elementId, mensaje) {
  const el = document.getElementById(elementId);
  if (el) {
    el.textContent    = mensaje;
    el.style.display  = "block";
    setTimeout(() => { el.style.display = "none"; }, 5000);
  } else {
    // Fallback si no existe el elemento
    showToast("❌ " + mensaje);
  }
}

// ================================================================
// TOGGLE CONTRASEÑA
// ================================================================
document.addEventListener("DOMContentLoaded", function () {
  const togglePassword = document.getElementById("togglePassword");
  const passwordInput  = document.getElementById("password");

  if (togglePassword && passwordInput) {
    togglePassword.addEventListener("click", function () {
      const type = passwordInput.type === "password" ? "text" : "password";
      passwordInput.type = type;
      this.classList.toggle("fa-eye");
      this.classList.toggle("fa-eye-slash");
    });
  }

  // Cargar nombre en cualquier página que lo tenga
  cargarNombreUsuario();
});

// ================================================================
// INDICADOR DE FUERZA DE CONTRASEÑA
// ================================================================
function checkStrength(val) {
  const fill  = document.getElementById("strengthFill");
  const label = document.getElementById("strengthLabel");
  if (!fill || !label) return;

  let strength = 0;
  if (val.length >= 8)          strength++;
  if (/[A-Z]/.test(val))        strength++;
  if (/[0-9]/.test(val))        strength++;
  if (/[^A-Za-z0-9]/.test(val)) strength++;

  const levels = [
    { w: "0%",   color: "#ccc",     text: "Ingresa una contraseña" },
    { w: "25%",  color: "#e53935",  text: "Muy débil" },
    { w: "50%",  color: "#fb8c00",  text: "Débil" },
    { w: "75%",  color: "#fdd835",  text: "Moderada" },
    { w: "100%", color: "#3a9e6f",  text: "Fuerte ✓" },
  ];

  const l          = val.length === 0 ? levels[0] : levels[strength];
  fill.style.width      = l.w;
  fill.style.background = l.color;
  label.textContent     = l.text;
  label.style.color     = l.color === "#ccc" ? "#5a6e5e" : l.color;
}