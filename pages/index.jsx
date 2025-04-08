// pages/index.jsx
import Head from 'next/head';
import Calendar from '../components/Calendar';
import ScheduleForm from '../components/ScheduleForm';
import '../styles/globals.css';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Agendador Zapt Arteatral</title>
        <link rel="icon" href="/logo.png" />
      </Head>
      <main style={{ padding: '20px', fontFamily: 'Open Sans, sans-serif' }}>
        <h1 style={{ color: '#00538F', textAlign: 'center' }}>Agendador Zapt Arteatral</h1>
        {/* Componente para exibir o calendário com eventos existentes */}
        <Calendar />
        {/* Componente com o formulário de agendamento */}
        <ScheduleForm />
      </main>
    </div>
  );
}