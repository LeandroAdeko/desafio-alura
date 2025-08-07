import ArtistaForm from '../../components/ArtistaForm';
import AlbunsForm from '../../components/AlbunsForm';
import ShowForm from '../../components/ShowForm';
import ClipsForm from '../../components/ClipsForm';
import TagForm from '../../components/TagsForm';
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
                <TagForm />
            </div>
        </div>
    );
}

export default Cadastros;
