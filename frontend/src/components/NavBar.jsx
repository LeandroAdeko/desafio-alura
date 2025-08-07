import { BrowserRouter, Routes, Route, Link} from "react-router-dom";
import AuthRequired from "./AuthRequired";

import Home from "../pages/Home";
import LoginScreen from "../pages/Login";
import Comentarios from "../pages/Comentarios";
import Cadastros from "../pages/Cadastros";
import Relatorios from "../pages/Relatorios";
import AreaDoArtista from "../pages/Comentarios/TelaComentario";


function NavBar() {

    return (
        <BrowserRouter>
            <nav id="main-nav">
                <div className="nav-item">
                    <Link to="/">
                        AluMusic
                    </Link>
                </div>
                <div className="nav-item">
                    <Link id='cadastro-nav' to="/cadastros">
                        Cadastros
                    </Link>
                    <Link id='relatorios-nav' to="/relatorios">
                        Relatórios
                    </Link>
                    <Link id='comentarios-nav' to="/comentarios">
                        Comentários
                    </Link>
                    <Link id='cadastro-nav' to="/login">
                        Login
                    </Link>
                </div>
            </nav>
        <Routes>
            <Route index element={<Home />} />
            <Route path="/" element={<Home />} />
            <Route path="/login" element={
                <AuthRequired onlyNotLogged>
                    <LoginScreen />
                </AuthRequired>} />
            <Route path="/cadastros" element={
                <AuthRequired loginRequired adminRequired>
                    <Cadastros />
                </AuthRequired>} />
            <Route path="/comentarios" element={
                <AuthRequired loginRequired>
                    <Comentarios />
                </AuthRequired>} />
            <Route path="/relatorios" element={
                <AuthRequired loginRequired adminRequired>
                    <Relatorios />
                </AuthRequired>} />

            <Route path="/artistas/:id" element={
                <AuthRequired loginRequired>
                    <AreaDoArtista />
                </AuthRequired>} />
        </Routes>
        </BrowserRouter>
    );
}

export default NavBar;
