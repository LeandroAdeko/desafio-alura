import React, { useState } from 'react';
import { create } from '../services/crud';


const ArtistaForm = () => {
  const [name, setName] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await create('artistas', { nome: name });
      const data = await response.json();

      let responseArtista = document.getElementById('response-artista');

      if (response.ok) {
        setName('');
        responseArtista.textContent = 'Artista criado com sucesso!';
      } else {
        responseArtista.textContent = 'Erro ao criar artista: ' + data.message;
      }
    } catch (error) {
      responseArtista.textContent = 'Erro ao criar artista: ' + error.message;
    }
  };

  return (
    <div className='cadastro-form'>
      <form id='artista-form' onSubmit={handleSubmit}>
        <div className='form-item'>
        <h2>Artistas</h2>
        <div className='label-input'>
          <label htmlFor="name">Nome:</label>
          <input
            placeholder='Insira o nome do artista'
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        </div>
        <div className='form-item'>
        <button type="submit">Cadastrar</button>
        <span id='response-artista'></span>
        </div>
      </form>
    </div>
  );
};

export default ArtistaForm;
