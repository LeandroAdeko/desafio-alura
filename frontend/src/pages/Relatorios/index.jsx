import React, { useState, useEffect } from 'react';
import { executeQuery } from '../../services/crud';
import reportQueries from './reportQuery';
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


const lineChartData = {
  labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho'],
  datasets: [
    {
      label: 'Lucro',
      data: [28, 48, 40, 19, 86, 27],
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
      fill: false,
    },
  ],
};

const pieChartData = {
  labels: ['Red', 'Blue', 'Yellow'],
  datasets: [
    {
      label: 'Dataset 1',
      data: [300, 50, 100],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
      ],
      hoverOffset: 4,
    },
  ],
};

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

const createLineChart = () => {
  return (
    <div className='chart'>
      <h2>Line Chart</h2>
      <Line data={lineChartData} />
    </div>
  );
};

const createPieChart = () => {
  return (
    <div className='chart'>
      <h2>Pie Chart</h2>
      <Pie data={pieChartData} />
    </div>
  );
};


const Relatorios = () => {
  const [dadosComentarios, setDadosComentarios] = useState(null);
  const [relatorioComentario7Dias, setRelatorioComentario7Dias] = useState(null);
  const [relatorioEvolucaoCritica, setRelatorioEvolucaoCritica] = useState(null);
  const [dadosComentariosFiltrados, setDadosComentariosFiltrados] = useState(null);

  const getAllComentsParsed = async ()  => {
    const dataTodosComentarios = await executeQuery(reportQueries.todosComentarios);
  
    const columnNames = [
      "comentario_texto",
      "comentario_categoria",
      "comentario_confianca",
      "comentario_criado_em",
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
        let newColumn = columnNames[i]
        if (columnNames[i] == "comentario_criado_em") {
          let dates = formatarParaDiaMes(row[i]);
          commentObject[newColumn] = dates[0];
          commentObject['data_manipulavel'] = dates[1];
        }
        else {
          commentObject[newColumn] = row[i];
        }
      }
      return commentObject;
    });
  
    setDadosComentarios(parsedData);
  }

  const filtrarComentariosPorDias = (dias) => {
    const dataAtual = new Date();
    const dataFiltrada = new Date(dataAtual.setDate(dataAtual.getDate() - dias));

    const comentariosFiltrados = dadosComentarios.filter(comentario => {
      const dataComentario = new Date(comentario.data_manipulavel);
      console.log(`Comentario ${dataComentario}`);
      let maiorFiltro = dataComentario >= dataFiltrada;
      let menorHoje = dataComentario <= dataAtual;
      console.log({dataFiltrada, dataComentario, maiorFiltro, menorHoje})
      return maiorFiltro;
    });
    let f = comentariosFiltrados;
    console.log(`Dados ${f}`);
    setDadosComentariosFiltrados(f);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        getAllComentsParsed()

      } catch (error) {
        console.error('Erro ao executar a query:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Relatórios</h1>
      {/* {relatorioComentario7Dias ? (
        <div>
          {createBarChart(
            'Comentários dos Últimos 7 Dias',
            'Comentários',
            relatorioComentario7Dias
          )}
        </div>
      ) : (
        <p>Carregando...</p>
      )}
      {relatorioComentario7Dias ? (
        <div>
          {createBarChart(
            'Evolução de Crítica',
            'Críticas',
            relatorioEvolucaoCritica
          )}
        </div>
      ) : (
        <p>Carregando...</p>
      )} */}
      
      {dadosComentarios && (
        <div>
          <h2>Todos os Comentários</h2>
          <div>
            <button onClick={() => filtrarComentariosPorDias(1)}>Último Dia</button>
            <button onClick={() => filtrarComentariosPorDias(2)}>Últimos 2 Dias</button>
            <button onClick={() => filtrarComentariosPorDias(7)}>Últimos 7 Dias</button>
          </div>
          <pre>{JSON.stringify(dadosComentariosFiltrados || dadosComentarios, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default Relatorios;
