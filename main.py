import streamlit as st
import datetime
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pytz

# ------------------------------
# INJETANDO CSS PERSONALIZADO
# ------------------------------
st.markdown("""
    <style>
    /* Classe para deixar o texto maior e em negrito */
    .big-label {
        font-size: 20px !important;
        font-weight: bold;
        margin-bottom: 5px;
    }

    /* Aumenta a fonte dentro dos campos de texto */
    div.stTextInput > div > input {
        font-size: 20px;
    }
    div.stTextInput label {
        font-size: 20px;
    }

    /* Aumenta a fonte dos time inputs */
    div.stTimeInput input {
        font-size: 20px;
    }
    div.stTimeInput label {
        font-size: 20px;
    }

    /* Aumenta a fonte dos date inputs */
    div.stDateInput input {
        font-size: 20px;
    }
    div.stDateInput label {
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# CONFIGURAÇÕES DA API CALENDAR
# ------------------------------
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Certifique-se de ter esse arquivo
CALENDAR_ID = "b1aac9afa7a059a231080f4d535b497c7c1ae45f9a8778e41007439132c79e20@group.calendar.google.com"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

# Definindo o fuso horário local (horário de Brasília)
LOCAL_TZ = pytz.timezone("America/Sao_Paulo")

# ----------------------------
# FUNÇÕES DE CALENDAR
# ----------------------------
def get_free_busy(start_time, end_time):
    """
    Verifica se há horários ocupados no intervalo informado (usando o fuso America/Sao_Paulo).
    Retorna uma lista de intervalos 'busy'.
    """
    # Converte para fuso local (adiciona offset)
    start_local = LOCAL_TZ.localize(start_time)
    end_local = LOCAL_TZ.localize(end_time)
    
    body = {
        "timeMin": start_local.isoformat(),
        "timeMax": end_local.isoformat(),
        "timeZone": "America/Sao_Paulo",
        "items": [{"id": CALENDAR_ID}],
    }
    events_result = service.freebusy().query(body=body).execute()
    busy_times = events_result['calendars'].get(CALENDAR_ID, {}).get('busy', [])
    return busy_times

def create_event(
    start_time, end_time,
    nome, telefone, date_selected,
    start_time_input, end_time_input,
    solicitante, local, publico,
    tematica, obrigatoriedades
):
    """
    Cria um evento no Google Calendar com as informações fornecidas,
    usando o fuso America/Sao_Paulo.
    """
    # Converte os horários para fuso local
    start_local_naive = datetime.datetime.combine(date_selected, start_time_input)
    end_local_naive = datetime.datetime.combine(date_selected, end_time_input)
    
    start_local = LOCAL_TZ.localize(start_local_naive)
    end_local = LOCAL_TZ.localize(end_local_naive)

    # Formata data e horários para exibição na descrição
    data_formatada = date_selected.strftime('%d/%m/%Y')
    hora_inicio_formatada = start_time_input.strftime('%H:%M')
    hora_termino_formatada = end_time_input.strftime('%H:%M')

    descricao = (
        f"Contato: {nome}\n"
        f"WhatsApp: {telefone}\n"
        f"Data: {data_formatada}\n"
        f"Início: {hora_inicio_formatada}\n"
        f"Término: {hora_termino_formatada}\n"
        f"Solicitante: {solicitante}\n"
        f"Local: {local}\n"
        f"Público: {publico}\n"
        f"Temática: {tematica}\n"
        f"Obrigatoriedades: {obrigatoriedades}"
    )

    event = {
        'summary': f'{solicitante} - {nome}',
        'description': descricao,
        'start': {
            'dateTime': start_local.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': end_local.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
    }
    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created_event

# ----------------------------
# EXPRESSÃO REGULAR DE TELEFONE
# ----------------------------
# Formato: (xx) 9xxxx-xxxx
phone_pattern = re.compile(r'^\(\d{2}\)\s9\d{4}-\d{4}$')

# ----------------------------
# INTERFACE STREAMLIT
# ----------------------------
st.title("Briefing Zapt Arteatral")
st.markdown("<div class='big-label'>Formulário para informações necessárias nos convites de apresentações do Zapt Arteatral</div>", unsafe_allow_html=True)

with st.form("agendamento_form"):
    
    st.markdown("<div class='big-label'>Contato</div>", unsafe_allow_html=True)
    st.markdown("Nome para entrarmos em contato")
    nome = st.text_input("", placeholder="Ex: João Silva")
    st.divider()
    
    st.markdown("<div class='big-label'>WhatsApp</div>", unsafe_allow_html=True)
    st.markdown("Número de WhatsApp com DDD para entrarmos em contato")
    telefone = st.text_input("", placeholder="(xx) 9xxxx-xxxx")
    st.divider()
    
    st.markdown("<div class='big-label'>Data</div>", unsafe_allow_html=True)
    st.markdown("Informe aqui a data da apresentação a ser realizada")
    date_selected = st.date_input(label="", value=datetime.date.today(), label_visibility="collapsed")
    st.divider()

    st.markdown("<div class='big-label'>Início</div>", unsafe_allow_html=True)
    st.markdown("Informe aqui o horário de início da apresentação a ser realizada")
    start_time_input = st.time_input("", datetime.time(9, 0))
    st.divider()

    st.markdown("<div class='big-label'>Término</div>", unsafe_allow_html=True)
    st.markdown("Informe aqui o horário de término da apresentação a ser realizada")
    end_time_input = st.time_input("", datetime.time(10, 0))
    st.divider()

    st.markdown("<div class='big-label'>Solicitante</div>", unsafe_allow_html=True)
    st.markdown("Informe aqui a mocidade ou casa espírita que está nos convidando para realizarmos a apresentação")
    solicitante = st.text_input("", placeholder="Ex: Mocidade Espírita XYZ")
    st.divider()

    st.markdown("<div class='big-label'>Local</div>", unsafe_allow_html=True)
    st.markdown("Informe aqui o local da apresentação a ser realizada")
    local = st.text_input("", placeholder="Ex: Centro Espírita ABC")
    st.divider()

    st.markdown("<div class='big-label'>Público</div>", unsafe_allow_html=True)
    st.markdown("Faixa etária, perfil (tímidos, animados, etc.) e quantidade de pessoas")
    publico = st.text_input("", placeholder="Ex: Público jovem, ~30 pessoas, animados")
    st.divider()

    st.markdown("<div class='big-label'>Temática</div>", unsafe_allow_html=True)
    st.markdown("Enfoque principal da apresentação ou peça preferida")
    tematica = st.text_input("", placeholder="Ex: Tema sobre juventude e espiritismo")
    st.divider()

    st.markdown("<div class='big-label'>Obrigatoriedades</div>", unsafe_allow_html=True)
    st.markdown("Algo específico que deva ser abordado na apresentação?")
    obrigatoriedades = st.text_input("", placeholder="Ex: Focar em passagens do Evangelho")
    
    submit = st.form_submit_button("Agendar")

# Ao enviar o formulário
if submit:
    # Verifica se todos os campos obrigatórios foram preenchidos
    required_fields = [
        nome, telefone, solicitante, local, publico, tematica, obrigatoriedades
    ]
    if not all(field.strip() for field in required_fields):
        st.error("Por favor, preencha todos os campos obrigatórios!")
    else:
        # Valida o telefone
        if not phone_pattern.match(telefone):
            st.error("Por favor, insira o telefone no formato (xx) 9xxxx-xxxx")
        else:
            # Converte data e hora para datetime (naive)
            dt_start = datetime.datetime.combine(date_selected, start_time_input)
            dt_end = datetime.datetime.combine(date_selected, end_time_input)
            
            # Verifica se o horário está livre
            busy = get_free_busy(dt_start, dt_end)
            if busy:
                st.error("O horário escolhido não está disponível.")
            else:
                try:
                    created_event = create_event(
                        dt_start, dt_end,
                        nome, telefone, date_selected,
                        start_time_input, end_time_input,
                        solicitante, local, publico,
                        tematica, obrigatoriedades
                    )
                    st.success("Apresentação reservada com sucesso! Vamos entrar em contato para confirmação e mais detalhes")
                except Exception as e:
                    st.error(f"Ocorreu um erro ao criar o evento: {e}")