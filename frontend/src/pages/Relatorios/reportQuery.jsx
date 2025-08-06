
const calculateDate = (days) => {
  const today = new Date();
  const pastDate = new Date(today);
  pastDate.setDate(today.getDate() - days);

  const year = pastDate.getFullYear();
  const month = String(pastDate.getMonth() + 1).padStart(2, '0');
  const day = String(pastDate.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
};


const reportQueries = {
  // Queries SQL para os relatórios
  tiposComentariosPorArtista: `
    SELECT
      tipo_comentario,
      COUNT(*) AS quantidade,
      (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM comentarios WHERE artista_id = $artista_id)) AS proporcao
    FROM
      comentarios
    WHERE
      artista_id = $artista_id
    GROUP BY
      tipo_comentario;
  `,
  tagsMaisCitadasUltimas48h: `
    SELECT
      tag,
      COUNT(*) AS quantidade
    FROM
      comentario_tags
    WHERE
      criado_em >= '${calculateDate(2)}'
    GROUP BY
      tag
    ORDER BY
      quantidade DESC
    LIMIT 10;
  `,
  evolucaoCriticasAposLancamentoAlbum: `
    SELECT
      DATE(criado_em) AS data,
      COUNT(*) AS quantidade_criticas
    FROM
      comentarios
    WHERE
      album_id = $album_id
      AND categoria = 'CRITICA'
      AND criado_em >= (SELECT data_lancamento FROM albuns WHERE id = $album_id)
    GROUP BY
      DATE(criado_em)
    ORDER BY
      data;
  `,
  artistaMaisElogiado: `
    SELECT
      a.nome AS artista,
      COUNT(c.id) AS quantidade_elogios
    FROM
      artistas a
    JOIN
      comentarios c ON a.id = c.artista_id
    WHERE
      c.categoria = 'ELOGIO'
    GROUP BY
      a.nome
    ORDER BY
      quantidade_elogios DESC
    LIMIT 10;
  `,
  volumeTotalComentariosPorDiaUltimos7Dias: `
    SELECT
      DATE(criado_em) AS data,
      COUNT(*) AS quantidade_comentarios
    FROM
      comentarios
    WHERE
      criado_em >= '${calculateDate(7)}'
    GROUP BY
      DATE(criado_em)
    ORDER BY
      data;
  `,
  comparacaoCategoriasEntreAlbunsMesmoArtista: `
    SELECT
      a.nome AS album,
    SUM(CASE WHEN c.categoria = 'ELOGIO' THEN 1 ELSE 0 END) AS quantidade_elogios,
      SUM(CASE WHEN c.categoria = 'CRITICA' THEN 1 ELSE 0 END) AS quantidade_criticas
    FROM
      albuns a
    JOIN
      comentarios c ON a.id = c.album_id
    WHERE
      a.artista_id = $artista_id
    GROUP BY
      a.nome
    ORDER BY
      a.nome;
  `,
  distribuicaoCategoriasUltimas24h: `
    SELECT
      categoria,
      COUNT(*) AS quantidade,
      (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM comentarios WHERE criado_em >= '${calculateDate(1)}')) AS proporcao
    FROM
      comentarios
    WHERE
      criado_em >= '${calculateDate(1)}'
    GROUP BY
      categoria;
  `,
  todosComentarios: `
  SELECT
    c.texto AS comentario_texto,
    c.categoria AS comentario_categoria,
    c.confianca AS comentario_confianca,
    c.criado_em AS comentario_criado_em,
    a.id AS artista_id,
    a.nome AS artista_nome,
    al.id AS album_id,
    al.nome AS album_nome,
    cl.id AS clipe_id,
    cl.nome AS clipe_nome,
    s.id AS show_id,
    s.nome AS show_nome
FROM
    comentarios c
LEFT JOIN
    artistas a ON c.artista_id = a.id
LEFT JOIN
    albuns al ON c.album_id = al.id
LEFT JOIN
    clipes cl ON c.clipe_id = cl.id
LEFT JOIN
    shows s ON c.show_id = s.id;`
};

export default reportQueries;
