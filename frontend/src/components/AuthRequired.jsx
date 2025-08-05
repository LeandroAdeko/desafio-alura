import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

function AuthRequired({ adminRequired = false, loginRequired = false, onlyNotLogged = false, children }) {
    const navigate = useNavigate();
    const accessToken = localStorage.getItem("accessToken");
    const isAdmin = localStorage.getItem("isAdmin") === 'true';
  
    // null = ainda verificando, false = acesso negado, true = autorizado
    const [allowed, setAllowed] = useState(null);
  
    useEffect(() => {
      // prioriza exclusividade: onlyNotLogged > loginRequired
      if (onlyNotLogged && accessToken) {
        alert("Você já está logado.");
        setAllowed(false);
        return;
      }
  
      if (loginRequired && !accessToken) {
        alert("Você deve estar logado.");
        navigate('/login', { replace: true });
        setAllowed(false);
        return;
      }
  
      if (adminRequired && !isAdmin) {
        alert("Você não possui permissão de acesso!");
        navigate('/', { replace: true }); // ou outra rota de “sem acesso”
        setAllowed(false);
        return;
      }
  
      setAllowed(true);
    }, [accessToken, isAdmin, loginRequired, onlyNotLogged, adminRequired, navigate]);
  
    // Enquanto decide: pode mostrar null ou um spinner leve
    if (allowed === null) return null;
  
    // Acesso negado: já redirecionou/alertou, não renderiza children
    if (!allowed) return null;
  
    // Acesso permitido
    return <>{children}</>;
  }
  
  AuthRequired.propTypes = {
    adminRequired: PropTypes.bool,
    loginRequired: PropTypes.bool,
    children: PropTypes.node,
  };
  
  export default AuthRequired;