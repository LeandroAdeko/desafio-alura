import React, { useState } from 'react';
import { create } from '../services/crud';

const TagForm = () => {
  const [formData, setFormData] = useState({
    codigo: '',
    descricao: ''
  });
  const [responseMessage, setResponseMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponseMessage(''); // Limpa a mensagem anterior

    try {
      const response = await create('tags', formData);
      const data = await response.json();

      if (response.ok) {
        setResponseMessage('Tag cadastrada com sucesso!');
        setFormData({
          codigo: '',
          descricao: ''
        });
      } else {
        setResponseMessage('Erro ao cadastrar tag: ' + data.message);
      }
    } catch (error) {
      setResponseMessage('Erro ao cadastrar tag: ' + error.message);
    }
  };

  return (
    <div className="tag-form-container">
      <form onSubmit={handleSubmit}>
      <h2>Cadastro de Tags</h2>
        <div className="form-group">
          <label htmlFor="codigo">Código da Tag:</label>
          <input
            type="text"
            id="codigo"
            name="codigo"
            value={formData.codigo}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="descricao">Descrição:</label>
          <input
            type="text"
            id="descricao"
            name="descricao"
            value={formData.descricao}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Cadastrar Tag</button>
      {responseMessage && <p>{responseMessage}</p>}
      </form>
    </div>
  );
};

export default TagForm;