// components/ScheduleForm.jsx
import React, { useState } from 'react';

export default function ScheduleForm() {
  const [formData, setFormData] = useState({
    nome: '',
    telefone: '',
    data: '',
    startTime: '',
    endTime: '',
    solicitante: '',
    local: '',
    publico: '',
    tematica: '',
    obrigatoriedades: '',
  });

  const [message, setMessage] = useState('');

  const handleChange = e => {
    setFormData({...formData, [e.target.name]: e.target.value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('Processando...');
    const res = await fetch('/api/agendar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    const data = await res.json();
    if (res.ok) {
      setMessage('Agendamento realizado com sucesso!');
      setFormData({
        nome: '',
        telefone: '',
        data: '',
        startTime: '',
        endTime: '',
        solicitante: '',
        local: '',
        publico: '',
        tematica: '',
        obrigatoriedades: '',
      });
    } else {
      setMessage('Erro: ' + data.error);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '600px', margin: '0 auto' }}>
      <h2 style={{ color: '#00538F', textAlign: 'center' }}>Agende seu Evento</h2>
      <div>
        <label>Nome:</label><br />
        <input type="text" name="nome" value={formData.nome} onChange={handleChange} required />
      </div>
      <div>
        <label>Telefone:</label><br />
        <input type="text" name="telefone" value={formData.telefone} onChange={handleChange} placeholder="(xx) 9xxxx-xxxx" required />
      </div>
      <div>
        <label>Data (AAAA-MM-DD):</label><br />
        <input type="date" name="data" value={formData.data} onChange={handleChange} required />
      </div>
      <div>
        <label>Hora Início (HH:MM):</label><br />
        <input type="time" name="startTime" value={formData.startTime} onChange={handleChange} required />
      </div>
      <div>
        <label>Hora Término (HH:MM):</label><br />
        <input type="time" name="endTime" value={formData.endTime} onChange={handleChange} required />
      </div>
      <div>
        <label>Solicitante:</label><br />
        <input type="text" name="solicitante" value={formData.solicitante} onChange={handleChange} required />
      </div>
      <div>
        <label>Local:</label><br />
        <input type="text" name="local" value={formData.local} onChange={handleChange} required />
      </div>
      <div>
        <label>Público:</label><br />
        <input type="text" name="publico" value={formData.publico} onChange={handleChange} required />
      </div>
      <div>
        <label>Temática:</label><br />
        <input type="text" name="tematica" value={formData.tematica} onChange={handleChange} required />
      </div>
      <div>
        <label>Obrigatoriedades:</label><br />
        <input type="text" name="obrigatoriedades" value={formData.obrigatoriedades} onChange={handleChange} required />
      </div>
      <br />
      <button type="submit" style={{ backgroundColor: '#00AFEF', color: '#FFFFFF', padding: '10px 20px', border: 'none', borderRadius: '4px' }}>
        Agendar
      </button>
      <p>{message}</p>
    </form>
  );
}