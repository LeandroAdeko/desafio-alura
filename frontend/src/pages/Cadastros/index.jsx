import ArtistaForm from '../../components/ArtistaForm';
import AlbunsForm from '../../components/AlbunsForm';
import ShowForm from '../../components/ShowForm';
import ClipsForm from '../../components/ClipsForm';
import './style.css'


function Cadastros () {

    return (
        <div>
            <h1>Cadastros</h1>
            <div id='cadastros'>
                <ArtistaForm />
                <AlbunsForm />
                <ShowForm />
                <ClipsForm />
            </div>
        </div>
    );
}

export default Cadastros;
