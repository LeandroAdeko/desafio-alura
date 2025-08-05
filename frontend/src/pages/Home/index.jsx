

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { listAll } from '../../services/crud';
import "./style.css"

function Home() {
    const [artistas, setArtistas] = useState([]);
    const [albuns, setAlbuns] = useState([]);
    const [shows, setShows] = useState([]);

    useEffect(() => {
        async function fetchData() {
            const artistasData = await listAll('artistas');
            setArtistas(artistasData);

            const albunsData = await listAll('albuns');
            setAlbuns(albunsData);

            const showsData = await listAll('shows');
            setShows(showsData);
        }

        fetchData();
    }, []);

    return (
        <div>
            <h1>Home</h1>
            <div id='home-list'>
            <div className='home-item'>
            <h2>Artistas</h2>
            <ul>
                {artistas.map(artista => (
                    <li key={artista.id}>
                        <Link to={`/artistas/${artista.id}`}>
                            {artista.nome}
                        </Link>
                    </li>
                ))}
            </ul>
            </div>
            <div className='home-item'>
            <h2>Albuns</h2>
            <ul>
                {albuns.map(album => (
                    <li key={album.id}>
                        <Link to={`/albuns/${album.id}`}>
                            {album.nome}
                        </Link>
                    </li>
                ))}
            </ul>
            </div>

            <div className='home-item'>
            <h2>Shows</h2>
            <ul>
                {shows.map(show => (
                    <li key={show.id}>
                        <Link to={`/shows/${show.id}`}>
                            {show.nome}
                        </Link>
                    </li>
                ))}
            </ul>
            </div>
            </div>
        </div>
    );
}

export default Home;
