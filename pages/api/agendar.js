// pages/api/agendar.js
import { google } from 'googleapis';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Método não permitido' });
    return;
  }

  try {
    const { nome, telefone, data, startTime, endTime, solicitante, local, publico, tematica, obrigatoriedades } = req.body;

    const calendar = google.calendar('v3');
    const auth = new google.auth.JWT(
      process.env.GOOGLE_CLIENT_EMAIL,
      null,
      process.env.GOOGLE_PRIVATE_KEY.replace(/\\n/g, '\n'),
      ['https://www.googleapis.com/auth/calendar']
    );
    await auth.authorize();

    // Combine data e horários (formato ISO)
    const startDateTime = new Date(`${data}T${startTime}`);
    const endDateTime = new Date(`${data}T${endTime}`);

    // Criação do evento com os dados do formulário
    const event = {
      summary: `${solicitante} - ${nome}`,
      description: `Contato: ${nome}\nWhatsApp: ${telefone}\nData: ${data}\nInício: ${startTime}\nTérmino: ${endTime}\nSolicitante: ${solicitante}\nLocal: ${local}\nPúblico: ${publico}\nTemática: ${tematica}\nObrigatoriedades: ${obrigatoriedades}`,
      start: {
        dateTime: startDateTime.toISOString(),
        timeZone: 'America/Sao_Paulo'
      },
      end: {
        dateTime: endDateTime.toISOString(),
        timeZone: 'America/Sao_Paulo'
      }
    };

    const calendarId = process.env.CALENDAR_ID;
    const response = await calendar.events.insert({
      auth,
      calendarId: calendarId,
      resource: event,
    });

    res.status(200).json({ message: 'Evento criado com sucesso', event: response.data });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Erro ao criar o evento', details: error.message });
  }
}