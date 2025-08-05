import { useNavigate } from "react-router-dom";


function BotaoVoltar (destino) {
    const navigator = useNavigate();

    const realizaNavegacao = () => {
        navigator(destino)
    }


    return (
        <button onClick={realizaNavegacao}>⬅️ Voltar</button>
    );
}


export default BotaoVoltar;