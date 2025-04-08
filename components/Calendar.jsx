// components/Calendar.jsx
import React, { useState, useEffect } from 'react';
import { Calendar as BigCalendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const localizer = momentLocalizer(moment);

export default function CalendarComponent() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch('/api/eventos')
      .then(res => res.json())
      .then(data => {
        const formattedEvents = data.events.map(event => ({
          title: event.summary,
          start: new Date(event.start.dateTime || event.start.date),
          end: new Date(event.end.dateTime || event.end.date),
        }));
        setEvents(formattedEvents);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ height: 500, marginBottom: '40px' }}>
      <BigCalendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        defaultView="month"
        style={{ height: 500 }}
      />
    </div>
  );
}