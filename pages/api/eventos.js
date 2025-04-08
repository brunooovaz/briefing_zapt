// pages/api/eventos.js
import { google } from 'googleapis';

export default async function handler(req, res) {
  if (req.method !== 'GET') {
    res.status(405).json({ error: 'Método não permitido' });
    return;
  }
  try {
    const calendar = google.calendar('v3');
    const auth = new google.auth.JWT(
      process.env.GOOGLE_CLIENT_EMAIL,
      null,
      process.env.GOOGLE_PRIVATE_KEY.replace(/\\n/g, '\n'),
      ['https://www.googleapis.com/auth/calendar']
    );
    await auth.authorize();

    const calendarId = process.env.CALENDAR_ID;
    const now = new Date().toISOString();
    const future = new Date();
    future.setMonth(future.getMonth() + 1);

    const response = await calendar.events.list({
      auth,
      calendarId: calendarId,
      timeMin: now,
      timeMax: future.toISOString(),
      singleEvents: true,
      orderBy: 'startTime',
    });

    res.status(200).json({ events: response.data.items });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Erro ao listar eventos', details: error.message });
  }
}