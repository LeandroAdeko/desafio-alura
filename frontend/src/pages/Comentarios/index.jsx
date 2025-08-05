import React, { useState, useEffect } from 'react';
import { listAll, create } from '../../services/crud';
import "./style.css"

function Comentarios() {
    const [artistas, setArtistas] = useState([]);
    const [albuns, setAlbuns] = useState([]);
    const [shows, setShows] = useState([]);
    const [clipes, setClipes] = useState([]);
    const [formData, setFormData] = useState({
        texto: '',
        artista_id: null,
        album_id: null,
        show_id: null,
        clipe_id: null
    });

    useEffect(() => {
        const fetchData = async () => {
            const artistasData = await listAll('artistas');
            setArtistas(artistasData);

            const albunsData = await listAll('albuns');
            setAlbuns(albunsData);

            const showsData = await listAll('shows');
            setShows(showsData);

            const clipesData = await listAll('clipes');
            setClipes(clipesData);
        };

        fetchData();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;

        if (value) {
            if (name === 'artista_id') {
                setFormData({ ...formData, [name]: value, album_id: null, show_id: null, clipe_id: null });
            } else if (name === 'album_id') {
                setFormData({ ...formData, [name]: value, artista_id: null, show_id: null, clipe_id: null });
            } else if (name === 'show_id') {
                setFormData({ ...formData, [name]: value, artista_id: null, album_id: null, clipe_id: null });
            } else if (name === 'clipe_id') {
                setFormData({ ...formData, [name]: value, artista_id: null, album_id: null, show_id: null });
            } else {
                setFormData({ ...formData, [name]: value });
            }
        } else {
            setFormData({ ...formData, [name]: value });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        let responseAlbum = document.getElementById('response-comentario');

        try {
            const newComentario = await create('comentarios', formData);
            responseAlbum.textContent = 'Comentário criado com sucesso!';
            
            setFormData({ texto: '', artista_id: null, album_id: null, show_id: null, clipe_id: null })
        } catch (error) {
            responseAlbum.textContent = `Erro ao criar comentário: ${error}`;
        }
    };


    return (
        <div>
            <h1>Comentarios</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="artista">Artista:</label>
                    <select id="artista" name="artista_id" onChange={handleChange} value={formData.artista_id}>
                        <option value="">Selecione um artista</option>
                        {artistas.map((artista) => (
                            <option key={artista.id} value={artista.id}>{artista.nome}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label htmlFor="album">Álbum:</label>
                    <select id="album" name="album_id" onChange={handleChange} value={formData.album_id}>
                        <option value="">Selecione um álbum</option>
                        {albuns.map((album) => (
                            <option key={album.id} value={album.id}>{album.nome}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label htmlFor="show">Show:</label>
                    <select id="show" name="show_id" onChange={handleChange} value={formData.show_id}>
                        <option value="">Selecione um show</option>
                        {shows.map((show) => (
                            <option key={show.id} value={show.id}>{show.nome}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label htmlFor="clipe">Clipe:</label>
                    <select id="clipe" name="clipe_id" onChange={handleChange} value={formData.clipe_id}>
                        <option value="">Selecione um clipe</option>
                        {clipes.map((clipe) => (
                            <option key={clipe.id} value={clipe.id}>{clipe.nome}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label htmlFor="texto">Comentário:</label>
                    <textarea id="texto" name="texto" onChange={handleChange} value={formData.texto} />
                </div>

                <button type="submit">Criar Comentário</button>
                <span id='response-comentario'></span>
            </form>
        </div>
    );
}

export default Comentarios;
