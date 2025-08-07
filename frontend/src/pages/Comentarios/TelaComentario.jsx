import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getById, listAll, executeQuery } from '../../services/crud';
import reportQueries from '../../components/reportQuery';
import "./style.css"

function AreaDoArtista() {
    const { id } = useParams();
    const [artista, setArtista] = useState([]);
    const [albuns, setAlbuns] = useState([]);
    const [shows, setShows] = useState([]);
    const [clipes, setClipes] = useState([]);
    const [formData, setFormData] = useState({
        texto: '',
        artista_id: null,
        album_id: null,
        show_id: null,
        clipe_id: null,
        tag_ids: []
    });

    useEffect(() => {
        const fetchData = async () => {
            const albunsData = await executeQuery(reportQueries.albunsDoArtista.replace("$1", id));
            setAlbuns(albunsData);

            const showsData = await executeQuery(reportQueries.showsDoArtista.replace("$1", id));
            setShows(showsData);

            const clipesData = await executeQuery(reportQueries.clipesDoArtista.replace("$1", id));
            setClipes(clipesData);

            const artistaData = await getById('artista', id);
            setArtista(artistaData);
        };

        fetchData();
    }, []);




    return (
        <div>
            <h1>Artista: {artista.nome}</h1>
            <div id='infos'>
                <div>
                <h2>Albuns</h2>
                <ul>
                    {albuns.forEach(album => (
                        <div>
                            <span>
                                {album[1]}
                            </span>
                            <span>
                                {album[2]}
                            </span>
                        </div>
                    ))}
                </ul>
                </div>

                <div>
                <h2>Shows</h2>
                <ul>
                    {shows.forEach(show => (
                        <div>
                            <span>
                                {show[1]}
                            </span>
                            <span>
                                {show[2]}
                            </span>
                            <span>
                                {show[3]}
                            </span>
                        </div>
                    ))}
                </ul>
                </div>
                
                <div>
                <h2>Clipes</h2>
                <ul>
                    {clipes.forEach(clip => (
                        <div>
                            <span>
                                {clip[1]}
                            </span>
                        </div>
                    ))}
                </ul>
                </div>
            </div>

        </div>
    );
}

export default AreaDoArtista;
