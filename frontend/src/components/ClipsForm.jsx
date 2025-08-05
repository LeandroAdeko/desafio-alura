import React, { useState, useEffect } from 'react';
import { create, listAll } from '../services/crud';

function ClipsForm() {
  const [nome, setNome] = useState('');
  const [artistaId, setArtistaId] = useState('');
  const [artistas, setArtistas] = useState([]);

  useEffect(() => {
    async function fetchArtistas() {
      try {
        const artistasData = await listAll('artistas');
        setArtistas(artistasData);
      } catch (error) {
        console.error('Error fetching artistas:', error);
      }
    }

    fetchArtistas();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const newClipe = await create('clipes', 
        {
          nome: nome,
          artista_id: artistaId
        }
      );
      console.log('Clipe created:', newClipe);
      // Optionally, reset the form after successful submission
      setNome('');
      setArtistaId('');
    } catch (error) {
      console.error('Error creating clipe:', error);
    }
  };

  return (
    <div className='cadastro-form'>
      <form id='clipe-form' onSubmit={handleSubmit}>
        <div className='form-data'>
          <h2>Clipes</h2>
          <div className='label-input'>
            <label htmlFor="nome">Nome:</label>
            <input
              type="text"
              id="nome"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
            />
          </div>
          <div className='label-input'>
            <label htmlFor="artista_id">Artista:</label>
            <select
              id="artista_id"
              value={artistaId}
              onChange={(e) => setArtistaId(e.target.value)}
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
        </div>
      </form>
    </div>
  );
}

export default ClipsForm;
