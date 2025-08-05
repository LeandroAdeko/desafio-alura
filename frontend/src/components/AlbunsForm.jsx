import React, { useState, useEffect } from 'react';
import { create, listAll } from '../services/crud';

const AlbunsForm = () => {
  const [nome, setNome] = useState('');
  const [lancamento, setLancamento] = useState('');
  const [artista_id, setArtistaId] = useState('');
  const [artistas, setArtistas] = useState([]);
  const [loadingArtistas, setLoadingArtistas] = useState(false);

  useEffect(() => {
    handleGetArtistas();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await create('albuns', {
        nome: nome,
        lancamento: lancamento,
        artista_id: artista_id
      });
      const data = await response.json();

      let responseAlbum = document.getElementById('response-album');

      if (response.ok) {
        setNome('');
        setLancamento('');
        setArtistaId('');
        responseAlbum.textContent = 'Album criado com sucesso!';
      } else {
        responseAlbum.textContent = 'Erro ao criar album: ' + data.message;
      }
    } catch (error) {
      responseAlbum.textContent = 'Erro ao criar album: ' + error.message;
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
      <form id='album-form' onSubmit={handleSubmit}>
        <div className='form-data'>
        <h2>Álbuns</h2>
        <div className='label-input'>
          <label htmlFor="nome">Nome:</label>
          <input
            placeholder='Insira o nome do álbum'
            type="text"
            id="nome"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
          />
          <label htmlFor="nome">Lançamento:</label>
          <input
            placeholder='Insira o nome do álbum'
            type="date"
            id="lancamento"
            value={lancamento}
            onChange={(e) => setLancamento(e.target.value)}
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
        <span id='response-album'></span>
        </div>
      </form>
    </div>
  );
};

export default AlbunsForm;
