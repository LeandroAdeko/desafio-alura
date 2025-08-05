import React, { useState, useEffect } from 'react';
import { create, listAll } from '../services/crud';

const ShowForm = () => {
  const [nome, setNome] = useState('');
  const [local, setLocal] = useState('');
  const [date, setData] = useState('');
  const [artista_id, setArtistaId] = useState('');
  const [artistas, setArtistas] = useState([]);
  const [loadingArtistas, setLoadingArtistas] = useState(false);

  const responseShow = document.getElementById('response-show');

  useEffect(() => {
    handleGetArtistas();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await create('shows', {
        nome: nome,
        local: local,
        data: date,
        artista_id: artista_id
      });
      const data = await response.json();

      if (response.ok) {
        setNome('');
        setLocal('');
        setData('');
        setArtistaId('');
        responseShow.textContent = 'Show criado com sucesso!';
      } else {
        responseShow.textContent = 'Erro ao criar show: ' + data.message;
      }
    } catch (error) {
      responseShow.textContent = 'Erro ao criar show: ' + error.message;
    }
  };

  const handleGetArtistas = async () => {
    setLoadingArtistas(true);
    try {
      const artistasData = await listAll('artistas');
      setArtistas(artistasData);
    } catch (error) {
      console.error('Erro ao buscar artistas:', error);
    } finally {
      setLoadingArtistas(false);
    }
  };

  return (
    <div className='cadastro-form'>
      <form id='show-form' onSubmit={handleSubmit}>
        <div className='form-data'>
        <h2>Shows</h2>
        <div className='label-input'>
          <label htmlFor="nome">Nome:</label>
          <input
            placeholder='Insira o nome do show'
            type="text"
            id="nome"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
          />
        </div>
        <div className='label-input'>
          <label htmlFor="local">Local:</label>
          <input
            placeholder='Insira o local do show'
            type="text"
            id="local"
            value={local}
            onChange={(e) => setLocal(e.target.value)}
          />
        </div>
        <div className='label-input'>
          <label htmlFor="data">Data:</label>
          <input
            placeholder='Insira a data do show'
            type="date"
            id="date"
            value={date}
            onChange={(e) => setData(e.target.value)}
          />
        </div>
        <div className='label-input'>
          <label htmlFor="artista_id">Artista:</label>
          <select
            id="artista_id"
            value={artista_id}
            onChange={(e) => setArtistaId(e.target.value)}
            disabled={loadingArtistas}
          >
            <option value="">Selecione um artista</option>
            {artistas.map((artista) => (
              <option key={artista.id} value={artista.id}>
                {artista.nome}
              </option>
            ))}
          </select>
        </div>
        </div>
        
        <div className='form-item'>
        <button type="submit">Cadastrar</button>
        <span id='response-show'></span>
        </div>
      </form>
    </div>
  );
};

export default ShowForm;
