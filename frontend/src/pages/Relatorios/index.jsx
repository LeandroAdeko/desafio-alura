import React, { useState, useEffect } from 'react';
import { listAll, executeQuery } from '../../services/crud';
import reportQueries from '../../components/reportQuery';
import { Bar, Line, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  ArcElement,
} from 'chart.js';
import "./style.css"

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  ArcElement
);


function formatarParaDiaMes(dataString) {
  const data = new Date(dataString);
  const dia = data.getUTCDate().toString().padStart(2, '0');
  const mes = (data.getUTCMonth() + 1).toString().padStart(2, '0');
  const ano = data.getUTCFullYear().toString();
  return [`${dia}/${mes}/${ano}`, data];
}

const createBarChart = (chart_name, label, chartData) => {
  var labels = [];
  var data = [];

  for (let i = 0; i < chartData.length; i++) {
    labels.push(chartData[i][0]);
    data.push(chartData[i][1]);
  }
  let barChartData = {
    labels: labels,
    datasets: [
      {
        label: label,
        data: data,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className='chart'>
      <h2>{chart_name}</h2>
      <Bar data={barChartData} />
    </div>
  );
};

const createLineChart = (chart_name, label, chartData) => {
  if (!chartData || chartData.length === 0) {
    return null;
  }

  const labels = chartData.map(item => item[0]);
  const data = chartData.map(item => item[1]);

  const lineChartData = {
    labels: labels,
    datasets: [
      {
        label: label,
        data: data,
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
        fill: false,
      },
    ],
  };

  return (
    <div className='chart'>
      <h2>{chart_name}</h2>
      <Line data={lineChartData} />
    </div>
  );
};

const createPieChart = (chart_name, chartData) => {
  if (!chartData) {
    return null;
  }

  const labels = Object.keys(chartData);
  const data = Object.values(chartData);

  const newPieChartData = {
    labels: labels,
    datasets: [
      {
        label: 'Comentários por Categoria',
        data: data,
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(255, 205, 86)',
          'rgb(75, 192, 192)',
          'rgb(153, 102, 255)',
          'rgb(201, 203, 207)',
        ],
        hoverOffset: 4,
      },
    ],
  };

  return (
    <div className='chart'>
      <h2>{chart_name}</h2>
      <Pie data={newPieChartData} />
    </div>
  );
};


const Relatorios = () => {
  const [artistas, setArtistas] = useState([]);
  const [albuns, setAlbuns] = useState([]);
  const [dadosComentarios, setDadosComentarios] = useState(null);
  const [pieComentariosPorArista, setPieComentariosPorArista] = useState();
  const [dadosArtistasElogiados, setDadosArtistasElogiados] = useState(null);
  const [relatorioVolumeComentarios, setRelatorioVolumeComentarios] = useState(null);
  const [relatorioTags48h, setRelatorioTags48h] = useState(null);
  const [relatorioEvolucaoCritica, setRelatorioEvolucaoCritica] = useState(null);
  const [dadosAlbunsElogiados, setDadosAlbunsElogiados] = useState(null);
  
  // Fetch selects
  const fetchSelects = async () => {
    try {
      const dataAlbuns = await listAll("albuns");
      setAlbuns(dataAlbuns);
    } catch (error) {
      console.error('Erro ao buscar álbuns:', error);
    }
    try {
      const dataArtistas = await listAll("artistas");
      setArtistas(dataArtistas);
    } catch (error) {
      console.error('Erro ao buscar artistas:', error);
    }
  };

  const getAllComentsParsed = async ()  => {
    const dataTodosComentarios = await executeQuery(reportQueries.todosComentarios);
    
    const columnNames = [
      "comentario_id",
      "comentario_texto",
      "comentario_categoria",
      "comentario_confianca",
      "comentario_criado_em",
      "tags_list",
      "artista_id",
      "artista_nome",
      "album_id",
      "album_nome",
      "clipe_id",
      "clipe_nome",
      "show_id",
      "show_nome",
    ];
  
    const parsedData = dataTodosComentarios.map((row) => {
      const commentObject = {};
      for (let i = 0; i < columnNames.length; i++) {
        const newColumn = columnNames[i];
        const value = row[i];
  
        if (newColumn === "comentario_criado_em") {
          const dates = formatarParaDiaMes(value);
          commentObject[newColumn] = dates[0];
          commentObject['data_manipulavel'] = dates[1];
        } else if (newColumn === "tags_list") {
          // Transforma a string de tags em uma lista de strings
          commentObject[newColumn] = value ? value.split(',') : [];
        } else {
          commentObject[newColumn] = value;
        }
      }
      return commentObject;
    });
  
    setDadosComentarios(parsedData);
  }

  // Grafico Pizza Comentarios do Artista
  const atualizarComentariosPorArtista = () => {
    let artistaId = document.getElementById('select-artista').value;

    let comentariosFiltrados = dadosComentarios?.filter(comentario => {
      return comentario.artista_id == artistaId;
    });

    let contagemDeCategoria = {};
    let contagemElogiosPorAlbum = {};
    
    comentariosFiltrados?.forEach(comentario => {
      // Lógica para o gráfico de pizza (categorias)
      let categoria = comentario.comentario_categoria;
      if (contagemDeCategoria[categoria]) contagemDeCategoria[categoria]++;
      else contagemDeCategoria[categoria] = 1;
      
      // Nova lógica para o gráfico de barras (elogios por álbum)
      if (comentario.comentario_categoria === 'ELOGIO' && comentario.album_id != null) {
          const nomeAlbum = comentario.album_nome;
          if (contagemElogiosPorAlbum[nomeAlbum]) {
              contagemElogiosPorAlbum[nomeAlbum]++;
          } else {
              contagemElogiosPorAlbum[nomeAlbum] = 1;
          }
      }
    });

    // Transforma os dados de elogios por álbum para o formato do createBarChart
    const dadosGraficoAlbuns = Object.entries(contagemElogiosPorAlbum);
    // Ordena pelo número de elogios em ordem decrescente
    dadosGraficoAlbuns.sort((a, b) => b[1] - a[1]);

    setDadosAlbunsElogiados(dadosGraficoAlbuns);
    setPieComentariosPorArista(contagemDeCategoria);
  };

  // Grafico Evolução de criticas
  const atualizarEvolucaoCriticas = (event) => {
    const albumId = event.target.value;

    if (!dadosComentarios || !albumId) {
      return null;
    }

    const album = albuns.find(a => a.id.toString() === albumId);
    if (!album) return null;

    const lancamentoAlbum = new Date(album.lancamento);
    const contagemCriticasPorData = {};

    dadosComentarios.forEach(comentario => {
      const dataComentario = new Date(comentario.data_manipulavel);
      if (comentario.album_id && comentario.album_id.toString() === albumId && comentario.comentario_categoria === 'CRITICA' && dataComentario >= lancamentoAlbum) {
        const dataFormatada = comentario.comentario_criado_em;
        if (contagemCriticasPorData[dataFormatada]) {
          contagemCriticasPorData[dataFormatada]++;
        } else {
          contagemCriticasPorData[dataFormatada] = 1;
        }
      }
    });

    const dadosGrafico = Object.entries(contagemCriticasPorData);
    dadosGrafico.sort((a, b) => new Date(a[0].split('/').reverse().join('-')) - new Date(b[0].split('/').reverse().join('-')));
    setRelatorioEvolucaoCritica(dadosGrafico);
  };

  // Grafico de Artistas Elogiados
  const gerarRelatorioArtistasElogiados = () => {
    if (!dadosComentarios) {
      return {};
    }

    const comentariosElogios = dadosComentarios.filter(comentario => {
      return comentario.artista_id != null && comentario.comentario_categoria === 'ELOGIO';
    });

    const contagemArtistas = {};
    comentariosElogios.forEach(comentario => {
      const nomeArtista = comentario.artista_nome;
      if (contagemArtistas[nomeArtista]) {
        contagemArtistas[nomeArtista]++;
      } else {
        contagemArtistas[nomeArtista] = 1;
      }
    });

    // Transforma o dicionário em um array de arrays para o formato do createBarChart
    return Object.entries(contagemArtistas);
  };

  // Grafico Linha comentarios por dia
  const gerarRelatorioVolumeComentarios = (dadosComentarios) => {
    if (!dadosComentarios) {
      return null;
    }
  
    const hoje = new Date();
    const seteDiasAtras = new Date(hoje);
    seteDiasAtras.setDate(hoje.getDate() - 7);
  
    const contagemPorData = {};
    dadosComentarios.forEach(comentario => {
      const dataComentario = new Date(comentario.data_manipulavel);
  
      if (dataComentario > seteDiasAtras && dataComentario <= hoje) {
        const dataFormatada = comentario.comentario_criado_em;
        if (contagemPorData[dataFormatada]) {
          contagemPorData[dataFormatada]++;
        } else {
          contagemPorData[dataFormatada] = 1;
        }
      }
    });
  
    // Transforma o dicionário em um array de arrays para o formato do createLineChart
    const dadosGrafico = Object.entries(contagemPorData);
  
    // Ordena os dados por data (ordem crescente)
    dadosGrafico.sort((a, b) => {
      const dataA = new Date(a[0].split('/').reverse().join('-'));
      const dataB = new Date(b[0].split('/').reverse().join('-'));
      return dataA - dataB;
    });
  
    return dadosGrafico;
  };

  // Grafioco Barra Tags das ultimas 48h
  const gerarRelatorioTags48h = (dadosComentarios) => {
    if (!dadosComentarios) {
      return null;
    }
  
    const agora = new Date();
    const quarentaOitoHorasAtras = new Date(agora);
    quarentaOitoHorasAtras.setHours(agora.getHours() - 48);
  
    const contagemTags = {};
    dadosComentarios.forEach(comentario => {
      const dataComentario = new Date(comentario.data_manipulavel);
  
      if (dataComentario > quarentaOitoHorasAtras && Array.isArray(comentario.tags_list)) {
        comentario.tags_list.forEach(tag => {
          if (tag) {
            if (contagemTags[tag]) {
              contagemTags[tag]++;
            } else {
              contagemTags[tag] = 1;
            }
          }
        });
      }
    });
  
    // Converte o objeto de contagem para o formato de array de arrays
    const dadosGrafico = Object.entries(contagemTags);
  
    // Ordena os dados pela quantidade de ocorrências (decrescente)
    dadosGrafico.sort((a, b) => b[1] - a[1]);
  
    return dadosGrafico;
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        getAllComentsParsed()
      } catch (error) {
        console.error('Erro ao executar a query:', error);
      }
      try {
        fetchSelects();
      } catch (error) {
        console.error('Erro ao preencher selects:', error);
      }
    };

    fetchData();
  }, []);


  useEffect(() => {
    if (dadosComentarios) {
      const dadosGraficoElogios = gerarRelatorioArtistasElogiados();
      setDadosArtistasElogiados(dadosGraficoElogios);
      
      const dadosGraficoComentarios = gerarRelatorioVolumeComentarios(dadosComentarios);
      setRelatorioVolumeComentarios(dadosGraficoComentarios);
    
      const dadosGraficoTags = gerarRelatorioTags48h(dadosComentarios);
      setRelatorioTags48h(dadosGraficoTags);
    }
  }, [dadosComentarios]);


  return (
    <div>
      <h1>Relatórios</h1>
      <div id='selects'>
        <div>
          <label htmlFor="select-artista">Filtrar Artista:</label>
          <select id="select-artista" onChange={atualizarComentariosPorArtista}>
            <option value="">Selecione um artista</option>
            {artistas && artistas.map(artista => (
              <option key={artista.id} value={artista.id}>{artista.nome}</option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="select-album">Filtrar Álbum:</label>
          <select id="select-album" onChange={atualizarEvolucaoCriticas}>
            <option value="">Selecione um álbum</option>
            {albuns && albuns.map(album => (
              <option key={album.id} value={album.id}>{album.nome}</option>
            ))}
          </select>
        </div>
      </div>
      
      <div id="charts">
      {pieComentariosPorArista && (
        createPieChart(
          'Comentários do Artista',
          pieComentariosPorArista
        )
      )}
      
      {dadosAlbunsElogiados && (
        createBarChart(
          'Álbuns elogiados do artista',
          'Quantidade de Elogios',
          dadosAlbunsElogiados
        )
      )}

      {dadosArtistasElogiados && (
        createBarChart(
          'Artistas Mais Elogiados',
          'Quantidade de Elogios',
          dadosArtistasElogiados
        )
      )}

      {relatorioVolumeComentarios && (
        createLineChart(
          'Volume de Comentários',
          'Total de Comentários',
          relatorioVolumeComentarios
        )
      )}

      {relatorioTags48h && (
        createBarChart(
          'Tags mais citadas (48h)',
          'Quantidade de Citações',
          relatorioTags48h
        )
      )}

      {relatorioEvolucaoCritica && (
        createLineChart(
          'Críticas do álbum',
          'Quantidade de Críticas',
          relatorioEvolucaoCritica
        )
      )}
      </div>
    </div>
  );
};

export default Relatorios;