const state = {
  apiKey: null,
  client: null,
  leads: [],
  editingLead: null,
};

// Nawigacja między sekcjami
function showSection(sectionId) {
  document.querySelectorAll('.view').forEach(s => s.classList.add('hidden'));
  document.getElementById(`${sectionId}-section`)?.classList.remove('hidden');
  document.getElementById(sectionId)?.classList.remove('hidden'); // dla dashboard
  
  // Ukryj/Pokaż przyciski w nav
  const isLogged = !!state.apiKey;
  document.getElementById('nav-login-btn').classList.toggle('hidden', isLogged);
  document.getElementById('nav-dashboard-btn').classList.toggle('hidden', !isLogged);
}

// Przełączanie zakładki w Dashboardzie
function switchTab(tabId) {
  document.querySelectorAll('.dashboard-tab').forEach(t => t.classList.add('hidden'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(tabId).classList.remove('hidden');
  event.currentTarget.classList.add('active');
}

// Funkcje pomocnicze
const getHeaders = () => ({
  'Content-Type': 'application/json',
  'X-API-Key': state.apiKey,
});

async function fetchClient() {
  const response = await fetch('/api/client/me', { headers: getHeaders() });
  if (!response.ok) throw new Error('Nie można pobrać danych');
  return response.json();
}

async function fetchLeads() {
  const response = await fetch('/api/leads', { headers: getHeaders() });
  return response.json();
}

// Renderowanie Leadów
function renderLeads(leads) {
  state.leads = leads;
  const table = document.getElementById('leads-table');
  const countDisplay = document.getElementById('lead-count');
  table.innerHTML = '';
  countDisplay.textContent = leads.length;

  leads.forEach(lead => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${lead.email}</td>
      <td>${lead.name || '-'}</td>
      <td><span class="status-badge">${lead.status}</span></td>
      <td>${lead.followup_stage}</td>
      <td>
        <button onclick="editLeadById(${lead.id})" class="btn-outline btn-sm">Edytuj</button>
        <button onclick="deleteLead(${lead.id})" class="btn-danger-outline btn-sm" style="width:auto">Usuń</button>
      </td>
    `;
    table.appendChild(row);
  });
}

// Akcje Logowania
async function handleLogin() {
  const apiKey = document.getElementById('api-key').value.trim();
  if (!apiKey) return;
  state.apiKey = apiKey;
  localStorage.setItem('leadpilot_api_key', apiKey);
  await loadDashboard();
}

async function loadDashboard() {
  try {
    const client = await fetchClient();
    state.client = client;
    fillClientForm(client);
    const leads = await fetchLeads();
    renderLeads(leads);
    showSection('dashboard');
    document.getElementById('welcome-title').textContent = `Witaj, ${client.name || 'Użytkowniku'}`;
  } catch (error) {
    handleLogout();
    alert("Błąd logowania - sprawdź klucz API.");
  }
}

function handleLogout() {
  state.apiKey = null;
  localStorage.removeItem('leadpilot_api_key');
  showSection('landing');
}

// Logika Admina (uproszczona z Twojego widgetu)
async function loginAdmin() {
  const email = document.getElementById('admin-email').value;
  const password = document.getElementById('admin-pass').value;
  try {
    const res = await fetch('/api/admin/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email, password})
    });
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem('adminToken', data.token);
      document.getElementById('admin-auth').classList.add('hidden');
      document.getElementById('admin-dashboard').classList.remove('hidden');
    }
  } catch (e) { console.error(e); }
}

function logoutAdmin() {
  localStorage.removeItem('adminToken');
  document.getElementById('admin-auth').classList.remove('hidden');
  document.getElementById('admin-dashboard').classList.add('hidden');
}

// Inicjalizacja
document.getElementById('login-button').addEventListener('click', handleLogin);
document.getElementById('logout-button').addEventListener('click', handleLogout);
document.getElementById('reload-button').addEventListener('click', loadDashboard);
document.getElementById('client-form').addEventListener('submit', handleClientSave); // funkcja z Twojego oryginału
document.getElementById('new-lead-form').addEventListener('submit', handleNewLead); // funkcja z Twojego oryginału

// Przywracanie sesji
const savedKey = localStorage.getItem('leadpilot_api_key');
if (savedKey) {
  state.apiKey = savedKey;
  loadDashboard();
}

// Funkcja pomocnicza do edycji (globalna, by działała z onclick w tabeli)
window.editLeadById = (id) => {
  const lead = state.leads.find(l => l.id === id);
  if (lead) {
    document.getElementById('lead-editor-card').classList.remove('hidden');
    const form = document.getElementById('lead-edit-form');
    form.lead_id.value = lead.id;
    form.email.value = lead.email;
    form.name.value = lead.name || '';
  }
};